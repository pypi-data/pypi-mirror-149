#pragma once

#include <cstddef>
#include <cstdint>
#include <memory>
#include <unordered_map>
#include <vector>

#include "akida/hardware_device.h"
#include "akida/hw_version.h"
#include "akida/np.h"
#include "akida/tensor.h"
#include "engine/dma.h"
#include "engine/dma_engine.h"
#include "engine/memory_mgr.h"
#include "engine/program_mem_mgr.h"
#include "infra/hardware_driver.h"

namespace akida {

namespace dma {
// forward declarations
enum class Target;
}  // namespace dma

class HardwareDeviceImpl final : public HardwareDevice {
 public:
  HardwareDeviceImpl(HardwareDriver* driver);

  ~HardwareDeviceImpl();

  // Device API
  HwVersion version() const override;

  const char* desc() const override { return driver_->desc(); }

  void pipeline(bool enable);

  void toggle_clock_counter(bool enable) override;

  uint32_t read_clock_counter() override;

  const np::Mesh& mesh() const override;

  void dma_config_write(const dma::w32* buffer, size_t buffer_size);

  void dma_config_read(dma::w32* buffer, const struct np::Ident& np,
                       dma::Target target, uint16_t addr_target_word,
                       uint32_t nb_words);

  void dma_start_config_multipass(dma::addr conf_base_address,
                                  uint32_t num_descs, uint32_t num_passes);

  // Device fit
  std::vector<TensorConstPtr> fit(
      const std::vector<TensorConstPtr>& inputs,
      const std::vector<int32_t>& input_labels) override {
    if (!current_program_learn_en_)
      panic("Learn must be enabled to call the fit method.");
    return dma_forward(inputs, &input_labels);
  }

  // Device forward
  std::vector<TensorConstPtr> forward(
      const std::vector<TensorConstPtr>& inputs) override {
    if (current_program_learn_en_)
      panic("Learn must be disabled to call the forward method.");
    return dma_forward(inputs, nullptr);
  };

  // Device predict
  std::vector<TensorConstPtr> predict(
      const std::vector<TensorConstPtr>& inputs) override;

  // perform hardware device programming
  void program(const uint8_t* program, size_t size, bool learn_en) override;

  // Clear the specified program
  void unprogram(const uint8_t* program);

  // unprogram current program
  void unprogram() override { unprogram(current_program_.first); }

  // Return the memory used currently in the device
  MemoryInfo memory() const override { return mem_mgr_.report(); };

  const BytesBuffer& program() const override { return current_program_; }

  bool learn_enabled() const override { return current_program_learn_en_; }

  size_t learn_mem_size() const override;

  void learn_mem(uint32_t* output_buffer) override;

  void update_learn_mem(const uint32_t* input_buffer) override;

  HardwareDriver* driver() const override { return driver_; }

  MemoryMgr* mem() { return &mem_mgr_; }

  ProgramMemoryMgr* program_mem() { return &current_program_mem_; }

 private:
  HardwareDriver* driver_;
  HwVersion version_;
  std::unique_ptr<np::Mesh> mesh_;
  dma::Config dma_config_;
  dma::Inputs dma_event_;
  dma::Inputs dma_hrc_;
  MemoryMgr mem_mgr_;
  BytesBuffer current_program_;
  bool current_program_learn_en_;
  ProgramMemoryMgr current_program_mem_;

  // Initialization helpers
  void reset_dma_engines();
  void init();

  std::vector<TensorConstPtr> dma_forward(
      const std::vector<TensorConstPtr>& inputs,
      const std::vector<int32_t>* labels);

  // DMA helpers
  const dma::Inputs& select_dma_engine(bool is_hrc);
  bool clock_counter_enabled();
};

}  // namespace akida
