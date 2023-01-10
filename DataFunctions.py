import networkx as nx

def createGraph():
    G = nx.Graph()
    G.add_node(1)
    G.add_node(2)
    G.add_node(3)
    G.add_node(4)
    G.add_node(5)
    G.add_node(6)
    G.add_node(7)
    G.add_node(8)
    G.add_node(9)

    G.add_edges_from([(1, 4), (1, 5), (1, 7), (1, 8)])
    G.add_edges_from([(2, 4), (2, 6), (2, 9), (2, 7)])
    G.add_edges_from([(3, 4), (3, 7), (3, 9)])
    G.add_edges_from([(5, 2), (5, 9)])
    return G

