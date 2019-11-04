import math
import random
import copy


class NeuroOptions:
    def __init__(self, options):
        self.options = {
            # Logistic activation function
            'activation': lambda x:  1/(1+math.exp(-x)),
            # Returns a random value between -1 and 1.
            'randomClamped': lambda: random.random() * 2 - 1,
            # Perceptron network structure (1 hidden
            'network': [1, [1], 1],
            # Population by generation.
            'population': 50,
            # Best networks kepts unchanged for the next generation (rate).
            'elitism': 0.2,
            # New random networks for the next generation (rate).
            'randomBehaviour': 0.2,
            # Mutation rate on the weights of synapses.
            'mutationRate': 0.1,
            # Interval of the mutation changes on the synapse weight.
            'mutationRange': 0.5,
            # Latest generations saved.
            'historic': 0,
            # Only save score (not the network).
            'lowHistoric': False,
            # Sort order (-1 = desc, 1 = asc).
            'scoreSort': -1,
            # Number of children by breeding.
            'nbChild': 1
        }
        self.set(options)

    def set(self, options):
        for items in options.items():
            self.options[items[0]] = items[1]


class Neuron:
    def __init__(self, neuroOptions):
        self.value = 0
        self.neuroOptions = neuroOptions
        self.weights = []

    # Initialize number of neuron weights to random clamped values.
    def populate(self, nb):
        self.weights = []
        for i in range(nb):
            self.weights.append(self.neuroOptions.options['randomClamped']())


class Layer:
    def __init__(self, index, neuroOptions):
        self.id = index or 0
        self.neuroOptions = neuroOptions
        self.neurons = []

    def populate(self, nbNeurons, nbInputs):
        """
        Populate the Layer with a set of randomly weighted Neurons.

        Each Neuron be initialied with nbInputs inputs with a random clamped value.

            @param nbNeurons: Number of neurons.
            @param nbInputs: Number of inputs.
            @return void
        """
        self.neurons = []
        for i in range(nbNeurons):
            n = Neuron(self.neuroOptions)
            n.populate(nbInputs)
            self.neurons.append(n)


class Network:
    def __init__(self, neuroOptions):
        self.layers = []
        self.neuroOptions = neuroOptions

    def perceptronGeneration(self, input, hiddens, output):
        index = 0
        previousNeurons = 0
        layer = Layer(index, self.neuroOptions)
        # Number of Inputs will be set to 0 since it is an input layer.
        layer.populate(input, previousNeurons)
        # number of input is size of previous layer.
        previousNeurons = input
        self.layers.append(layer)
        index += 1
        for i in range(len(hiddens)):
            # Repeat same process as first layer for each hidden layer.
            layer = Layer(index, self.neuroOptions)
            layer.populate(hiddens[i], previousNeurons)
            previousNeurons = hiddens[i]
            self.layers.append(layer)
            index += 1
        layer = Layer(index, self.neuroOptions)
        # Number of input is equal to the size of the last hidden layer.
        layer.populate(output, previousNeurons)
        self.layers.append(layer)

    def getSave(self,):
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

    def setSave(self, save):
        previousNeurons = 0
        index = 0
        indexWeights = 0
        self.layers = []
        for i in range(len(save['neurons'])):
            # Create and populate layers.
            layer = Layer(index, self.neuroOptions)
            layer.populate(save['neurons'][i], previousNeurons)
            for j in range(len(layer.neurons)):
                for k in range(len(layer.neurons[j].weights)):
                    # Apply neurons weights to each Neuron.
                    layer.neurons[j].weights[k] = save['weights'][indexWeights]
                    indexWeights += 1  # Increment index of flat array.
            previousNeurons = save['neurons'][i]
            index += 1
            self.layers.append(layer)

    def compute(self, inputs):
        # Set the value of each Neuron in the input layer.
        for i in range(len(inputs)):
            if self.layers[0] and self.layers[0].neurons[i]:
                self.layers[0].neurons[i].value = inputs[i]

        prevLayer = self.layers[0]  # Previous layer is input layer.
        for i in range(1, len(self.layers)):
            for j in range(len(self.layers[i].neurons)):
                # For each Neuron in each layer.
                sum = 0
                for k in range(len(prevLayer.neurons)):
                    # Every Neuron in the previous layer is an input to each Neuron in the next layer.
                    sum += prevLayer.neurons[k].value * \
                        self.layers[i].neurons[j].weights[k]
                # Compute the activation of the Neuron.
                self.layers[i].neurons[j].value = self.neuroOptions.options['activation'](
                    sum)
            prevLayer = self.layers[i]

        # All outputs of the Network.
        out = []
        lastLayer = self.layers[len(self.layers) - 1]
        for i in range(len(lastLayer.neurons)):
            out.append(lastLayer.neurons[i].value)
        return out


class Genome:
    def __init__(self, score, network):
        self.score = score or 0
        self.network = network or None


class Generation:
    def __init__(self, neuroOptions):
        self.genomes = []
        self.neuroOptions = neuroOptions

    def addGenome(self, genome):
        # Locate position to insert Genome into.
        # The genomes should remain sorted.
        idx = 0
        for i in range(len(self.genomes)):
            # Sort in descending order.
            if self.neuroOptions.options['scoreSort'] < 0:
                if genome.score > self.genomes[i].score:
                    idx = i
                    break
                # Sort in ascending order.
            elif genome.score < self.genomes[i].score:
                idx = i
                break

        # Insert genome into correct position.
        self.genomes.insert(idx, genome)

    def breed(self, g1, g2, nbChilds):
        datas = []
        for nb in range(nbChilds):
            # Deep clone of genome 1.
            data = copy.deepcopy(g1)
            for i in range(len(g2.network['weights'])):
                # Genetic crossover
                # 0.5 is the crossover factor.
                # FIXME Really should be a predefined constant.
                if random.random() <= 0.5:
                    data.network['weights'][i] = g2.network['weights'][i]

            # Perform mutation on some weights.
            mutationRange = self.neuroOptions.options['mutationRange']
            for i in range(len(data.network['weights'])):
                if random.random() <= self.neuroOptions.options['mutationRate']:
                    data.network['weights'][i] += mutationRange * \
                        (random.random() * 2 - 1)
            datas.append(data)
        return datas

    def generateNextGeneration(self):
        nexts = []
        elitism = self.neuroOptions.options['elitism']
        population = self.neuroOptions.options['population']
        randomBehaviour = self.neuroOptions.options['randomBehaviour']
        randomClamped = self.neuroOptions.options['randomClamped']
        nbChild = self.neuroOptions.options['nbChild']

        for i in range(round(elitism * population)):
            if len(nexts) < population and len(self.genomes) > i:
                # Push a deep copy of its Genome's Network.
                nexts.append(copy.deepcopy(self.genomes[i].network))

        if len(self.genomes) > 0:
            for i in range(round(randomBehaviour * population)):
                n = copy.deepcopy(self.genomes[0].network)
                for k in range(len(n['weights'])):
                    n['weights'][k] = randomClamped()

                if len(nexts) < population:
                    nexts.append(n)

        max = 0
        while True:
            for i in range(max):
                # Create the children and push them to the nexts array.
                childs = self.breed(
                    self.genomes[i], self.genomes[max], nbChild if nbChild > 0 else 1)
                for c in range(len(childs)):
                    nexts.append(childs[c].network)
                    if len(nexts) >= population:
                        # Return once number of children is equal to the
                        # population by generation value.
                        return nexts
            max += 1
            if max >= len(self.genomes) - 1:
                max = 0


class Generations:
    def __init__(self, neuroOptions):
        self.generations = []
        self.neuroOptions = neuroOptions
        self.currentGeneration = Generation(self.neuroOptions)

    def firstGeneration(self):
        out = []
        network = self.neuroOptions.options['network']
        for i in range(self.neuroOptions.options['population']):
            # Generate the Network and save it.
            nn = Network(self.neuroOptions)
            nn.perceptronGeneration(network[0], network[1], network[2])
            out.append(nn.getSave())

        self.generations.append(Generation(self.neuroOptions))
        return out

    def nextGeneration(self):
        if len(self.generations) == 0:
            # Need to create first generation.
            return False

        lastGeneration = self.generations[len(self.generations) - 1]
        gen = lastGeneration.generateNextGeneration()
        self.generations.append(Generation(self.neuroOptions))
        return gen

    def addGenome(self, genome):
        # Can't add to a Generation if there are no Generations.
        if len(self.generations) == 0:
            return False
        self.generations[len(self.generations) - 1].addGenome(genome)


class Neuroevolution:
    def __init__(self, options):
        self.neuroOptions = NeuroOptions(options)
        self.generations = Generations(self.neuroOptions)

    def restart(self):
        self.generations = Generations(self.neuroOptions)

    def nextGeneration(self):
        networks = []

        if len(self.generations.generations) == 0:
            print('If no Generations, create first.')
            networks = self.generations.firstGeneration()
        else:
            print('Otherwise, create next one.')
            networks = self.generations.nextGeneration()

        # Create Networks from the current Generation.
        nns = []
        for i in range(len(networks)):
            nn = Network(self.neuroOptions)
            nn.setSave(networks[i])
            nns.append(nn)

        if self.neuroOptions.options['lowHistoric']:
            # Remove old Networks.
            if len(self.generations.generations) >= 2:
                genomes = self.generations.generations[len(
                    self.generations.generations) - 2].genomes
                for i in range(len(genomes)):
                    genomes[i].network = None

        historic = self.neuroOptions.options['historic']
        if historic != -1:
            # Remove older generations.
            if len(self.generations.generations) > historic + 1:
                count = len(self.generations.generations) - (historic + 1)
                while count > 0:
                    self.generations.generations.pop(0)
                    count -= 1

        return nns

    def networkScore(self, network, score):
        self.generations.addGenome(Genome(score, network.getSave()))
