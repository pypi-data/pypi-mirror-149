# Akida Engine library

The **Akida Engine** library is a C++ library allowing to perform an inference
on an Akida model loaded into an Akida compatible device.

As a prerequisite, the Akida model program has to be generated on a host using
the [Akida python package](https://pypi.org/project/Akida/).

## Building the library

### Build system

The Akida Engine library does not have any specific build system requirements.

### Toolchain/Compiler

The Akida Engine library requires a 32 or 64 bit little endian toolchain with
support for floating point numbers.

The toolchain must include a C++ compiler supporting at least C++ 11.

The toolchain must provide a minimal implementation of the C standard library,
like for instance GCC newlib and the corresponding target-specific stubs.

The Akida Engine library does not use C++ exceptions, so exception support can
be disabled when generating binaries for embedded targets.

### Dependencies

The library relies on external symbols whose target-specific implementation must
be provided by the build system.

#### Google flatbuffers

The library has a dependency towards the Google flatbuffer header-only library:
   https://github.com/google/flatbuffers/releases/tag/v1.12.0

The sources must be downloaded from the link above and made available to the
library as an additional include path.

#### Standard Template Library (STL)

The Akida Engine library relies on a few C++ STL classes whose implementation
must be provided by the build system.

The following headers must be supported:

<algorithm>
<array>
<functional>
<memory>
<queue>
<set>
<tuple>
<typeindex>
<vector>

#### System infra

The Akida Engine library requires a few system methods to be implemented.

Please refer to api/infra/system.h for a list and description of the methods to
implement.

### Building a static library

A basic cmake build file is provided for convenience:

~~~~
mkdir build
cmake . -B build
make -C build
~~~~

### Using the library

#### Hardware driver

The Akida Engine library primary entry point is the HardwareDevice class.

One can obtain an HardwareDevice instance by passing a target-specific
HardwareDriver instance to HardwareDevice::create().

~~~~
#include "akida/hardware_device.h"
#include "infra/hardware_driver.h"

class MyDriver : public HardwareDriver {
...
}

...

auto driver = MyDriver();
auto device = HardwareDevice::create(driver);
~~~~

The HardwareDriver main purpose is to abstract the read and write operations
into the Akida DMA.
It also provides:
- the base address for Akida blocks registers
- the 'scratch' memory region where the library can allocate buffers to
communicate with the Akida DMA (runtime configuration, inputs/outputs).

Please refer to api/infra/hardware_driver.h for a complete description of the
HardwareDriver API and how to implement your specific driver.

#### Generate model programs

The akida engine library allows to program an akida device with machine
learning models previously trained and compiled.

The akida and cnn2snn python packages are required to generate model programs
from pre-trained keras models.

The akida_models python package contains helpers to fetch models from the akida
model zoo.

~~~~
#!/usr/bin/env python
import os
from akida import AKD1000
from akida.deploy array_to_cpp
from cnn2snn import convert
from akida_models import ds_cnn_kws_pretrained

# Load Keras pre-trained model from Akida model zoo
model_keras = ds_cnn_kws_pretrained()

# Convert Keras model to Akida
model_akida = convert(model_keras)

# Map/compile converted model for an AKD1000 device
model_akida.map(device=AKD1000(), hw_only=True)

# Check model mapping: NP allocation and binary size
model_akida.summary()

# Retrieve model program binary
program = model_akida.sequences[0].program

# Generate a binary that can be flashed
with open('kws_model.bin', 'wb') as file:
    file.write(program)
    file.close()

# Or generate source files to be included -> kws_model.{cpp,h}
    array_to_cpp('.’, program, 'kws_model')
~~~~

#### Load model programs

Once loaded in memory, the raw bytes buffer corresponding to a model program
can be passed to the HardwareDevice to program the model on the device.

~~~~
#include "kws_model.h"

// Load program with learn disabled
device->program(kws_model, kws_model_size, false);
~~~~

#### Perform an inference

Once a model has been programmed, a vector of input Tensor objects can be passed
for inference, the device returning a corresponding vector of Tensor outputs.

~~~~
#include "akida/dense.h"

// Passing a single input from a raw input dense buffer
auto input = Dense::create_view(input_buf, TensorType::uint8, {49, 10, 1},
                                TensorLayout::RowMajor);
auto outputs = device->predict({input});
~~~~

Two types of tensors can be passed as input and returned as outputs:
- Dense tensors are standard contiguous buffers whose items are ordered either
using the row-major or col-major convention,
- Sparse tensors are list of coordinates and values.

Several static constructors are available to create tensors of both types,
depending on your use case: pre-allocate, copy, convert, ...

### Generating test applications

The test directory contains several 'fixtures' allowing to generate unit test
applications using the akida package.

~~~~
akida engine generate --fixture-files test/fixtures/*.py
                      --dest-path <path>
~~~~

## Licensing

Copyright 2022 Brainchip, Inc

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
