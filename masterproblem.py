from gurobipy import *
from subproblem import subproblem
import time
import numpy as np

def diff(a,b):
    if b != []:
        result = []
        for i in range(len(a)):
            result.append(a[i]-b[i])
        return result
    return a

def compute_vec_distance(tour_pool, requested_coverage):
    #tour = [(tour, Z), ...] --> [([1,0,0,0,0,0], [1,1,1,1,1,1,1,0,0,0]), ...]
    remaining_coverage = requested_coverage
    for i in range(len(tour_pool)):
        temp = np.array(tour_pool[i][1])*int(Y[i].X)
        remaining_coverage = diff(remaining_coverage, temp)
    return remaining_coverage

t1=time.time()
I = 10
periods = 336

requested_coverage = [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1]*7 
remaining_coverage = requested_coverage

tour_pool = []

masterproblem = Model()

Y = {}
for i in range(I):
    Y[i] = masterproblem.addVar(0,1, vtype=GRB.BINARY, name=f"Y_{i}")
    masterproblem.addConstr(Y[i] <= 1)

masterproblem.addConstr(quicksum(Y[i] for i in range(I)) <= I)

#objective_function = quicksum((requested_coverage[i] - tupla[1][i] * Y[j]) ** 2 for i in range(len(requested_coverage)) for j, tupla in enumerate(tour_pool))
#masterproblem.setObjective(objective_function, sense=GRB.MINIMIZE)
#print(f"SONO QUIIIIIIIIIIIIIIIIIIIIIIIIII \t\t\t{objective_function}")

masterproblem.update()

iteration = 0
while iteration < 10:
    masterproblem.optimize()
    tour, Z = subproblem(remaining_coverage)
    tour_pool.append((tour, Z))
    masterproblem.update()
    remaining_coverage = compute_vec_distance(tour_pool, remaining_coverage)
    
    if tour_pool:
        objective_function = quicksum((requested_coverage[i] - tupla[1][i] * Y[j]) ** 2 for i in range(len(requested_coverage)) for j, tupla in enumerate(tour_pool))
        masterproblem.setObjective(objective_function, sense=GRB.MINIMIZE)

    if masterproblem.status == GRB.OPTIMAL:
        print(Y)

    iteration+=1

   
'''for i in range(len(tour_pool)):
    for k in range(len(tour_pool[i][0])):
        if k != 0 and k % 24 == 0:
            print("\n")    
        
        print(tour_pool[i][0][k], end="")'''

print(remaining_coverage)
chosen_tours = [tour_pool[i][0] for i in range(len(tour_pool)) if Y[i].X == 1]

print(chosen_tours)

'''
Do
    For each local search structure:
        Do:
            Execute current local search -> SUBPROBLEM?
        Repeat until no improvements are found -> ? 
    Next local search structure ?
Repeat until no more improvements have been found with any local search
'''

