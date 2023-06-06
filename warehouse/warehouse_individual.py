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
        self.max_steps = 0

    # posicao x do path[i][x] == path[j][x] - colisao (forklifts diferentes na mm posicao no mm passo)
    # posicao x do path[i][x] == path[j][x+1] e path-path[i][x +1] == path[j][x] colisao (forklifts passam um pelo outro)
    # penalty quando 1 forklift apanha muito menos produtos que os outros
    # total max_steps muito alto
    #


    @property
    def compute_fitness(self, j=None) -> float:
        forklifts = self.problem.forklifts
        products = self.problem.products
        agent_search = self.problem.agent_search
        penalty = 0
        self.fitness = 0
        genome_length = len(self.genome)
        self.path = []
        self.max_steps = 0
        num_forklifts = len(forklifts)
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
            self.path.append(forklift_path)

        # se algum forklift apanhar muito menos produtos que os outros
        for i in range(num_forklifts - 1):
            for j in range(i + 1, num_forklifts):
                # len(path) - 2 = numero de produtos apanhados por forklift (exclui a posicao inicial e final)
                if len(self.path[i]) < (len(self.path[j]))/num_forklifts:
                    penalty += int(len(self.path[j])/num_forklifts)
                elif len(self.path[j]) < (len(self.path[i]))/num_forklifts:
                    penalty += int(len(self.path[i])/num_forklifts)


        # guarda todas as cells por onde o forklift passou
        self.forklift_path = []
        for i in range(num_forklifts):
            forklift_path = [self.path[i][0]]
            for j in range(len(self.path[i]) - 1):
                # obter todas as cells entre cada par
                for cell in self.problem.agent_search.get_cells(self.path[i][j], self.path[i][j + 1]):
                    if not (cell.__eq__(forklift_path[len(forklift_path) - 1])):
                        forklift_path.append(cell)

            self.forklift_path.append(forklift_path)
            self.max_steps = len(forklift_path) if len(forklift_path) > self.max_steps else self.max_steps

        # colisoes
        #num_forklifts = len(path) pq cada forklift tem uma lista de cells
        for i in range (num_forklifts - 1):
            for j in range (len(self.forklift_path[i])-1):
                for k in range(i+1, num_forklifts):
                    if j >= len(self.forklift_path[k])-1:
                        break
                    if self.forklift_path[i][j].__eq__(self.forklift_path[k][j]):
                        penalty += 5
                    # if len(self.forklift_path[k]) < len(self.forklift_path[k])-1:
                    #     break
                    elif self.forklift_path[i][j].__eq__(self.forklift_path[k][j+1]) and self.forklift_path[i][j + 1].__eq__(self.forklift_path[k][j]):
                        penalty += 5

        #soma do total das distancias
        for i in range(num_forklifts):
            for j in range(len(self.path[i]) - 1):
                self.fitness += agent_search.get_value(self.path[i][j], self.path[i][j + 1])
        if self.max_steps > self.fitness/(num_forklifts):
            penalty += self.max_steps - int(self.fitness/num_forklifts)
        # self.path = path
        # self.fitness = fitness
        self.fitness += penalty
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
        return self.forklift_path, self.max_steps


    def __str__(self):
        string = 'Fitness: ' + f'{self.fitness}' + '\n'
        string += str (self.genome) + "\n\n"

        for i in range(len(self.forklifts)):
            string +=  "Nºprodutos apanhados pelo " + str(i + 1) + "ºForklift: "+str(len(self.path[i])-2) + " Max Passos: " + str(len(self.forklift_path[i]) -1 )+ "\n ["
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
        new_instance.max_steps = self.max_steps
        # TODO

        return new_instance