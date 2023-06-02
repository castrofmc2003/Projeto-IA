import copy

from ga.individual_int_vector import IntVectorIndividual
from warehouse.cell import Cell


class WarehouseIndividual(IntVectorIndividual):

    def __init__(self, problem: "WarehouseProblemGA", num_genes: int):
        super().__init__(problem, num_genes)
        self.forklifts = problem.forklifts
        self.products = problem.products
        self.path = []
        self.fitness = 0
        self.forklift_path = []


    @property
    def compute_fitness(self, j=None) -> float:
        forklifts = self.problem.forklifts
        products = self.problem.products
        agent_search = self.problem.agent_search

        fitness = 0
        genome_length = len(self.genome)
        path = []
        num_products = len(products)
        j = 0
        for i in range(len(forklifts)):
            forklift_path = [forklifts[i]]
            while j < genome_length:
                if self.genome[j] <= num_products:
                    forklift_path.append(products[self.genome[j] - 1])
                    j += 1
                else:
                    j += 1
                    break
            forklift_path.append(agent_search.exit)
            path.append(forklift_path)

        for i in range(len(path)):
            for j in range(len(path[i]) - 1):
                fitness += agent_search.get_value(path[i][j], path[i][j + 1])

        self.path = path
        self.fitness = fitness
        return self.fitness



    '''
    colisoes no obtain allpath
    #return forklifts_path, max_steps
    #forklifts_path[i][j]
    #path -> lista de todas as cells por onde o forklift passou
    #guardar cells por onde o forklift passou no pair 
    #solution -> devolver todas as cells entre cada par
    ==================================
    #guardar a posicao inicial do forklift 
    #ao correr as cells, verificar se o produto inicial é superior ao outro, e percorrer as cells do fim pro inicio
    #path para cada forklift ... ?
    '''


    @property
    def obtain_all_path(self):
        forklift_pairs = []
        path =[]
        max_steps = 0
        forklift_path = []
        genome_length = len(self.genome)
        num_products = len(self.problem.products)
        j = 0
        # for i in range(len(self.problem.forklifts)):
        #     #inicializacao do path com a posicao inicial do forklift
        #     forklift_path = [self.problem.forklifts[i]]
        #     while j < genome_length:
        #         if self.genome[j] <= num_products:
        #             # append dos produtos para cada forklift
        #             forklift_path.append(self.problem.products[self.genome[j] - 1])
        #             j += 1
        #         else:
        #             j += 1
        #             break
        #     #append da saida para cada forklift
        #     forklift_path.append(self.problem.agent_search.exit)
        #     #append da lista de cada forklift
        #     path.append(forklift_path)
        self.forklift_path = []
        for i in range(len(self.path)):
            forklift_path=[self.path[i][0]]
            for j in range(len(self.path[i]) - 1):
                #obter todas as cells entre cada par
                for cell in self.problem.agent_search.get_cells(self.path[i][j], self.path[i][j + 1]):
                    if not(cell.__eq__(forklift_path[len(forklift_path)-1])):
                        forklift_path.append(cell)

            self.forklift_path.append(forklift_path)
            max_steps = len(forklift_path) if len(forklift_path) > max_steps else max_steps
        return self.forklift_path, max_steps


    def __str__(self):
        string = 'Fitness: ' + f'{self.fitness}' + '\n'
        string += str (self.genome) + "\n\n"

        for i in range(len(self.forklifts)):
            string +=  "Nºprodutos apanhados pelo " + str(i + 1) + "ºForklift: "+str(len(self.path[i])-2) + "\n ["
            for j in range(1,len(self.path[i])-1):
                string +="("+  str(self.path[i][j]) + ")"
            string += "]" + "\n"
        return string

    def better_than(self, other: "WarehouseIndividual") -> bool:
        return True if self.fitness < other.fitness else False

    # __deepcopy__ is implemented here so that all individuals share the same problem instance
    def __deepcopy__(self, memo):
        new_instance = self.__class__(self.problem, self.num_genes)
        new_instance.genome = self.genome.copy()
        new_instance.fitness = self.fitness
        new_instance.path = self.path.copy()
        new_instance.forklift_path = self.forklift_path.copy()
        # TODO

        return new_instance