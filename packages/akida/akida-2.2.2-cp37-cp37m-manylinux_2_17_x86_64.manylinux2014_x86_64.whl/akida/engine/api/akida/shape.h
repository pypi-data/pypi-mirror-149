#pragma once

#include <cstddef>
#include <cstdint>
#include <limits>
#include <vector>

#include "infra/system.h"

namespace akida {

/**
 * @brief An abstract type to represent dimensions
 */
using Index = uint32_t;

/**
 * @brief A vector of dimensions representing a shape
 */
using Shape = std::vector<Index>;

/**
 * @brief Returns the total size of the shape (product of its dimensions)
 */
inline uint32_t shape_size(const Shape& s) {
  uint64_t size = 1;
  for (auto dim : s) {
    size *= dim;
  }
  constexpr size_t max_size = std::numeric_limits<uint32_t>::max();
  if (size > max_size) {
    panic("Shape size %lu exceeds maximum shape size (%u)", size, max_size);
  }
  return static_cast<uint32_t>(size);
}

/**
 * @brief Returns the linear index for the given coords and strides
 */
template<typename T>
inline size_t linear_index(const T* coords,
                           const std::vector<uint32_t>& strides) {
  size_t index = 0;
  for (size_t i = 0; i < strides.size(); ++i) {
    index += coords[i] * strides[i];
  }
  return index;
}

/**
 * @brief Returns the linear index for the given coords and strides
 */
inline size_t linear_index(const std::vector<Index>& coords,
                           const std::vector<uint32_t>& strides) {
  return linear_index(coords.data(), strides);
}

}  // namespace akida
