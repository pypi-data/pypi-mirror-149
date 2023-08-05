#pragma once

#include <cstddef>
#include <cstdint>
#include <vector>

#include "infra/exports.h"
#include "infra/interrupts.h"

namespace akida {

class BlockDevice {
 public:
  virtual ~BlockDevice() = default;
  /**
   * @brief read operation.
   * @param address: address where data should be read
   * @param data: pointer data that will store the result
   * @param size: size data to be read
   */
  virtual void read(uint32_t address, uint32_t* data, uint32_t size) const = 0;

  /**
   * @brief read operation.
   * @param address: address where data should be read
   * @param size: size data to be read
   */
  std::vector<uint32_t> read(uint32_t address, uint32_t size) const {
    std::vector<uint32_t> ret(size);
    read(address, ret.data(), size);
    return ret;
  }

  /**
   * @brief read operation.
   * @param address: address where data should be read
   */
  uint32_t read32(uint32_t address) const {
    uint32_t ret;
    read(address, &ret, 1);
    return ret;
  }

  /**
   * @brief write operation
   * @param address: address where data should be written
   * @param data: pointer data to be written
   * @param size: data size in number of 32 bit words
   */
  virtual void write(uint32_t address, const uint32_t* data, size_t size) = 0;

  /**
   * @brief write operation.
   * @param address: address where data should be written
   * @param data: data to be written (a vector of uint32_t)
   */
  void write(uint32_t address, const std::vector<uint32_t>& data) {
    write(address, data.data(), data.size());
  }

  /**
   * @brief write operation
   * @param address: address where data should be written
   * @param data: uint32_t data value to be written
   */
  void write32(uint32_t address, const uint32_t data) {
    write(address, &data, 1);
  }
};

class HardwareDriver : public BlockDevice {
 public:
  /**
   * @brief Return a null terminated string with driver description.
   */
  virtual const char* desc() const = 0;

  /**
   * @brief Return address used for scratch memory.
   */
  virtual uint32_t scratch_memory() const = 0;

  /**
   * @brief Return size (in bytes) available as scratch memory.
   */
  virtual uint32_t scratch_size() const = 0;

  /**
   * @brief Return address used for top level registers.
   */
  virtual uint32_t top_level_reg() const = 0;

  /**
   * @brief allow the system to perform driver background tasks.
   * @param wait_for_interrupt: if enabled, it will immediately return if an
   * interrupt happens.
   * @param timeout: after this delay (in ms), the function will return anyway
   *
   * The wait_for_interrupt parameter will come back if any of the enabled
   * interrupts happens.
   * Will return false if timeout is reached (unless timeout is 0).
   */
  virtual bool yield(bool wait_for_interrupt, uint32_t timeout) = 0;

  /**
   * @brief allow the interrupt source to wake up when calling yield.
   */
  virtual void enable_interrupt(enum akida_interrupt src) = 0;
};

}  // namespace akida
