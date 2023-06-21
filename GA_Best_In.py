import random
import time
import networkx as nx
import numpy as np
from multiprocessing.pool import ThreadPool

import WriteToCsv


class GA_Best_In:
    def __init__(self, graph, types_emp_id_dict,level_name, algo_types,population_size):
        self.graph = graph
        self.matrix = nx.to_numpy_array(graph)
        self.types_emp_id_dict = types_emp_id_dict
        self.generations = 20
        self.best_clique = []
        self.best_clique_size = 0
        self.best_clique_weight = 0
        self.population = []
        self.total_types = len(self.types_emp_id_dict)
        self.total_from_each_type = len(self.types_emp_id_dict[0])
        self.max_friends = self.total_types * self.total_from_each_type - self.total_from_each_type
        self.total_vertexes = self.total_types * self.total_from_each_type
        self.degree_dict = {}
        self.level = level_name
        self.algo = algo_types
        self.population_size = population_size


    def solve(self):
        timeout = time.time() + 2  # 2 sec
        num_threads = 6

        # Creating an initial population
        self.create_population()

        i = 0
        while True:
            if time.time() > timeout:
                return self.best_clique

            chunk_size = len(self.population) // num_threads
            chunks = [self.population[i:i + chunk_size] for i in range(0, len(self.population), chunk_size)]

            pool = ThreadPool(processes=num_threads)
            winners = []
            for chunk in chunks:
                async_result = pool.apply_async(tournament_selection, (chunk, int(len(chunk))))
                winners.append(async_result.get())

            best_n_index = winners

            grades = []
            for x in best_n_index:
                grades.append(fitness(x))

            # Combine lst and grade into tuples and sort by grade
            sorted_data = sorted(zip(best_n_index, grades), key=lambda x: x[1], reverse=True)

            # Unpack sorted_data back into separate lists
            best_n_index, grades = zip(*sorted_data)


            # # 1. Evaluation
            # check if the best Chromosome from the Population is better than current best clique
            best_clique_candidate = (best_n_index[0], grades[0])
            if self.is_better(best_clique_candidate):
                self.best_clique = best_clique_candidate[0]
                self.best_clique_weight = best_clique_candidate[1]
                if self.best_clique_weight == self.total_types:
                    return self.best_clique

            # 2. Crossover
            crossover_list = []
            for ind in best_n_index:
                crossover_list.append(ind)
            children = self.crossover(crossover_list)
            # 3. Mutation
            mutation_children = self.mutation(children)
            self.population = self.population[:100]
            self.population[0:len(mutation_children)] = mutation_children
            children_grades = []
            for x in mutation_children:
                children_grades.append(fitness(x))
            # Combine lst and grade into tuples and sort by grade
            sorted_data = sorted(zip(mutation_children, children_grades), key=lambda x: x[1], reverse=True)
            # Unpack sorted_data back into separate lists
            mutation_children, children_grades = zip(*sorted_data)

            best_clique_candidate = (mutation_children[0], children_grades[0])
            if self.is_better(best_clique_candidate):
                self.best_clique = best_clique_candidate[0]
                self.best_clique_weight = best_clique_candidate[1]
                if self.best_clique_weight == self.total_types:
                    return self.best_clique
            i += 1


    def calculate_length(self, group):
        return len([i for i in group if i != -1])

    def fill_degree_dict(self):
        for worker in range(self.total_vertexes):
            different_friends = 0
            worker_friends = self.graph[worker]
            for work_type in self.types_emp_id_dict:
                workers_from_type = self.types_emp_id_dict[work_type]
                for w in workers_from_type:
                    if w in worker_friends:
                        different_friends += 1
            self.degree_dict[worker] = different_friends

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
            if v not in self.graph[other_vertex].keys():
                return False
        return True

    def fill_empty_crossover(self, parent1, parent2):
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

        k = int(len(self.types_emp_id_dict[0])/5)
        sorted_worst = np.argpartition(p1_degree_list, k)[:k]
        for i in sorted_worst:
            child1[i] = -1
            p1_empty_index.append(i)


        for i in p1_empty_index:
            candidate_v = parent2[i]
            if self.is_valid(child1, candidate_v):
                child1[i] = candidate_v
        return child1

    def crossover(self, best_chromosomes):
        after_crossover = []
        k = 0
        for i in range(len(best_chromosomes)):
            parent1 = best_chromosomes[i]

        for i in range(0, len(best_chromosomes)):
            for j in range(i+1, len(best_chromosomes)):
                parent1 = best_chromosomes[i]
                parent2 = best_chromosomes[j]
                child1 = self.fill_empty_crossover(parent1, parent2)
                child2 = self.fill_empty_crossover(parent2, parent1)
                if child1 not in after_crossover:
                    after_crossover.append(child1)
                if child2 not in after_crossover:
                    after_crossover.append(child2)
                k += 1
        return after_crossover

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

    def create_population(self):
        initial_population = []
        for i in range(self.population_size):
            chromosome = self.create_chromosome()
            if chromosome in initial_population:
                continue
            initial_population.append(chromosome)
        self.population = initial_population

    def evaluate_chromosome(self, chromosome):
        grade = 0
        for i in chromosome:
            if i != -1:
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

def fitness(chromosome):
    grade = 0
    for i in chromosome:
        if i != -1:
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
    tournament = random.sample(population, tournament_size)
    winner = max(tournament, key=fitness)
    return winner