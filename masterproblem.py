from gurobipy import *
from subproblem import subproblem
import time
import numpy as np
import random as rn

def diff(a,b):
    result = []
    for i in range(len(a)):
        result.append(a[i]-b[i])
    return result

def compute_vec_distance(tour_pool, requested_coverage):
#tour = [(tour, Z), ...] --> [([1,0,0,0,0,0], [1,1,1,1,1,1,1,0,0,0]), ...]
    remaining_coverage = requested_coverage
    for i in range(len(tour_pool)):
        temp = np.array(tour_pool[i][1])*int(Y[i].X)

        remaining_coverage = diff(remaining_coverage, temp)

    return remaining_coverage

def objfn(requested_coverage, tour_pool, Y):
    return quicksum((requested_coverage[i] - tupla[1][i] * Y[j]) ** 2 for i in range(len(requested_coverage)) for j, tupla in enumerate(tour_pool))

def get_random_coverage(days):
    i = 0
    while i < 3: 
        day_coverage.extend([rn.randint(2,4)]*8)
        i += 1
    return day_coverage*days

t1=time.time()
I = 13
periods = 336
day_coverage = []

#requested_coverage = get_random_coverage(14)
requested_coverage = [2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4]*14
remaining_coverage = requested_coverage

tour_pool = []
masterproblem = Model()

#* Y[i] = 1 se il tour i-esimo è selezionato, 0 altrimenti
Y = {}
for i in range(I):
    Y[i] = masterproblem.addVar(0,1, vtype=GRB.BINARY, name=f"Y_{i}") 
    
masterproblem.update()

iteration = 0
prev_mp_obj_val = 0.1
while True:
    print(f"Iterazione numero: {iteration}")
    
    if iteration >= I:
        Y[iteration] = masterproblem.addVar(0,1, vtype=GRB.BINARY, name=f"Y_{iteration}")
    
    tour, Z = subproblem(remaining_coverage)
    tour_pool.append((tour, Z))

    masterproblem.setObjective(objfn(requested_coverage, tour_pool, Y), sense=GRB.MINIMIZE)
    masterproblem.addConstr(quicksum(Y[i] for i in range(len(Y))) <= I)

    masterproblem.update()
    masterproblem.optimize()
    remaining_coverage = compute_vec_distance(tour_pool, requested_coverage)
    
    if (masterproblem.objVal / prev_mp_obj_val) < 1.05:
        break
    else:
        prev_mp_obj_val = masterproblem.objVal
    
    iteration+=1
t2 = time.time()


for i in range(len(Y)):
    print(f"Y_{i}: {Y[i].X}")
    '''for j in range(0, len(tour_pool[i][0])):
        if j % 24 != 0:
            print(tour_pool[i][0][j], end="")
        else:
            print("\n")
            print(tour_pool[i][0][j], end ="")'''

print(requested_coverage)
print("------------------------------------------------")
for j in range(0, len(remaining_coverage)):
    if j % 24 != 0:
        print(f"[{remaining_coverage[j]}]", end="")
    else:
        print("\n")
        print(f"[{remaining_coverage[j]}]", end ="")
#print(remaining_coverage)
print(sum(remaining_coverage))

print(f"In: {iteration} iterazioni")
print(f"In: {round(t2-t1, 2)} secondi")