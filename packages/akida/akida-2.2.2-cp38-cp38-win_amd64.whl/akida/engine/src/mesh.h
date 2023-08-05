#pragma once

#include <memory>
#include <vector>

#include "akida/np.h"
#include "engine/hardware_device_impl.h"

namespace akida {

namespace mesh {

/**
 * Discover the topology of a Device Mesh
 */
std::unique_ptr<np::Mesh> discover(HardwareDeviceImpl* device);

}  // namespace mesh

}  // namespace akida
