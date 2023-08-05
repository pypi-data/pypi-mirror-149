#pragma once

#include <cstdint>
#include <vector>

namespace akida {
namespace dma {

using w32 = uint32_t;
using wbuffer = std::vector<w32>;

// Akida memory addresses are stored in uint32_t
using addr = uint32_t;
// Many operations require address alignment to 32 bit.
// Inputs and outputs for all inbound buffers for DMA controllers (except for
// HRC, that can be just byte aligned), and for all outbound buffers used by DMA
// controllers.
constexpr uint32_t kAlignment = sizeof(addr);

}  // namespace dma
}  // namespace akida
