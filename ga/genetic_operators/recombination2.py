from ga.genetic_algorithm import GeneticAlgorithm
from ga.individual import Individual
from ga.genetic_operators.recombination import Recombination

class Recombination2(Recombination):

    def __init__(self, probability: float):
        super().__init__(probability)

    def recombine(self, ind1: Individual, ind2: Individual) -> None:
        #Order 1 Crossover
        num_genes = ind1.num_genes
        cut1 = GeneticAlgorithm.rand.randint(0, num_genes - 1)
        cut2 = GeneticAlgorithm.rand.randint(0, num_genes - 1)
        if cut1 > cut2:
            cut1, cut2 = cut2, cut1
        child1 = [None] * num_genes
        child2 = [None] * num_genes
        for i in range(cut1, cut2):
            child1[i], child2[i] = ind1.genome[i], ind2.genome[i]
        chid1Pos = cut2
        child2Pos = cut2
        for i in range(cut2, num_genes):
            if ind2.genome[i] not in child1:
                child1[chid1Pos] = ind2.genome[i]
                if chid1Pos == num_genes - 1:
                    chid1Pos = 0
                else:
                    chid1Pos += 1
        for i in range (0,cut2):
            if ind2.genome[i] not in child1:
                child1[chid1Pos] = ind2.genome[i]
                if chid1Pos == num_genes - 1:
                    chid1Pos = 0
                else:
                    chid1Pos += 1
        for i in range(cut2, num_genes):
            if ind1.genome[i] not in child2:
                child2[child2Pos] = ind1.genome[i]
                if child2Pos == num_genes - 1:
                    child2Pos = 0
                else:
                    child2Pos += 1
        for i in range (0,cut2):
            if ind1.genome[i] not in child2:
                child2[child2Pos] = ind1.genome[i]
                if child2Pos == num_genes - 1:
                    child2Pos = 0
                else:
                    child2Pos += 1

        ind1.genome = child1
        ind2.genome = child2


    def __str__(self):
        return "Recombination 2 (" + f'{self.probability}' + ")"
