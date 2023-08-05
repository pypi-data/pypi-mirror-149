from akida.core import (Layer, FullyConnectedParams, DataProcessingParams,
                        NumNeuronsParams, WeightBitsParams, LearningParams,
                        ActivationsParams)


class FullyConnected(Layer):
    """This represents a Dense or Linear neural layer.

    The FullyConnected layer accepts 1-bit, 2-bit or 4-bit input tensors.
    The FullyConnected can be configured with 1-bit, 2-bit or 4-bit weights.
    It multiplies the inputs by its internal unit weights, returning a 4D
    tensor of values whose first dimension is the number of samples and the
    last dimension represents the number of units.
    It can optionally apply a step-wise ReLU activation to its outputs.

    Args:
        units (int): number of units.
        name (str, optional): name of the layer.
        weights_bits (int, optional): number of bits used to quantize weights.
        activation (bool, optional): enable or disable activation
            function.
        threshold (int, optional): threshold for neurons to fire or
            generate an event.
        act_step (float, optional): length of the potential
            quantization intervals.
        act_bits (int, optional): number of bits used to
            quantize the neuron response.

    """

    def __init__(self,
                 units,
                 name="",
                 weights_bits=1,
                 activation=True,
                 threshold=0,
                 act_step=1,
                 act_bits=1):
        try:
            params = FullyConnectedParams(
                DataProcessingParams(
                    NumNeuronsParams(units), WeightBitsParams(weights_bits),
                    LearningParams(),
                    ActivationsParams(activation, threshold, act_step,
                                      act_bits)))

            # Call parent constructor to initialize C++ bindings
            # Note that we invoke directly __init__ instead of using super, as
            # specified in pybind documentation
            Layer.__init__(self, params, name)
        except BaseException:
            self = None
            raise
