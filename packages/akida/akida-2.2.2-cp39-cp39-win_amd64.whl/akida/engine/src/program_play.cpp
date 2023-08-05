#include "program_play.h"

#include <cassert>
#include <cstring>

#include "akida/hardware_device.h"
#include "akida/hw_version.h"
#include "akida/shape.h"
#include "akida/version.h"
#include "engine/akida_device_program_fb_generated.h"
#include "engine/dma_config_ops.h"
#include "engine/fnp2_mem_conf_reg.h"
#include "engine/hardware_device_impl.h"
#include "engine/program_mem_mgr.h"
#include "engine/registers_epg.h"
#include "flatbuffers/flatbuffers.h"
#include "infra/hardware_driver.h"

#include "dma_desc_format.h"
#include "dma_engine_ops.h"

namespace akida {
namespace program {

static void check_device_version(const HardwareDevice& device,
                                 const fb::Program& program) {
  // verify device version matches with program
  auto* prog_dev_version = program.device_version();
  auto dev_version = device.version();

  bool valid_version =
      dev_version.vendor_id == prog_dev_version->vendor_id() &&
      dev_version.product_id == prog_dev_version->product_id() &&
      dev_version.major_rev == prog_dev_version->major_rev() &&
      dev_version.minor_rev == prog_dev_version->minor_rev();
  if (!valid_version) {
    panic("Program device version and device version are not compatible");
  }
}

void verify(const HardwareDeviceImpl& device, const uint8_t* data,
            size_t size) {
  if (!data) {
    panic("Program is null");
  }
  // build program and verify it
  auto* program = fb::GetProgram(data);
  flatbuffers::Verifier verifier(data, size);
  if (!program || !program->Verify(verifier)) {
    panic("Unable to parse program");
  }
  // Check that the akida version this program was compiled with matches the
  // current version.
  const auto& program_version = program->version()->c_str();
  const auto& lib_version = version();
  if (strcmp(program_version, lib_version) != 0) {
    panic("Program version [%s] does not match library version [%s]",
          program_version, lib_version);
  }
  check_device_version(device, *program);
}

static void rewind_fnp2_track(HardwareDeviceImpl* device,
                              const fb::Fnp2FilterTrack& track) {
  device->program_mem()->free_from_id(&track);
}

static void rewind_np_track(HardwareDeviceImpl* device,
                            const fb::NpTrack& track, bool multi_pass) {
  if (multi_pass) {
    // in multi pass, free config header allocated with track as id
    device->program_mem()->free_from_id(&track);
  }
}

static void rewind_record(HardwareDeviceImpl* device, const fb::Record& record,
                          bool multi_pass) {
  // rewind fnp2 track if it is there
  const auto* fnp2_track = record.fnp2_track();
  if (fnp2_track) {
    rewind_fnp2_track(device, *fnp2_track);
  }
  // rewind all normal tracks
  const auto* np_tracks = record.np_tracks();
  uint32_t np_tracks_size = np_tracks->size();
  for (int i = np_tracks_size - 1; i >= 0; i--) {
    const auto& np_track = *np_tracks->Get(i);
    rewind_np_track(device, np_track, multi_pass);
  }
}

static void play_np_track(HardwareDeviceImpl* device,
                          const fb::NpTrack& track) {
  const auto* buffer = track.data();
  device->dma_config_write(buffer->data(), buffer->size());
}

static dma::addr play_np_track_multi_pass(HardwareDeviceImpl* device,
                                          const fb::NpTrack& track,
                                          dma::addr desc_addr) {
  const auto* buffer = track.data();
  auto buf_size = buffer->size();
  // allocate DDR memory and copy buffer in it. Use track pointer as id.
  // TODO: later on embedded devices this copy could be avoided
  auto buf_in_mem =
      device->program_mem()->alloc_for_id(&track, buf_size * sizeof(uint32_t));
  auto driver = device->driver();
  driver->write(buf_in_mem, buffer->data(), buf_size);

  // format descriptor
  constexpr uint32_t output_addr = 0;  // not used for write
  auto descriptor =
      dma::format_config_desc(dma::DESC_CONFIG_DIRECTION_WRITE, buf_in_mem,
                              output_addr, static_cast<uint32_t>(buf_size));
  // write descriptor in its place
  driver->write(desc_addr, descriptor);
  return desc_addr + dma::config::DESC_BYTE_SIZE;
}

static void play_fnp2_track(HardwareDeviceImpl* device,
                            const fb::Fnp2FilterTrack& track) {
  auto* driver = device->driver();
  const auto* buffer = track.data();
  // alloc and write FNP2 filter data
  uint32_t address = device->program_mem()->alloc_for_id(
      &track, buffer->size() * sizeof(uint32_t));
  driver->write(address, buffer->data(), buffer->size());

  // Now write DDR address used for this NP in the dedicated conf register
  // Note that there are 4 registers where the weights adress can be stored.
  // This works because currently existing mesh designs only contain one node
  // with 4 FNPs. Each NP will use the content of the register indexed by the ID
  // of the NP.
  // If at some point a mesh is created with a different layout, this might
  // raise an issue.
  // Also, this means that in multipass this register can only be used once per
  // program, and the FNP2 cannot be reused later, because that would require
  // updating the register value with another address, and there is no way to do
  // that.
  const auto np_id = track.np()->id();
  auto fnp2_mem_conf_reg_addr =
      fnp2_memory_conf(driver->top_level_reg(), np_id);
  driver->write32(fnp2_mem_conf_reg_addr, address);
}

static void play_record_single_pass(HardwareDeviceImpl* device,
                                    const fb::Record& record) {
  // play all normal tracks
  const auto* np_tracks = record.np_tracks();
  int np_tracks_size = np_tracks->size();
  for (int i = 0; i < np_tracks_size; i++) {
    const auto& np_track = *np_tracks->Get(i);
    if (np_track.data()->size() > 0)
      play_np_track(device, np_track);
  }

  // play fnp2 track if it is there
  const auto* fnp2_track = record.fnp2_track();
  if (fnp2_track) {
    play_fnp2_track(device, *fnp2_track);
  }
}

static dma::addr play_record_multi_pass(HardwareDeviceImpl* device,
                                        const fb::Record& record,
                                        dma::addr dma_desc_addr) {
  // play all normal tracks
  const auto* np_tracks = record.np_tracks();
  int np_tracks_size = np_tracks->size();
  for (int i = 0; i < np_tracks_size; i++) {
    const auto& np_track = *np_tracks->Get(i);
    dma_desc_addr = play_np_track_multi_pass(device, np_track, dma_desc_addr);
  }

  // play fnp2 track if it is there
  const auto* fnp2_track = record.fnp2_track();
  if (fnp2_track) {
    play_fnp2_track(device, *fnp2_track);
  }
  return dma_desc_addr;
}

static void play_epg_track(HardwareDriver* driver, uint32_t epg_base,
                           uint32_t address, uint32_t data) {
  driver->write32(epg_base + address, data);
}

void rewind(HardwareDeviceImpl* device, const uint8_t* program_data) {
  auto* program = fb::GetProgram(program_data);

  const auto& passes = *program->passes();
  int passes_size = passes.size();
  bool multi_pass = passes_size > 1;

  const auto learn = program->learning_layer();
  if (learn) {
    if (device->learn_enabled() && !multi_pass)
      rewind_record(device, *learn->learning_registers(), multi_pass);
    else
      rewind_record(device, *learn->inference_registers(), multi_pass);
    rewind_record(device, *learn->ram(), multi_pass);
  }

  // rewind in reverse order
  for (int i = passes_size - 1; i >= 0; i--) {
    const auto& layer_records = *passes[i]->records();
    int cur_pass_size = layer_records.size();
    for (int j = cur_pass_size - 1; j >= 0; j--) {
      const auto& record = *layer_records[j];
      rewind_record(device, record, multi_pass);
    }
  }

  if (multi_pass) {
    // free up descriptors uses for all passes tracks (and dummy ones).
    // Allocation was tracked using passes
    device->program_mem()->free_from_id(&passes);
    // free up dummy config header + output
    device->program_mem()->free_from_id(program);
  }
}

static std::pair<dma::addr, dma::addr> dma_config_header_dummy(
    HardwareDeviceImpl* device, const akida::fb::Program* program) {
  auto dummy_header = program->dummy_desc_hdr();
  const uint32_t dummy_header_data[dma::HDR_CONFIG_LEN] = {dummy_header->w1(),
                                                           dummy_header->w2()};
  // Allocate the space of header size + 1 word for output
  auto mem = device->program_mem()->alloc_for_id(
      program, (dma::HDR_CONFIG_LEN + 1) * sizeof(uint32_t));
  // Write header in memory
  device->driver()->write(mem, dummy_header_data, dma::HDR_CONFIG_LEN);
  return std::make_pair(mem, mem + dma::HDR_CONFIG_LEN * sizeof(uint32_t));
}

static dma::addr write_dummy_descs(HardwareDeviceImpl* device,
                                   dma::addr descriptors_addr,
                                   dma::addr dummy_input,
                                   dma::addr dummy_output,
                                   uint32_t num_dummy_descs) {
  for (uint32_t j = 0; j < num_dummy_descs; j++) {
    // Dummy descriptor is a read of size 1. Descriptor size is the header size
    auto dummy_desc =
        dma::format_config_desc(dma::DESC_CONFIG_DIRECTION_READ, dummy_input,
                                dummy_output, dma::HDR_CONFIG_LEN);
    device->driver()->write(descriptors_addr, dummy_desc);
    // dummy descriptors are to allow all pass to have the same number of
    // descriptors
    descriptors_addr += dma::config::DESC_BYTE_SIZE;
  }
  return descriptors_addr;
}

static void play_epg(HardwareDeviceImpl* device, const fb::Program* program) {
  // Apply EPG program
  const auto* epg_tracks = program->epg_tracks();
  if (epg_tracks) {
    auto epg_tracks_size = epg_tracks->size();
    auto driver = device->driver();
    auto epg_base = epg_reg_base(driver->top_level_reg());
    for (uint32_t i = 0; i < epg_tracks_size; i++) {
      const auto& epg_track = epg_tracks->Get(i);
      play_epg_track(driver, epg_base, epg_track->address(), epg_track->data());
    }
  }
}

void multi_pass_play(HardwareDeviceImpl* device, const fb::Program* program) {
  const auto& passes = *program->passes();
  uint32_t passes_size = passes.size();
  // In multi pass mode, there will always be at least 2 passes
  assert(passes_size >= 2);

  dma::addr descriptors_addr;
  dma::addr descriptors_addr_base;
  // estimate memory required to hold passes descriptors.
  auto max_num_desc_pass = program->max_num_desc();
  auto descs_required_memory =
      passes_size * max_num_desc_pass * dma::config::DESC_BYTE_SIZE;
  // use program to allocate dummy config, input and output space
  dma::addr dummy_input, dummy_output;
  std::tie(dummy_input, dummy_output) =
      dma_config_header_dummy(device, program);

  // allocate contiguous descriptors using id from passes address
  descriptors_addr =
      device->program_mem()->alloc_for_id(&passes, descs_required_memory);
  // save address to set in the config multipass
  descriptors_addr_base = descriptors_addr;

  uint32_t np_tracks_played = 0;

  // now that we have the memory, we can fill the descriptors
  for (uint32_t i = 0; i < passes_size; i++) {
    const auto& layer_records = *passes[i]->records();
    uint32_t records_size = layer_records.size();
    np_tracks_played = 0;
    for (uint32_t j = 0; j < records_size; j++) {
      auto* record = layer_records[j];

      // get number of NP tracks (corresponding to number of DMA descriptors).
      uint32_t np_tracks_size = record->np_tracks()->size();
      descriptors_addr =
          play_record_multi_pass(device, *record, descriptors_addr);
      np_tracks_played += np_tracks_size;
    }

    // fill unused pass descriptors with "dummy" descriptors for this pass
    uint32_t num_dummy_descs = max_num_desc_pass - np_tracks_played;
    descriptors_addr = write_dummy_descs(device, descriptors_addr, dummy_input,
                                         dummy_output, num_dummy_descs);
  }
  const auto learn = program->learning_layer();
  if (learn) {
    const auto& ram = *learn->ram();
    const auto& registers = *learn->inference_registers();

    auto np_tracks_size =
        registers.np_tracks()->size() + ram.np_tracks()->size();

    descriptors_addr =
        play_record_multi_pass(device, registers, descriptors_addr);
    descriptors_addr = play_record_multi_pass(device, ram, descriptors_addr);

    // fill unused pass descriptors with "dummy" descriptors for this pass
    np_tracks_played += np_tracks_size;
    uint32_t num_dummy_descs = max_num_desc_pass - np_tracks_played;
    descriptors_addr = write_dummy_descs(device, descriptors_addr, dummy_input,
                                         dummy_output, num_dummy_descs);
  }

  // Finish configuration and start config DMA
  device->dma_start_config_multipass(descriptors_addr_base, max_num_desc_pass,
                                     passes_size);
}

static void single_pass_play(HardwareDeviceImpl* device,
                             const fb::Program* program) {
  const auto& passes = *program->passes();
  assert(passes.size() == 1);
  const auto& layer_records = *passes[0]->records();
  int records_size = layer_records.size();

  // play all records
  for (int i = 0; i < records_size; i++) {
    const auto& record = *layer_records[i];
    play_record_single_pass(device, record);
  }

  const auto learn = program->learning_layer();
  if (learn) {
    const auto& registers = device->learn_enabled()
                                ? *learn->learning_registers()
                                : *learn->inference_registers();
    play_record_single_pass(device, registers);
    play_record_single_pass(device, *learn->ram());
  }
}

void play(HardwareDeviceImpl* device, const uint8_t* program_data) {
  auto* program = fb::GetProgram(program_data);

  const auto passes_size = program->passes()->size();
  if (passes_size == 1)
    single_pass_play(device, program);
  else
    multi_pass_play(device, program);

  play_epg(device, program);
}

static void single_pass_configure_learning_mode(HardwareDeviceImpl* device,
                                                const fb::Program* program,
                                                bool learn_en) {
  const auto learn = program->learning_layer();
  assert(learn);
  const auto& old_registers =
      !learn_en ? *learn->learning_registers() : *learn->inference_registers();
  const auto& new_register =
      learn_en ? *learn->learning_registers() : *learn->inference_registers();

  rewind_record(device, old_registers, false);
  play_record_single_pass(device, new_register);
}

static void multi_pass_configure_learning_mode(HardwareDeviceImpl* device,
                                               const fb::Program* program,
                                               bool learn_en) {
  const auto learn = program->learning_layer();
  assert(learn);
  const auto& inference_tracks = *learn->inference_registers()->np_tracks();
  const auto& learning_tracks = *learn->learning_registers()->np_tracks();
  assert(inference_tracks.size() == 1 && learning_tracks.size() == 1);
  const auto inference_registers = inference_tracks[0]->data();
  const auto learning_registers = learning_tracks[0]->data();
  const auto address = device->program_mem()->tracked(inference_tracks[0]);
  const auto registers = learn_en ? learning_registers : inference_registers;
  device->driver()->write(address, registers->data(), registers->size());
}

void configure_learning_mode(HardwareDeviceImpl* device,
                             const uint8_t* program_data, bool learn_en) {
  auto* program = fb::GetProgram(program_data);
  const auto passes_size = program->passes()->size();
  if (passes_size == 1)
    single_pass_configure_learning_mode(device, program, learn_en);
  else
    multi_pass_configure_learning_mode(device, program, learn_en);
}

Shape output_dims(const uint8_t* program_data) {
  auto* program = fb::GetProgram(program_data);
  assert(program->output_dims()->size() == 3);
  const auto* output_dims_data = program->output_dims()->data();
  Shape ret(output_dims_data, output_dims_data + 3);
  return ret;
}

const Index* input_dims(const uint8_t* program_data) {
  auto* program = fb::GetProgram(program_data);
  assert(program->input_dims()->size() == 3);

  return program->input_dims()->data();
}

bool input_is_dense(const uint8_t* program_data) {
  auto* program = fb::GetProgram(program_data);
  return program->input_type() == fb::IoType_dense;
}

bool input_is_fnp(const uint8_t* program_data) {
  auto* program = fb::GetProgram(program_data);
  return program->input_type() == fb::IoType_fnp_sparse;
}

bool output_is_dense(const uint8_t* program_data) {
  auto* program = fb::GetProgram(program_data);
  return program->output_type() == fb::IoType_dense;
}

bool output_is_fnp(const uint8_t* program_data) {
  auto* program = fb::GetProgram(program_data);
  return program->output_type() == fb::IoType_fnp_sparse;
}

dma::OutputFormat output_format(const uint8_t* program_data) {
  auto* program = fb::GetProgram(program_data);
  switch (program->output_type()) {
    case fb::IoType_fnp_sparse: {
      return program->activation() ? dma::OutputFormat::FullyActivations
                                   : dma::OutputFormat::FullyPotentials;
    }
    case fb::IoType_cnp_sparse: {
      return program->activation() ? dma::OutputFormat::ConvActivations
                                   : dma::OutputFormat::ConvPotentials;
    }
    case fb::IoType_hrc_sparse: {
      return program->activation() ? dma::OutputFormat::HrcActivations
                                   : dma::OutputFormat::ConvHighPotentials;
    }
    case fb::IoType_dense: {
      return program->activation() ? dma::OutputFormat::DenseActivations
                                   : dma::OutputFormat::DensePotentials;
    }
    default:
      panic("Unsupported output type");
  }
}

bool activation(const uint8_t* program_data) {
  auto* program = fb::GetProgram(program_data);
  return program->activation();
}

uint32_t dense_window_w(const uint8_t* program_data) {
  auto* program = fb::GetProgram(program_data);
  return program->dense_window_w();
}

uint32_t dense_window_h(const uint8_t* program_data) {
  auto* program = fb::GetProgram(program_data);
  return program->dense_window_h();
}

Buffer<int32_t> shifts(const uint8_t* program_data) {
  auto* program = fb::GetProgram(program_data);
  auto shifts = program->shifts();
  auto data = shifts->data();
  auto size = shifts->size();
  return {data, size};
}

Buffer<float> scales(const uint8_t* program_data) {
  auto* program = fb::GetProgram(program_data);
  auto scales = program->scales();
  auto data = scales->data();
  auto size = scales->size();
  return {data, size};
}

bool can_learn(const uint8_t* program_data) {
  auto* program = fb::GetProgram(program_data);
  return program->learning_layer();
}

uint8_t max_num_desc(const uint8_t* program_data) {
  auto* program = fb::GetProgram(program_data);
  return program->max_num_desc();
}

uint32_t num_passes(const uint8_t* program_data) {
  auto* program = fb::GetProgram(program_data);
  return program->passes()->size();
}

bool is_multi_pass(const uint8_t* program_data) {
  return num_passes(program_data) > 1;
}

uint32_t learn_mem_size(const uint8_t* program_data) {
  auto* program = fb::GetProgram(program_data);
  auto learning_layer = program->learning_layer();
  if (!learning_layer) {
    return 0;
  }
  // return mem size, in number of 32bit words
  return learning_layer->learn_mem_size();
}

void update_learn_mem(HardwareDeviceImpl* device, const uint8_t* program_data,
                      const uint32_t* ram_dump) {
  auto* program = fb::GetProgram(program_data);
  auto learning_layer = program->learning_layer();
  if (!learning_layer) {
    panic(
        "Learn memory update requires a device programmed with learning "
        "layers");
  }

  // detect ram size
  auto size = learning_layer->learn_mem_size();
  // detect if FNP2 or FNP3
  auto record = learning_layer->ram();
  assert(record);
  auto fnp2_track = record->fnp2_track();
  if (fnp2_track) {
    // get memory address for this track
    auto mem_addr = device->program_mem()->tracked(fnp2_track);
    // update memory
    device->driver()->write(mem_addr, ram_dump, size);
  } else {
    auto update_learn_mem_hdr = learning_layer->update_learn_mem_hdr();
    // Note: for now a copy is necessary to update learn memory, to have config
    // header placed just before memory. In the future, a possible optimization
    // could be returning the header when reading the memory.
    std::vector<dma::w32> sram(dma::HDR_CONFIG_LEN + size);
    // first copy header in vector
    sram[0] = update_learn_mem_hdr->w1();
    sram[1] = update_learn_mem_hdr->w2();
    // then copy ram dump
    sram.insert(sram.begin() + dma::HDR_CONFIG_LEN, ram_dump, ram_dump + size);
    // now do transfer
    device->dma_config_write(sram.data(), sram.size());
  }
}

void learn_mem(HardwareDeviceImpl* device, const uint8_t* program_data,
               uint32_t* ram_dump) {
  auto* program = fb::GetProgram(program_data);
  auto learning_layer = program->learning_layer();
  if (!learning_layer) {
    panic("Learn memory retrieval requires a program from learning layers");
  }

  // detect ram size
  auto size = learning_layer->learn_mem_size();
  // detect if FNP2 or FNP3
  auto record = learning_layer->ram();
  assert(record);
  auto fnp2_track = record->fnp2_track();
  if (fnp2_track) {
    // get memory address for this track
    auto mem_addr = device->program_mem()->tracked(fnp2_track);
    device->driver()->read(mem_addr, ram_dump, size);
  } else {
    // in this case record is FNP3: read SRAM
    auto np = learning_layer->np();
    np::Ident ident(np->col(), np->row(), np->id());
    device->dma_config_read(ram_dump, ident, dma::Target::FnpWeights, 0, size);
  }
}

}  // namespace program
}  // namespace akida
