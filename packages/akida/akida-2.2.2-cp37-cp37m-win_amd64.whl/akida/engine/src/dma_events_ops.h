#pragma once
#include <cstdint>

#include "akida/shape.h"
#include "akida/tensor.h"
#include "engine/dma_desc_ops.h"
#include "infra/hardware_driver.h"

namespace akida {

namespace dma {

enum class OutputFormat {
  ConvActivations /**<Convolution Sparse 4-bit Activations*/,
  HrcActivations /**<Convolution Sparse 4-bit Activations in HRC*/,
  ConvPotentials /**<Convolution Sparse 20-bit Potentials*/,
  ConvHighPotentials /**<Convolution Sparse 24-bit Potentials*/,
  FullyActivations /**<FullyConnected Sparse 4-bit Activations*/,
  FullyPotentials /**<FullyConnected Sparse 20-bit Potentials*/,
  DenseActivations /**<Dense 4-bit Activations*/,
  DensePotentials /**<Dense 32-bit Potentials*/
};

}  // namespace dma

// Send events through dma
dma::Descriptor dma_packet_write(HardwareDriver* driver, TensorConstPtr inputs,
                                 bool input_is_fnp, uint32_t addr_in,
                                 uint32_t addr_out, uint32_t job_id,
                                 uint32_t learn_class);

// Read events at the given memory address and reformat them to spikes
TensorConstPtr dma_events_read_outputs(HardwareDriver* driver,
                                       const uint32_t addr_output_events,
                                       const Shape output_dimensions,
                                       dma::OutputFormat output_format);

// Get input frame size in bytes
uint32_t input_frame_size(uint32_t nb_items, bool is_dense);
// Get output frame size in bytes
uint32_t output_frame_size(uint32_t nb_items, dma::OutputFormat output_format);
// Get output buffer size in bytes (including header)
uint32_t output_buffer_size(uint32_t frame_size);

}  // namespace akida
