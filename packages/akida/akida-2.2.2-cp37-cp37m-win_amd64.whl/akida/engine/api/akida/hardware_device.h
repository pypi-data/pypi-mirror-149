/*******************************************************************************
 * Copyright 2021 Brainchip Holdings Ltd.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 ********************************************************************************
 */

#pragma once

#include <cstdint>
#include <memory>
#include <vector>

#include "akida/device.h"
#include "akida/tensor.h"
#include "infra/hardware_driver.h"

namespace akida {

class HardwareDevice;

using HardwareDevicePtr = std::shared_ptr<HardwareDevice>;
using HardwareDeviceConstPtr = std::shared_ptr<const HardwareDevice>;

/**
 * class HardwareDevice
 *
 * Public interface to an Akida Hardware Device.
 *
 * The main difference with Akida Device is the fact that HardwareDevice
 * objects driver real hardware, so they are capable of programming, performing
 * inference and few other hardware-specific calls.
 *
 */
class AKIDASHAREDLIB_EXPORT HardwareDevice : public Device {
 public:
  /**
   * @brief Creates a Hardware Device
   *
   * @param driver : the driver that should be used by the hardware device
   *
   * @return a HardwareDevice
   */
  static HardwareDevicePtr create(HardwareDriver* driver);

  /**
   * @brief Toggle the HardwareDevice clock counter on/off
   * @param enable : boolean to enable/disable clock counter
   */
  virtual void toggle_clock_counter(bool enable) = 0;

  /**
   * @brief Read the current HardwareDevice clock counter
   * @return a uint32 representing the clock count (can overlap)
   */
  virtual uint32_t read_clock_counter() = 0;

  /**
   * @brief Return memory information
   * @return a tuple containing current memory usage (in bytes) and top memory
   * usage (in bytes)
   */
  using MemoryInfo = std::pair<uint32_t, uint32_t>;
  virtual MemoryInfo memory() const = 0;

  /**
   * @brief Perform hardware device programming
   * @param program : serialized buffer containing the Device program
   * @param size : byte size of the buffer
   * @param learn_en : boolean to enable learning on the last layer
   */
  virtual void program(const uint8_t* program, size_t size, bool learn_en) = 0;

  /**
   * @brief Retrieve current program buffer
   * @return a pair of pointer and size of current program
   */
  using BytesBuffer = std::pair<const uint8_t*, size_t>;
  virtual const BytesBuffer& program() const = 0;

  /**
   * @brief Tells if current program has learning enabled
   * @return true if current program has learning enabled
   */
  virtual bool learn_enabled() const = 0;

  /**
   * @brief Tells current program learning memory size
   * @return memory size, in number of 32 bit words
   */
  virtual size_t learn_mem_size() const = 0;

  /**
   * @brief Writes a copy of the learn memory of current program in the given
   * buffer.
   * @param output_buffer : A pointer to a buffer large enough to contain
   * learning memory.
   */
  virtual void learn_mem(uint32_t* output_buffer) = 0;

  std::vector<uint32_t> learn_mem() {
    auto size = learn_mem_size();
    std::vector<uint32_t> ret(size);
    learn_mem(ret.data());
    return ret;
  }

  /**
   * @brief Updated learn memory from buffer containg a previously saved one
   * @param input_buffer : A pointer to a buffer containing updated learning
   * memory buffer
   */
  virtual void update_learn_mem(const uint32_t* input_buffer) = 0;

  /**
   * @brief Clear current program from hardware device, restoring its initial
   * state
   */
  virtual void unprogram() = 0;

  /**
   * @brief Processes inputs to train on a programmed device
   * @param inputs       : pointer to Sparse or Dense inputs
   * @param input_labels : integer value labels of the input classes,
   * for supervised learning
   * @param batch_size   : maximum number of inputs that should be processed at
   * a time. If 0, the whole input size will be taken.
   * @return Sparse or Dense outputs from the model last layer
   */
  virtual std::vector<TensorConstPtr> fit(
      const std::vector<TensorConstPtr>& inputs,
      const std::vector<int32_t>& input_labels) = 0;

  /**
   * @brief Processes inputs on a programmed device
   * @param inputs : vector of 3D inputs Tensor
   * @return vector of 3D outputs from the device
   */
  virtual std::vector<TensorConstPtr> forward(
      const std::vector<TensorConstPtr>& inputs) = 0;

  /**
   * @brief Evaluates the results of processing on a programmed device
   *
   * This method propagates a set of inputs through a programmed device and
   * returns the results in the form of a Tensor of float values.
   * It applies ONLY on programs coming from models that do not have an
   * activation on the last layer.
   * The output values are obtained from the outputs discrete potentials by
   * applying a shift and a scale.
   *
   * @param inputs : vector of 3D inputs Tensor
   * @return vector of 3D rescaled output potentials from the programmed device
   */
  virtual std::vector<TensorConstPtr> predict(
      const std::vector<TensorConstPtr>& inputs) = 0;

  /**
   * @brief Get the driver used by the device
   * @return The HardwareDriver object used by the device
   */
  virtual HardwareDriver* driver() const = 0;
};

}  // namespace akida
