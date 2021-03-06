from random import randint

def get_random_graph(number_of_nodes):
    list_of_edges = []
    for i in range(number_of_nodes):
        list_of_edges += [[]]

    for i in range(number_of_nodes):
        for j in range(number_of_nodes):
            if i == j:
                continue

            if randint(0,100) < 5:
                list_of_edges[i] += [j]
                list_of_edges[j] += [i]
                list_of_edges[i] = list(set(list_of_edges[i]))
                list_of_edges[j] = list(set(list_of_edges[j]))

    return list_of_edges

def convert_to_matrix(list_of_edges):
    matrix = []
    for i,node_list in enumerate(list_of_edges):
        matrix += [[0 for j in range(len(list_of_edges))]]
        for edge in node_list:
            matrix[i][edge] = 1

    return matrix
