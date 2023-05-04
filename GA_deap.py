import random
from math import comb

from deap import base, creator, tools
from collections import UserList




class GA_deap:
    def __init__(self, graph, types_emp_id_dict):
        self.graph = graph
        self.types_emp_id_dict = types_emp_id_dict
        self.total_from_each_type = len(types_emp_id_dict[0])
        self.generations = 100
        self.POPULATION_SIZE = 300
        self.BEST_N_AMOUNT = 10
        self.population = []
        self.grades = []
        self.best_n_index = []
        self.best_sol = []



        self.toolbox = base.Toolbox()
        # Create the DEAP self.toolbox and define the problem variables
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual",list , fitness=creator.FitnessMax)
        #self.toolbox.register("attr_int", random.randint, 0, 100)
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.init_individual)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        # Define the genetic operators
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutUniformInt, low=0, up=100, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

        # Define the evaluation function and the main GA loop
        self.toolbox.register("evaluate", self.evaluate_chromosome)



    def eval_sum(self,individual):
        return sum(individual),


    def evaluate_chromosome(self, group):
        chromosome = [i for i in group if i != -1]
        num_of_friends_in_team = 0
        for i in range(0, len(chromosome)):
            for j in range(i + 1, len(chromosome)):
                vi_id = chromosome[i]
                vj_id = chromosome[j]
                has_edge = self.graph.has_edge(vi_id, vj_id)
                if has_edge:
                    num_of_friends_in_team += 1
        maximum_edges = comb(len(chromosome), 2)
        grade = num_of_friends_in_team / maximum_edges if maximum_edges > 0 else 0

        return grade,

    def init_individual(self):
        lst = []
        for empType in self.types_emp_id_dict.keys():
            # choose random root
            emp_from_same_type_list = self.types_emp_id_dict[empType]
            random_num = random.randrange(0, len(self.types_emp_id_dict[0]))
            lst.append(emp_from_same_type_list[random_num])
        return lst

    
    
    def solve(self):
        '''
        CXPB:  probability for crossover. 0.5 means 50% chance of crossover.
        MUTPB: probability for mutation. 0.2 means 20% chance of mutation.
        NGEN: number of generations GA will run.
        '''
        pop = self.toolbox.population(n=10)
        CXPB, MUTPB, NGEN = 0.5, 0.2, 100
        print(pop)
        for g in range(NGEN):
            offspring = self.toolbox.select(pop, len(pop))
            offspring = list(map(self.toolbox.clone, offspring))
    
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < CXPB:
                    self.toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values
    
            for mutant in offspring:
                if random.random() < MUTPB:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values
    
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = self.toolbox.map(self.toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
    
            pop[:] = offspring
    
            fits = [ind.fitness.values[0] for ind in pop]
            length = len(pop)
            mean = sum(fits) / length
            sum2 = sum(x * x for x in fits)
            std = abs(sum2 / length - mean ** 2) ** 0.5
            print(pop)
            print("Generation {:>3} -- Min: {:>5}, Max: {:>5}, Avg: {:>5.2f}, Std: {:>5.2f}".format(g, min(fits), max(fits), mean, std))
    
#     
# if __name__ == "__main__":
#     main()