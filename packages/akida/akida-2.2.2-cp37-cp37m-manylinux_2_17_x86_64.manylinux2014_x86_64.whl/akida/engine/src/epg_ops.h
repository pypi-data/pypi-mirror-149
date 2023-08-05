#pragma once

#include <cstdint>

#include "infra/hardware_driver.h"

namespace akida {

namespace epg {

void epg_reset(HardwareDriver* driver);

// number of 32 bit words necessary to store an event
static constexpr uint32_t EVENT_WORD_SIZE = 2;

}  // namespace epg

}  // namespace akida
