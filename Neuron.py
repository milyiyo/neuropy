
class Neuron:
    def __init__(self, neuro_options):
        self.value = 0
        self.neuro_options = neuro_options
        self.weights = []

    # Initialize number of neuron weights to random clamped values.
    def populate(self, nb):
        self.weights = []
        for i in range(nb):
            self.weights.append(self.neuro_options.options['randomClamped']())
