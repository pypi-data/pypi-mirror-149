#include "dma_events_ops.h"

#include <cstddef>
#include <functional>
#include <vector>

#include "akida/dense.h"
#include "akida/shape.h"
#include "akida/sparse.h"
#include "akida/tensor.h"
#include "dma_cnp_events.h"
#include "dma_events_format.h"
#include "dma_fnp_events.h"
#include "dma_hrc_events.h"
#include "engine/dma.h"
#include "engine/dma_desc_ops.h"
#include "engine/int_conversion.h"
#include "infra/registers_common.h"

namespace akida {

// number of 32 bit words necessary to store an event
static constexpr uint32_t EPG_EVENT_WORD_SIZE = 2;
// outputs header size
static constexpr uint32_t OUTPUT_HEADER_SIZE = 0x20;

static void set_cnp_event(Index x, Index y, Index z, uint8_t v,
                          dma::w32* evt_word1, dma::w32* evt_word2) {
  set_field(evt_word1, CONV_X, x);
  set_field(evt_word1, CONV_Y, y);
  set_field(evt_word2, CONV_F, z);
  set_field(evt_word2, CONV_ACTIVATION, v);
  // NOTE: polarity is not set
}

static void set_fnp_event(Index f, uint8_t v, dma::w32* evt_word1,
                          dma::w32* evt_word2) {
  set_field(evt_word1, FC_F, f);
  set_field(evt_word2, FC_ACTIVATION, v);
  set_field(evt_word2, FC_POLARITY, 1);
  // NOTE: the "fire" field is always set
}

static void add_dummy_event_fnp(const TensorConstPtr inputs,
                                dma::wbuffer* events) {
  // Add a dummy event for fnp, outside of dimensions with value 1. One index
  // out of the tensor in every dimension
  // (max coord is (shape[0] -1, shape[1] - 1, shape[2] - 1)
  // When null event forwarding, a dummy neuron is needed on NSoC-v2 and is
  // harmless on newer IP versions.
  const auto& shape = inputs->dimensions();
  auto strides = Dense::eval_strides(shape, Dense::Layout::ColMajor);
  auto index = static_cast<Index>(linear_index(shape, strides));
  dma::w32 evt_words[2] = {0, 0};
  set_fnp_event(index, 1, &evt_words[0], &evt_words[1]);
  events->insert(events->end(), evt_words, evt_words + 2);
}

static void add_dummy_event_cnp(const TensorConstPtr inputs,
                                dma::wbuffer* events) {
  // Add a dummy event for cnp, outside of dimensions with value 1. One index
  // out of the tensor in every dimension
  // (max coord is (shape[0] -1, shape[1] - 1, shape[2] - 1)
  // When null event forwarding, a dummy neuron is needed on NSoC-v2 and is
  // harmless on newer IP versions.
  const auto& shape = inputs->dimensions();
  dma::w32 evt_words[2] = {0, 0};
  set_cnp_event(shape[0], shape[1], shape[2], 1, &evt_words[0], &evt_words[1]);
  events->insert(events->end(), evt_words, evt_words + 2);
}

static dma::wbuffer format_cnp_events(const SparseConstPtr inputs) {
  auto nbevents = inputs->size();
  dma::wbuffer events(EPG_EVENT_WORD_SIZE * nbevents, 0);

  auto events_it = inputs->begin();
  for (size_t i = 0; i < nbevents; i++) {
    // map event words
    auto& evt_word1 = events[i * EPG_EVENT_WORD_SIZE];
    auto& evt_word2 = events[i * EPG_EVENT_WORD_SIZE + 1];

    auto v = events_it->value<uint8_t>();
    auto coords = events_it->coords();
    set_cnp_event(coords[0], coords[1], coords[2], v, &evt_word1, &evt_word2);
    events_it->next();
  }
  return events;
}

static dma::wbuffer format_fnp_events_3D(const SparseConstPtr inputs) {
  auto nbevents = inputs->size();
  dma::wbuffer events(EPG_EVENT_WORD_SIZE * nbevents, 0);

  // Evaluate the strides of the inputs following a col-major convention,
  // because the hardware linearizes the inputs using that convention
  auto strides =
      Dense::eval_strides(inputs->dimensions(), Dense::Layout::ColMajor);
  auto events_it = inputs->begin();
  for (size_t i = 0; i < nbevents; i++) {
    // map event words
    auto& evt_word1 = events[i * EPG_EVENT_WORD_SIZE];
    auto& evt_word2 = events[i * EPG_EVENT_WORD_SIZE + 1];

    auto v = events_it->value<uint8_t>();
    auto c = static_cast<Index>(events_it->unravel(strides));
    set_fnp_event(c, v, &evt_word1, &evt_word2);
    events_it->next();
  }
  return events;
}

static dma::wbuffer format_fnp_events(const SparseConstPtr inputs) {
  auto shape = inputs->dimensions();
  if ((shape.size() == 3) && ((shape[0] != 1) || (shape[1] != 1))) {
    // non-flat FNP inputs should be formatted as CNP, but if channel do not fit
    // on 11 bits, they need to be formatted as FNP and then we need to flatten
    // them
    assert(shape[2] > (1u << CONV_F.nb_bits) && "channels should be > 2048");
    return format_fnp_events_3D(inputs);
  }

  auto nbevents = inputs->size();
  dma::wbuffer events(EPG_EVENT_WORD_SIZE * nbevents, 0);

  auto events_it = inputs->begin();
  for (size_t i = 0; i < nbevents; i++) {
    // map event words
    auto& evt_word1 = events[i * EPG_EVENT_WORD_SIZE];
    auto& evt_word2 = events[i * EPG_EVENT_WORD_SIZE + 1];

    auto v = events_it->value<uint8_t>();
    // For a flat input, we only care about the last coordinate
    auto c = events_it->coords()[2];
    set_fnp_event(c, v, &evt_word1, &evt_word2);
    events_it->next();
  }
  return events;
}

static dma::wbuffer format_cnp_events(const DenseConstPtr inputs) {
  // We don't know how many events the Dense contains, but assume it is full
  dma::wbuffer events;
  events.reserve(EPG_EVENT_WORD_SIZE * inputs->size());

  auto shape = inputs->dimensions();
  auto w = shape[0];
  auto h = shape[1];
  auto c = shape[2];
  auto values_ptr = inputs->data<uint8_t>();
  for (Index x = 0; x < w; ++x) {
    for (Index y = 0; y < h; ++y) {
      for (Index z = 0; z < c; ++z) {
        // Extract value for the current coordinate
        auto value = *values_ptr;
        if (*values_ptr > 0) {
          dma::w32 evt_words[2] = {0, 0};
          set_cnp_event(x, y, z, value, &evt_words[0], &evt_words[1]);
          events.insert(events.end(), evt_words, evt_words + 2);
        }
        ++values_ptr;
      }
    }
  }
  return events;
}

static dma::wbuffer format_fnp_events(const DenseConstPtr inputs) {
  // We don't know how many events the Dense contains, but assume it is full
  dma::wbuffer events;
  events.reserve(EPG_EVENT_WORD_SIZE * inputs->size());

  auto values = inputs->data<uint8_t>();
  // For a flat input, we don't care about the coordinates
  for (Index i = 0; i < inputs->size(); ++i) {
    // Extract value for the current index
    auto value = values[i];
    if (value > 0) {
      dma::w32 evt_words[2] = {0, 0};
      set_fnp_event(i, value, &evt_words[0], &evt_words[1]);
      events.insert(events.end(), evt_words, evt_words + 2);
    }
  }
  return events;
}

static dma::wbuffer format_cnp_events(const TensorConstPtr inputs) {
  // Assume the tensor is Sparse
  auto sparse = Tensor::as_sparse(inputs);
  if (sparse) {
    return format_cnp_events(sparse);
  }
  return format_cnp_events(Tensor::as_dense(inputs));
}

static dma::wbuffer format_fnp_events(const TensorConstPtr inputs) {
  // Assume the tensor is Sparse
  auto sparse = Tensor::as_sparse(inputs);
  if (sparse) {
    return format_fnp_events(sparse);
  }
  return format_fnp_events(Tensor::as_dense(inputs));
}

using read_coords_cb = std::function<std::vector<Index>(dma::w32, dma::w32)>;
using read_value_cb = std::function<int32_t(dma::w32, dma::w32)>;

/**
 * Extract the potentials from a DMA word buffer and build an int32 Dense tensor
 */
static TensorConstPtr format_output_potentials(
    const dma::wbuffer& output_words, const Shape& out_dims,
    dma::OutputFormat output_format) {
  // We use lambdas to distinguish between the three potentials output formats
  read_value_cb read_value;
  read_coords_cb read_coords;
  switch (output_format) {
    case dma::OutputFormat::FullyPotentials: {
      read_coords = [](dma::w32 word, uint32_t) -> std::vector<Index> {
        auto f = static_cast<Index>(get_field(word, FC_F));
        return std::vector<Index>({0, 0, f});
      };
      read_value = [](dma::w32, dma::w32 word2) -> int32_t {
        return intN_to_int32<20>(get_field(word2, FC_ACTIVATION));
      };
    } break;
    case dma::OutputFormat::ConvHighPotentials: {
      read_coords = [](dma::w32 word1, dma::w32 word2) -> std::vector<Index> {
        auto x = static_cast<Index>(get_field(word1, CONV_X));
        auto y = static_cast<Index>(get_field(word1, CONV_Y));
        auto f = static_cast<Index>(get_field(word2, CONV_F));
        return std::vector<Index>({x, y, f});
      };
      read_value = [](dma::w32 word1, dma::w32 word2) -> int32_t {
        // The potential 4 MSB (including the sign) are on word 1
        auto pot_msb = intN_to_int32<4>(get_field(word1, CONV_POTENTIAL_MSB));
        // And the 20 LSB (positive number only) are on word 2
        auto pot_lsb =
            static_cast<int32_t>(get_field(word2, CONV_POTENTIAL_LSB));
        return (pot_msb << CONV_POTENTIAL_LSB.nb_bits) | pot_lsb;
      };
    } break;
    case dma::OutputFormat::ConvPotentials: {
      read_coords = [](dma::w32 word1, dma::w32 word2) -> std::vector<Index> {
        auto x = static_cast<Index>(get_field(word1, CONV_X));
        auto y = static_cast<Index>(get_field(word1, CONV_Y));
        auto f = static_cast<Index>(get_field(word2, CONV_F));
        return std::vector<Index>({x, y, f});
      };
      read_value = [](dma::w32, dma::w32 word2) -> int32_t {
        // The whole potential (including the sign) is on word 2
        return intN_to_int32<20>(get_field(word2, CONV_POTENTIAL_LSB));
      };
    } break;
    default: {
      panic("Unexpected output type");
    }
  }
  // Allocate the output dense buffer
  auto dense =
      Dense::create(TensorType::int32, out_dims, Dense::Layout::RowMajor);
  // Iterate over DMA events to fill the dense buffer
  uint32_t n_events =
      static_cast<uint32_t>(output_words.size() / EPG_EVENT_WORD_SIZE);
  for (uint32_t i = 0; i < n_events; i++) {
    // Events are stored in two consecutive words
    const auto& output_word1 = output_words[i * EPG_EVENT_WORD_SIZE];
    const auto& output_word2 = output_words[i * EPG_EVENT_WORD_SIZE + 1];
    // Read the output coords and value
    auto coords = read_coords(output_word1, output_word2);
    auto v = read_value(output_word1, output_word2);
    // Set the result
    dense->set(coords, v);
  }
  return dense;
}

static dma::Descriptor dma_event_data_write(HardwareDriver* driver,
                                            const dma::wbuffer& event_data,
                                            uint32_t addr_in, uint32_t addr_out,
                                            uint32_t job_id,
                                            uint32_t learn_class) {
  driver->write(addr_in, event_data);
  return dma::format_event_desc(job_id, addr_in, addr_out,
                                static_cast<uint32_t>(event_data.size()),
                                learn_class);
}

dma::Descriptor dma_packet_write(HardwareDriver* driver, TensorConstPtr inputs,
                                 bool input_is_fnp, uint32_t addr_in,
                                 uint32_t addr_out, uint32_t job_id,
                                 uint32_t learn_class) {
  // Check if we have been passed DMA CNP events
  const auto dma_cnp_events = dynamic_cast<const DmaCnpEvents*>(inputs.get());
  if (dma_cnp_events) {
    // Pass back the DMA CNP events data buffer directly
    return dma_event_data_write(driver, dma_cnp_events->data(), addr_in,
                                addr_out, job_id, learn_class);
  }
  // Check if we have been passed DMA FNP events
  const auto dma_fnp_events = dynamic_cast<const DmaFnpEvents*>(inputs.get());
  if (dma_fnp_events) {
    // Pass back the DMA FNP events data buffer directly
    return dma_event_data_write(driver, dma_fnp_events->data(), addr_in,
                                addr_out, job_id, learn_class);
  }
  // create Dma events from inputs
  dma::wbuffer event_data;
  if (input_is_fnp) {
    event_data = format_fnp_events(inputs);
    // workaround when null event
    if (event_data.empty()) {
      add_dummy_event_fnp(inputs, &event_data);
    }
  } else {
    event_data = format_cnp_events(inputs);
    // workaround when null event
    if (event_data.empty()) {
      add_dummy_event_cnp(inputs, &event_data);
    }
  }
  // check we are below the maximum number of events
  auto max_dma_events = dma::max_dma_events();
  if (event_data.size() > max_dma_events * EPG_EVENT_WORD_SIZE) {
    panic("%d exceeds the maximum number of events: %d", event_data.size(),
          max_dma_events);
  }

  return dma_event_data_write(driver, event_data, addr_in, addr_out, job_id,
                              learn_class);
}

TensorConstPtr dma_events_read_outputs(HardwareDriver* driver,
                                       const uint32_t addr_output_events,
                                       const Shape output_dimensions,
                                       dma::OutputFormat output_format) {
  // The header is the first word of the output
  uint32_t header = driver->read32(addr_output_events);
  uint32_t output_word_size = get_field(header, OUTPUT_WORD_SIZE);

  // adjust past header to data
  uint32_t read_offset_addr = addr_output_events + OUTPUT_HEADER_SIZE;

  switch (output_format) {
    case dma::OutputFormat::ConvActivations: {
      // Read back data aligned on 32-bit words
      auto output_events = driver->read(read_offset_addr, output_word_size);
      // We can directly wrap the output events in a DmaCnpEvents sparse tensor
      return std::make_shared<DmaCnpEvents>(output_dimensions,
                                            std::move(output_events));
    }
    case dma::OutputFormat::FullyActivations: {
      // Read back data aligned on 32-bit words
      auto output_events = driver->read(read_offset_addr, output_word_size);
      // We can directly wrap the output events in a DmaFnpEvents sparse tensor
      return std::make_shared<DmaFnpEvents>(output_dimensions,
                                            std::move(output_events));
    }
    case dma::OutputFormat::HrcActivations: {
      // Read back data aligned on 32-bit words
      auto output_events = driver->read(read_offset_addr, output_word_size);
      // We can directly wrap the output events in a DmaCnpEvents sparse tensor
      return std::make_shared<DmaHrcEvents>(output_dimensions,
                                            std::move(output_events));
    }
    case dma::OutputFormat::DenseActivations: {
      // Read back data aligned on 32-bit words
      auto output_events = driver->read(read_offset_addr, output_word_size);
      // We need to copy the output activation bytes in a dense tensor
      auto out_bytes = reinterpret_cast<const char*>(output_events.data());
      auto out_size = shape_size(output_dimensions) * sizeof(uint8_t);
      return Dense::copy(out_bytes, out_size, TensorType::uint8,
                         output_dimensions, Dense::Layout::RowMajor);
    }
    case dma::OutputFormat::DensePotentials: {
      // Create an empty tensor
      auto dense = Dense::create(TensorType::int32, output_dimensions,
                                 Dense::Layout::RowMajor);
      // Since potentials are 32-bit aligned, we can directly read back the data
      auto potentials = reinterpret_cast<uint32_t*>(dense->buffer()->data());
      driver->read(read_offset_addr, potentials, output_word_size);
      return dense;
    }
    default: {
      // Read back data aligned on 32-bit words
      auto output_events = driver->read(read_offset_addr, output_word_size);
      // Extract potentials and create a Dense
      return format_output_potentials(output_events, output_dimensions,
                                      output_format);
    }
  }
}

uint32_t input_frame_size(uint32_t nb_items, bool is_dense) {
  uint32_t item_byte_size = 1;
  if (!is_dense) {
    // Sparse events format
    item_byte_size = EPG_EVENT_WORD_SIZE * 4;
  }
  return nb_items * item_byte_size;
}

uint32_t output_frame_size(uint32_t nb_items, dma::OutputFormat output_format) {
  uint32_t item_byte_size;
  switch (output_format) {
    case dma::OutputFormat::DenseActivations: {
      item_byte_size = 1;
      break;
    }
    case dma::OutputFormat::DensePotentials: {
      item_byte_size = 4;
      break;
    }
    default: {
      // Sparse events format
      item_byte_size = EPG_EVENT_WORD_SIZE * 4;
      break;
    }
  }
  return nb_items * item_byte_size;
}

uint32_t output_buffer_size(uint32_t frame_size) {
  // Output buffer also includes a header
  return frame_size + OUTPUT_HEADER_SIZE;
}

}  // namespace akida
