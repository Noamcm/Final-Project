import copy
import math
import random
import time
import csv
from math import comb
from deap import base, creator, tools



class GA_deap:
    def __init__(self, graph, types_emp_id_dict):
        self.graph = graph
        self.types_emp_id_dict = types_emp_id_dict
        self.total_from_each_type = len(types_emp_id_dict[0])
        self.generations = 100
        self.POPULATIONSIZE=100
        self.population = []
        #self.grades = []
        #self.best_n_index = []
        self.best_sol = []
        #self.best_score = 0
        #self.best_size = 0
        self.generations_statistics = []
        self.crossover_statistics = []
        self.worst_out_statistics = []
        self.duplicates = 0

        self.toolbox = base.Toolbox()
        # Create the DEAP self.toolbox and define the problem variables
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        # self.toolbox.register("attr_int", random.randint, 0, 100)
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
        #print(self.population)
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
                # v = random.choice(empFromSameTypeList)
                for v in empFromSameTypeList:
                    success = self.is_valid(group, v)
                    if success:
                        group[i] = v
                        break
        if self.calculate_length(self.best_sol) < self.calculate_length(group):
            # print(group)
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
        max_parent_grade = max(self.evaluate_chromosome(parent1), self.evaluate_chromosome(parent2))
        crossovers=[]
        for _ in range(100):
            child1 ,child2 = copy.deepcopy(parent1), copy.deepcopy(parent2)
            self.toolbox.mate(child1, child2, 0.5)
            crossovers.append(child1)
            crossovers.append(child2)
        grades = self.evaluate_Generation(crossovers)
        # avg = sum(grades) / len(grades)
        # for g in grades:
        #     self.crossover_statistics.append([generation_no , self.evaluate_chromosome(parent1),self.evaluate_chromosome(parent2), g , avg])
        #     generation_no += 0.0001
        # return
        self.crossover_statistics.append([generation_no , self.evaluate_chromosome(parent1),self.evaluate_chromosome(parent2), sum(grades) / len(grades), max(grades), min(grades)])
        return
    def solve(self):
        '''
        CXPB:  probability for crossover. 0.8 means 80% chance of crossover.
        MUTPB: probability for mutation. 0.5 means 50% chance of mutation.
        NGEN: number of generations GA will run.
        '''
        #self.create_population(self.POPULATIONSIZE)
        self.population = self.toolbox.population(n=self.POPULATIONSIZE)

        #hof = tools.HallOfFame(1)
        CXPB, MUTPB, NGEN = 0.8, 0.5, 100
        print(self.population)
        timeout = time.time() + 2  # 2 sec
        generation=0
        # for g in NGEN:
        while time.time() < timeout:
            self.generations_statistics.append(self.calculate_statistics(generation))
            if generation%5==0:
                #self.crossover_statistics.append(self.calculate_crossover_statistics(generation))
                self.calculate_crossover_statistics(generation)

            offspring = self.toolbox.select(self.population, len(self.population))
            offspring = list(map(self.toolbox.clone, offspring))
            #offspring = copy.deepcopy(self.population)
            #offspring = self.population

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
                ind.fitness.values = fit,

            self.population[:] = offspring
            highest_grade_chromosome = copy.deepcopy(max(self.population, key=lambda x: self.evaluate_chromosome(x)))
            self.worst_out(highest_grade_chromosome)
            if self.calculate_length(self.best_sol)==self.total_from_each_type:
                return self.best_sol
            generation+=1

        for group in self.population:
            self.worst_out(group)
        # print(self.population)
        # print(max([self.calculate_length(lst) for lst in self.population]))
        # print(self.evaluate_Generation(self.population))
        for lst in self.population:
            if self.calculate_length(lst) > self.calculate_length(self.best_sol) and self.evaluate_chromosome(lst) > self.evaluate_chromosome(self.best_sol):
                self.best_sol = lst
        # open the file in the write mode
        with open('generations_statistics.csv', 'w', newline='') as f:
            #for row in self.generations_statistics:
            writer = csv.writer(f)
            writer.writerow(["generation","avg","max","min"])
            writer.writerows(self.generations_statistics)
        with open('worst_out_statistics.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.worst_out_statistics)
        with open('crossover_statistics.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["generation","parent1","parent2","avg","max","min"])
            #writer.writerow(["generation","parent1","parent2","grade","avg","max","min"])
            writer.writerows(self.crossover_statistics)
        print(self.duplicates)
        return self.best_sol
        # print(self.evaluate_Generation(pop))

        # fits = [ind.fitness.values[0] for ind in pop]
        # length = len(pop)
        # mean = sum(fits) / length
        # sum2 = sum(x * x for x in fits)
        # std = abs(sum2 / length - mean ** 2) ** 0.5
        # print("Generation {:>3} -- Min: {:>5}, Max: {:>5}, Avg: {:>5.2f}, Std: {:>5.2f}".format(g, min(fits), max(fits), mean, std))

