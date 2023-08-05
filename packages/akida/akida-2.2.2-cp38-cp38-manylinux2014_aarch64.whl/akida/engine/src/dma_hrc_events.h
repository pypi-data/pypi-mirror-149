#pragma once

#include <memory>

#include "akida/shape.h"
#include "akida/sparse.h"

#include "infra/int_ops.h"

#include "engine/dma.h"

namespace akida {

class DmaHrcEvents final : public Sparse {
 public:
  DmaHrcEvents(const Shape& shape, const dma::wbuffer&& dma_words)
      : shape_(shape), dma_words_(std::move(dma_words)) {}

  TensorType type() const override { return TensorType::uint8; }

  size_t size() const override {
    // Each event is stored in two DMA words
    return dma_words_.size() / 2;
  }

  Shape dimensions() const override { return shape_; }

  class Iterator final : public sparse::Iterator {
   public:
    // The events are stored contiguously using two dma words
    static constexpr size_t kEventsStride = 2 * sizeof(dma::w32);
    explicit Iterator(const DmaHrcEvents& events)
        :  // Coords and values strides are deduced form the event stride
          coords_stride_(kEventsStride / sizeof(*coords_)),
          bytes_stride_(kEventsStride / sizeof(*bytes_)),
          max_index_(shape_size(events.shape_) - 1),
          shape_(events.shape_) {
      // The coords are aligned on 16-bit starting from the first event word
      coords_ = reinterpret_cast<const uint16_t*>(events.dma_words_.data());
      // Coordinates end is deduced from the number of events
      coords_end_ = coords_ + events.size() * coords_stride_;
      // The values are in the last 16-bit part of the second event word
      auto values =
          reinterpret_cast<const uint16_t*>(events.dma_words_.data() + 1) + 1;
      // Values are actually represented using a bytes pointer
      bytes_ = reinterpret_cast<const char*>(values);
    }
    // Iterator public API
    std::vector<Index> coords() const override {
      // shape interpretation is inverted in the HRC internal operation
      if (coords_[0] >= shape_[1] || coords_[1] >= shape_[0] ||
          coords_[2] >= shape_[2]) {
        panic("HRC: coordinates (%d, %d, %d) are out-of-range.", coords_[1],
              coords_[0], coords_[2]);
      }
      return std::vector<Index>{coords_[1], coords_[0], coords_[2]};
    }
    const char* bytes() const override { return bytes_; }
    void next() override {
      coords_ += coords_stride_;
      bytes_ += bytes_stride_;
    }
    bool end() const override { return (coords_ == coords_end_); }
    // Iterator internal API
    size_t unravel(const std::vector<uint32_t>& strides) const override {
      size_t index = 0;

      // Invert stride if hrc events
      index += coords_[0] * strides[1];
      index += coords_[1] * strides[0];
      index += coords_[2] * strides[2];

      if (index > max_index_) {
        panic("HRC: coordinates (%d, %d, %d) are out-of-range.", coords_[1],
              coords_[0], coords_[2]);
      }
      return index;
    }

   private:
    const uint16_t* coords_;
    const size_t coords_stride_;
    const uint16_t* coords_end_;
    const char* bytes_;
    const size_t bytes_stride_;
    const size_t max_index_;
    const Shape shape_;
  };

  sparse::IteratorPtr begin() const override {
    return std::make_shared<Iterator>(*this);
  }

  const dma::wbuffer& data() const { return dma_words_; }

 protected:
  Shape shape_;
  dma::wbuffer dma_words_;
};

using DmaHrcEventsPtr = std::shared_ptr<DmaHrcEvents>;
}  // namespace akida
