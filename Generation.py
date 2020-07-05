import random
import copy


class Generation:
    def __init__(self, neuro_options):
        self.genomes = []
        self.neuro_options = neuro_options

    def add_genome(self, genome):
        # Locate position to insert Genome into.
        # The genomes should remain sorted.
        idx = 0
        for i in range(len(self.genomes)):
            # Sort in descending order.
            if self.neuro_options.options['scoreSort'] < 0:
                if genome.score > self.genomes[i].score:
                    idx = i
                    break
                # Sort in ascending order.
            elif genome.score < self.genomes[i].score:
                idx = i
                break

        # Insert genome into correct position.
        self.genomes.insert(idx, genome)

    def breed(self, g1, g2, nb_childs):
        datas = []
        for nb in range(nb_childs):
            # Deep clone of genome 1.
            data = copy.deepcopy(g1)
            for i in range(len(g2.network['weights'])):
                # Genetic crossover
                # 0.5 is the crossover factor.
                # FIXME Really should be a predefined constant.
                if random.random() <= 0.5:
                    data.network['weights'][i] = g2.network['weights'][i]

            # Perform mutation on some weights.
            mutation_range = self.neuro_options.options['mutationRange']
            for i in range(len(data.network['weights'])):
                if random.random() <= self.neuro_options.options['mutationRate']:
                    data.network['weights'][i] += mutation_range * \
                                                  (random.random() * 2 - 1)
            datas.append(data)
        return datas

    def generate_next_generation(self):
        nexts = []
        elitism = self.neuro_options.options['elitism']
        population = self.neuro_options.options['population']
        random_behaviour = self.neuro_options.options['randomBehaviour']
        random_clamped = self.neuro_options.options['randomClamped']
        nb_child = self.neuro_options.options['nbChild']

        for i in range(round(elitism * population)):
            if len(nexts) < population and len(self.genomes) > i:
                # Push a deep copy of its Genome's Network.
                nexts.append(copy.deepcopy(self.genomes[i].network))

        if len(self.genomes) > 0:
            for i in range(round(random_behaviour * population)):
                n = copy.deepcopy(self.genomes[0].network)
                for k in range(len(n['weights'])):
                    n['weights'][k] = random_clamped()

                if len(nexts) < population:
                    nexts.append(n)

        max_val = 0
        while True:
            for i in range(max_val):
                # Create the children and push them to the nexts array.
                children = self.breed(
                    self.genomes[i], self.genomes[max_val], nb_child if nb_child > 0 else 1)
                for c in range(len(children)):
                    nexts.append(children[c].network)
                    if len(nexts) >= population:
                        # Return once number of children is equal to the
                        # population by generation value.
                        return nexts
            max_val += 1
            if max_val >= len(self.genomes) - 1:
                max_val = 0
