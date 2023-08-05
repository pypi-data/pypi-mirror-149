#include "akida/sparse.h"

#include <algorithm>
#include <cstdint>

#include "akida/shape.h"
#include "akida/tensor.h"

#include "sparse_impl.h"

namespace akida {

SparsePtr Sparse::from_buffers(const Shape& shape, const Index* coords,
                               const char* data, size_t n_items,
                               TensorType type) {
  return std::make_shared<SparseImpl>(shape, coords, data, n_items, type);
}

bool Sparse::operator==(const Tensor& ref) const {
  // We cannot compare Sparse easily, so we first to convert the ref to a dense
  auto dense = dynamic_cast<const Dense*>(&ref);
  if (dense) {
    // We can use the Dense operator directly
    return *dense == *this;
  }
  // As a fallback, we create a ColMajor Dense clone
  auto dense_clone = Dense::from_sparse(*this, Dense::Layout::ColMajor);
  // return Dense comparison
  return *dense_clone == ref;
}

static std::vector<Index> build_coord(Dense::Layout layout,
                                      std::vector<Index> base, Index i) {
  std::vector<Index> coord;
  coord.reserve(base.size() + 1);
  if (layout == Dense::Layout::RowMajor) {
    coord.insert(coord.begin(), base.begin(), base.end());
    coord.push_back(i);
  } else {
    coord.push_back(i);
    coord.insert(coord.end(), base.begin(), base.end());
  }
  return coord;
}

static void add_events_from_buffer(Dense::Layout layout, const char** bytes,
                                   size_t v_size, SparseImplPtr sparse,
                                   std::vector<Index> base) {
  auto shape = sparse->dimensions();
  auto cur_dim_index = (layout == Dense::Layout::RowMajor)
                           ? base.size()
                           : shape.size() - 1 - base.size();
  auto cur_dim = shape[cur_dim_index];
  if (base.size() < (shape.size() - 1)) {
    // Intermediate dimension, add coordinates for that dimension to the base
    for (Index i = 0; i < cur_dim; ++i) {
      auto new_base = build_coord(layout, base, i);
      // Recursively ask inner dimensions to complete the base coordinates
      add_events_from_buffer(layout, bytes, v_size, sparse, new_base);
    }
  } else {
    // This is the inner-most dimension: build full coordinates
    for (Index i = 0; i < cur_dim; ++i) {
      // Extract value for the next coordinate
      int v = 0;
      for (size_t j = 0; j < v_size; ++j) {
        v |= (*bytes)[j];
        if (v > 0) {
          break;
        }
      }
      if (v > 0) {
        auto coord = build_coord(layout, base, i);
        sparse->push_back(coord, *bytes);
      }
      *bytes += v_size;
    }
  }
}

SparsePtr Sparse::from_dense(const Dense& dense) {
  // Create an empty sparse
  auto sparse = std::make_shared<SparseImpl>(dense.dimensions(), dense.type());
  // Evaluate the bytes size of each value
  size_t v_size = tensor_type_size(dense.type());
  // Get a pointer to the dense data
  auto bytes = dense.buffer()->data();
  // Recursively add events to the Sparse for non-zero dense values
  add_events_from_buffer(dense.layout(), &bytes, v_size, sparse, {});
  return sparse;
}

}  // namespace akida
