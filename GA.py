import random
import time


class GA:
    def __init__(self, graph, types_emp_id_dict):
        self.graph = graph
        self.types_emp_id_dict = types_emp_id_dict
        self.generations = 100
        self.POPULATION_SIZE = 100
        self.BEST_N_AMOUNT = 10
        self.best_clique = []
        self.best_clique_size = 0
        self.best_clique_weight = 0
        self.population = []

    def solve(self):
        timeout = time.time() + 2  # 2 sec

        # Creating an initial population
        self.create_population()
        print(self.population)

        for i in range(self.generations):
            if time.time() > timeout:
                return self.best_clique

            # 1. Evaluation
            grades = self.evaluate_population()
            best_n_index = sorted(range(len(grades)), key=lambda i: grades[i])[-self.BEST_N_AMOUNT:]
            best_n_index = sorted(best_n_index)

            # check if the best Chromosome from the Population is better than current best clique
            best_clique_candidate = (self.population[best_n_index[0]], grades[best_n_index[0]])
            if self.is_better(best_clique_candidate):
                self.best_clique = best_clique_candidate[0]
                self.best_clique_weight = best_clique_candidate[1]
                # self.best_clique_size = len(self.best_clique)

            if self.best_clique_weight == self.types_emp_id_dict.keys():
                return self.best_clique

            # 2. Crossover
            print("Crossover")
            crossover_list = []
            for ind in best_n_index:
                crossover_list.append(self.population[ind])
            children = self.crossover(crossover_list)

            # 3. Mutation
            print("Mutation")
            mutation_children = self.mutation(children)
            self.population.append(mutation_children)

        return self.best_clique

    def is_better(self, cur_clique):
        if self.best_clique_size == 0:
            return cur_clique
        else:
            return cur_clique[1] > self.best_clique_weight

    def is_valid(self, clique, v):
        """
        :param clique: current clique
        :param v: vertex that we want to add to the clique
        :return:  bool -  if the addition of vertex v is legal (if v connected to all the vertex in current clique)
        """
        for other_vertex in clique:
            if other_vertex == -1:
                continue
            friends = self.graph[other_vertex].keys()
            if v not in friends:
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
        index_of_small = p1_degree_list.index(min(filter(lambda x: x > 0, p1_degree_list)))
        p1_empty_index.append(index_of_small)
        child1[index_of_small] = -1

        for i in p1_empty_index:
            candidate_v = parent2[i]
            if self.is_valid(child1, candidate_v):
                child1[i] = candidate_v
        return child1

    def crossover(self, best_chromosomes):
        after_crossover = []
        for i in range(0, len(best_chromosomes) - 2):
            after_crossover.append(self.fill_empty_crossover(best_chromosomes[i], best_chromosomes[i + 1]))
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
        for i in range(self.POPULATION_SIZE):
            chromosome = self.create_chromosome()
            initial_population.append(chromosome)
        self.population = initial_population

    @staticmethod
    def evaluate_chromosome(chromosome):
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
