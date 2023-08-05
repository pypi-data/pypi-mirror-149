from akida.core import (Layer, InputDataParams, InputLayerParams, InputParams)


class InputData(Layer):
    """This layer is used to specify the input dimensions of a low bitwidth Model.

    Models accepting 8-bit images must start with an InputConvolutional layer,
    but layers accepting integer inputs with a lower bitwidth (i.e. not images)
    must start instead with an InputData layer.
    This layer does not modify its inputs: it just allows to define the Model
    input dimensions and bitwidth.

    Args:
        input_shape (tuple): the 3D input shape.
        input_bits (int): input bitwidth.
        name (str, optional): name of the layer.

    """

    def __init__(self, input_shape, input_bits=4, name=""):
        try:
            params = InputDataParams(InputLayerParams(InputParams(input_shape)),
                                     input_bits)

            # Call parent constructor to initialize C++ bindings
            # Note that we invoke directly __init__ instead of using super, as
            # specified in pybind documentation
            Layer.__init__(self, params, name)
        except BaseException:
            self = None
            raise
