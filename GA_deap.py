import math
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
        self.toolbox.register("mate", tools.cxUniform)
        self.toolbox.register("mutate", self.mutation)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

        # Define the evaluation function and the main GA loop
        self.toolbox.register("evaluate", self.evaluate_chromosome)

        # Create a statistics object
        self.stats = tools.Statistics()
        self.stats.register("avg", lambda x: sum(x) / len(x))
        self.stats.register("min", min)
        self.stats.register("max", max)

    def mutation(self, group):
        rand_type = random.randrange(0, len(self.types_emp_id_dict.keys()))
        rand_emp = random.randrange(self.types_emp_id_dict[rand_type][0], self.types_emp_id_dict[rand_type][-1])
        group[int(rand_type)] = rand_emp

    # def evaluate_chromosome(self, group):
    #     chromosome = [i for i in group if i != -1]
    #     num_of_friends_in_team = 0
    #     for i in range(0, len(chromosome)):
    #         for j in range(i + 1, len(chromosome)):
    #             vi_id = chromosome[i]
    #             vj_id = chromosome[j]
    #             has_edge = self.graph.has_edge(vi_id, vj_id)
    #             if has_edge:
    #                 num_of_friends_in_team += 1
    #     maximum_edges = comb(len(chromosome), 2)
    #     grade = num_of_friends_in_team / maximum_edges if maximum_edges > 0 else 0
    #
    #     return grade,
    def evaluate_chromosome(self, chromosome):
        grade = 0
        for i in chromosome:
            if i != -1:
                # vertex_weight = self.degree_dict[i] / self.max_friends
                # grade += 10 + 1 * vertex_weight
                grade += 1
        return grade

    def evaluate_Generation(self, lst_of_lst):
        return [self.evaluate_chromosome(lst)[0] for lst in lst_of_lst]

    # def init_individual(self):
    #     lst = []
    #     for empType in self.types_emp_id_dict.keys():
    #         # choose random root
    #         emp_from_same_type_list = self.types_emp_id_dict[empType]
    #         random_num = random.randrange(0, len(self.types_emp_id_dict[0]))
    #         lst.append(emp_from_same_type_list[random_num])
    #     return lst

    def init_individual(self):
        chromosome = []
        for empType in self.types_emp_id_dict.keys():
            # choose random root
            emp_from_same_type_list = self.types_emp_id_dict[empType]
            random.shuffle(emp_from_same_type_list)
            success = False
            for v in emp_from_same_type_list:
                if self.is_valid(chromosome, v):
                    chromosome.append(v)
                    success = True
                    break
            if not success:
                chromosome.append(-1)
        return list(chromosome)

    def worst_out(self):
        for group in self.population:
            #print("before removal: " , group)
            group = self.remove_bad_emp(group)
            #print("after removal: " , group)
            group = self.add_good_emp(group)
            #print("after add: " , group)


    def employees_popularity(self, emp_list):
        group_grade = []
        for i in range(len(emp_list)):
            num_of_friends = 0
            for j in range(len(emp_list)):
                if self.graph.has_edge(emp_list[i], emp_list[j]) and i != j:
                    num_of_friends += 1
            if num_of_friends==0:
                group_grade.append(math.inf)
            else:
                group_grade.append(num_of_friends)
        return group_grade

    def remove_bad_emp(self, group):
        while self.evaluate_chromosome(group)[0] < 1:  # pop weak emp until legal
            group_grade = self.employees_popularity(group)
            removed_emp_idx = group_grade.index(min(group_grade))
            group[removed_emp_idx] = -1
            if max(group) == -1 or min(group_grade) == math.inf:
                break
        if self.evaluate_chromosome(group) == 1.0:  # update new sol
            if self.calculate_length(self.best_sol) < self.calculate_length(group):
                self.best_sol = group
        return group

    def add_good_emp(self, group):
        for i in range(len(group)):
            if group[i]==-1:
                empFromSameTypeList = self.types_emp_id_dict[i].copy()  # {1: [1, 2 ,3], 2: [4, 5, 6]..}
                random.shuffle(empFromSameTypeList)
                # v = random.choice(empFromSameTypeList)
                for v in empFromSameTypeList:
                    success = self.is_valid(group, v)
                    if success:
                        group[i]=v
                        break
        if self.calculate_length(self.best_sol) < self.calculate_length(group):
            #print(group)
            self.best_sol = group
        return group

    def is_valid(self, clique, v):
        """
        :param clique: current clique
        :param v: vertex that we want to add to the clique
        :return:  bool -  if the addition of vertex v is legal (if v connected to all the vertex in current clique)
        """
        for other_vertex in clique:
            if other_vertex!=-1:
                friends = self.graph[other_vertex].keys()
                if v not in friends:
                    return False
        return True

    def calculate_length(self, group):
        return len([i for i in group if i != -1])

    def solve(self):
        '''
        CXPB:  probability for crossover. 0.5 means 50% chance of crossover.
        MUTPB: probability for mutation. 0.2 means 20% chance of mutation.
        NGEN: number of generations GA will run.
        '''
        self.population = self.toolbox.population(n=10)
        hof = tools.HallOfFame(1)
        CXPB, MUTPB, NGEN = 0.5, 0.2, 100
        print(self.population)
        for g in range(NGEN):
            offspring = self.toolbox.select(self.population, len(self.population))
            offspring = list(map(self.toolbox.clone, offspring))

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                self.toolbox.mate(child1, child2, CXPB)
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


            self.population[:] = offspring
        self.worst_out()
        #print(self.population)
        #print(max([self.calculate_length(lst) for lst in self.population]))
        #print(self.evaluate_Generation(self.population))
        best =[]
        best_score=0
        best_size=0
        for lst in self.population:
            if self.calculate_length(lst)>best_size and self.evaluate_chromosome(lst)[0]>best_score:
                best=lst
        return best
            #print(self.evaluate_Generation(pop))

            # fits = [ind.fitness.values[0] for ind in pop]
            # length = len(pop)
            # mean = sum(fits) / length
            # sum2 = sum(x * x for x in fits)
            # std = abs(sum2 / length - mean ** 2) ** 0.5
            #print("Generation {:>3} -- Min: {:>5}, Max: {:>5}, Avg: {:>5.2f}, Std: {:>5.2f}".format(g, min(fits), max(fits), mean, std))

