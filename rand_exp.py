from random import random
from math import log, e
import matplotlib.pyplot as plt

experiments = 1000

def g(x,l):
    return -log(1-x)/l
    
def f(x,l):
    return l*e**(-l*x)
    
_lambda = 0.2

ns = [random() for i in range(experiments)]

#plt.hist(ns)

exp_ns = [g(el, _lambda) for el in ns]

n, bins, patches = plt.hist(exp_ns, bins=int(10/_lambda))

#pdf_ns = [f(el, _lambda) for el in ns]

#plt.plot(pdf_ns)

plt.plot(n, '--')

plt.ylabel('occurence')
plt.show()


