import random
import time


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
    return child1, child2

def crossover(best_Chromosomes):
    # crossover_type = 'uniform_crossover'
    after_crossover = []
    for i in range(0, len(best_Chromosomes)-1):
        after_crossover.append(uniform_crossover(best_Chromosomes[i], best_Chromosomes[i+1]))
    return after_crossover

def createChromosome(types_emp_id_dict):
    chromosome = []
    for key in types_emp_id_dict.keys():
        value = random.choice(types_emp_id_dict[key])
        chromosome.append(value)
    print(chromosome)
    return list(chromosome)


def createPopulation(types_emp_id_dict, population_size):
    initial_population = []

    for i in range(population_size):
        chromosome = createChromosome(types_emp_id_dict)
        initial_population.append(chromosome)
    return initial_population


def evaluateChromosome(graph, chromosome):
    grade = 0
    num_of_friends_in_team = 0
    for i in range(0, len(chromosome)):
        for j in range(i, len(chromosome)):
            vi_id = chromosome[i]
            vj_id = chromosome[j]
            has_edge = graph.has_edge(vi_id, vj_id)
            if has_edge:
                num_of_friends_in_team += 1
    grade = num_of_friends_in_team
    return grade


def evaluatePopulation(graph, population):
    grades = []
    for chromosome in population:
        grade = evaluateChromosome(graph, chromosome)
        grades.append(grade)
    return grades


def Mutation(childrens):
    pass


def solve(graph, types_emp_id_dict):
    ITERS = 10
    POPULATION_SIZE = 100
    BEST_N_AMOUNT = 10
    best_clique = []
    timeout = time.time() + 2  # 2 sec

    for i in range(ITERS):
        if time.time() > timeout:
            break
        population = createPopulation(types_emp_id_dict, POPULATION_SIZE)
        print(population)
        grades = evaluatePopulation(graph, population)
        print("before: ")
        print(grades)

        best_n_index = sorted(range(len(grades)), key=lambda i: grades[i])[-BEST_N_AMOUNT:]
        print(best_n_index)
        crossover_list = []
        for i in best_n_index:
            crossover_list.append(population[i])
        childrens = crossover(crossover_list)
        # mutation_childrens = Mutation(childrens)
        population = childrens
        grades = evaluatePopulation(graph, population)
        print("after: ")
        print(grades)


        break
    return best_clique
