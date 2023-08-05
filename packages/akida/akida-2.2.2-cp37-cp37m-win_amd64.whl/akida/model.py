import numpy as np

from .core import Layer, LayerType
from .statistics import Statistics


# Private utility functions
def _copy_layer_variables(layer, copied_layer):
    for var in copied_layer.get_variable_names():
        layer.set_variable(var, copied_layer.get_variable(var))


def _copy_layer(model, layer):
    new_layer = Layer(layer.parameters, layer.name)
    inbounds = []
    # For each original inbound layer
    for inbound in layer.inbounds:
        names = [layer.name for layer in model.layers]
        if inbound.name in names:
            new_inbound = model.get_layer(inbound.name)
        else:
            # Use the last layer of the target model
            new_inbound = model.layers[-1]
        inbounds.append(new_inbound)
    model.add(new_layer, inbounds)
    if layer.learning:
        # Recompile model with layer parameters
        learn_params = {
            attr: getattr(layer.learning, attr)
            for attr in dir(layer.learning)
            if '__' not in attr and 'learning_type' not in attr
        }
        model.compile(**learn_params)
    _copy_layer_variables(new_layer, layer)


def model_str(self):
    data = "akida.Model, layer_count=" + str(self.get_layer_count())
    data += ", sequence_count=" + str(len(self.sequences))
    out_dims = self.output_shape if self.get_layer_count() else []
    data += ", output_shape=" + str(out_dims)
    return data


def model_repr(self):
    out_dims = self.output_shape if self.get_layer_count() else []
    data = "<akida.Model, layer_count=" + str(self.get_layer_count())
    data += ", output_shape=" + str(out_dims)
    data += ", sequences=" + repr(self.sequences) + ">"
    return data


@property
def statistics(self):
    """Get statistics by sequence for this model.

    Returns:
        a dictionary of :obj:`SequenceStatistics` indexed by name.

    """
    return Statistics(model=self)


def summary(self):
    """Prints a string summary of the model.

    This method prints a summary of the model with details for every layer,
    grouped by sequences:

    - name and type in the first column
    - output shape
    - kernel shape

    If there is any layer with unsupervised learning enabled, it will list
    them, with these details:

    - name of layer
    - number of incoming connections
    - number of weights per neuron

    """

    def _model_summary(model):
        # prepare headers
        headers = ['Input shape', 'Output shape', 'Sequences', 'Layers']
        # prepare an empty table
        table = [headers]
        row = [
            str(model.input_shape),
            str(model.output_shape),
            str(len(model.sequences)),
            str(len(model.layers))
        ]
        table.append(row)
        print_table(table, "Model Summary")

    def _layers_summary(sequence):
        # Prepare headers
        headers = ['Layer (type)', 'Output shape', 'Kernel shape']
        program = sequence.program
        if program is not None:
            headers.append('NPs')
        # prepare an empty table
        table = [headers]
        for p in sequence.passes:
            for layer in p.layers:
                nps = None if layer.mapping is None else layer.mapping.nps
                # layer name (type)
                layer_type = layer.parameters.layer_type
                # kernel shape
                if "weights" in layer.get_variable_names():
                    kernel_shape = layer.get_variable("weights").shape
                else:
                    kernel_shape = "N/A"
                # Prepare row and add it
                row = [str(layer), str(layer.output_dims), str(kernel_shape)]
                if nps is not None:
                    if layer_type == LayerType.InputConvolutional:
                        row.append('N/A')
                    else:
                        row.append(len(nps))
                table.append(row)
                if layer_type == LayerType.SeparableConvolutional:
                    # Add pointwise weights on a second line
                    kernel_pw_shape = layer.get_variable("weights_pw").shape
                    row = ['', '', kernel_pw_shape]
                    if nps is not None:
                        row.append('')
                    table.append(row)
        # Get backend info
        backend = str(sequence.backend).split('.')[-1]
        title = sequence.name + " (" + backend + ")"
        if program is not None:
            title += " - size: " + str(len(program)) + " bytes"
        print_table(table, title)

    def _learning_summary(layer):
        if not layer.learning:
            return
        # Prepare headers
        headers = ["Learning Layer", "# Input Conn.", "# Weights"]
        table = [headers]
        name = layer.name
        # Input connections is the product of input dims
        input_connections = np.prod(layer.input_dims)
        # Num non zero weights per neuron (counted on first neuron)
        weights = layer.get_variable("weights")
        incoming_conn = np.count_nonzero(weights[:, :, :, 0])
        # Prepare row and add it
        row = [name, str(input_connections), incoming_conn]
        table.append(row)
        print()
        print_table(table, "Learning Summary")

    # Print first the general Model summary
    _model_summary(self)
    for sequence in iter(self.sequences):
        print()
        # Print sequence summary
        _layers_summary(sequence)
    # Print learning summary if we have more than one input layer
    if len(self.layers) > 1:
        # Only the last layer of a model can learn
        _learning_summary(self.layers[-1])
    print()


def print_table(table, title):
    # Convert to np.array
    to_str = np.vectorize(str, otypes=['O'])
    table = to_str(table)
    # get column lengths
    str_len_f = np.vectorize(lambda cell: len(str(cell)))
    str_lens = np.amax(str_len_f(table), 0)
    line_len = np.sum(str_lens)
    # Prepare format rows
    size_formats = np.vectorize(lambda cell: f"{{:{cell}.{cell}}}")
    format_strings = size_formats(str_lens)
    format_row = "  ".join(format_strings)
    # Generate separators
    separator_len = line_len + 2 * len(table[0])
    separator = "_" * separator_len
    double_separator = "=" * separator_len

    # Print header
    center_format = f"{{:^{separator_len}}}"
    print(center_format.format(title))
    print(separator)
    print(format_row.format(*table[0]))
    print(double_separator)
    # Print body
    for row in table[1:, :]:
        print(format_row.format(*row))
        print(separator)


def predict_classes(self, inputs, num_classes=0, batch_size=0):
    """Predicts the class labels for the specified inputs.

    Args:
        inputs (:obj:`numpy.ndarray`): a (n, x, y, c) uint8 tensor
        num_classes (int, optional): the number of output classes
        batch_size (int, optional): maximum number of inputs that should be
            processed at a time

    Returns:
        :obj:`numpy.ndarray`: an array of class labels

    """

    outputs = self.predict(inputs, batch_size)
    classes = np.argmax(outputs, axis=-1).flatten()
    num_neurons = outputs.shape[-1]
    if num_classes != 0 and num_classes != num_neurons:
        neurons_per_class = num_neurons // num_classes
        classes = classes // neurons_per_class
    return classes
