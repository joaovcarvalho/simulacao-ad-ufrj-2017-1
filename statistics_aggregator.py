import csv
import math
import time
import pickle
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

list_of_states = []
experiment = 0
iteration = 10
graph = None

def load_experiment(experiment_index, iteration):
    global list_of_states
    global graph
    list_of_states = []

    # Loads graph
    with open('experiments/iteration_{0}/graph.pickle'.format(iteration), 'rb') as pickle_file:
        pickler = pickle.Unpickler(pickle_file)
        graph = pickler.load()

    # Loads experiment list of states
    with open('experiments/iteration_{0}/experiment_{1}.csv'.format(iteration,experiment_index), 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=' ')
        for row in reader:
            list_of_states += [(row[0], row[1:])]

def mean(_list):
    return sum(_list)/len(_list)

def count_nodes_by_state(state_nodes):
    dict = {}
    for node in state_nodes:
        if node in dict:
            dict[node] += 1
        else:
            dict[node] = 1
    return dict

def get_average_num_of_state(iteration, state_of_interest, num_experiments):
    areas = []
    for exp in range(num_experiments):
        load_experiment(exp, iteration)
        current_time = 0
        area = 0

        for state in list_of_states:
            nodes_grouped_by_origin = count_nodes_by_state(state[1])
            number_of_interest = nodes_grouped_by_origin.get(state_of_interest, 0)
            passed_time = float(state[0])
            current_time += passed_time

            area += number_of_interest * passed_time
        areas += [area/current_time]
    return areas
