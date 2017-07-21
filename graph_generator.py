from random import randint

def get_random_graph(number_of_nodes):
    list_of_edges = []
    for i in range(number_of_nodes):
        list_of_edges += [[]]

    for i in range(number_of_nodes):
        for j in range(number_of_nodes):
            if i == j:
                continue

            if randint(0,100) < 50:
                list_of_edges[i] += [j]
                list_of_edges[j] += [i]
                list_of_edges[i] = list(set(list_of_edges[i]))
                list_of_edges[j] = list(set(list_of_edges[j]))

    return list_of_edges
