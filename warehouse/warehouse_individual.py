import copy

from ga.individual_int_vector import IntVectorIndividual


class WarehouseIndividual(IntVectorIndividual):

    def __init__(self, problem: "WarehouseProblemGA", num_genes: int):
        super().__init__(problem, num_genes)
        self.forklifts = problem.forklifts
        self.products = problem.products
        self.path = []

    @property
    def compute_fitness(self, j=None) -> float:
        forklifts = self.problem.forklifts
        products = self.problem.products
        agent_search = self.problem.agent_search
        path = [forklifts[0]]

        num_forklift = 0
        fitness = 0
        genome_length = len(self.genome)
        #optimizar isto
        if self.genome[0] <= len(products):
            fitness += agent_search.get_pair(forklifts[num_forklift], products[self.genome[0] - 1]).value
            prod_fork = 1  # 0 - forklift (previous element), 1 - product
        else:
            fitness += agent_search.get_pair(forklifts[num_forklift], agent_search.exit).value
            num_forklift += 1
            prod_fork = 0  # 0 - forklift (previous element), 1 - product
        for i in range(1,genome_length - 1):
            current_gene = self.genome[i]
            if current_gene <= len(products):
                if prod_fork == 1:
                    fitness += agent_search.get_pair(products[self.genome[i - 1] - 1], products[current_gene - 1]).value
                else:
                    fitness += agent_search.get_pair(forklifts[num_forklift], products[current_gene - 1]).value
                prod_fork = 1
            else:
                if prod_fork == 1:
                    fitness += agent_search.get_pair(products[self.genome[i - 1] - 1], agent_search.exit).value
                else:
                    fitness += agent_search.get_pair(forklifts[num_forklift], agent_search.exit).value
                num_forklift += 1
                prod_fork = 0

        last_gene = self.genome[genome_length - 1]
        prev_last_gene = self.genome[genome_length - 2]

        if last_gene <= len(products):
            if prod_fork == 1:
                fitness += agent_search.get_pair(products[prev_last_gene - 1], products[last_gene - 1]).value
                fitness += agent_search.get_pair(products[last_gene - 1], agent_search.exit).value
            else:
                fitness += agent_search.get_pair(forklifts[num_forklift], products[last_gene - 1]).value
                fitness += agent_search.get_pair(products[last_gene - 1], agent_search.exit).value
        else:
            num_forklift += 1
            if prod_fork == 1:
                fitness += agent_search.get_pair(products[prev_last_gene - 1], agent_search.exit).value
                fitness += agent_search.get_pair(forklifts[num_forklift], agent_search.exit).value
            else:
                fitness += agent_search.get_pair(forklifts[num_forklift - 1], agent_search.exit).value
                fitness += agent_search.get_pair(forklifts[num_forklift], agent_search.exit).value


        self.fitness = fitness
        # self.path = path
        # for cell in path:
        #     print(cell)
        # print("END")
        return self.fitness

    '''
    colisoes no obtain allpath
    return forklifts_path, max_steps
    path -> lista de todas as cells por onde o forklift passou
    guardar cells por onde o forklift passou no pair 
    solution -> devolver todas as cells entre cada par
    ==================================
    guardar a posicao inicial do forklift 
    ao correr as cells, verificar se o produto inicial é superior ao outro, e percorrer as cells do fim pro inicio
    '''
    def obtain_all_path(self):
        pass
        # path = []
        # state = copy.copy(self.problem.agent_search.initial_environment)
        # for cell in range (len(self.genome)):
        #     state.line_forklift = self.problem.forklifts[gene]
        #     state.column_forklift = self.problem.forklifts[gene]
        #     if self.genome[gene + 1] <= len(self.problem.products):
        #         goal_position = self.problem.product_positions[gene]
        #     else:
        #         goal_position = self.problem.agent_search.exit
        #     agent_path = self.problem.agent_search.solve_problem(state, goal_position)
        #     path.extend(agent_path.get_actions())
        # return path

    def __str__(self):
        string = 'Fitness: ' + f'{self.fitness}' + '\n'
        string += str (self.genome) + "\n\n"
        # TODO
        #numero de  passos de cada forklift
        # for i in range(len(self.forklifts)):

        return string

    def better_than(self, other: "WarehouseIndividual") -> bool:
        return True if self.fitness < other.fitness else False

    # __deepcopy__ is implemented here so that all individuals share the same problem instance
    def __deepcopy__(self, memo):
        new_instance = self.__class__(self.problem, self.num_genes)
        new_instance.genome = self.genome.copy()
        new_instance.fitness = self.fitness
        # TODO
        return new_instance