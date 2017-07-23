import sys
import math
from math import log, inf, sqrt
from random import random
from pprint import PrettyPrinter
import matplotlib.pyplot as plt
from random import randint
import graph_generator
import simulation

pp = PrettyPrinter(indent=4)

def mean(_list):
    return sum(_list)/len(_list)

MU = 1 # decontamination/healing rate I -> S
LAMBDA = 10 # external infection rate S -> I
GAMMA = 1 # internal infection
ALPHA = 0.01  # S -> V
BETA = 20  # I -> D

TIME = 500
EXPERIMENTS = 10

vec_N = range(10,100,4)

v=0.1
vec_variable = [v+i*0.05 for i in range(3)]

num_of_total_iterations = len(vec_N) * len(vec_variable)
current_iteration = 1
for value in vec_variable:
    iN = 0

    averages = (len(vec_N)) * [None]
    std_deviation = (len(vec_N)) * [0]
    conf_interval = []

    for N in vec_N:
        sys.stdout.flush()
        print("Interaction {0} / {1}".format(current_iteration, num_of_total_iterations))
        # print(N,alpha,MU,LAMBDA,BETA,GAMMA, EXPERIMENTS,TIME, current_iteration)
        X = simulation.simulation(
            number_of_nodes=N,
            alpha=ALPHA,
            mu=MU,
            lambda0=LAMBDA,
            beta=value,
            gamma=GAMMA,
            num_experiments=EXPERIMENTS,
            stopping_time=TIME, 
            iteration=current_iteration)
        # pp.pprint(X)
        averages[iN] = mean(X)
        for x in X:
            std_deviation[iN] += ((x - averages[iN])**2)/(N-1)

        averages[iN] = averages[iN]/N
        std_deviation[iN] = std_deviation[iN]/N

        # conf_interval += [( averages[iN] - 1.96*sqrt(std_deviation[iN])/sqrt(N), averages[iN] + 1.96*sqrt(std_deviation[iN])/sqrt(N) )]
        conf_interval += [1.96*sqrt(std_deviation[iN])/sqrt(N)]
        iN += 1
        current_iteration = current_iteration + 1

    # pp.pprint(averages)
    ## Plotting values
    # Choose the values to plot
    plt.plot(vec_N, averages, linewidth=1, label=r'$\alpha =$'+ str(value))
    # plt.errorbar(vec_N, averages, conf_interval, linestyle='None', marker='^')

## Plotting options
# Choose the corret legend, according values plotted
plt.xlabel('number of nodes in the network')
plt.ylabel('probability of tagged node is dead')
#plt.ylabel('expected number of contamined nodes')

#plt.xlim([0,40])
#plt.ylim([0,2])
plt.grid()

## Choose one position
#plt.legend(loc='upper right')
#plt.legend(loc='center right')
plt.legend(loc='lower right')

plt.show()
