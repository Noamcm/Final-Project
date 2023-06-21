import itertools
import math
import random
import time
import WriteToCsv


class AntColony:
    def __init__(self, graph, d,level_name, algo_types,n_ants,pheromone_deposit,evaporation_rate):
        self.graph = graph
        self.d = d
        self.level = level_name
        self.algo = algo_types
        self.N_ANTS = n_ants
        self.PHEROMONE_DEPOSIT = pheromone_deposit
        self.EVAPORATION_RATE = evaporation_rate

    def solve(self):
        bestClique = self.ant_colony_optimization(self.graph, self.d)
        return bestClique

    def update_pheromone_matrix(self,pheromone_trail, best_clique):
        for i, j in itertools.combinations(best_clique, 2):
            if (i, j) in pheromone_trail:
                pheromone_trail[(i, j)] = (1 - self.EVAPORATION_RATE) * pheromone_trail[(i, j)] + self.PHEROMONE_DEPOSIT
            else:
                pheromone_trail[(j, i)] = (1 - self.EVAPORATION_RATE) * pheromone_trail[(j, i)] + self.PHEROMONE_DEPOSIT


    def ant_colony_optimization(self,graph, d):
        timeout = time.time() + 2  # 2 sec
        MAX_CLIQUE_SIZE = len(d.keys())
        # Initialize the pheromone trail for all edges
        pheromone_trail = {(i, j): 1.0 for i, j in graph.edges}

        best_clique = set()
        best_clique_size = 0
        i=0

        # Repeat the algorithm for n_iterations
        while time.time() < timeout:
            worst = set()
            local_best_clique = set()
            local_best_clique_size = 0
            index = 1
            for _ in range(self.N_ANTS):
                if time.time() > timeout:
                    break
                clique = _generate_clique(graph, d, pheromone_trail)

            # Evaluate the quality of each clique and store the best
                index += 1
                if len(clique) > local_best_clique_size:
                    local_best_clique = clique
                    local_best_clique_size = len(clique)
                    if local_best_clique_size == MAX_CLIQUE_SIZE:
                        best_clique = local_best_clique
                        best_clique_size = local_best_clique_size
                        return best_clique

            # Update the pheromone trail for the edges in the best clique
            self.update_pheromone_matrix(pheromone_trail, local_best_clique)
            if local_best_clique_size > best_clique_size:
                best_clique = local_best_clique
                best_clique_size = local_best_clique_size
            i+=1
        return best_clique


def _generate_clique(graph, d, pheromone_trail):
    clique = set()
    shuffledKeysList = list(d.keys())
    random.shuffle(shuffledKeysList)

    # choose random root
    for empType in shuffledKeysList:
        empFromSameTypeList = d[empType]
        v = _select_next_vertex(graph, empFromSameTypeList, clique, d, pheromone_trail)
        if v is None:
            continue
        clique.add(v)
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
    next_vertex = random.choices(list(optional_vertices_score_dict.keys()), weights=list(optional_vertices_score_dict.values()), k=1)[0]
    return next_vertex

def order_by_lottery(g, same_type_vertices, clique, d, pheromone_trail):
    """
    Select the next vertex to add to the clique using a combination of pheromone trail information
    and heuristics (e.g. degree of the vertex)
    """
    optional_vertices = remove_irrelevant_vertices(g, same_type_vertices, d, clique)
    if len(optional_vertices) == 0:
        return None

    optional_vertices_score_dict = {i: neighbor_score(i, pheromone_trail, clique) for i in optional_vertices}
    lottery_list = []
    for key in optional_vertices_score_dict.keys():
        num_of_tickets = optional_vertices_score_dict[key]
        lottery_list.extend(int(num_of_tickets) * [math.ceil(key)])
    if len(lottery_list) > 1:
        random.shuffle(lottery_list)
    ordered_emp_list = list(dict.fromkeys(lottery_list))

    return ordered_emp_list