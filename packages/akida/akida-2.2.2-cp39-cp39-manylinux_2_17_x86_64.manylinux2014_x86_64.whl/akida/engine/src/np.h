#pragma once

#include <cstdint>

#include "akida/np.h"

namespace akida {

class HardwareDeviceImpl;

namespace np {

Types get_types(HardwareDeviceImpl* device, const Ident& np);

}  // namespace np

}  // namespace akida
