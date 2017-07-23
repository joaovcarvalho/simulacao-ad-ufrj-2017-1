import sys
import math
from math import log, inf, sqrt
from random import random
from pprint import PrettyPrinter
import matplotlib.pyplot as plt
from random import randint
import graph_generator
import csv
import os, errno

pp = PrettyPrinter(indent=4)


def get_node_destiny(node, lambdac, alpha, mu, beta):
    if node.origin == 0:
        return __get_random_node_destiny(lambdac / (lambdac + alpha), [1, 2])
        # return 1
    elif node.origin == 1:
        return __get_random_node_destiny(mu / (mu + beta), [0, 3])
        # return 0
    elif node.origin == 2:
        return 2
    elif node.origin == 3:
        return 3

def get_time_until_destinty(node, lambda0, alpha, mu, beta, gamma, num_infected):
    if node.origin == 2 or node.origin == 3:
        return float('inf')

    if node.origin == 0:
        if node.destiny == 1:
            return inverse_exp_n(lambda0, gamma, num_infected)
        if node.destiny == 2:
            return inverse_exp(alpha)
    if node.origin == 1:
        if node.destiny == 0:
            return inverse_exp(mu)
        if node.destiny == 3:
            return inverse_exp(beta)

def __get_random_node_destiny(natural_probability, possible_states):
    percent_prob = natural_probability * 100
    random_event = randint(0, 100)

    if random_event < percent_prob:
        return possible_states[0]
    else:
        return possible_states[1]


states = ['S', 'I', 'V', 'D']

class State:
    def __init__(self, origin, destiny, dt, id_node):
        self.id_node = id_node
        self.origin = origin # where I am
        self.destiny = destiny # where I'm going to
        self.dt = dt # amount of time I'm going to spend at 'origin'

    def getState(self):
        return states[self.origin]

    def getDestinyState(self):
        return states[self.destiny]

    def __str__(self):
        # return "({0} -> {1}, {2:.2f})".format(self.getState(), self.getDestinyState(), self.dt)
        return "{0}".format(self.getState(), self.getDestinyState(), self.dt)

    def __repr__(self):
        return self.__str__()

    def clone(self):
        return State(self.origin, self.destiny, self.dt)

def mean(_list):
    return sum(_list)/len(_list)

# exponentially distributed random number generator with rate 'rate'
def inverse_exp(rate):
    return -log(1-random())/rate

# multiplicative model
def n(_lambda, gamma, number_of_infected):
    return 1/(_lambda*gamma**number_of_infected)

# exponentially distributed random number generator with a multiplicative rate
def inverse_exp_n(_lambda, gamma, number_of_infected):
    return -log(1-random())/(_lambda*gamma**number_of_infected)

# exponentially distributed random number generator with an additive rate
def inverse_exp_add(_lambda, gamma, number_of_infected):
    return -log(1-random())/(_lambda + number_of_infected*gamma)

# determines the amount of infected in the population
def get_number_of_infected(id_node, state_nodes, graph):
    count = 0
    list_of_edges = graph[id_node]
    for edge in list_of_edges:
        for state in state_nodes:
            if state.id_node == edge:
                if state.origin == 1:
                    count += 1
    return count

def count_nodes_by_state(state_nodes):
    dict = {}
    for node in state_nodes:
        if node.origin in dict:
            dict[node.origin] += 1
        else:
            dict[node.origin] = 1
    return dict

def simulation(number_of_nodes,alpha, mu, lambda0,beta,gamma, num_experiments, stopping_time, iteration):
    graph = graph_generator.get_random_graph(number_of_nodes)
    lambdan = lambda0/number_of_nodes
    # critical part of the simulation and it's not generic at all. This part has to be completely changed if, for example,
    # a new state node were to be added to the simulation model
    # snapshots = []
    areas = []
    if not os.path.exists("experiments/iteration_" + str(iteration)):
        os.makedirs("experiments/iteration_" + str(iteration))

    for exp in range(num_experiments):
        with open('experiments/iteration_{0}/experiment_{1}.csv'.format(iteration, exp), 'w', newline='') as csvfile:
            log_writter = csv.writer(csvfile, delimiter=',',
                                    quotechar=' ', quoting=csv.QUOTE_MINIMAL)

            area = 0.0
            number_of_infected = 0
            # creates N individuals at the 'S'(0) state, who can go to the 'I'(1), but initially are staying "forever" at 'S'
            # in this case, the destiny and dt attributes of the initial population do not matter,
            # since they are randomly initialized afterwards
            state_nodes = [State(0,0,0,i) for i in range(number_of_nodes)]
            log_writter.writerow([0] + state_nodes )

            current_time = 0

            while current_time < stopping_time:
                node = state_nodes[0]

                if(node.dt == float('inf')):
                    current_time = stopping_time
                    break

                # sets the origin from the second node and so forth. Since there are only two nodes, the origin of the current
                # node is always going to be the destiny of the previous node
                node.origin = node.destiny
                # if you are at state 'S'(0) you can only go to state 'I'(1)
                passed_time = node.dt
                current_time += node.dt

                nodes_grouped_by_origin = count_nodes_by_state(state_nodes)
                number_of_interest = nodes_grouped_by_origin.get(3, 0)

                area += number_of_interest * passed_time

                for i in range(1,number_of_nodes):
                    state_nodes[i].dt -= node.dt

                node.destiny = get_node_destiny(node, lambdan, alpha, mu, beta)
                node.dt = get_time_until_destinty(node, lambdan, alpha, mu, beta, gamma, get_number_of_infected(node.id_node, state_nodes, graph))

                state_nodes = sorted(state_nodes, key=lambda event: event.dt, reverse=False)
                log_writter.writerow(["%.2f" % passed_time] + sorted(state_nodes, key=lambda event: event.id_node, reverse=False) )


            areas += [area/current_time]

    return areas
