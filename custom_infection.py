import sys
import math
from math import log, inf, sqrt
from random import random
from pprint import PrettyPrinter
import matplotlib.pyplot as plt
from random import randint
import graph_generator

pp = PrettyPrinter(indent=4)

MU = 1 # decontamination/healing rate I -> S
LAMBDA = 10 # external infection rate S -> I
GAMMA = 1
ALPHA = 1  # S -> V
BETA = 0.01  # I -> D

def get_node_destiny(node):
    if node.origin == 0:
        return __get_random_node_destiny(LAMBDA / (LAMBDA + alpha), [1, 2])
    elif node.origin == 1:
        return __get_random_node_destiny(MU / (MU + BETA), [0, 3])
    elif node.origin == 2:
        return 2
    elif node.origin == 3:
        return 3

def get_time_until_destinty(node, alpha, num_infected):
    if node.origin == 2 or node.origin == 3:
        return float('inf')

    if node.origin == 0:
        if node.destiny == 1:
            return inverse_exp_n(LAMBDA, GAMMA, num_infected)
        if node.destiny == 2:
            return inverse_exp(alpha)
    if node.origin == 1:
        if node.destiny == 0:
            return inverse_exp(MU)
        if node.destiny == 3:
            return inverse_exp(BETA)

def __get_random_node_destiny(natural_probability, possible_states):
    percent_prob = natural_probability * 100
    random_event = randint(0, 100)

    if random_event < percent_prob:
        return possible_states[0]
    else:
        return possible_states[1]


EXPERIMENTS = 30 # number of snapshots of the system

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
        return "({} -> {}, {})".format(self.getState(), self.getDestinyState(), self.dt)

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
            dict[node.origin] = dict[node.origin] + 1
        else:
            dict[node.origin] = 1
    return dict

def simulation(N,alpha, MU, LAMBDA0, EXPERIMENTS):
    graph = graph_generator.get_random_graph(N)
    LAMBDA = LAMBDA0/N
    # critical part of the simulation and it's not generic at all. This part has to be completely changed if, for example,
    # a new state node were to be added to the simulation model
    # snapshots = []
    areas = []
    for exp in range(EXPERIMENTS):
        area = 0.0
        number_of_infected = 0
        # creates N individuals at the 'S'(0) state, who can go to the 'I'(1), but initially are staying "forever" at 'S'
        # in this case, the destiny and dt attributes of the initial population do not matter,
        # since they are randomly initialized afterwards
        state_nodes = [State(0,1,0,i) for i in range(N)] # 0: 'S', 1: 'I'

        current_time = 0
        # print(state_nodes)

        while current_time < 1000:
            # pp.pprint(current_time)
            node = state_nodes[0]

            if(node.dt == float('inf')):
                current_time = 500
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

            for i in range(1,N):
                state_nodes[i].dt -= node.dt

            node.destiny = get_node_destiny(node)
            node.dt = get_time_until_destinty(node, alpha, get_number_of_infected(node.id_node, state_nodes, graph))

            state_nodes = sorted(state_nodes, key=lambda event: event.dt, reverse=False)

        areas += [area/current_time]

    return areas

vec_N = range(30,60,10)

v=0.1
vec_alpha = [v+i*0.5 for i in range(5)]

num_of_total_iterations = len(vec_N) * len(vec_alpha)
current_iteration = 1
for alpha in vec_alpha:
    iN = 0

    averages = (len(vec_N)) * [None]
    std_deviation = (len(vec_N)) * [0]
    conf_interval = []

    for N in vec_N:
        sys.stdout.flush()
        print("Interaction {0} / {1}".format(current_iteration, num_of_total_iterations))
        current_iteration = current_iteration + 1
        # print(gamma)
        # print(N)
        # print()
        X = simulation(N, alpha, MU, LAMBDA, EXPERIMENTS)
        # pp.pprint(X)
        averages[iN] = mean(X)/N
        for x in X:
            std_deviation[iN] += (((x/N) - averages[iN])**2)/(N-1)

        # conf_interval += [( averages[iN] - 1.96*sqrt(std_deviation[iN])/sqrt(N), averages[iN] + 1.96*sqrt(std_deviation[iN])/sqrt(N) )]
        conf_interval += [1.96*sqrt(std_deviation[iN])/sqrt(N)]
        iN += 1

    # pp.pprint(averages)
    ## Plotting values
    # Choose the values to plot
    plt.plot(vec_N, averages, linewidth=1, label=r'$\alpha =$'+ str(alpha))
    plt.errorbar(vec_N, averages, conf_interval, linestyle='None', marker='^')

## Plotting options
# Choose the corret legend, according values plotted
plt.xlabel('number of nodes in the network')
plt.ylabel('probability of tagged node is infected')
#plt.ylabel('expected number of contamined nodes')

#plt.xlim([0,40])
#plt.ylim([0,2])
plt.grid()

## Choose one position
#plt.legend(loc='upper right')
#plt.legend(loc='center right')
plt.legend(loc='lower right')

plt.show()
