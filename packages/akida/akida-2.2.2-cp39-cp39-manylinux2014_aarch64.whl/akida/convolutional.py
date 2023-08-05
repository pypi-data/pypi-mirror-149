from akida.core import (Layer, ConvolutionalParams, Padding, PoolType,
                        ConvolutionKernelParams, NumNeuronsParams, StrideParams,
                        WeightBitsParams, PoolingParams, ActivationsParams,
                        DataProcessingParams, LearningParams)


class Convolutional(Layer):
    """This represents a standard Convolutional layer.

    The Convolutional layer accepts 1-bit, 2-bit or 4-bit 3D input tensors with
    an arbitrary number of channels.
    The Convolutional layer can be configured with 1-bit, 2-bit or 4-bit weights.
    It applies a convolution (not a cross-correlation) optionally followed by a
    pooling operation to the input tensors.
    It can optionally apply a step-wise ReLU activation to its outputs.
    The layer expects a 4D tensor whose first dimension is the sample index
    as input.
    It returns a 4D tensor whose first dimension is the sample index and the
    last dimension is the number of convolution filters.
    The order of the input spatial dimensions is preserved, but their value may
    change according to the convolution and pooling parameters.

    Args:
        kernel_size (list): list of 2 integer representing the spatial
            dimensions of the convolutional kernel.
        filters (int): number of filters.
        name (str, optional): name of the layer.
        padding (:obj:`Padding`, optional): type of convolution.
        kernel_stride (list, optional): list of 2 integer representing the
            convolution stride (X, Y).
        weights_bits (int, optional): number of bits used to quantize weights.
        pool_size (list, optional): list of 2 integers, representing the window
            size over which to take the maximum or the average (depending on
            pool_type parameter).
        pool_type (:obj:`PoolType`, optional): pooling type
            (None, Max or Average).
        pool_stride (list, optional): list of 2 integers representing
            the stride dimensions.
        activation (bool, optional): enable or disable activation
            function.
        threshold (int, optional): threshold for neurons to fire or
            generate an event.
        act_step (float, optional): length of the potential
            quantization intervals.
        act_bits (int, optional): number of bits used to quantize
            the neuron response.

    """

    def __init__(self,
                 kernel_size,
                 filters,
                 name="",
                 padding=Padding.Same,
                 kernel_stride=(1, 1),
                 weights_bits=1,
                 pool_size=(-1, -1),
                 pool_type=PoolType.NoPooling,
                 pool_stride=(-1, -1),
                 activation=True,
                 threshold=0,
                 act_step=1,
                 act_bits=1):
        try:
            params = ConvolutionalParams(
                DataProcessingParams(
                    NumNeuronsParams(filters), WeightBitsParams(weights_bits),
                    LearningParams(),
                    ActivationsParams(activation, threshold, act_step,
                                      act_bits)),
                ConvolutionKernelParams(kernel_size, padding),
                PoolingParams(pool_size, pool_type, pool_stride),
                StrideParams(kernel_stride))

            # Call parent constructor to initialize C++ bindings
            # Note that we invoke directly __init__ instead of using super, as
            # specified in pybind documentation
            Layer.__init__(self, params, name)
        except BaseException:
            self = None
            raise
