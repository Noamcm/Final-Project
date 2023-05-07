import math
import random
from math import comb

import networkx as nx
import numpy as np
from deap import base, creator, tools
from deap import *
from collections import UserList

class GA_DEAP_Best_In:
    def __init__(self, graph, types_emp_id_dict):
        self.graph = graph
        self.matrix = nx.to_numpy_array(graph)
        self.types_emp_id_dict = types_emp_id_dict
        self.generations = 20
        self.POPULATION_SIZE = 10
        self.BEST_N_AMOUNT = 8
        self.best_clique = []
        self.best_clique_size = 0
        self.best_clique_weight = 0
        self.population = []
        self.total_types = len(self.types_emp_id_dict)
        self.total_from_each_type = len(self.types_emp_id_dict[0])
        self.max_friends = self.total_types * self.total_from_each_type - self.total_from_each_type
        self.total_vertexes = self.total_types * self.total_from_each_type

        self.toolbox = base.Toolbox()
        # # Create the DEAP self.toolbox and define the problem variables
        # creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        # creator.create("Individual",list , fitness=creator.FitnessMax)
        # #self.toolbox.register("attr_int", random.randint, 0, 100)
        # self.toolbox.register("individual", tools.initIterate, creator.Individual, self.init_individual)
        # self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        #
        # # Define the genetic operators
        # self.toolbox.register("mate", tools.cxUniform)
        # self.toolbox.register("mutate", self.mutation)
        # self.toolbox.register("select", tools.selTournament, tournsize=3)
        #
        # # Define the evaluation function and the main GA loop
        # self.toolbox.register("evaluate", self.evaluate_chromosome)

        # Create the DEAP self.toolbox and define the problem variables
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        self.toolbox.register("attr_bool", random.randint, 0, 1)
        self.toolbox.register("individual", self.create_chromosome)
        self.toolbox.register("population", self.create_population)
        self.toolbox.register("evaluate", self.evaluate_chromosome)
        self.toolbox.register("mate", self.crossover)
        self.toolbox.register("mutate", self.mutation)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

        # Define the evaluation function and the main GA loop

        # Create a statistics object
        self.stats = tools.Statistics()
        self.stats.register("avg", lambda x: sum(x) / len(x))
        self.stats.register("min", min)
        self.stats.register("max", max)

    # def mutation(self, group):
    #     rand_type = random.randrange(0, len(self.types_emp_id_dict.keys()))
    #     rand_emp = random.randrange(self.types_emp_id_dict[rand_type][0], self.types_emp_id_dict[rand_type][-1])
    #     group[int(rand_type)] = rand_emp
    #
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
    #
    # def evaluate_Generation(self, lst_of_lst):
    #     return [self.evaluate_chromosome(lst)[0] for lst in lst_of_lst]
    #
    # def init_individual(self):
    #     lst = []
    #     for empType in self.types_emp_id_dict.keys():
    #         # choose random root
    #         emp_from_same_type_list = self.types_emp_id_dict[empType]
    #         random_num = random.randrange(0, len(self.types_emp_id_dict[0]))
    #         lst.append(emp_from_same_type_list[random_num])
    #     return lst
    #
    # def worst_out(self):
    #     for group in self.population:
    #         #print("before removal: " , group)
    #         group = self.remove_bad_emp(group)
    #         #print("after removal: " , group)
    #         group = self.add_good_emp(group)
    #         #print("after add: " , group)
    #
    # def employees_popularity(self, emp_list):
    #     group_grade = []
    #     for i in range(len(emp_list)):
    #         num_of_friends = 0
    #         for j in range(len(emp_list)):
    #             if self.graph.has_edge(emp_list[i], emp_list[j]) and i != j:
    #                 num_of_friends += 1
    #         if num_of_friends==0:
    #             group_grade.append(math.inf)
    #         else:
    #             group_grade.append(num_of_friends)
    #     return group_grade
    #
    # def remove_bad_emp(self, group):
    #     while self.evaluate_chromosome(group)[0] < 1:  # pop weak emp until legal
    #         group_grade = self.employees_popularity(group)
    #         removed_emp_idx = group_grade.index(min(group_grade))
    #         group[removed_emp_idx] = -1
    #         if max(group) == -1 or min(group_grade) == math.inf:
    #             break
    #     if self.evaluate_chromosome(group) == 1.0:  # update new sol
    #         if self.calculate_length(self.best_sol) < self.calculate_length(group):
    #             self.best_sol = group
    #     return group
    #
    # def add_good_emp(self, group):
    #     for i in range(len(group)):
    #         if group[i]==-1:
    #             empFromSameTypeList = self.types_emp_id_dict[i].copy()  # {1: [1, 2 ,3], 2: [4, 5, 6]..}
    #             random.shuffle(empFromSameTypeList)
    #             # v = random.choice(empFromSameTypeList)
    #             for v in empFromSameTypeList:
    #                 success = self.is_valid(group, v)
    #                 if success:
    #                     group[i]=v
    #                     break
    #     if self.calculate_length(self.best_sol) < self.calculate_length(group):
    #         #print(group)
    #         self.best_sol = group
    #     return group
    #
    # def is_valid(self, clique, v):
    #     """
    #     :param clique: current clique
    #     :param v: vertex that we want to add to the clique
    #     :return:  bool -  if the addition of vertex v is legal (if v connected to all the vertex in current clique)
    #     """
    #     for other_vertex in clique:
    #         if other_vertex!=-1:
    #             friends = self.graph[other_vertex].keys()
    #             if v not in friends:
    #                 return False
    #     return True
    #
    # def calculate_length(self, group):
    #     return len([i for i in group if i != -1])
    def create_chromosome(self):
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

    def is_better(self, cur_clique):
        if self.best_clique_weight == 0:
            return cur_clique
        else:
            return cur_clique[1] > self.best_clique_weight

    def is_valid(self, clique, v):
        """
        :param clique: current clique
        :param v: vertex that we want to add to the clique
        :return:  bool -  if the addition of vertex v is legal (if v connected to all the vertex in current clique)
        """
        if v == -1:
            return False
        for other_vertex in clique:
            if other_vertex == -1:
                continue
            # friends = self.graph[other_vertex]
            # print(friends)
            if v not in self.graph[other_vertex].keys():
                return False
            # if len(friends) == 0 or v not in list(friends).any(v):
            # if len(friends) == 0 or v not in friends:
            #     return False
        return True

    def fill_empty_crossover(self, parent1, parent2):
        # print(parent1)
        # print(parent2)
        child1 = parent1

        # remove the worst employee, and try to fill the empty cells
        p1_empty_index = []
        p1_degree_list = []
        for i in range(len(parent1)):
            if parent1[i] == -1:
                p1_empty_index.append(i)
                p1_degree_list.append(-1)
            else:
                p1_degree_list.append(self.graph.degree[i])

        k = int(len(self.types_emp_id_dict[0]) / 5)
        sorted_worst = np.argpartition(p1_degree_list, k)[:k]
        for i in sorted_worst:
            child1[i] = -1
            p1_empty_index.append(i)

        # index_of_small = p1_degree_list.index(min(filter(lambda x: x > 0, p1_degree_list)))
        # p1_empty_index.append(index_of_small)
        # child1[index_of_small] = -1

        for i in p1_empty_index:
            candidate_v = parent2[i]
            if self.is_valid(child1, candidate_v):
                child1[i] = candidate_v
        return child1

    def crossover(self, best_chromosomes):
        # print("crossover start")
        after_crossover = []
        k = 0
        for i in range(len(best_chromosomes)):
            parent1 = best_chromosomes[i]

        for i in range(0, len(best_chromosomes)):
            for j in range(i + 1, len(best_chromosomes)):
                parent1 = best_chromosomes[i]
                parent2 = best_chromosomes[j]
                child1 = self.fill_empty_crossover(parent1, parent2)
                child2 = self.fill_empty_crossover(parent2, parent1)
                if child1 not in after_crossover:
                    after_crossover.append(child1)
                if child2 not in after_crossover:
                    after_crossover.append(child2)
                k += 1
                # after_crossover.append(self.fill_empty_crossover(best_chromosomes[i], best_chromosomes[i + 1]))
        return after_crossover

    def create_population(self):
        initial_population = []
        for i in range(self.POPULATION_SIZE):
            chromosome = self.create_chromosome()
            if chromosome in initial_population:
                continue
            initial_population.append(chromosome)
        self.population = initial_population

    def evaluate_chromosome(self, chromosome):
        # num_of_friends_in_team = 0
        # for i in range(0, len(chromosome)):
        #     for j in range(i, len(chromosome)):
        #         vi_id = chromosome[i]
        #         vj_id = chromosome[j]
        #         has_edge = self.graph.has_edge(vi_id, vj_id)
        #         if has_edge:
        #             num_of_friends_in_team += 1
        # grade = num_of_friends_in_team

        grade = 0
        for i in chromosome:
            if i != -1:
                # vertex_weight = self.degree_dict[i] / self.max_friends
                # grade += 10 + 1 * vertex_weight
                grade += 1
        return grade

    def evaluate_population(self):
        grades = []
        for chromosome in self.population:
            grade = self.evaluate_chromosome(chromosome)
            grades.append(grade)
        return grades

    def mutation(self, children):
        for child in children:
            for empType in self.types_emp_id_dict.keys():
                if child[empType] != -1:
                    continue
                emp_from_same_type_list = self.types_emp_id_dict[empType]
                random.shuffle(emp_from_same_type_list)
                success = False
                for v in emp_from_same_type_list:
                    if self.is_valid(child, v):
                        child[int(empType)] = v
                        success = True
                        break
                if not success:
                    child[empType] = -1
        return children

    # one-point crossover
    # def one_point_crossover(parent1, parent2):
    #     # choose a random split point
    #     split_point = random.randint(0, len(parent1) - 1)
    #     # create the children
    #     child1 = parent1[:split_point] + parent2[split_point:]
    #     child2 = parent2[:split_point] + parent1[split_point:]
    #     return child1, child2
    #
    # # uniform crossover
    # def uniform_crossover(parent1, parent2):
    #     # create the children
    #     child1 = []
    #     child2 = []
    #     for i in range(len(parent1)):
    #         if random.random() < 0.5:
    #             child1.append(parent1[i])
    #             child2.append(parent2[i])
    #         else:
    #             child1.append(parent2[i])
    #             child2.append(parent1[i])
    #     return child1, child2
    #

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

def fitness(chromosome):
    grade = 0
    for i in chromosome:
        if i != -1:
            # vertex_weight = self.degree_dict[i] / self.max_friends
            # grade += 10 + 1 * vertex_weight
            grade += 1
    return grade

def tournament_selection(population, tournament_size):
    """Selects an individual from the population using tournament selection.

    Args:
        population (list): The population to select from.
        tournament_size (int): The number of individuals to include in each tournament.

    Returns:
        An individual selected using tournament selection.
    """
    # print("tournament_selection:len(population):", len(population))
    # print("tournament_selection:tournament_size:", tournament_size)
    tournament = random.sample(population, tournament_size)
    winner = max(tournament, key=fitness)
    # print(winner)
    return winner