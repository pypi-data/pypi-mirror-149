#include "np.h"

#include "akida/np.h"
#include "engine/dma_config_ops.h"
#include "engine/hardware_device_impl.h"
#include "engine/registers_np.h"
#include "infra/registers_common.h"

namespace akida {

namespace np {

Types get_types(HardwareDeviceImpl* device, const Ident& np) {
  Types result;
  // NP type informations are stored in register 1.
  uint32_t register_1;
  device->dma_config_read(&register_1, np, dma::Target::NpRegisters, 0, 1);
  auto fnp_type = get_field(register_1, REG1_FNP_INSTAL);
  auto cnp_type = get_field(register_1, REG1_CNP_INSTAL);

  if (fnp_type == 2) {
    result.insert(np::Type::FNP2);
  } else if (fnp_type == 3) {
    result.insert(np::Type::FNP3);
  }
  if (cnp_type == 1) {
    result.insert(np::Type::CNP1);
  } else if (cnp_type == 2) {
    // Mark CNP2 layers as CNP1 because for now we don't make a difference
    result.insert(np::Type::CNP1);
    result.insert(np::Type::CNP2);
  }
  return result;
}

}  // namespace np

}  // namespace akida
