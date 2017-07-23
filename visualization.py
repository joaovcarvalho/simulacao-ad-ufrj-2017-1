import csv
import math

list_of_states = []
time = 0
experiment = 0

def load_experiment(i):
    global time
    global list_of_states
    list_of_states = []
    time = 0
    print('Next experiment: ' + str(i))
    with open('experiments/iteration_53/experiment_{0}.csv'.format(i), 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=' ')
        for row in reader:
            list_of_states += [(row[0], row[1:])]

def setup():
    global experiment
    load_experiment(experiment)
    size(800, 800)

def draw_node(node,x,y):
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

    ellipse(x, y, 50, 50)


def draw():
    global time
    global experiment
    states = list_of_states[time][1]

    translate(400, 400)
    background(255)

    teta = 0
    if 360 / len(states) < 20:
        teta_step = 30
    else:
        teta_step = 360 / len(states)

    radious = 150

    for i,node in enumerate(states):
        x = (radious)*math.cos(teta * math.pi / 180)
        y = (radious)*math.sin(teta * math.pi / 180)

        if teta > 360:
            radious += 50
            teta = 0

        teta += teta_step
        draw_node(node,x,y)

    if time == len(list_of_states) - 1:
        experiment += 1
        load_experiment(experiment)
    else:
        time += 1
