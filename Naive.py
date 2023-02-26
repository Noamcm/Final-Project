import itertools
import networkx as nx

def maximum_clique(graph, d):
    clique = []

    groups_lists = list(d.values())
    combinations = list(itertools.product(*groups_lists))
    print(len(combinations))

    for clique_candidate in combinations:
        if not is_valid_clique(graph, clique_candidate):
            continue
        if len(clique_candidate) > len(clique):
            clique = clique_candidate
    return clique

def solve(graph, d):
    d_with_none = dict(d)
    for key in d_with_none:
        d_with_none[key].append(-1)
    # clique = maximum_clique(graph, d_with_none)
    clique = mx(graph)
    return clique

def is_valid_clique(graph, clique):
    for v in clique:
        for other_v in clique:
            if v == -1 or other_v == -1 or v == other_v:
                continue
            if v not in graph[other_v].keys():
                return False
    return True


def mx(graph):
    print("mx")
    best_clique = nx.make_max_clique_graph(graph)
    clique_lists = list(nx.find_cliques(graph))
    best_clique = max(clique_lists, key=len)
    print(best_clique)
    print(len(best_clique))
    return best_clique