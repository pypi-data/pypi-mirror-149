#pragma once

#include "infra/exports.h"

namespace akida {

/**
 * The hardware version identifier
 * Vendor_id / Product_id / Major_rev / Minor_rev
 */
struct AKIDASHAREDLIB_EXPORT HwVersion {
  uint8_t vendor_id;
  uint8_t product_id;
  uint8_t major_rev;
  uint8_t minor_rev;

  bool operator==(const HwVersion& ref) const {
    return (vendor_id == ref.vendor_id) && (product_id == ref.product_id) &&
           (major_rev == ref.major_rev) && (minor_rev == ref.minor_rev);
  }

  bool operator!=(const HwVersion& ref) const { return !(*this == ref); }
};

static constexpr HwVersion NSoC_v1 = {0xBC, 0, 0, 1};
static constexpr HwVersion NSoC_v2 = {0xBC, 0, 0, 2};
static constexpr HwVersion Latest = {0xBC, 1, 1, 0};

}  // namespace akida
