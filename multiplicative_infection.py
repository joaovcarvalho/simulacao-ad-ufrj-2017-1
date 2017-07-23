from math import log, inf, sqrt
from random import random
from pprint import PrettyPrinter
import matplotlib.pyplot as plt
import numpy as np

pp = PrettyPrinter(indent=4)

MU = 1 # decontamination/healing rate
LAMBDA = 10 # external infection rate

EXPERIMENTS = 15 # number of snapshots of the system

states = ['S', 'I']

class State:
    def __init__(self, origin, destiny, dt):
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

# exponentially distributed random number generator with a additive rate
def inverse_exp_add(_lambda, gamma, number_of_infected):
    return -log(1-random())/(_lambda + number_of_infected*gamma)

# exponentially distributed random number generator with a multiplicative rate
def inverse_exp_n(_lambda, gamma, number_of_infected):
    return -log(1-random())/(_lambda*gamma**number_of_infected)

# determines the amount of infected in the population
def get_number_of_infected(state_nodes):
    count = 0
    for e in state_nodes:
        if e.origin == 1:
            count += 1
    return count



def simulation(N,GAMMA, MU, LAMBDA0, EXPERIMENTS):
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
        state_nodes = [State(0,1,0) for i in range(N)] # 0: 'S', 1: 'I'

        current_time = 0
        # print(state_nodes)

        while current_time < 500:
            # pp.pprint(current_time)
            node = state_nodes[0]
            # sets the origin from the second node and so forth. Since there are only two nodes, the origin of the current
            # node is always going to be the destiny of the previous node
            node.origin = node.destiny
            # if you are at state 'S'(0) you can only go to state 'I'(1)
            passed_time = node.dt
            current_time += node.dt

            number_of_infected = get_number_of_infected(state_nodes)
            area += number_of_infected * passed_time

            for i in range(1,N):
                state_nodes[i].dt -= node.dt

            if node.origin == 0:
                node.destiny = 1
                node.dt = inverse_exp_n(LAMBDA, GAMMA, get_number_of_infected(state_nodes))
            # if you are at state 'I'(1) you can only go to state 'S'(0)
            elif node.origin == 1:
                node.destiny = 0
                node.dt = inverse_exp(MU)

            state_nodes = sorted(state_nodes, key=lambda event: event.dt, reverse=False)
            # pp.pprint(state_nodes)

        areas += [area/current_time]

    return areas

vec_N = range(10,60,4)

v=0.1
vec_gamma = [v+i*0.5 for i in range(6)]
for gamma in vec_gamma:
    iN = -1

    averages = (len(vec_N)) * [None]
    std_deviation = (len(vec_N)) * [0]
    conf_interval = []

    for N in vec_N:
        # print(gamma)
        # print(N)
        # print()
        iN += 1
        X = simulation(N, gamma, MU, LAMBDA, EXPERIMENTS)
        averages[iN] = mean(X)/N
        for x in X:
            std_deviation[iN] += (( (x/N) - averages[iN])**2)/(N-1)

        # conf_interval += [( averages[iN] - 1.96*sqrt(std_deviation[iN])/sqrt(N), averages[iN] + 1.96*sqrt(std_deviation[iN])/sqrt(N) )]
        conf_interval += [1.96*sqrt(std_deviation[iN])/sqrt(N)]

    # pp.pprint(conf_interval)
    ## Plotting values
    # Choose the values to plot
    plt.plot(vec_N, averages, linewidth=1, label=r'$\gamma =$'+ str(gamma))
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
plt.legend(loc='center right')
#plt.legend(loc='lower right')

plt.show()

#plt.savefig('figuras/test.eps')
