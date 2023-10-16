from gurobipy import *
from subproblem import subproblem
import time

t1=time.time()
I = 10
periods = 336

tour0 = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]*7
tour1 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]*7
tour2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]*7
#tour2 = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

requested_coverage = [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1]*7 
# provided esiste per ogni tour, e c'è solo se il tour è assegnato. 
provided_coverage = [1]*336 

masterproblem = Model()

Y = {}
for i in range(I):
    Y[i] = masterproblem.addVar(0,1, vtype=GRB.BINARY, name=f"Y_{i}")
    masterproblem.addConstr(Y[i] <= 1)

def compute_vec_distance(requested, provided):
    return [requested[i]-provided[i] for i in range(len(requested))]

masterproblem.setObjective(compute_vec_distance(requested_coverage, provided_coverage), sense=GRB.MINIMIZE)

masterproblem.update()

while True:
    masterproblem.optimize()


'''
Do
    For each local search structure:
        Do:
            Execute current local search -> SUBPROBLEM?
        Repeat until no improvements are found -> ? 
    Next local search structure ?
Repeat until no more improvements have been found with any local search
'''