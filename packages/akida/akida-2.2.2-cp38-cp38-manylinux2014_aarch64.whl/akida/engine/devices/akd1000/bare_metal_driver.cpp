#include "akd1000/bare_metal_driver.h"

#include <cstdio>
#include <cstring>
#include <vector>

#include "infra/registers_common.h"

#include "akd1000/registers_soc.h"

namespace akida {

static constexpr uint32_t regs_offset = 0xFCC00000u;

BareMetalDriver::BareMetalDriver() {}

void BareMetalDriver::read(uint32_t address, uint32_t* data,
                           uint32_t size) const {
  memcpy(data, reinterpret_cast<void*>(address), sizeof(uint32_t) * size);
}

void BareMetalDriver::write(uint32_t address, const uint32_t* data,
                            size_t size) {
  memcpy(reinterpret_cast<void*>(address), data, sizeof(uint32_t) * size);
}

const char* BareMetalDriver::desc() const {
  static char version_str[32];
  auto reg = read32(REG_CHIP_INFO);
  auto version = get_field(reg, REG_CHIP_VERSION);
  snprintf(version_str, sizeof(version_str), "Embedded/NSoC_v%ld", version);
  return version_str;
}

bool BareMetalDriver::yield(bool wait_for_interrupt, uint32_t timeout) {
  return true;
}

void BareMetalDriver::enable_interrupt(enum akida_interrupt src) {}

}  // namespace akida
