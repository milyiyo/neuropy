from Layer import Layer


class Network:
    def __init__(self, neuro_options):
        self.layers = []
        self.neuro_options = neuro_options

    def perceptron_generation(self, input, hiddens, output):
        index = 0
        previous_neurons = 0
        layer = Layer(index, self.neuro_options)
        # Number of Inputs will be set to 0 since it is an input layer.
        layer.populate(input, previous_neurons)
        # number of input is size of previous layer.
        previous_neurons = input
        self.layers.append(layer)
        index += 1
        for i in range(len(hiddens)):
            # Repeat same process as first layer for each hidden layer.
            layer = Layer(index, self.neuro_options)
            layer.populate(hiddens[i], previous_neurons)
            previous_neurons = hiddens[i]
            self.layers.append(layer)
            index += 1
        layer = Layer(index, self.neuro_options)
        # Number of input is equal to the size of the last hidden layer.
        layer.populate(output, previous_neurons)
        self.layers.append(layer)

    def get_save(self, ):
        datas = {
            'neurons': [],  # Number of Neurons per layer.
            'weights': []  # Weights of each Neuron's inputs.
        }
        for i in range(len(self.layers)):
            datas['neurons'].append(len(self.layers[i].neurons))
            for j in range(len(self.layers[i].neurons)):
                for k in range(len(self.layers[i].neurons[j].weights)):
                    # push all input weights of each Neuron of each Layer into a flat array.
                    datas['weights'].append(
                        self.layers[i].neurons[j].weights[k])
        return datas

    def set_save(self, save):
        previous_neurons = 0
        index = 0
        index_weights = 0
        self.layers = []
        for i in range(len(save['neurons'])):
            # Create and populate layers.
            layer = Layer(index, self.neuro_options)
            layer.populate(save['neurons'][i], previous_neurons)
            for j in range(len(layer.neurons)):
                for k in range(len(layer.neurons[j].weights)):
                    # Apply neurons weights to each Neuron.
                    layer.neurons[j].weights[k] = save['weights'][index_weights]
                    index_weights += 1  # Increment index of flat array.
            previous_neurons = save['neurons'][i]
            index += 1
            self.layers.append(layer)

    def compute(self, inputs):
        # Set the value of each Neuron in the input layer.
        for i in range(len(inputs)):
            if self.layers[0] and self.layers[0].neurons[i]:
                self.layers[0].neurons[i].value = inputs[i]

        prev_layer = self.layers[0]  # Previous layer is input layer.
        for i in range(1, len(self.layers)):
            for j in range(len(self.layers[i].neurons)):
                # For each Neuron in each layer.
                sum_val = 0
                for k in range(len(prev_layer.neurons)):
                    # Every Neuron in the previous layer is an input to each Neuron in the next layer.
                    sum_val += prev_layer.neurons[k].value * \
                           self.layers[i].neurons[j].weights[k]
                # Compute the activation of the Neuron.
                self.layers[i].neurons[j].value = self.neuro_options.options['activation'](
                    sum_val)
            prev_layer = self.layers[i]

        # All outputs of the Network.
        out = []
        last_layer = self.layers[len(self.layers) - 1]
        for i in range(len(last_layer.neurons)):
            out.append(last_layer.neurons[i].value)
        return out
