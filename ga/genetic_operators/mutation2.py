import numpy as np

from ga.individual_int_vector import IntVectorIndividual
from ga.genetic_operators.mutation import Mutation

class Mutation2(Mutation):
    def __init__(self, probability):
        super().__init__(probability)

    def mutate(self, ind: IntVectorIndividual) -> None:
        # Scramble mutation
        num_genes = len(ind.genome)
        cut1 = np.random.randint(0, num_genes - 1)
        cut2 = cut1
        while (cut1 == cut2):
            cut2 = np.random.randint(0, num_genes - 1)

        if cut1 > cut2:
            cut1, cut2 = cut2, cut1
        aux = []
        index = 0

        for i in range(cut1, cut2):
            aux.append(ind.genome[i])
        np.random.shuffle(aux)

        for i in range(cut1, cut2):
            ind.genome[i] = aux[index]
            index +=1

    def __str__(self):
        return "Mutation 2 (" + f'{self.probability}' + ")"
