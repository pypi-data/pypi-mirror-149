import numpy as np


def _get_cyclic_input(shape, max_value, duplicate_values):
    input_size = np.prod(shape)
    inputs = np.zeros((input_size), dtype=np.uint8)
    for i in range(input_size):
        inputs[i] = (i // duplicate_values) % (max_value + 1)
    return inputs.reshape(shape)


def get_cyclic_input(model, n=1, duplicate_values=1):
    """
    Generate an input with cyclic values.

    Args:
        model (:obj:`akida.Model`): the model for which we want an input
        n (int, optional): number of frames or samples. Default to 1.
        duplicate_values (int, optional): duplication of each value. For
            example, a "1,2,3" pattern of values with a duplicate_values of 2
            will be "1,1,2,2,3,3". Default to 1, the values are not duplicated.
    Returns:
        :obj:`np.ndarray`: the cyclic inputs
    """
    assert duplicate_values >= 1, "duplicate_values must be strictly positive"
    input_shape = (n,) + tuple(model.input_shape)
    bitwidth = model.get_layer(0).input_bits
    return _get_cyclic_input(input_shape, max_value=2**(bitwidth) - 1,
                             duplicate_values=duplicate_values)


def set_cyclic_weights(model):
    for j in range(model.get_layer_count()):
        layer = model.get_layer(j)
        for var_name in "weights", "weights_pw":
            if var_name in layer.variables.names:
                weights = layer.get_variable(var_name)
                bitwidth = layer.parameters.weights_bits
                # Generate a vector of cycling weights
                new_weights = np.zeros(weights.size, dtype=np.int8)
                if bitwidth == 1:
                    for i in range(weights.size):
                        new_weights[i] = i % 2
                else:
                    max_value = 2**(bitwidth - 1) - 1
                    n_values = 2 * max_value + 1
                    for i in range(weights.size):
                        # We set weights in sequence, each new sequence
                        # starting at an increasing value in the sequence
                        new_weights[i] = (i + i % n_values) % n_values - max_value
                # Weights are WHCF, but we want to cycle in each filter, so we
                # reshape the vector to FCHW to have weights grouped by filters
                new_weights = new_weights.reshape(np.flip(weights.shape))
                # ... then transpose to obtain the WHCF weights
                new_weights = np.transpose(new_weights)
                layer.set_variable(var_name, new_weights)


def set_constant_weights(model, value):
    for i in range(model.get_layer_count()):
        layer = model.get_layer(i)
        for var_name in "weights", "weights_pw":
            if var_name in layer.variables.names:
                weights = layer.get_variable(var_name)
                weights[:, :, :, :] = value
                layer.set_variable(var_name, weights)


def set_cyclic_threshold(model):
    for i in range(model.get_layer_count()):
        layer = model.get_layer(i)
        # There will be a threshold everywhere but in the input data
        if 'threshold' in layer.variables.names:
            num_neurons = layer.variables["threshold"].size
            # Set deterministic thresholds and steps
            # Values must fit in 19 bits (i.e. 20 -1 for the sign), so they are
            # clipped and multiplied by the sign to keep positive and negative
            # numbers
            MAX_THRESH = (1 << 19) - 1
            # Thresholds are set in the range on -num_neurons and num_neurons.
            threshold = np.arange(num_neurons, dtype=np.int32) % MAX_THRESH
            threshold -= (num_neurons // 2)
            layer.variables["threshold"] = threshold
            # Steps in hardware are represented as fixed point with 4 bit for
            # decimals. So the minimum step is 1 / 16 = 0.0625
            MIN_STEP = 1 / 16
            # Steps are stored in 20 bit, 4 bit for the decimals, so max value
            # is:
            MAX_ACT_STEP = (1 << (20 - 4)) - 1
            # Steps are required to be strictly positive, so minimum value will
            #  be MIN_STEP and maximum will be MAX_ACT_STEP
            layer.variables["act_step"] = np.arange(
                num_neurons * MIN_STEP, step=MIN_STEP,
                dtype=np.float32) % MAX_ACT_STEP + MIN_STEP
