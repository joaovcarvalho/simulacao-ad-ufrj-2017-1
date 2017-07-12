# Ooopa
# in English: Whooops
from random import randint


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


states = ['S', 'I', 'V', 'D']

MU = 1  # I -> S
LAMBDA = 1  # S -> I
ALPHA = 1  # S -> V
BETA = 1  # I -> D


def get_node_destiny(node):
    if node.origin == 0:
        node.destiny = __get_random_node_destiny(LAMBDA / (LAMBDA + ALPHA), [1, 2])
    elif node.origin == 1:
        node.destiny = __get_random_node_destiny(MU / (MU + BETA), [0, 3])
    elif node.origin == 2:
        node.destiny = 2
    elif node.origin == 3:
        node.destiny = 3


def __get_random_node_destiny(natural_probability, possible_states):
    percent_prob = natural_probability * 100
    print("Prob p (%): {}\n".format(percent_prob))

    random_event = randint(0, 100)
    print("Random number: {}\n".format(random_event))

    if random_event < percent_prob:
        return possible_states[0]
    else:
        return possible_states[1]


test_node = State(0, 0, 0)
print("Origin: {}\n".format(states[test_node.origin]))
get_node_destiny(test_node)
print("Destiny: {}\n".format(states[test_node.destiny]))