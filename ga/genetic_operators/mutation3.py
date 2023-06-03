import numpy as np

from ga.individual_int_vector import IntVectorIndividual
from ga.genetic_operators.mutation import Mutation

class Mutation3(Mutation):
    def __init__(self, probability):
        super().__init__(probability)

    def mutate(self, ind: IntVectorIndividual) -> None:
        num_genes = len(ind.genome)
        cut1 = np.random.randint(0, num_genes - 1)
        cut2 = np.random.randint(cut1 + 1, num_genes)

        aux = ind.genome[cut1 + 1]
        ind.genome[cut1 + 1] = ind.genome[cut2]
        for i in range(cut1 + 2, cut2 + 1):
            ind.genome[i], aux = aux, ind.genome[i]

    def __str__(self):
        return "Mutation 3 (" + f'{self.probability}' + ")"
