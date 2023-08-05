#include "reset_nps.h"

#include <cassert>
#include <cstddef>
#include <cstdint>

#include "engine/dma.h"
#include "engine/dma_config_ops.h"
#include "engine/registers_np.h"
#include "infra/hardware_driver.h"
#include "infra/registers_common.h"
#include "infra/system.h"
#include "registers_reset.h"
#include "registers_top_level.h"

namespace akida {

// This method resets logic and configuration of all NPs. It is available on
// versions > nsoc v1
void reset_nps_logic_and_cfg(HardwareDriver* driver) {
  const auto top_level_reg_offset = driver->top_level_reg();
  auto reg_gen_ctrl =
      driver->read32(top_level_reg_offset + REG_GENERAL_CONTROL);
  // Reset logic & configuration
  set_field(&reg_gen_ctrl, AK_LOGIC_RST, 1);
  set_field(&reg_gen_ctrl, AK_MESH_RST, 1);
  driver->write32(top_level_reg_offset + REG_GENERAL_CONTROL, reg_gen_ctrl);
  // 20 cycles should be waited. Waiting 1ms is more than enough.
  msleep(1);
  // Fields need to be reset to 0
  set_field(&reg_gen_ctrl, AK_LOGIC_RST, 0);
  set_field(&reg_gen_ctrl, AK_MESH_RST, 0);
  driver->write32(top_level_reg_offset + REG_GENERAL_CONTROL, reg_gen_ctrl);
  // 40 cycles should be waited. Waiting 1ms is more than enough.
  msleep(1);
}

}  // namespace akida
