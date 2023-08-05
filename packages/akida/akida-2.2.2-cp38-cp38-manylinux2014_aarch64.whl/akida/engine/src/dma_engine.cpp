#include "engine/dma_engine.h"
#include "dma_engine_ops.h"

#include <cassert>
#include <vector>

#include "akida/hw_version.h"
#include "engine/dma.h"
#include "engine/dma_desc_ops.h"
#include "infra/hardware_driver.h"
#include "infra/int_ops.h"
#include "infra/registers_common.h"
#include "infra/system.h"

#include "dma_desc_format.h"
#include "registers_dma_engine.h"

namespace akida {
namespace dma {

static void mask_interrupts(HardwareDriver* driver, uint32_t reg_base_addr,
                            bool mask_it);

Engine::Engine(uint32_t reg_base_addr, uint32_t descriptor_len)
    : descriptor_base_addr(0),
      descriptor_len(descriptor_len),
      reg_base_addr(reg_base_addr),
      num_descriptors(0) {}

static void reset_engine(HardwareDriver* driver, uint32_t reg_base_addr) {
  uint32_t reg = 0;
  // perform a soft reset
  set_field(&reg, DMA_CTRL_SOFT_RESET, 1);
  driver->write32(reg_base_addr + DMA_CTRL_REG, reg);
}

static uint32_t container_byte_size(uint32_t container_wlen) {
  // HW DMA descriptor container size in bytes
  return align_up(container_wlen * static_cast<uint32_t>(sizeof(uint32_t)), 32);
}

static void config_desc_base_addr(HardwareDriver* driver,
                                  uint32_t reg_base_addr,
                                  uint32_t descriptor_base_addr) {
  // Configure base address
  driver->write32(reg_base_addr + DMA_CONT_ADDR_REG, descriptor_base_addr);
}

static bool wait_for_interrupt_ext(HardwareDriver* driver,
                                   uint32_t reg_base_addr,
                                   const RegDetail& flag) {
  // This is a manual polling with a timeout of few ms
  constexpr int64_t kTimeout = 5000;
  auto start = time_ms();

  // Busy loop until timeout is reached or interrupt is generated.
  while (true) {
    uint32_t reg = driver->read32(reg_base_addr + DMA_BUF_MON_STATUS_REG);
    // check outbound interrupt
    if (get_field(reg, flag)) {
      // interrupt received, clear status and interrupt
      reg = driver->read32(reg_base_addr + DMA_IB_BUF_MON_CTRL_REG);
      set_field(&reg, DMA_STATUS_CLEAR, 1);
      driver->write32(reg_base_addr + DMA_IB_BUF_MON_CTRL_REG, reg);
      return true;
    }

    auto end = time_ms();
    if ((end - start) > kTimeout) {
      return false;
    }
    // add a short delay before checking status register
    driver->yield(true, 1);
  }
}

void start_config_multi_pass(HardwareDriver* driver, const Config& config,
                             addr conf_base_address, uint32_t num_descs,
                             uint32_t num_passes) {
  const uint32_t& reg_base_addr = config.engine.reg_base_addr;

  // soft reset engine
  reset_engine(driver, reg_base_addr);

  // mask interrupts
  mask_interrupts(driver, reg_base_addr, true);

  // set container address: note that this is different from
  // config.engine.descriptor_base_addr, because it is allocated at runtime
  config_desc_base_addr(driver, reg_base_addr, conf_base_address);

  // Enable replay mode by setting max desc burst mode
  uint32_t reg = 0;
  set_field(&reg, DMA_REPLAY_MAX_DESC_BURST_MODE, 1);
  driver->write32(reg_base_addr + DMA_REPLAY_BUF_CTRL_REG, reg);

  // Set number of descriptors per burst
  reg = 0;
  set_field(&reg, DMA_REPLAY_MAX_DESC_BURST_VALUE, num_descs);
  driver->write32(reg_base_addr + DMA_REPLAY_BURST_VAL_REG, reg);

  // Set delay start
  reg = 0;
  set_field(&reg, DMA_DESC_START_DELAY, 0x20);
  driver->write32(reg_base_addr + DMA_DESC_START_DELAYS_REG, reg);

  // Set inbound container size to 2 in multipass
  reg = 0;
  set_field(
      &reg, DMA_DESC_CONT_SIZE,
      div_round_up(container_byte_size(config.engine.descriptor_len), 32));
  // descriptors are max 15 per pass
  uint32_t num_containers = num_descs * num_passes - 1;
  set_field(&reg, DMA_MAX_DESC_CONTS, num_containers);
  driver->write32(reg_base_addr + DMA_CONT_SIZE_REG, reg);

  // Set last valid to a value > max descriptors, e.g +1 to loop forever. Note
  // that the value cannot exceed 0xff (maximum value for descriptors id).
  uint32_t cur_desc_default_val = 0xff;
  reg = 0;
  uint32_t last_valid_descriptor = (num_containers + 1);
  assert(last_valid_descriptor < cur_desc_default_val);
  set_field(&reg, DMA_LAST_DESC_CONT, last_valid_descriptor);
  set_field(&reg, DMA_CUR_DESC_CONT, cur_desc_default_val);
  driver->write32(reg_base_addr + DMA_DESC_CONT_REG, reg);

  // Set outbound container size to 2 (as inbound)
  reg = 0;
  set_field(&reg, DMA_REPLAY_MAX_OB_DESC_BUFFERS, 2);
  driver->write32(reg_base_addr + DMA_REPLAY_MAX_OB_BUFFERS_REG, reg);

  // start config DMA, that will stay enabled all the time
  toggle_engine(driver, reg_base_addr, true);

  wait_for_interrupt_ext(driver, reg_base_addr,
                         DMA_BUFFER_END_INTS_DESC_BURST_DONE);
}

static void init_engine(HardwareDriver* driver, const Engine& dma) {
  config_desc_base_addr(driver, dma.reg_base_addr, dma.descriptor_base_addr);
  // Set container size (constant in 32 bytes)
  uint32_t reg = 0;
  set_field(&reg, DMA_DESC_CONT_SIZE,
            div_round_up(container_byte_size(dma.descriptor_len), 32));
  // Set maximum number of descriptors. Note this corresponds to the maximum
  // value the descriptor index can take, so that will go from 0 to
  // num_descriptors -1.
  set_field(&reg, DMA_MAX_DESC_CONTS, dma.num_descriptors - 1);
  driver->write32(dma.reg_base_addr + DMA_CONT_SIZE_REG, reg);

  // reset replay mode registers to 0 (disable all hardware reconfig features
  // used for multi pass)
  driver->write32(dma.reg_base_addr + DMA_REPLAY_BUF_CTRL_REG, 0);
  driver->write32(dma.reg_base_addr + DMA_REPLAY_BURST_VAL_REG, 0);
}

void toggle_engine(HardwareDriver* driver, uint32_t reg_base_addr,
                   bool enabled) {
  uint32_t reg = 0;
  // Set control register to run
  set_field(&reg, DMA_CTRL_RUN, enabled ? 1 : 0);
  set_field(&reg, DMA_CTRL_INT_EN, 1);
  // Configure output header
  set_field(&reg, DMA_CTRL_WR_INFO_EN, 1);
  set_field(&reg, DMA_CTRL_WR_INFO_HDR, 1);
  constexpr uint32_t header_byte_size = 32;
  set_field(&reg, DMA_CTRL_WR_INFO_HDR_SZ, header_byte_size);
  driver->write32(reg_base_addr + DMA_CTRL_REG, reg);
}

static void reset(HardwareDriver* driver, const Engine& dma) {
  reset_engine(driver, dma.reg_base_addr);
  init_engine(driver, dma);
  toggle_engine(driver, dma.reg_base_addr, false);
}

void reset(HardwareDeviceImpl* device, Engine* dma, uint32_t num_descriptors) {
  assert(num_descriptors <= dma::MAX_NB_DESCRIPTORS_MULTIPASS);
  auto* mem_mgr = device->mem();

  // if number of decriptor has changed or memory has not been allocated, set
  // number of containers and allocate descriptors buffer
  if (num_descriptors != dma->num_descriptors ||
      dma->descriptor_base_addr == 0) {
    if (dma->descriptor_base_addr) {
      mem_mgr->free(dma->descriptor_base_addr);
    }
    // allocate buffer to contain descriptors. Memory type is system:
    // this type will not be freed at unprogram, so descriptors will be
    // available as long as the device is available.
    dma->descriptor_base_addr =
        mem_mgr->alloc(num_descriptors * dma->descriptor_len * sizeof(uint32_t),
                       MemoryMgr::Type::SYSTEM);
    dma->num_descriptors = num_descriptors;
  }

  auto* driver = device->driver();
  // perform low level reset
  reset(driver, *dma);
}

void release(HardwareDeviceImpl* device, Engine* dma) {
  if (dma->descriptor_base_addr) {
    device->mem()->free(dma->descriptor_base_addr);
  }
}

static bool wait_for_interrupt(HardwareDriver* driver, uint32_t reg_base_addr) {
  return wait_for_interrupt_ext(driver, reg_base_addr, DMA_BUFFER_END_INTS_OB);
}

void wait_for_interrupt_multipass(HardwareDriver* driver, const Inputs& dma) {
  const uint32_t& reg_base_addr = dma.engine.reg_base_addr;
  if (!wait_for_interrupt_ext(driver, reg_base_addr,
                              DMA_BUFFER_END_STATUS_DESC_BURST_DONE)) {
    panic("Fatal error: no interrupt while processing inputs in multipass");
  }
}

void set_output_buffer_clear(HardwareDriver* driver, const Inputs& dma,
                             uint32_t clear_size) {
  const uint32_t& reg_base_addr = dma.engine.reg_base_addr;
  // Configure the output buffer clearing size
  dma::w32 reg = 0;
  // The output buffer clear size is expressed in 32-bit words
  set_field(&reg, DMA_OB_PLD_CLR_SIZE, div_round_up(clear_size, 4));
  set_field(&reg, DMA_OB_PLD_CLR_EN, clear_size > 0 ? 1 : 0);
  driver->write32(reg_base_addr + DMA_OB_PLD_CLEAR_SIZE_REG, reg);
}

void prepare_engine_multi_pass(HardwareDriver* driver, const Inputs& dma,
                               dma::addr address_out, dma::addr hw_desc_addr,
                               dma::addr hw_payload_addr, uint32_t num_loops,
                               bool first_frame) {
  const uint32_t& reg_base_addr = dma.engine.reg_base_addr;
  // reset and init engine
  if (first_frame) {
    reset_engine(driver, reg_base_addr);
  }
  init_engine(driver, dma.engine);
  // Leave the controller disabled before setting the registers.
  toggle_engine(driver, reg_base_addr, false);

  // mask interrupts
  mask_interrupts(driver, reg_base_addr, true);

  // Enable replay mode by setting hw generated descriptors mode, dynamic size,
  // set replay timer
  // TODO: consider disabling this as small power enhancement.
  uint32_t reg = 0;
  set_field(&reg, DMA_REPLAY_MAX_DESC_BURST_MODE, 1);
  set_field(&reg, DMA_REPLAY_HW_OB_ADDR_GEN_MODE, 1);
  set_field(&reg, DMA_REPLAY_HW_OB_ADDR_DYN_MODE, 1);
  set_field(&reg, DMA_REPLAY_BUFFER_MODE, 1);
  set_field(&reg, DMA_REPLAY_TIMER_MODE, 1);
  driver->write32(reg_base_addr + DMA_REPLAY_BUF_CTRL_REG, reg);

  // Set number of loops
  reg = 0;
  set_field(&reg, DMA_REPLAY_LOOPS, num_loops);
  // DMA_REPLAY_LOOPS_LAYER_PR is set with same value as num_loops, used for
  // layer partial reconfig but mandatory to make it work nevertheless.
  set_field(&reg, DMA_REPLAY_LOOPS_LAYER_PR, num_loops);
  driver->write32(reg_base_addr + DMA_REPLAY_BURST_VAL_REG, reg);

  // Address of the main buffer space for the HW generated Descriptors, (only
  // one is going to be used)
  uint32_t addr_main_desc = hw_desc_addr;
  // main payload base address, set to output address
  uint32_t addr_payload_base_addr = address_out;
  // scratch descriptors container can be set at the same address than main desc
  uint32_t addr_scratch_desc = addr_main_desc;
  // scratch payload base address has 1 as size, it only contains header (i.e.
  // size) because DMA controller does not know that partial reconfiguration is
  // using internal buffer.
  uint32_t addr_scratch_payload_base_addr = hw_payload_addr;
  driver->write32(reg_base_addr + DMA_REPLAY_DESC_MAIN_BUF_ADDR_REG,
                  addr_main_desc);
  driver->write32(reg_base_addr + DMA_REPLAY_DESC_SCRATCH_BUF_ADDR_REG,
                  addr_scratch_desc);
  driver->write32(reg_base_addr + DMA_REPLAY_OB_EVENT_BUF_ADDR_REG,
                  addr_payload_base_addr);
  driver->write32(reg_base_addr + DMA_REPLAY_OB_EVENT_SCRATCH_ADDR_REG,
                  addr_scratch_payload_base_addr);
  // initialize output payload header to 0, to prevent reading bogus values
  driver->write32(addr_payload_base_addr, 0);

  // start DMA, that will stay enabled to send events
  toggle_engine(driver, reg_base_addr, true);
}

void fetch_descriptors(HardwareDriver* driver, const Engine& dma,
                       const std::vector<dma::Descriptor>& descriptors) {
  assert(descriptors.size() > 0 &&
         descriptors.size() < dma::MAX_NB_DESCRIPTORS);
  // Get the previous descriptor processed by DMA (it is default initialized
  // to 0xFF)
  auto desc_container_reg_addr = dma.reg_base_addr + DMA_DESC_CONT_REG;
  auto reg = driver->read32(desc_container_reg_addr);
  RegDetail dma_last_desc_cont = DMA_LAST_DESC_CONT;
  auto last_descriptor_id = get_field(reg, dma_last_desc_cont);
  for (const auto& descriptor : descriptors) {
    // increment last_descriptor_id
    last_descriptor_id = (last_descriptor_id + 1) % dma.num_descriptors;
    // Then write descriptor at the right place in DDR
    auto last_descriptor_addr =
        dma.descriptor_base_addr +
        (container_byte_size(dma.descriptor_len) * last_descriptor_id);
    driver->write(last_descriptor_addr, descriptor);
  }
  // then write the incremented value in field DMA_LAST_DESC_CONT.
  // DMA will then process descriptors from DMA_DESC_CONT_REG to
  // DMA_LAST_DESC_CONT
  set_field(&reg, DMA_LAST_DESC_CONT, last_descriptor_id);
  driver->write32(desc_container_reg_addr, reg);
}

void process(HardwareDriver* driver, const Config& dma,
             const dma::Descriptor& descriptor) {
  toggle_engine(driver, dma.engine.reg_base_addr, true);
  // fetch descriptor
  fetch_descriptors(driver, dma.engine, {descriptor});
  // then wait for interrupt
  if (!wait_for_interrupt(driver, dma.engine.reg_base_addr)) {
    // dma needs to be reset to work properly after a timeout
    reset(driver, dma.engine);
    panic("Timed out while processing dma configuration request");
  }
  toggle_engine(driver, dma.engine.reg_base_addr, false);
}

uint32_t get_last_job_id_processed(HardwareDriver* driver, const Inputs& dma) {
  auto reg = driver->read32(dma.engine.reg_base_addr + DMA_DESC_STATUS_REG);
  return get_field(reg, DMA_JOB_ID);
}

void toggle_buffer_timer(HardwareDriver* driver, const Inputs& dma,
                         bool enabled) {
  auto reg = driver->read32(dma.engine.reg_base_addr + DMA_IB_BUF_MON_CTRL_REG);
  set_field(&reg, DMA_BUF_TIMER_EN, enabled ? 1 : 0);
  driver->write32(dma.engine.reg_base_addr + DMA_IB_BUF_MON_CTRL_REG, reg);
}

uint32_t read_buffer_timer(HardwareDriver* driver, const Inputs& dma) {
  return driver->read32(dma.engine.reg_base_addr + DMA_BUFFER_TIMER_STATUS_REG);
}

bool is_buffer_timer_enabled(const HardwareDriver& driver, const Inputs& dma) {
  auto reg = driver.read32(dma.engine.reg_base_addr + DMA_IB_BUF_MON_CTRL_REG);
  auto enabled = get_field(reg, DMA_BUF_TIMER_EN);
  return enabled != 0;
}

void toggle_pipeline(HardwareDriver* driver, const Inputs& dma, bool enabled) {
  auto reg = driver->read32(dma.engine.reg_base_addr + DMA_IB_BUF_MON_CTRL_REG);
  set_field(&reg, DMA_BUF_END_SELECT, enabled ? 1 : 0);
  // Note: The settings supported are:
  // 0x0: DMA Outbound Buffer End -> No pipelining
  // 0x1: DMA Inbound Buffer End -> Full pipelining
  // 0x2: External Buffer End (from other DMA) -> Used only for debugging HRC:
  // No HRC pipeling, Mesh pipelining
  // Value 0x2 should probably not be used.

  driver->write32(dma.engine.reg_base_addr + DMA_IB_BUF_MON_CTRL_REG, reg);
}

static void mask_interrupts(HardwareDriver* driver, uint32_t reg_base_addr,
                            bool mask_it) {
  auto reg = driver->read32(reg_base_addr + DMA_IB_BUF_MON_CTRL_REG);
  set_field(&reg, DMA_BUFFER_END_MASK, mask_it ? 0x7 : 0);
  // When masked, a Buffer End will not generate an interrupt, but will set a
  // status. Note: The settings supported are:
  //
  // Bit0: DMA OB Buffer End
  // Bit1: DMA IB Buffer End
  // Bit2: External Buffer End (from other DMA)
  // Bit3: Descriptor Burst End
  //
  // So setting it to 0x7 will mask all interrupts except burst end.

  driver->write32(reg_base_addr + DMA_IB_BUF_MON_CTRL_REG, reg);
}

static bool is_pipeline_enabled(const HardwareDriver& driver,
                                const Inputs& dma) {
  auto reg = driver.read32(dma.engine.reg_base_addr + DMA_IB_BUF_MON_CTRL_REG);
  auto enabled = get_field(reg, DMA_BUF_END_SELECT);
  return enabled == 1;
}

uint32_t wait_for_new_job_id(HardwareDriver* driver, const Inputs& dma,
                             uint32_t old_job_id, int32_t timeout) {
  auto start = time_ms();
  for (;;) {
    // get the last job processed by DMA
    auto last_job_id_processed_by_hw =
        dma::get_last_job_id_processed(driver, dma);
    // keep system alive
    kick_watchdog();
    if (last_job_id_processed_by_hw != old_job_id) {
      return last_job_id_processed_by_hw;
    }
    // wait a bit before checking job id again
    driver->yield(true, 1);
    auto end = time_ms();
    if ((end - start) > timeout) {
      // dma needs to be reset if timeout occurs, and pipeline state restored
      auto pipeline_enabled = is_pipeline_enabled(*driver, dma);
      reset(driver, dma.engine);
      toggle_pipeline(driver, dma, pipeline_enabled);
      panic("Timed out while waiting a job to end");
    }
  }
}

}  // namespace dma
}  // namespace akida
