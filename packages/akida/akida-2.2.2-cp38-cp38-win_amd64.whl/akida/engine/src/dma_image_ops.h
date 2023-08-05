#pragma once

#include <cstdint>

#include "akida/dense.h"
#include "engine/dma_desc_ops.h"
#include "infra/hardware_driver.h"

namespace akida {

dma::Descriptor dma_image_write(HardwareDriver* driver,
                                const Dense::Buffer* buffer, uint32_t addr_in,
                                uint32_t addr_out, uint32_t job_id,
                                uint32_t learn_class,
                                const uint32_t* input_shape, uint32_t window_w,
                                uint32_t window_h);
}  // namespace akida
