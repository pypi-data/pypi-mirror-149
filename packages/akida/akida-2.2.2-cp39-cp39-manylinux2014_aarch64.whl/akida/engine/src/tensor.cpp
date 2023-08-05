#include "akida/tensor.h"

#include <memory>

#include "akida/dense.h"
#include "akida/sparse.h"

#include "sparse_impl.h"

#include "infra/system.h"

namespace akida {

DenseConstPtr Tensor::as_dense(TensorConstPtr tensor) {
  return std::dynamic_pointer_cast<const Dense>(tensor);
}

SparseConstPtr Tensor::as_sparse(TensorConstPtr tensor) {
  return std::dynamic_pointer_cast<const Sparse>(tensor);
}

DenseConstPtr Tensor::ensure_dense(TensorConstPtr tensor) {
  // Assume this is already a Dense
  auto dense = Tensor::as_dense(tensor);
  if (dense) {
    return dense;
  }
  // If we were passed a Sparse, convert it to a Dense
  auto sparse = std::dynamic_pointer_cast<const Sparse>(tensor);
  if (sparse) {
    return Dense::from_sparse(*sparse, Dense::Layout::RowMajor);
  }
  return nullptr;
}

SparseConstPtr Tensor::ensure_sparse(TensorConstPtr tensor) {
  // Assume this is a Sparse
  auto sparse = std::dynamic_pointer_cast<const Sparse>(tensor);
  if (sparse) {
    return sparse;
  }
  // Assume this is a Dense
  auto dense = std::dynamic_pointer_cast<const Dense>(tensor);
  if (dense) {
    return Sparse::from_dense(*dense);
  }
  return nullptr;
}

static std::vector<TensorConstPtr> split_sparse(const Sparse& sparse,
                                                Index dim) {
  auto initial_shape = sparse.dimensions();
  // Sub-tensors have one dimension less
  Shape shape(initial_shape.begin(), initial_shape.end());
  shape.erase(shape.begin() + dim);

  // Prepare empty Sparse sub-tensors
  auto n_sparse = initial_shape[dim];
  std::vector<SparseImplPtr> sparses;
  sparses.reserve(n_sparse);
  auto type = sparse.type();
  for (size_t n = 0; n < n_sparse; ++n) {
    sparses.push_back(std::make_shared<SparseImpl>(shape, type));
  }

  // Fill sub-tensors
  auto sparse_it = sparse.begin();
  while (!sparse_it->end()) {
    // Extract current coordinates
    auto coord = sparse_it->coords();
    // Get output index
    auto index = coord[dim];
    // Remove the collapsing dimension index
    coord.erase(coord.begin() + dim);
    // Populate the corresponding sub-tensor
    sparses[index]->push_back(coord, sparse_it->bytes());
    // Go to the next item
    sparse_it->next();
  }

  // Convert to abstract class vector
  std::vector<TensorConstPtr> outputs(sparses.begin(), sparses.end());
  return outputs;
}

static std::vector<TensorConstPtr> split_dense(const Dense& dense) {
  auto initial_shape = dense.dimensions();
  auto layout = dense.layout();
  // we split along the dimension with the biggest stride
  Index dim = static_cast<Index>(
      layout == Dense::Layout::RowMajor ? 0 : (initial_shape.size() - 1));
  // Sub-tensors have one dimension less
  Shape shape(initial_shape.begin(), initial_shape.end());
  shape.erase(shape.begin() + dim);

  // Prepare empty Dense sub-tensors
  auto n_dense = initial_shape[dim];
  std::vector<TensorConstPtr> denses;
  denses.reserve(n_dense);

  // Create sub-denses from underlying contiguous buffers
  auto bytes = dense.buffer()->data();
  auto byte_size = dense.buffer()->size() / n_dense;
  auto type = dense.type();
  for (size_t n = 0; n < n_dense; ++n) {
    auto view = Dense::create_view(bytes, type, shape, layout);
    denses.push_back(view);
    bytes += byte_size;
  }
  return denses;
}

std::vector<TensorConstPtr> Tensor::split(TensorConstPtr tensor, Index dim) {
  auto shape = tensor->dimensions();
  auto n_dims = shape.size();
  if (n_dims == 1) {
    panic("Cannot split a one-dimension tensor");
  }
  if (dim >= n_dims) {
    panic("Split: index %d is out-of-range (%d)", dim, n_dims);
  }
  // Assume the tensor is a dense
  auto dense = Tensor::as_dense(tensor);
  if (dense) {
    // We only support splitting a Dense along its highest stride dimension, as
    // it is a buffer copy
    auto layout = dense->layout();
    if ((layout == Dense::Layout::RowMajor && dim == 0) ||
        (layout == Dense::Layout::ColMajor && dim == n_dims - 1)) {
      return split_dense(*dense);
    } else {
      // Rely on Sparse split
      auto sparse_clone = Sparse::from_dense(*dense);
      return split_sparse(*sparse_clone, dim);
    }
  } else {
    // Then it is a Sparse
    auto sparse = Tensor::as_sparse(tensor);
    if (sparse) {
      return split_sparse(*sparse, dim);
    }
  }
  return {};
}

}  // namespace akida
