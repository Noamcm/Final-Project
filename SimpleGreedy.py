import random


def isBetter(cur_clique, best_clique):
    """
        :param cur_clique - list of nodes
        :param best_clique - list of nodes
        :return: true -  if cur_clique is better
                 false - if best_clique is better
        """
    return len(cur_clique) > len(best_clique)

def isValid(graph, clique, v):
    """
    :param graph: nx graph
    :param clique: current clique
    :param v: vertex that we want to add to the clique
    :return:  bool -  if the addition of vertex v is legal (if v connected to all the vertex in current clique)
    """
    for other_vertex in clique:
        if v not in graph[other_vertex].keys():
            return False
    return True

def getBestNode(graph, clique, v_friends):
    """
    :param graph: nx graph
    :param clique: current clique
    :param v_friends: list of nodes that connected to current vertex
    :return: the function choose the best next valid vertex - to add the clique
    """
    for v in v_friends:
        if isValid(graph, clique, v):
            return v
    return None

def getGroupListByEmpID(types_emp_id_dict, val):
    """
        :param types_emp_id_dict: { type1 : [empID_1, empID_2, empID_3], type2 : [empID_4, empID_5, empID_6]...}
        :param val: employee ID
        :return: values: list of the ID's of all the employees from the type of the input employee ID.
                example - input: val = empID_4
                          output: values = [empID_5, empID_6]
    """
    for key in types_emp_id_dict:
        values = list(types_emp_id_dict[key])
        if values.__contains__(val):
            values.remove(val)
            return values
    return None

def removeSameTypeEmployees(graph, types_emp_id_dict, node):
    """
    :param graph: nx graph
    :param types_emp_id_dict: { type1 : [empID_1, empID_2, empID_3], type2 : [empID_4, empID_5, empID_6]...}
    :param node: new vertex
    the function remove all the employees with the same type of the new vertex from the graph
     - so that we don't choose them later.
    """
    nodes_to_remove = getGroupListByEmpID(types_emp_id_dict, node)
    if nodes_to_remove:
        for node in nodes_to_remove:
            graph.remove_node(node)

def solve(graph, types_emp_id_dict):
    """
    :param graph: nx graph
    :param types_emp_id_dict: { type1 : [empID_1, empID_2, empID_3], type2 : [empID_4, empID_5, empID_6]...}
    :return: best_clique: list of the vertex of the best max clique we found by "Greedy Algorithm"
    """
    NUM_OF_ITER = 10000
    best_clique = []

    # Greedy Algorithm loop
    for i in range(NUM_OF_ITER):
        # copy the original graph & dict
        g = graph.copy()
        dict_copy = types_emp_id_dict.copy()  # {1: [1, 2 ,3], 2: [4, 5, 6]..}
        cur_clique = []

        # choose random root
        v = random.choice(list(g.nodes()))
        v_friends = g[v].keys()
        cur_clique.append(v)

        # as long as possible - add more vertex to the clique
        while len(v_friends) > 0:
            removeSameTypeEmployees(g, dict_copy, v)
            v = getBestNode(g, cur_clique, v_friends)

            if v:
                v_friends = g[v].keys()
                cur_clique.append(v)

            else:
                break
        print("iter " + str(i) + " - Current Clique: " + str(cur_clique))
        # print(cur_clique)
        # See if the current team is the best we've found so far
        if isBetter(cur_clique, best_clique):
            best_clique = cur_clique
    print("***** Best Clique: " + str(best_clique) + " *****")
    print("***** Solution length: " + str(len(best_clique)) + " *****")
    return best_clique
