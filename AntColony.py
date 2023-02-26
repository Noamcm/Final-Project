#
# INITIAL_PHEROMONE_VALUE = 1
# NUM_VERTICES = 10
#
# def init_pheromone_matrix():
#     pheromone_matrix = []
#     for i in range(1, NUM_VERTICES):
#         pheromone_matrix[i] = []
#         for j in range(1, NUM_VERTICES):
#             pheromone_matrix[i][j] = INITIAL_PHEROMONE_VALUE
#     return pheromone_matrix
#
#
# def calculate_probability(j, pheromone_matrix, current_clique):
#   # Calculate the probability of choosing vertex j based on the pheromone matrix and the current clique
#   # The probability is calculated using the formula:
#   # p(j) = (tau(j) * eta(j)) / (sum of (tau(k) * eta(k)) for all unvisited vertices k)
#   # tau(j) is the pheromone value for vertex j
#   # eta(j) is the heuristic value for vertex j (a measure of the desirability of adding vertex j to the clique)
#   p = (pheromone_matrix[j] * heuristic_value(j, current_clique)) / sum_of_probabilities(pheromone_matrix,
import itertools
import random
import time

N_ANTS = 300
N_ITERATIONS = 300000
PHEROMONE_DEPOSIT = 5
EVAPORATION_RATE = 0.9

def solve(graph, d):
    bestClique = ant_colony_optimization(graph, d)
    return bestClique

def update_pheromone_matrix(pheromone_trail, best_clique):
    for i, j in itertools.combinations(best_clique, 2):
        if (i, j) in pheromone_trail:
            pheromone_trail[(i, j)] = (1 - EVAPORATION_RATE) * pheromone_trail[(i, j)] + PHEROMONE_DEPOSIT
        else:
            pheromone_trail[(j, i)] = (1 - EVAPORATION_RATE) * pheromone_trail[(j, i)] + PHEROMONE_DEPOSIT
def ant_colony_optimization(graph, d):
    timeout = time.time() + 2  # 2 sec

    MAX_CLIQUE_SIZE = len(d.keys())
    # Initialize the pheromone trail for all edges
    pheromone_trail = {(i, j): 1.0 for i, j in graph.edges}

    best_clique = set()
    best_clique_size = 0

    # Repeat the algorithm for n_iterations
    for iteration in range(N_ITERATIONS):
        # Generate n_ants candidate solutions (cliques)
        cliques = [_generate_clique(graph, d, pheromone_trail) for _ in range(N_ANTS)]

        index = 1
        # Evaluate the quality of each clique and store the best
        for clique in cliques:
            if time.time() > timeout:
                return best_clique
            # print("clique " + str(index) + ": " + str(clique))
            index+=1
            if len(clique) > best_clique_size:
                best_clique = clique
                best_clique_size = len(clique)
                if best_clique_size == MAX_CLIQUE_SIZE:
                    return best_clique

        # Update the pheromone trail for the edges in the best clique
        update_pheromone_matrix(pheromone_trail, best_clique)
    #     print("len best_clique: " + str(len(best_clique)))
    # print("best_clique: " + str(best_clique))
    return best_clique

def _generate_clique(graph, d, pheromone_trail):
    clique = set()
    shuffledKeysList = list(d.keys())
    random.shuffle(shuffledKeysList)

    # choose random root
    for empType in shuffledKeysList:
        empFromSameTypeList = d[empType]
        v = _select_next_vertex(graph, empFromSameTypeList, clique, d, pheromone_trail)

        if isValid(graph, clique, v):
            clique.add(v)

    # current_vertex = random.choice(list(graph.nodes()))
    # clique.add(current_vertex)
    #
    # while True:
    #     neighbors = graph[current_vertex]
    #     next_vertex = _select_next_vertex(graph, neighbors, clique, d, pheromone_trail)
    #     if next_vertex is None:
    #         break
    #
    #     clique.add(next_vertex)
    #     current_vertex = next_vertex

    return clique


def neighbor_score(new_v, pheromone_trail, clique):
    grade = 1
    for v in clique:
        v_tuple = (v, new_v)
        if v_tuple not in pheromone_trail:
            v_tuple = (new_v, v)
        grade *= pheromone_trail[v_tuple]
    return grade

def isValid(graph, clique, new_v):
    """
    :param graph: nx graph
    :param clique: current clique
    :param v: vertex that we want to add to the clique
    :return:  bool -  if the addition of vertex v is legal (if v connected to all the vertex in current clique)
    """
    for v in clique:
        if new_v not in graph[v]:
            return False
    return True

# def remove_irrelevant_neighbors(g, neighbors, d, clique):
#     updated_neighbors = []
#     for n in neighbors:
#         valid_neighbor = True
#
#         # The clique already contains a member from the same "employee type"
#         values = []
#         for i in d.keys():
#             if d[i].__contains__(n):
#                 values = d[i]
#         if any(i in clique for i in values):
#             break
#
#         # The member is not a friend of one of the members of the current clique
#         if not isValid(g, clique, n):
#             break
#
#         if valid_neighbor:
#             updated_neighbors.append(n)
#     return updated_neighbors
# def _select_next_vertex(g, neighbors, clique, d, pheromone_trail):
#     """
#     Select the next vertex to add to the clique using a combination of pheromone trail information
#     and heuristics (e.g. degree of the vertex)
#     """
#     neighbors = remove_irrelevant_neighbors(g, neighbors, d, clique)
#     if len(neighbors) == 0:
#         return None
#
#     neighbors_score_dict = {i: neighbor_score(i, pheromone_trail, clique) for i in neighbors}
#     neighbors_score_dict_items = list(neighbors_score_dict.items())
#     random.shuffle(neighbors_score_dict_items)
#     neighbors_score_dict = dict(neighbors_score_dict_items)
#     # print(neighbors_score_dict)
#     return max(neighbors_score_dict, key=neighbors_score_dict.get)


def remove_irrelevant_vertices(g, same_type_vertices, d, clique):
    updated_neighbors = []
    for n in same_type_vertices:
        # The member is not a friend of one of the members of the current clique
        if not isValid(g, clique, n):
            continue
        updated_neighbors.append(n)
    return updated_neighbors
def _select_next_vertex(g, same_type_vertices, clique, d, pheromone_trail):
    """
    Select the next vertex to add to the clique using a combination of pheromone trail information
    and heuristics (e.g. degree of the vertex)
    """
    optional_vertices = remove_irrelevant_vertices(g, same_type_vertices, d, clique)
    if len(optional_vertices) == 0:
        return None

    optional_vertices_score_dict = {i: neighbor_score(i, pheromone_trail, clique) for i in optional_vertices}
    optional_vertices_score_dict_items = list(optional_vertices_score_dict.items())
    random.shuffle(optional_vertices_score_dict_items)
    optional_vertices_score_dict = dict(optional_vertices_score_dict_items)
    # print(neighbors_score_dict)
    return max(optional_vertices_score_dict, key=optional_vertices_score_dict.get)