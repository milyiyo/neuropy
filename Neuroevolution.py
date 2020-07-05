from Generations import Generations
from Genome import Genome
from Network import Network
from NeuroOptions import NeuroOptions


class Neuroevolution:
    def __init__(self, options):
        self.neuro_options = NeuroOptions(options)
        self.generations = Generations(self.neuro_options)

    def restart(self):
        self.generations = Generations(self.neuro_options)

    def next_generation(self):
        networks = []

        if len(self.generations.gens) == 0:
            # If no Generations, create first.
            networks = self.generations.first_generation()
        else:
            # Otherwise, create next one.
            networks = self.generations.next_generation()

        # Create Networks from the current Generation.
        nns = []
        for i in range(len(networks)):
            nn = Network(self.neuro_options)
            nn.set_save(networks[i])
            nns.append(nn)

        if self.neuro_options.options['lowHistoric'] and len(self.generations.gens) >= 2:
            # Remove old Networks.
            genomes = self.generations.gens[len(
                self.generations.gens) - 2].genomes
            for i in range(len(genomes)):
                genomes[i].network = None

        historic = self.neuro_options.options['historic']
        if historic != -1 and len(self.generations.gens) > historic + 1:
            # Remove older generations.
            count = len(self.generations.gens) - (historic + 1)
            while count > 0:
                self.generations.gens.pop(0)
                count -= 1

        return nns

    def network_score(self, network, score):
        self.generations.add_genome(Genome(score, network.get_save()))
