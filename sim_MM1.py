from random import random
from math import log
from pprint import PrettyPrinter
import matplotlib.pyplot as plt

pp = PrettyPrinter(indent=4)

def exp(x,rate):
    return -log(1-x)/rate

def mean(_list):
    return sum(_list)/len(_list)    

mu = 0.5 # service rate
_lambda = 0.4 # queue rate
experiments = 10**2

#l_mu = [exp(random(), mu) for n in range(experiments)]
#l_lambda = [exp(random(), _lambda) for n in range(experiments)]

#print(l_mu)
#print(l_lambda)

class Event:
    def __init__(self, rate, time):
        self.rate = rate
        self.time = time
    def __eq__(self, other):
        return self.time == other.time
        
class QueueEvent(Event):
    def __init__(self, rate):
        Event.__init__(self, rate, exp(random(), rate))
    def __str__(self):
        return "(Q): {:.20f}".format(self.time)
    def __repr__(self):
        return self.__str__()
    def new(self):
        return QueueEvent(self.rate)

class ServiceEvent(Event):
    def __init__(self, rate):
        Event.__init__(self, rate, exp(random(), rate))
    def __str__(self):
        return "(S): {:.20f}".format(self.time)
    def __repr__(self):
        return self.__str__()
    def new(self):
        return ServiceEvent(self.rate)        
    

simulation_clock = 0
N = 0
total_events = 0
history = []

q = QueueEvent(_lambda)
s = ServiceEvent(mu)

event_list = [q]

while event_list and total_events < experiments:
    event = event_list.pop(0)
    total_events += 1
    if event.time > simulation_clock:
        simulation_clock = event.time
    history += [event]
    if isinstance(event, QueueEvent):
        N += 1
        event_list += [q.new()]
        if N == 1:
            event_list += [s.new()]
    elif isinstance(event, ServiceEvent):
        N -= 1
        if N>0:
            event_list += [s.new()]
    event_list = sorted(event_list, key=lambda ev: ev.time)

history = sorted(history, key=lambda event: event.time)
print("Simulation time: {:.2f} time units, Total of events: {}, People waiting in queue: {}".format(simulation_clock, total_events, N))
#pp.pprint(history)

W = []
clients = list(filter(lambda ev: isinstance(ev, QueueEvent), history))
services = list(filter(lambda ev: isinstance(ev, ServiceEvent), history))

while clients and services:
    client = clients.pop(0)
    service = services.pop(0)
    if service.time > client.time:
        wait_time = service.time - client.time
    else:
        wait_time = 0
    W += [wait_time]

avg_wait_time = mean(W)
print("Wait time for each client (average: {:.2f}):".format(avg_wait_time))
#pp.pprint(W)

plt.step(x=range(len(W)), y=W)
plt.ylabel('waiting time')
plt.xlabel('served client')
plt.axhline(y=avg_wait_time, color='r', linestyle='-')
plt.show()
        
        

