import random
import time
from math import comb
import numpy as np


class GA_WorstOut:
    def __init__(self, graph, types_emp_id_dict):
        self.graph = graph
        self.types_emp_id_dict = types_emp_id_dict
        self.total_from_each_type = len(types_emp_id_dict[0])
        self.generations = 10000
        self.POPULATION_SIZE = 100
        self.BEST_N_AMOUNT = 10
        self.population = []
        self.grades = []
        self.best_n_index = []
        self.best_sol= []

    def solve(self):
        # timeout = time.time() + 1  # 1 sec

        # Creating an initial population
        self.create_population()
        # print(self.population)

        for i in range(self.generations):
            # if time.time() > timeout:
            #    return self.best_clique

            # 1. Evaluation
            self.evaluate()
            if self.best_sol:
                print("FOUND" , self.best_sol)
                return self.best_sol
            # best_n_index = sorted(best_n_index)

            # 2. Crossover
            # print("Crossover")
            crossover_list = []
            for ind in self.best_n_index:
                crossover_list.append(self.population[ind])
            childrens = self.crossover(crossover_list)

            # 3. Mutation
            # print("Mutation")
            mutation_children = self.mutation(childrens)  # maybe nothing happens
            self.population = mutation_children

        return []

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
        if max(self.grades)==1.0:
            self.best_sol =  self.population[self.grades.index(1)]
        self.best_n_index = sorted(range(len(self.grades)), key=lambda i: self.grades[i])[-self.BEST_N_AMOUNT:]

    def evaluate_population(self):
        grades = []
        for chromosome in self.population:
            grade = self.evaluate_chromosome(chromosome)
            grades.append(grade)
        return grades

    def is_valid(self, clique, v):
        """
        :param clique: current clique
        :param v: vertex that we want to add to the clique
        :return:  bool -  if the addition of vertex v is legal (if v connected to all the vertex in current clique)
        """
        for other_vertex in clique:
            friends = self.graph[other_vertex].keys()
            if v not in friends:
                return False
        return True

    def popularity(self, emp_id, clique):
        num_of_friends_in_team = 0
        for edge in clique:
            if emp_id == edge:
                continue
            has_edge = self.graph.has_edge(emp_id, edge)
            if has_edge:
                num_of_friends_in_team += 1
        return num_of_friends_in_team

    def crossover(self, best_chromosomes):
        after_crossover = best_chromosomes.copy()
        for i in range(len(best_chromosomes)):
            for j in range(i + 1, len(best_chromosomes)):
                after_crossover.append(self.simple_crossover(best_chromosomes[i], best_chromosomes[j]))
        return after_crossover

    def simple_crossover(self, parent1, parent2):
        child = []
        for i in range(len(parent1)):
            if random.random() < 0.5:
                child.append(parent1[i])
            else:
                child.append(parent2[i])
        return child

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

    def evaluate_chromosome(self, chromosome):
        num_of_friends_in_team = 0
        for i in range(0, len(chromosome)):
            for j in range(i + 1, len(chromosome)):
                vi_id = chromosome[i]
                vj_id = chromosome[j]
                has_edge = self.graph.has_edge(vi_id, vj_id)
                if has_edge:
                    num_of_friends_in_team += 1
        maximum_edges = comb(len(chromosome), 2)
        grade = num_of_friends_in_team / maximum_edges
        return grade

    def mutation(self, children):
        mutation_percentage = 5
        for child in children:
            random_num = random.randint(0, 100)
            if random_num < mutation_percentage:
                rand_type = random.randrange(0, len(self.types_emp_id_dict.keys()))
                rand_emp = random.randrange(self.types_emp_id_dict[rand_type][0], self.types_emp_id_dict[rand_type][-1])
                child[int(rand_type)] = np.int32(rand_emp)
        return children


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
