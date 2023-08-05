#include "dma_image_ops.h"

#include <algorithm>
#include <cassert>
#include <memory>
#include <vector>

#include "akida/dense.h"
#include "engine/dma.h"
#include "engine/dma_desc_ops.h"
#include "infra/hardware_driver.h"
#include "infra/int_ops.h"

namespace akida {

dma::Descriptor dma_image_write(HardwareDriver* driver,
                                const Dense::Buffer* buffer, uint32_t addr_in,
                                uint32_t addr_out, uint32_t job_id,
                                uint32_t learn_class,
                                const uint32_t* input_shape, uint32_t window_w,
                                uint32_t window_h) {
  // According to the HRC convention input shape is (h, w, c)
  const auto im_w = input_shape[1];
  const auto im_h = input_shape[0];
  const auto im_c = input_shape[2];

  // Generate input spikes for each image, tagged by image order
  uint32_t window_row_byte_size = window_w * im_c;
  uint32_t next_row_offset = im_w * im_c;
  uint32_t row_byte_size = im_w * im_c;
  uint32_t col_height = im_h;

  // If the HRC is used (i.e Not in bypass mode) the window sizes should be
  // different from 0. The HRC descriptor sent to the DMA needs to contain
  // the window sizes instead of the actual input sizes (they are only different
  // when using VALID convolutions) because the HRC needs to see only the pixels
  // it will use.
  if (window_h != 0 && window_w != 0) {
    row_byte_size = window_row_byte_size;
    col_height = window_h;
  } else {
    // if the HRC is in bypass mode this value is not needed by the descriptor
    next_row_offset = 0;
  }
  // TODO: window overlap parameters for now not supported
  const uint32_t window_overlap_bytesize = 0;
  const uint32_t x_offset = 0;
  const uint32_t y_offset = 0;

  // driver->write_data needs a buffer of dma words.
  uint32_t img_byte_size = im_w * im_h * im_c;
  assert(img_byte_size == buffer->size());
  uint32_t unaligned_bytes = img_byte_size % sizeof(uint32_t);
  uint32_t aligned_bytes = img_byte_size - unaligned_bytes;
  // write aligned bytes
  const auto data = buffer->data();
  driver->write(addr_in, reinterpret_cast<const uint32_t*>(data),
                aligned_bytes / sizeof(uint32_t));
  if (unaligned_bytes) {
    // copy unaligned bytes to last word
    uint32_t last_word = 0;
    memcpy(reinterpret_cast<uint8_t*>(&last_word), &data[aligned_bytes],
           unaligned_bytes);
    // write last word of unaligned bytes
    driver->write32(addr_in + aligned_bytes, last_word);
  }
  // generate descriptor
  return dma::format_hrc_desc(job_id, addr_in, addr_out, row_byte_size,
                              col_height, next_row_offset, window_row_byte_size,
                              window_h, window_overlap_bytesize, y_offset,
                              x_offset, learn_class);
}

}  // namespace akida
