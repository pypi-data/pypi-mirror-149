#pragma once

#include <cstdint>

namespace akida {

namespace dma {

struct Engine {
 public:
  explicit Engine(uint32_t reg_base_addr, uint32_t descriptor_len);

  uint32_t descriptor_base_addr;
  const uint32_t descriptor_len;
  const uint32_t reg_base_addr;
  uint32_t num_descriptors;
};

struct Config {
  Engine engine;
};

struct Inputs {
  Engine engine;
};

}  // namespace dma

}  // namespace akida
