#include "akida/dense.h"
#include "akida/hardware_device.h"

#include "TEST_NAME/inputs.h"
#include "TEST_NAME/outputs.h"
#include "TEST_NAME/program.h"

bool TEST_NAME(akida::HardwareDriver* driver) {
  // Instantiate the device for the corresponding driver
  auto device = akida::HardwareDevice::create(driver);
  // Program device
  device->program(program, program_len, false);
  // Wrap inputs inside a Dense
  auto input_tensor = akida::Dense::create_view(
      reinterpret_cast<const char*>(inputs), inputs_type, inputs_shape,
      akida::Dense::Layout::RowMajor);
  // Split inputs in sub-tensors as expected by the engine
  auto input_vector = akida::Tensor::split(input_tensor);
  // Wrap expected outputs inside a Dense
  auto output_tensor = akida::Dense::create_view(
      reinterpret_cast<const char*>(outputs), outputs_type, outputs_shape,
      akida::Dense::Layout::RowMajor);
  auto expected_vector = akida::Tensor::split(output_tensor);
  std::vector<akida::TensorConstPtr> obtained_vector;
  if (outputs_type == akida::TensorType::float32) {
    obtained_vector = device->predict(input_vector);
  } else {
    obtained_vector = device->forward(input_vector);
  }
  // Check the number of outputs
  if (obtained_vector.size() != expected_vector.size()) {
    return false;
  }
  // Compare each individual output
  for (size_t i = 0; i < obtained_vector.size(); ++i) {
    if (!(*obtained_vector[i] == *expected_vector[i])) {
      return false;
    }
  }
  return true;
}
