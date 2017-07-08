## Scaled SIS infected model
# Simulates infected model from \gamma and \lambda1
# Version 1.0:
# Author:   Daniel Sadoc 
#           Vilc Rufino
# 
# plot tagged node


import math
import matplotlib.pyplot as plt
import numpy as np


def nCk(n,r):
    f = math.factorial
    return f(n) // f(r) // f(n-r)

## Probability of infected tagged node

#  N - represents the total elements (individuals)
qtd_N = 15 # number of samples (+/- 1)
inf_N = 8  # inferior limit (include)
sup_N = 40 # upper limit
stp_N = math.ceil((sup_N - inf_N)/qtd_N) # steps
vec_N = np.arange(inf_N,sup_N,stp_N) # pre compute values
qtd_N = len(vec_N) # number of samples

# Gamma - represents the endogenous infection rate
# \gamma to be tested:
#qtd_gamma = 3
#inf_gamma = 0.1
#sup_gamma = 3.0
#stp_gamma = ((sup_gamma - inf_gamma)/qtd_gamma)/2
#vec_gamma = np.arange(inf_gamma,sup_gamma,stp_gamma)
vec_gamma = np.array([0.1, 0.58, 1.09, 1.25, 2.03, 2.5])
qtd_gamma = len(vec_gamma)

# lambda1 - represents the exogenous infection rate
#qtd_lambda1 = 100
#inf_lambda1 = 0.1
sup_lambda1 = 10
#stp_lambda1 = (sup_lambda1 - inf_lambda1)/qtd_lambda1
#vec_lambda1 = np.arange(inf_lambda1, sup_lambda1, stp_lambda1)
#qtd_lambda1 = len(vec_lambda1)

# healing rate
mu=1

# Inicialize matrix of system parameter
sis_gamma 	= np.zeros((qtd_gamma, qtd_N))
sis_lambda1 	= np.zeros((qtd_gamma, qtd_N))
sis_N 		= np.zeros((qtd_gamma, qtd_N))
sis_pi 		= (qtd_gamma * qtd_N) * [None]
sis_Z 	= (qtd_gamma * qtd_N) * [None]
sis_pi_tagged_Z = (qtd_gamma * qtd_N) * [None]

# Initializing \gamma index
igamma=-1


## Defining system parameters
# pi
# Z - normalization factor to all nodes
# pi_tagged_Z - normalization factor to tagged node
for gamma in vec_gamma:
	igamma += 1
	
	## \lambda1 is a rate exogenous infection
	iN = -1
	
	## For diferent N values
	for N in vec_N: 
		iN += 1
		
		# Connectivity Matrix to completed graph
		A=np.ones((N,N))
		for i in range(N):
			A[i,i]=0
		
		# x is a vector representing the states, x(j) is the j-esimo element. 
		x=np.zeros((N,1))
		
		# \pi is a vector representing the constant of equilibrium of
		# transition states matrix Q and the probability of the states
		# Initializing \pi
		pi = np.zeros((N+1,1))
		pi_Z = np.zeros((N+1,1))
		
		# Define lambda1 (exogenous infection rate) in function of N
		lambda1 = sup_lambda1/N

		Zx = np.zeros((1,N+1))
		pi_tagged_Zx = np.zeros((1,N+1))
		#print(Zx)
		
		# To contamitations 0..N
		for i in range(N+1):
			# Load x to all states of contamination [0 0 ... 0]' until [1 1 ... 1]'
			x=np.zeros((N,1))
			for j in range(i):
				x[j,0] = 1
			
			# To connetivity A:
			# my_exponent1 is number of contamined edges
			my_exponent1=((np.matrix(x).T * np.matrix(A) * np.matrix(x)) / 2)[0,0]
			aux1 = (lambda1/mu)**i			
			aux2 = gamma**my_exponent1
			#print('gamma='+str(gamma)+' - expo='+str(my_exponent1)+' - gamma^expo='+str(aux2))
			#pi_Z[i,0] = (lambda1/mu)**i * gamma**my_exponent1
			pi_Z[i,0] = aux1 * aux2
			
			# all arrangments of i contamined nodes
			# Z[i+1,0] = (nCk(N,i+1-1)) * pi[i+1,0]
			#print('N='+str(N)+' - i='+str(i)+' - C(N,i)='+str(nCk(N,i)))
			Zx[0,i] = (nCk(N,i)) * pi_Z[i,0]
			
			# Check the special case: zero infected node
			if (i>0):
				# probability of a tagged node being infected
				# pi_tagged_Z[0,i+1] = (nCk(N-1,i+1-1-1)) * pi_Z[i+1,0]
				pi_tagged_Zx[0,i] = (nCk(N-1,i-1)) * pi_Z[i,0]
			else:
				# probability of a tagged node being infected is zero
				pi_tagged_Zx[0,i] = 0 # pi_Z[i+1,0]
		
		
		sis_gamma[igamma,iN] 			= gamma
		sis_lambda1[igamma,iN] 			= lambda1
		sis_N[igamma,iN] 			= N
		sis_pi[igamma + iN*qtd_gamma] 		= pi_Z
		sis_Z[igamma + iN*qtd_gamma] 		= Zx
		sis_pi_tagged_Z[igamma + iN*qtd_gamma]	= pi_tagged_Zx


# Expectations and probabilities
igamma=-1;

#for all gamma
for gamma in vec_gamma:
	iN = -1
	igamma += 1
	
	meaninfected = (len(vec_N)) * [None]
	pitaggedinfected = (len(vec_N)) * [None]
	
	# for all N
	for N in vec_N:
		iN += 1
		pi = sis_Z[igamma + (iN * qtd_gamma)]
		AA = np.matrix(pi/np.sum(pi))
		BB = np.matrix(np.arange(N+1))
		
		meaninfected[iN] = (AA * (BB.T))[0,0]
		pi_tagged = sis_pi_tagged_Z[igamma + (iN * qtd_gamma)]
		pitaggedinfected[iN] = np.sum(pi_tagged)/np.sum(pi)

	## Plotting values
	# Choose the values to plot
	plt.plot(vec_N, pitaggedinfected, linewidth=1, label=r'$\gamma =$'+ str(gamma))
	#plt.plot(vec_N, meaninfected, linewidth=1, label=r'$\gamma =$'+ str(gamma))

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

