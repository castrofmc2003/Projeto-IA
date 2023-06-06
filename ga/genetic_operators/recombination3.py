
import numpy as np

from ga.genetic_algorithm import GeneticAlgorithm
from ga.genetic_operators.recombination import Recombination
from ga.individual import Individual
class Recombination3(Recombination):

    def __init__(self, probability: float):
        super().__init__(probability)

    def recombine(self, ind1: Individual, ind2: Individual) -> None:
        # Cycle Crossover
        size = len(ind1.genome)
        offspring1 = [-1] * size
        offspring2 = [-1] * size

        # Select a random index to start the cycle
        index = GeneticAlgorithm.rand.randint(0, size - 1)
        indexInic = index
        # Add the first element to the offspring
        offspring1[index] = ind1.genome[index]
        offspring2[index] = ind2.genome[index]
        while True:
            # Add the current element to the offspring

            # Find the element in parent2 that is at the same index as the element in parent1
            value = ind2.genome[index]
            for i in range(size):
                if ind1.genome[i] == value:
                    index = i
                    break
            offspring1[index] = ind1.genome[index]
            offspring2[index] = ind2.genome[index]
            # Check if the cycle is complete
            if ind2.genome[index] == ind1.genome[indexInic]:
                break

        # Fill in the remaining elements in the offspring
        for i in range(size):
            if offspring1[i] == -1:
                offspring1[i] = ind2.genome[i]
                offspring2[i] = ind1.genome[i]
        ind2.genome = offspring2
        ind1.genome = offspring1
        return ind1.genome, ind2.genome

    def __str__(self):
        return "Recombination 3 (" + f'{self.probability}' + ")"