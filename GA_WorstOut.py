import math
import random
import time
from math import comb

import numpy as np


class GA_WorstOut:
    def __init__(self, graph, types_emp_id_dict,level_name, algo_types):
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

    def solve(self):
        timeout = time.time() + 2  # 2 sec

        # Creating an initial population
        self.create_population()

        #for i in range(self.generations):
        while time.time()<timeout:
            # if time.time() > timeout:
            # return self.best_sol

            # 1. Evaluation
            self.evaluate()
            if self.best_sol:
                print("FOUND", self.best_sol)
                return self.best_sol

            # 2. Crossover
            crossover_list = []
            for ind in self.best_n_index:
                crossover_list.append(self.population[ind])
            children = self.crossover(crossover_list)

            # 3. Mutation
            mutation_children = self.mutation(children)  # maybe nothing happens
            self.population = mutation_children

        self.evaluate()
        self.worst_out()

        return self.best_sol

    def create_population(self):
        initial_population = []
        for i in range(self.POPULATION_SIZE):
            chromosome = []
            for empType in self.types_emp_id_dict.keys():
                # choose random root
                emp_from_same_type_list = self.types_emp_id_dict[empType]
                random_num = random.randrange(0, self.total_from_each_type)
                chromosome.append(emp_from_same_type_list[random_num])
            initial_population.append(chromosome)
        self.population = initial_population

    def evaluate(self):
        self.grades = self.evaluate_population()
        if max(self.grades) == 1.0:
            self.best_sol = self.population[self.grades.index(1)]
        self.best_n_index = sorted(range(len(self.grades)), key=lambda i: self.grades[i])[-self.BEST_N_AMOUNT:]

    def evaluate_population(self):
        grades = []
        for chromosome in self.population:
            grade = self.evaluate_chromosome(chromosome)
            grades.append(grade)
        return grades

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


    def crossover(self, best_chromosomes):
        after_crossover = []
        for i in range(len(best_chromosomes)):
            for j in range(i + 1, len(best_chromosomes)):
                if set(best_chromosomes[i])==set(best_chromosomes[j]):
                    continue
                child = self.simple_crossover(best_chromosomes[i], best_chromosomes[j])
                if child not in after_crossover:
                    after_crossover.append(child)
        for chr in best_chromosomes:
            if chr not in after_crossover:
                after_crossover.append(chr)
        #print(len(after_crossover))
        return after_crossover

    def simple_crossover(self, parent1, parent2):
        child = []
        for i in range(len(parent1)):
            if random.random() < 0.5:
                child.append(parent1[i])
            else:
                child.append(parent2[i])
        return child

    def mutation(self, children):
        mutation_percentage = 5
        for child in children:
            random_num = random.randint(0, 100)
            if random_num < mutation_percentage:
                rand_type = random.randrange(0, len(self.types_emp_id_dict.keys()))
                rand_emp = random.randrange(self.types_emp_id_dict[rand_type][0], self.types_emp_id_dict[rand_type][-1])
                child[int(rand_type)] = np.int32(rand_emp)
        return children

    def worst_out(self):
        for group in self.population:
            print("before removal: " , group)
            group = self.remove_bad_emp(group)
            print("after removal: " , group)
            group = self.add_good_emp(group)
            print("after add: " , group)


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

# one-point crossover
def one_point_crossover(parent1, parent2):
    # choose a random split point
    split_point = random.randint(0, len(parent1) - 1)
    # create the children
    child1 = parent1[:split_point] + parent2[split_point:]
    child2 = parent2[:split_point] + parent1[split_point:]
    return child1, child2

    # uniform crossover


def uniform_crossover(parent1, parent2):
    # create the children
    child1 = []
    child2 = []
    for i in range(len(parent1)):
        if random.random() < 0.5:
            child1.append(parent1[i])
            child2.append(parent2[i])
        else:
            child1.append(parent2[i])
            child2.append(parent1[i])
    return [child1, child2]
