import random


def createChromosome(types_emp_id_dict):
    chromosome = []
    for key in types_emp_id_dict.keys():
        value = random.choice(types_emp_id_dict[key])
        chromosome.append(value)
    print(chromosome)
    return list(chromosome)


def createPopulation(types_emp_id_dict):
    initial_population = []
    POPULATION_SIZE = 10

    for i in range(POPULATION_SIZE):
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


def solve(graph, types_emp_id_dict):
    while True:
        population = createPopulation(types_emp_id_dict)
        print(population)
        grades = evaluatePopulation(graph, population)

        break
    return None
