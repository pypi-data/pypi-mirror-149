#pragma once

#include "engine/dma_engine.h"

#include <cstdint>
#include <vector>

#include "akida/hw_version.h"
#include "engine/dma.h"
#include "engine/dma_desc_ops.h"
#include "engine/hardware_device_impl.h"
#include "infra/hardware_driver.h"

namespace akida {

namespace dma {
static constexpr uint32_t MAX_PIPELINE_SIZE = (MAX_NB_DESCRIPTORS - 1);

// Perform three actions:
// 1. soft reset DMA engine
// 2. initialize DMA engine (i.e.: set container size, max number of containers,
// disable multipass)
// 3. toggle engine off
void reset(HardwareDeviceImpl* device, Engine* dma, uint32_t num_descriptors);

// Release DMA resources
void release(HardwareDeviceImpl* device, Engine* dma);

// Configure control register and enable/disable engine
void toggle_engine(HardwareDriver* driver, uint32_t reg_base_addr,
                   bool enabled);

// Copy descriptors to DDR, set last descrtiptor container id register to let
// engine process descriptors.
void fetch_descriptors(HardwareDriver* driver, const Engine& dma,
                       const std::vector<dma::Descriptor>& descriptors);

// Tell config DMA engine to process a given descriptor
void process(HardwareDriver* driver, const Config& dma,
             const Descriptor& descriptor);

// Used in single pass: return ID of last processed job
uint32_t get_last_job_id_processed(HardwareDriver* driver, const Inputs& dma);

// Used in single pass: poll register to check whan a job has been processed
uint32_t wait_for_new_job_id(HardwareDriver* driver, const Inputs& dma,
                             uint32_t old_job_id, int32_t timeout = 5000);

// Turn clock counter measures on or off
void toggle_buffer_timer(HardwareDriver* driver, const Inputs& dma,
                         bool enabled);

// Retrieve clock counter measures
uint32_t read_buffer_timer(HardwareDriver* driver, const Inputs& dma);

// Tell if clock counter is enabled
bool is_buffer_timer_enabled(const HardwareDriver& driver, const Inputs& dma);

// Enable or disable pipeline. When enabled, it will be kept enable on best
// effort, disabled in multi pass and when learning is enabled.
void toggle_pipeline(HardwareDriver* driver, const Inputs& dma, bool enabled);

// Program config controller to process multi pass descriptors for a given
// number of passes. The controller will synchronize itself with the inputs DMA
// controller to continue processing the different steps of a program.
void start_config_multi_pass(HardwareDriver* driver, const Config& config,
                             addr conf_base_address, uint32_t num_descs,
                             uint32_t num_passes);

// Configure inputs controller to generate descriptors and process the multiple
// passes necessary to process events.
void prepare_engine_multi_pass(HardwareDriver* driver, const Inputs& dma,
                               dma::addr address_out, dma::addr hw_desc_addr,
                               dma::addr hw_payload_addr, uint32_t num_loops,
                               bool first_frame);

// Configure output buffer clearing policy
void set_output_buffer_clear(HardwareDriver* driver, const Inputs& dma,
                             uint32_t clear_size);

// Used in multipass: wait for input engine to finish processing last descriptor
void wait_for_interrupt_multipass(HardwareDriver* driver, const Inputs& dma);

}  // namespace dma

}  // namespace akida
