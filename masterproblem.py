from gurobipy import *
from subproblem import subproblem
import time

t1=time.time()
I = 10
periods = 48
#demand is given
tour0 = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
tour1 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
tour2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
#tour2 = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

d = [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1]  # Sostituisci con i valori effettivi
#d = [2, 5, 6, 5, 7, 7, 4, 6, 7, 7, 7, 7, 6, 5, 6, 6, 5, 4, 7, 6, 6, 4, 5, 5, 6, 6, 5, 7, 7, 6, 9, 6, 7, 6, 6, 7, 7, 4, 5, 5, 4, 5, 3, 4, 5, 3, 5, 4]
Z = [] #?
masterproblem = Model()

Y = []

for i in I:
    Y[i] = masterproblem.addVar(0,1, vtype=GRB.BINARY, name=f"Y_{i}")
    masterproblem.addConstr(Y[i] <= 1)

masterproblem.update()

'''
Do
    For each local search structure:
        Do:
            Execute current local search -> SUBPROBLEM?
        Repeat until no improvements are found -> ? 
    Next local search structure ?
Repeat until no more improvements have been found with any local search
'''