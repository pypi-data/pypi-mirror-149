
#include "engine/memory_mgr.h"

#include <cassert>
#include <cstdint>

#include "engine/dma.h"
#include "infra/int_ops.h"
#include "infra/system.h"

namespace akida {

MemoryMgr::MemoryInfo MemoryMgr::report() const {
  auto current_memory = mem_offset_ - mem_base_offset_;
  auto top_memory = mem_top_offset_ - mem_base_offset_;
  return std::make_pair(current_memory, top_memory);
}

dma::addr MemoryMgr::alloc(size_t size, Type type) {
  assert(mem_offset_ == align_up(mem_offset_, dma::kAlignment));
  size = align_up(static_cast<uint32_t>(size), dma::kAlignment);
  // This will just make an address increment to store filters at different
  // addresses. Note that for now there is no memory management at all, this
  // feature could be added later.
  if (mem_offset_ + size > mem_bottom_offset_) {
    panic("Out of memory (requested 0x%u, currently using 0x%u)",
          static_cast<uint32_t>(size),
          static_cast<uint32_t>(mem_offset_ - mem_base_offset_));
  }
  auto ret = mem_offset_;
  scratch_buf_.push_back({mem_offset_, size, type});
  mem_offset_ += static_cast<uint32_t>(size);
  // update top memory usage if necessary
  if (mem_offset_ > mem_top_offset_) {
    mem_top_offset_ = mem_offset_;
  }
  return ret;
}

void MemoryMgr::free(uint32_t addr) {
  if (scratch_buf_.empty()) {
    panic("Cannot free address 0x%x", addr);
  }
  // reverse traverse vector, allocations probably happen in reverse order
  for (auto it = scratch_buf_.rbegin(); it != scratch_buf_.rend(); it++) {
    auto size = static_cast<uint32_t>(it->size);
    if (it->addr == addr) {
      // remove allocation. Note that erase takes a normal iterator, so we get
      // to the base iterator and point to the previous element.
      scratch_buf_.erase(it.base() - 1);
      // if this is the last item, then update the mem_offset_ by checking the
      // "highest" allocation in the list. This is necessary if the free had
      // been done in "disorder".
      if (addr + size == mem_offset_) {
        // if scratch_buf is empty, mem_offset can be completly reset
        if (scratch_buf_.empty()) {
          mem_offset_ = mem_base_offset_;
          return;
        }
        // update mem_offset to removed block start
        mem_offset_ = addr;
        for (auto& block : scratch_buf_) {
          auto block_upper_limit =
              block.addr + static_cast<uint32_t>(block.size);
          if (block_upper_limit > mem_offset_) {
            mem_offset_ = block_upper_limit;
          }
        }
      }
      return;
    }
  }
  panic("Address 0x%x not found: cannot free", addr);
}

void MemoryMgr::reset(MemoryMgr::Type type) {
  for (auto it = scratch_buf_.rbegin(); it != scratch_buf_.rend(); it++) {
    if (it->type == type) {
      free(it->addr);
    }
  }
}

}  // namespace akida
