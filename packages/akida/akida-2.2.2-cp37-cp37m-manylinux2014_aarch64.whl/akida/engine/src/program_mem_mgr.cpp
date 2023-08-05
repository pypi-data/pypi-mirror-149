
#include "engine/program_mem_mgr.h"

#include <cstdint>

#include "engine/memory_mgr.h"
#include "infra/system.h"

namespace akida {

uint32_t ProgramMemoryMgr::alloc_for_id(AllocId id, size_t byte_size) {
  // prevent allocating if ledger already contains an entry
  if (alloc_ledger_.find(id) != alloc_ledger_.end()) {
    panic("Tracked allocation ID 0x%p already taken", id);
  }
  auto addr = mem_mgr_->alloc(byte_size, MemoryMgr::Type::PROGRAM);
  // record in ledger
  alloc_ledger_[id] = addr;
  return addr;
}

void ProgramMemoryMgr::free_from_id(AllocId id) {
  auto addr = tracked(id);
  mem_mgr_->free(addr);
  alloc_ledger_.erase(id);
}

uint32_t ProgramMemoryMgr::tracked(AllocId id) const {
  auto entry = alloc_ledger_.find(id);
  // check if item is not in ledger
  if (entry == alloc_ledger_.end()) {
    panic("Tracked allocation ID 0x%p not found", id);
  }
  auto& addr = entry->second;
  return addr;
}

void ProgramMemoryMgr::reset() {
  // free all elements, in reverse order
  for (auto iter = alloc_ledger_.rbegin(); iter != alloc_ledger_.rend();
       ++iter) {
    mem_mgr_->free(iter->second);
  }
  // clear up map
  alloc_ledger_.clear();
}

}  // namespace akida
