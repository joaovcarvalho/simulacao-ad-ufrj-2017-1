from math import log, inf
from random import random

MU = 5 # decontamination/healing rate
GAMMA = 1.1 # internal infection rate
LAMBDA = 2 # external infection rate

N = 20 # population size

EXPERIMENTS = 10 # number of snapshots of the system

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

# creates 20 individuals at the 'S'(0) state, who can go to the 'I'(1), but initially are staying "forever" at 'S'
# in this case, the destiny and dt attributes of the initial population do not matter, since they are randomly initialized afterwards
state_nodes = [State(0,1,inf) for i in range(N)] # 0: 'S', 1: 'I'

# exponential distributed random number generator with rate 'rate'
def inverse_exp(rate):
    return -log(1-random())/rate

# multiplicative model
def n(_lambda, gamma, number_of_infected):
    return 1/(_lambda*gamma**number_of_infected)

# exponential distributed random number generator with a multiplicative rate
def inverse_exp_n(_lambda, gamma, number_of_infected):
    return -log(1-random())/(_lambda*gamma**number_of_infected)

# determines the amount of infected in the population
def get_number_of_infected(state_nodes):
    count = 0
    for e in state_nodes:
        if e.origin != 0:
            count += 1
    return count


# critical part of the simulation and it's not generic at all. This part has to be completely changed if, for example, a new state node
# were to be added to the simulation model
snapshots = []
for exp in range(EXPERIMENTS):
    for i in range(N):
        node = state_nodes[i]
        # sets the origin from the second node and so forth. Since there are only two nodes, the origin of the current
        # node is always going to be the destiny of the previous node
        if exp > 0:
            node.origin = snapshots[exp - 1][i].destiny

        # if you are at state 'S'(0) you can only go to state 'I'(1)
        if node.origin == 0:
            node.destiny = 1
            node.dt = inverse_exp_n(LAMBDA, GAMMA, get_number_of_infected(state_nodes))
        # if you are at state 'I'(1) you can only go to state 'S'(0)
        elif node.origin == 1:
            node.destiny = 0
            node.dt = inverse_exp(MU)

    # workaround to make copies of the objects
    state_nodes_clone = []
    for e in state_nodes:
        state_nodes_clone += [e.clone()]

    snapshots += [state_nodes_clone]

#tests with the first individual of the population
#TODO make this part generic for every individual

tS0 = 0
tI0 = 0
t = 0

# Output format
# (State 1 -> State 2, time t)
# The individual remains an amount of time t in the State 1 before transitioning to State 2
print('Tests with the first individual of the population')
for e in snapshots:
    strBuff = ""
    strBuff += str(e[0]) + " "
    if e[0].origin == 0:
        tS0 += e[0].dt
    if e[0].origin == 1:
        tI0 += e[0].dt
    t += e[0].dt
    print(strBuff)

print("S0 {:.2f}% ".format(tS0*100 / t)) # percentage of time the first individual remains susceptible to infection
print("I0 {:.2f}% ".format(tI0*100 / t)) # percentage of time the first individual is infected
