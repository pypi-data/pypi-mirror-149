#pragma once

#include <cassert>
#include <memory>
#include <vector>

#include "akida/shape.h"
#include "akida/sparse.h"
#include "akida/tensor.h"

#include "infra/system.h"

namespace akida {

class SparseImpl final : public Sparse {
 public:
  explicit SparseImpl(const Shape& shape = {},
                      TensorType type = TensorType::uint8)
      : type_(type), shape_(shape) {
    // How many coords do we need per event ?
    auto n_dims = shape_.size();
    // Evaluate the maximum number of events
    auto max_events = shape_size(shape_);
    coords_.reserve(n_dims * max_events);
    auto type_size = tensor_type_size(type);
    bytes_.reserve(type_size * max_events);
  }

  SparseImpl(const Shape& shape, const Index* coords, const char* bytes,
             size_t n_items, TensorType type)
      : SparseImpl(shape, type) {
    // How many coords do we need per event ?
    size_t n_dims = shape_.size();
    // Copy coordinates, verifying they fit in the shape
    coords_.reserve(n_items * n_dims);
    auto coord_ptr = coords;
    for (size_t n = 0; n < n_items; ++n) {
      for (size_t d = 0; d < n_dims; ++d) {
        if (*coord_ptr >= shape_[d]) {
          panic("Coordinate %d at index %d is out of range: %d >= %d", d, n,
                *coord_ptr, shape_[d]);
        }
        coords_.push_back(*coord_ptr);
        coord_ptr++;
      }
    }
    // Copy data
    auto type_size = tensor_type_size(type);
    bytes_.assign(bytes, bytes + n_items * type_size);
  }

  TensorType type() const override { return type_; }

  size_t size() const override {
    return shape_.size() ? coords_.size() / shape_.size() : 0;
  }

  Shape dimensions() const override { return shape_; }

  class Iterator final : public sparse::Iterator {
   public:
    explicit Iterator(const SparseImpl& sparse)
        :  // Event coords are contiguous: stride = number of coords per event
          coords_stride_(sparse.shape_.size()),
          // Event values are contiguous: stride = number of bytes per value
          bytes_stride_(tensor_type_size(sparse.type_)) {
      coords_ = sparse.coords_.data();
      // Coordinates end is deduced from the number of events
      coords_end_ = sparse.coords_.data() + sparse.size() * coords_stride_;
      bytes_ = sparse.bytes_.data();
    }
    // Iterator public API
    std::vector<Index> coords() const override {
      return std::vector<Index>(coords_, coords_ + coords_stride_);
    }
    const char* bytes() const override { return bytes_; }
    void next() override {
      coords_ += coords_stride_;
      bytes_ += bytes_stride_;
    }
    bool end() const override { return (coords_ == coords_end_); }
    // Iterator internal API
    size_t unravel(const std::vector<uint32_t>& strides) const override {
      return linear_index(coords_, strides);
    }

   private:
    const Index* coords_;
    const size_t coords_stride_;
    const Index* coords_end_;
    const char* bytes_;
    const size_t bytes_stride_;
  };

  sparse::IteratorPtr begin() const override {
    return std::make_shared<Iterator>(*this);
  }

  template<typename C>
  void push_back(const C& coords, const char* v) {
    assert(coords.size() == shape_.size());
    coords_.insert(coords_.end(), coords.begin(), coords.end());
    auto v_size = tensor_type_size(type());
    bytes_.insert(bytes_.end(), v, v + v_size);
  }

  template<typename C, typename V>
  void push_back(const C& coords, const V v) {
    auto vbytes = reinterpret_cast<const char*>(&v);
    push_back(coords, vbytes);
  }

 protected:
  TensorType type_;
  Shape shape_;
  std::vector<Index> coords_;
  std::vector<char> bytes_;
};

using SparseImplPtr = std::shared_ptr<SparseImpl>;
}  // namespace akida
