from Neuron import Neuron


class Layer:
    def __init__(self, index, neuro_options):
        self.id = index or 0
        self.neuro_options = neuro_options
        self.neurons = []

    def populate(self, nb_neurons, nb_inputs):
        """
        Populate the Layer with a set of randomly weighted Neurons.

        Each Neuron be initialized with nbInputs inputs with a random clamped value.

            @param nb_neurons: Number of neurons.
            @param nb_inputs: Number of inputs.
            @return void
        """
        self.neurons = []
        for i in range(nb_neurons):
            n = Neuron(self.neuro_options)
            n.populate(nb_inputs)
            self.neurons.append(n)
