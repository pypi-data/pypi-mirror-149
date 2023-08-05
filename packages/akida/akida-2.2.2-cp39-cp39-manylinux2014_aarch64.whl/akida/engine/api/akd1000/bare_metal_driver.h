#pragma once

#include <cstdint>
#include <vector>

#include "akd1000/memory_mapping.h"
#include "infra/hardware_driver.h"

namespace akida {

class BareMetalDriver final : public HardwareDriver {
 public:
  BareMetalDriver();

  void read(uint32_t address, uint32_t* data, uint32_t size) const override;

  void write(uint32_t address, const uint32_t* data, size_t size) override;

  const char* desc() const override;

  uint32_t scratch_memory() const override { return soc::kScratchBase; }

  uint32_t scratch_size() const override { return soc::kScratchSize; }

  uint32_t top_level_reg() const override { return soc::kTopLevelRegBase; }

  bool yield(bool wait_for_interrupt, uint32_t timeout) override;

  void enable_interrupt(enum akida_interrupt src) override;
};

}  // namespace akida
