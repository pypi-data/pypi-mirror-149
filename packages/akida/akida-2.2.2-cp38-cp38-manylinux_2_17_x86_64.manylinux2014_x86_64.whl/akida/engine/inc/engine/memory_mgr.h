#pragma once
#include <cstddef>
#include <utility>
#include <vector>

#include "engine/dma.h"

namespace akida {

class MemoryMgr {
 public:
  enum class Type { SYSTEM, IO, PROGRAM };
  struct Allocation {
    dma::addr addr;
    size_t size;
    Type type;
  };

  explicit MemoryMgr(const dma::addr base, const dma::addr size)
      : mem_base_offset_(base),
        mem_offset_(base),
        mem_top_offset_(base),
        mem_bottom_offset_(base + size) {}

  // This will give DDR memory (e.g.: to use for FNP2 filters).
  dma::addr alloc(size_t byte_size, Type type);

  // This will mark previously allocated memory as free
  void free(dma::addr addr);

  // Return the memory used currently in the device
  using MemoryInfo = std::pair<uint32_t, uint32_t>;
  MemoryInfo report() const;

  // Free all memory allocations of a given class
  void reset(Type type);

 private:
  const dma::addr mem_base_offset_;
  dma::addr mem_offset_;
  dma::addr mem_top_offset_;
  const dma::addr mem_bottom_offset_;
  std::vector<Allocation> scratch_buf_;
};

}  // namespace akida
