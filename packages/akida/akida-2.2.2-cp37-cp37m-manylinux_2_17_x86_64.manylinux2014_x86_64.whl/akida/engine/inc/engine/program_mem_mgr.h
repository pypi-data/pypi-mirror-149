#pragma once
#include <cstddef>
#include <map>

#include "engine/dma.h"
#include "engine/memory_mgr.h"

namespace akida {

class ProgramMemoryMgr {
 public:
  explicit ProgramMemoryMgr(MemoryMgr* mgr) : mem_mgr_(mgr) {}

  // Allocate and keep track in ledger. To be used by program
  using AllocId = const void*;
  uint32_t alloc_for_id(AllocId id, size_t byte_size);
  // Allocate and keep track in ledger, use any pointer type
  template<class T>
  uint32_t alloc_for_id(const T* p, size_t byte_size) {
    AllocId id = reinterpret_cast<AllocId>(p);
    return alloc_for_id(id, byte_size);
  }
  // Free memory allocated with alloc and track
  void free_from_id(AllocId id);
  // Free memory allocated with alloc and track, use any pointer type
  template<class T>
  void free_from_id(const T* p) {
    AllocId id = reinterpret_cast<AllocId>(p);
    free_from_id(id);
  }
  // get previously allocated address by id
  uint32_t tracked(AllocId id) const;
  // get previously allocated address by id, use any pointer type
  template<class T>
  uint32_t tracked(const T* p) const {
    AllocId id = reinterpret_cast<AllocId>(p);
    return tracked(id);
  }

  // Free all memory allocations, to restore initial state
  void reset();

 private:
  // memory manager
  MemoryMgr* mem_mgr_;
  // allocation ledger, a map of id:addresss
  std::map<AllocId, uint32_t> alloc_ledger_;
};

}  // namespace akida
