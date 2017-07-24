import csv
import math
import time as time_lib
import pickle

list_of_states = []
time = 0
experiment = 0
iteration = 10
graph = None
nodes_position = []
width = 1200
height = 800

def load_experiment(i):
    global time
    global list_of_states
    global graph
    list_of_states = []
    time = 0
    print('Next experiment: ' + str(i))

    # Loads graph
    with open('experiments/iteration_{0}/graph.pickle'.format(iteration), 'rb') as pickle_file:
        pickler = pickle.Unpickler(pickle_file)
        graph = pickler.load()

    # Loads experiment list of states
    with open('experiments/iteration_{0}/experiment_{1}.csv'.format(iteration,i), 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=' ')
        for row in reader:
            list_of_states += [(row[0], row[1:])]

def setup():
    global experiment
    global nodes_position
    global width
    global height
    frameRate(12)
    load_experiment(experiment)
    nodes_position = [(0,0) for i in list_of_states]
    init_nodes_pos()
    size(width, height)

def get_node_degree(i):
    global graph
    return sum([j if j == 1 else 0 for j in graph[i] ])

def init_nodes_pos():
    global time
    global experiment
    global graph
    global width
    global height

    states = list_of_states[time][1]

    teta = 0
    if 360 / len(states) < 20:
        teta_step = 40
    else:
        teta_step = 360 / len(states)

    radious = 150

    list_of_indices = [
        i[0] for i in sorted(enumerate(states), key=lambda x: get_node_degree(x[0]))
    ]

    # Calculate nodes positions and store it
    for i in list_of_indices:
        if teta > 360:
            radious += 150
            teta_step -= 5
            teta = 0

        x = (radious)*math.cos(teta * math.pi / 180)
        y = (radious)*math.sin(teta * math.pi / 180)

        teta += teta_step

        nodes_position[i] = (x,y)

def draw_node(node,x,y, size=50):
    # S - > green
    if(node == 'S'):
        fill(0,255,0)
    # I - > red
    if(node == 'I'):
        fill(255,0,0)
    # V - > blue
    if(node == 'V'):
        fill(0,0,255)
    # D - > black
    if(node == 'D'):
        fill(0,0,0)

    ellipse(x, y, size, size)

def draw_edge(i,j):
    global nodes_position
    i_pos = nodes_position[i]
    j_pos = nodes_position[j]
    stroke(100)
    line(i_pos[0], i_pos[1], j_pos[0], j_pos[1])
    stroke(0)

def draw():
    global time
    global experiment
    global graph
    states = list_of_states[time][1]

    background(255)

    textSize(20)
    fill(0, 102, 153)
    text("Iteration: " + str(iteration), 20, 30)
    text("Experiment: " + str(experiment), 20, 60)
    text("Time: " + str(time), 20, 90)

    translate(width/2, height/2)
    scale(0.5)

    # Draw edges
    for i in range(len(graph)):
        for j in range(len(graph)):
            if graph[i][j] == 1:
                draw_edge(i,j)

    # Draw all nodes
    for i,node in enumerate(states):
        (x,y) = nodes_position[i]
        size = 50 + get_node_degree(i) * 4

        draw_node(node,x,y, size)

        if node == "D" or node == "V":
            fill(255)
        else:
            fill(0)

        text("{0}/{1}".format(get_node_degree(i), len(states)), x - 25,y)
        fill(0)


    # if is last time
    # then load next experiment
    if time == len(list_of_states) - 1:
        time_lib.sleep(2)
        experiment += 1
        load_experiment(experiment)
    else:
        time += 1
