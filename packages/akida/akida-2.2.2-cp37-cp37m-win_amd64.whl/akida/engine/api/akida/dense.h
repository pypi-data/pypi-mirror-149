#pragma once

#include <cstdint>
#include <cstring>
#include <memory>
#include <vector>

#include "akida/shape.h"
#include "akida/tensor.h"
#include "infra/exports.h"

/** file akida/dense.h
 * Contains the abstract Dense object and its related types
 */

namespace akida {

/**
 * @brief A shared pointer to a Dense object
 */
using DensePtr = std::shared_ptr<Dense>;

/**
 * @brief A shared pointer to a const Dense object
 */
using DenseConstPtr = std::shared_ptr<const Dense>;

/**
 * class Dense
 *
 * An abstraction of a multi-dimensional dense array
 *
 * Stores data using a column-major (default) or row-major layout
 *
 * To iterate over the values of a Dense of type T, one would typically call
 * the data<T>() templated member.
 *
 */
class AKIDASHAREDLIB_EXPORT Dense : public Tensor {
 public:
  virtual ~Dense() {}

  bool operator==(const Tensor& ref) const override;

  bool operator==(const Dense& ref) const {
    auto shape = dimensions();
    return type() == ref.type() && layout() == ref.layout() &&
           std::equal(shape.begin(), shape.end(), ref.dimensions().begin()) &&
           size() == ref.size() &&
           std::memcmp(buffer()->data(), ref.buffer()->data(),
                       buffer()->size()) == 0;
  }

  class Buffer {
   public:
    virtual ~Buffer() = default;

    /**
     * @brief Returns the size of the buffer data in bytes
     */
    virtual size_t size() const = 0;
    /**
     * @brief Returns a raw pointer to the buffer data
     */
    virtual char* data() = 0;
    /**
     * @brief Returns a raw pointer to the buffer data
     */
    virtual const char* data() const = 0;
  };

  /**
   * @brief Returns the underlying buffer
   */
  virtual Buffer* buffer() = 0;

  /**
   * @brief Returns the underlying buffer
   */
  virtual const Buffer* buffer() const = 0;

  /**
   * @brief Returns a data pointer corresponding to the specified templated type
   */
  template<typename T>
  T* data() {
    check_type<T>();
    return reinterpret_cast<T*>(buffer()->data());
  }

  /**
   * @brief Returns a data pointer corresponding to the specified templated type
   */
  template<typename T>
  const T* data() const {
    check_type<T>();
    return reinterpret_cast<const T*>(buffer()->data());
  }

  /**
   * @enum  Layout
   * @brief The Dense memory layout (storage order)
   * The memory layout of a Dense tensor has an impact on how the linear index
   * of the elements is calculated from each element coordinates.
   * For a row-major Dense, when you increment the first coordinate, the element
   * index is incremented by a factor corresponding to the product of all
   * dimensions but the first one.
   * On the contrary, for a column-major Dense, when you increment the first
   * coordinate, the index is just incremented by one.
   */
  enum class Layout {
    RowMajor /**<RowMajor, or 'biggest stride first'*/,
    ColMajor /**<ColMajor, or 'smallest stride first'*/
  };

  /**
   * @brief returns the Dense tensor layout
   * @return : Layout::ColMajor or Layout::RowMajor
   */
  virtual Layout layout() const = 0;

  /**
   * @brief returns the Dense strides for each dimension
   * @return : a vector of strides for direct access to the tensor data
   */
  virtual const std::vector<uint32_t>& strides() const = 0;

  /**
   * @brief Get the value at the specified coordinates
   * @param coords : the set of coordinates
   * @return the Dense value at these coordinates
   */
  template<typename T>
  T get(const std::vector<Index>& coords) const {
    auto index = linear_index(coords, strides());
    if (index > size() - 1) {
      panic("Coordinates are out-of-range");
    }
    return data<T>()[index];
  }

  /**
   * @brief Set the value at the specified coordinates
   * @param coords : the set of coordinates
   * @param value : the value at these coordinates
   */
  template<typename T>
  void set(const std::vector<Index>& coords, T value) {
    auto index = linear_index(coords, strides());
    if (index > size() - 1) {
      panic("Coordinates are out-of-range");
    }
    data<T>()[index] = value;
  }

  /**
   * @brief Set the same value at all coordinates
   * @param value : the value
   */
  template<typename T>
  void fill(T value) {
    auto cached_size = size();
    for (size_t i = 0; i < cached_size; ++i) {
      data<T>()[i] = value;
    }
  }

  /**
   * @brief Returns the strides corresponding to the given shape
   * @param shape : the Dense tensor dimensions
   * @param layout : the Dense tensor layout
   * @return : a vector of strides for direct access to the tensor data
   */
  static std::vector<uint32_t> eval_strides(const Shape& shape, Layout layout);

  /**
   * @brief Create a Dense, allocating its internal buffer
   *
   * Note that the internal buffer is not zero-initialized.
   *
   * @param type   : the Tensor data type, as an akida::TensorType
   * @param dims   : the Tensor dimensions
   * @param layout : the source array layout, can be one of akida::RowMajor,
   * akida::ColMajor
   *
   * If the source array is Row-major, then the order of dimensions of the
   * created Tensor will be reversed.
   */
  static DensePtr create(TensorType type, const Shape& dims,
                         Dense::Layout layout);

  /**
   * @brief Create a Dense whose internal buffer contains a copy of a byte array
   * @param array  : a pointer to the source byte array
   * @param size   : the array size in bytes
   * @param type   : the Tensor data type, as an akida::TensorType
   * @param dims   : the Tensor dimensions
   * @param layout : the source array layout, can be one of akida::RowMajor,
   * akida::ColMajor
   *
   * If the source array is Row-major, then the order of dimensions of the
   * created Tensor will be reversed.
   */
  static DensePtr copy(const char* array, size_t bytes_size, TensorType type,
                       const Shape& dims, Dense::Layout layout);

  /**
   * @brief Create a Dense from Sparse
   * @param sparse : the Sparse object to clone
   */
  static DensePtr from_sparse(const Sparse& sparse, Layout layout);

  /**
   * @brief Create a Dense view from a C/C++ byte array
   * @param array  : a pointer to the source byte array
   * @param type   : the Tensor data type, as an akida::TensorType
   * @param dims   : the Tensor dimensions
   * @param layout : the source array layout, can be one of akida::RowMajor,
   * akida::ColMajor
   *
   * If the source array is Row-major, then the order of dimensions of the
   * created Tensor will be reversed. This DensePtr will not own a buffer, but
   * rather point to an externally allocated buffer
   */
  static DensePtr create_view(char* array, TensorType type, const Shape& dims,
                              Dense::Layout layout);

  /**
   * @brief Create a Dense view from a C/C++ byte array
   * @param array  : a pointer to the source byte array
   * @param type   : the Tensor data type, as an akida::TensorType
   * @param dims   : the Tensor dimensions
   * @param layout : the source array layout, can be one of akida::RowMajor,
   * akida::ColMajor
   *
   * Constant version of create_view.
   */
  static DenseConstPtr create_view(const char* array, TensorType type,
                                   const Shape& dims, Dense::Layout layout);
};

}  // namespace akida
