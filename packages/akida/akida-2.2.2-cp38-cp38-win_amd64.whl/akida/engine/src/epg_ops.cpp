#include "epg_ops.h"

#include <cstdint>

#include "engine/registers_epg.h"
#include "infra/registers_common.h"

namespace akida {
namespace epg {

void epg_reset(HardwareDriver* driver) {
  uint32_t reg = 0;
  // perform a soft reset
  set_field(&reg, SOFT_RESET, 1);
  // reset sequence id counter
  set_field(&reg, SEQ_ID_RESET, 1);
  driver->write32(epg_reg_base(driver->top_level_reg()) + AE_CTRL_REG, reg);
}

}  // namespace epg
}  // namespace akida
