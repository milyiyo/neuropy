import neuroevolution as ne

neuroevol = ne.Neuroevolution({
    'population': 50,
    'network': [2, [2], 1],
})
generation = neuroevol.nextGeneration()

for gen in  generation:
    out = gen.compute([2,2])
    print(out)