import copy
import math
import random
import time
import csv
from math import comb
from deap import base, creator, tools


WRITE_STATISTICS = False

class GA_Worst_out:
    def __init__(self, graph, types_emp_id_dict,level_name, algo_types,crossover,population_size):
        self.graph = graph
        self.types_emp_id_dict = types_emp_id_dict
        self.total_from_each_type = len(types_emp_id_dict[0])
        self.generations = 100
        self.population = []
        self.level = level_name
        self.algo = algo_types
        self.best_sol = []
        self.generations_statistics = []
        self.crossover_statistics = []
        self.worst_out_statistics = []
        self.duplicates = 0
        self.crossover = crossover
        self.population_size = population_size

        self.toolbox = base.Toolbox()
        # Create the DEAP self.toolbox and define the problem variables
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        # self.toolbox.register("attr_int", random.randint, 0, 100)
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.init_individual)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

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
        return grade

    def evaluate_Generation(self, lst_of_lst):
        return [self.evaluate_chromosome(lst) for lst in lst_of_lst]

    def create_population(self, population_size):
        for i in range(population_size):
            self.population.append(self.init_individual())

    def init_individual(self):
        lst = []
        for empType in self.types_emp_id_dict.keys():
            # choose random root
            emp_from_same_type_list = self.types_emp_id_dict[empType]
            random_num = random.randrange(0, len(self.types_emp_id_dict[0]))
            lst.append(emp_from_same_type_list[random_num])
        if lst in self.population:
            self.duplicates+=1
        return lst

    def worst_out(self, group):
        group = self.remove_bad_emp(group)
        after_removal = self.calculate_length(group)
        group = self.add_good_emp(group)
        after_addition = self.calculate_length(group)
        self.worst_out_statistics.append([after_removal,after_addition])

    def employees_popularity(self, emp_list):
        group_grade = []
        for i in range(len(emp_list)):
            num_of_friends = 0
            for j in range(len(emp_list)):
                if self.graph.has_edge(emp_list[i], emp_list[j]) and i != j:
                    num_of_friends += 1
            if num_of_friends == 0:
                group_grade.append(math.inf)
            else:
                group_grade.append(num_of_friends)
        return group_grade

    def remove_bad_emp(self, group):
        while self.evaluate_chromosome(group) < 1:  # pop weak emp until legal
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
            if group[i] == -1:
                empFromSameTypeList = self.types_emp_id_dict[i].copy()  # {1: [1, 2 ,3], 2: [4, 5, 6]..}
                random.shuffle(empFromSameTypeList)
                for v in empFromSameTypeList:
                    success = self.is_valid(group, v)
                    if success:
                        group[i] = v
                        break
        if self.calculate_length(self.best_sol) < self.calculate_length(group):
            self.best_sol = group
        return group

    def is_valid(self, clique, v):
        """
        :param clique: current clique
        :param v: vertex that we want to add to the clique
        :return:  bool -  if the addition of vertex v is legal (if v connected to all the vertex in current clique)
        """
        for other_vertex in clique:
            if other_vertex != -1:
                friends = self.graph[other_vertex].keys()
                if v not in friends:
                    return False
        return True

    def calculate_length(self, group):
        return len([i for i in group if i != -1])

    def calculate_statistics(self,generation_no):
        grades = self.evaluate_Generation(self.population)
        return (generation_no , sum(grades) / len(grades), max(grades), min(grades))  # [avg,max,min]

    def calculate_crossover_statistics(self, generation_no):
        parent1, parent2 = sorted(self.population, key=lambda x: self.evaluate_chromosome(x), reverse=True)[:2]
        crossovers=[]
        for _ in range(100):
            child1 ,child2 = copy.deepcopy(parent1), copy.deepcopy(parent2)
            if self.crossover == tools.cxUniform:
                self.toolbox.mate(child1, child2, 0.5)
            else:
                if random.random() <= 0.5:
                    self.toolbox.mate(child1, child2)
            crossovers.append(child1)
            crossovers.append(child2)
        grades = self.evaluate_Generation(crossovers)
        self.crossover_statistics.append([generation_no , self.evaluate_chromosome(parent1),self.evaluate_chromosome(parent2), sum(grades) / len(grades), max(grades), min(grades)])
        return

    def solve(self):
        '''
        CXPB:  probability for crossover. 0.8 means 80% chance of crossover.
        MUTPB: probability for mutation. 0.5 means 50% chance of mutation.
        NGEN: number of generations GA will run.
        '''
        self.toolbox.register("mate", self.crossover)
        self.population = self.toolbox.population(n=self.population_size)
        CXPB, MUTPB, NGEN = 0.8, 0.5, 100
        timeout = time.time() + 2  # 2 sec
        generation=0
        while time.time() < timeout:
            if WRITE_STATISTICS:
                self.generations_statistics.append(self.calculate_statistics(generation))
                if generation%5==0:
                    self.calculate_crossover_statistics(generation)
            offspring = self.toolbox.select(self.population, len(self.population))
            offspring = list(map(self.toolbox.clone, offspring))
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if self.crossover == tools.cxUniform:
                    self.toolbox.mate(child1, child2, CXPB)
                else:
                    if random.random() <= CXPB:
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
                ind.fitness.values = fit,

            self.population[:] = offspring
            highest_grade_chromosome = copy.deepcopy(max(self.population, key=lambda x: self.evaluate_chromosome(x)))
            self.worst_out(highest_grade_chromosome)
            if self.calculate_length(self.best_sol)==self.total_from_each_type:
                return self.best_sol
            generation+=1

        for group in self.population:
            self.worst_out(group)
        for lst in self.population:
            if self.calculate_length(lst) > self.calculate_length(self.best_sol) and self.evaluate_chromosome(lst) > self.evaluate_chromosome(self.best_sol):
                self.best_sol = lst
        if WRITE_STATISTICS:
            # open the file in the write mode
            with open('Results/Statistics/generations_statistics.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["generation","avg","max","min"])
                writer.writerows(self.generations_statistics)
            with open('Results/Statistics/worst_out_statistics.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(self.worst_out_statistics)
            with open('Results/Statistics/crossover_statistics.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["generation","parent1","parent2","avg","max","min"])
                writer.writerows(self.crossover_statistics)
        return self.best_sol
