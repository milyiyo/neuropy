from Generation import Generation
from Network import Network


class Generations:
    def __init__(self, neuro_options):
        self.gens = []
        self.neuro_options = neuro_options
        self.current_generation = Generation(self.neuro_options)

    def first_generation(self):
        out = []
        network = self.neuro_options.options['network']
        for i in range(self.neuro_options.options['population']):
            # Generate the Network and save it.
            nn = Network(self.neuro_options)
            nn.perceptron_generation(network[0], network[1], network[2])
            out.append(nn.get_save())

        self.gens.append(Generation(self.neuro_options))
        return out

    def next_generation(self):
        if len(self.gens) == 0:
            # Need to create first generation.
            return False

        last_generation = self.gens[len(self.gens) - 1]
        gen = last_generation.generate_next_generation()
        self.gens.append(Generation(self.neuro_options))
        return gen

    def add_genome(self, genome):
        # Can't add to a Generation if there are no Generations.
        if len(self.gens) == 0:
            return False
        self.gens[len(self.gens) - 1].add_genome(genome)
