from gurobipy import *
from subproblem import subproblem
import time
import numpy as np


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


t1=time.time()
I = 16
periods = 336

requested_coverage = [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]*14
print(f"Pippoooo:{sum(requested_coverage)}")
remaining_coverage = requested_coverage

tour_pool = []
masterproblem = Model()


#* Y[i] = 1 se il tour i-esimo è selezionato, 0 altrimenti
Y = {}
for i in range(I):
    Y[i] = masterproblem.addVar(0,1, vtype=GRB.BINARY, name=f"Y_{i}") 
    
masterproblem.update()

iteration = 0
flag = False 
prev_sub_obj_val = 0
while True:
    print(f"Iterazione numero: {iteration}")
    
    # "Column Generation ;-)"
    if iteration >= I:
        Y[iteration] = masterproblem.addVar(0,1, vtype=GRB.BINARY, name=f"Y_{iteration}")
    
    subproblem_obj_val, tour, Z = subproblem(remaining_coverage)
    tour_pool.append((tour, Z))

    masterproblem.setObjective(objfn(requested_coverage, tour_pool, Y), sense=GRB.MINIMIZE)
    masterproblem.addConstr(quicksum(Y[i] for i in range(len(Y))) <= I)

    masterproblem.update()
    masterproblem.optimize()
    remaining_coverage = compute_vec_distance(tour_pool, requested_coverage)
    print(f"\nObjVal: {masterproblem.objVal}")
    
    if subproblem_obj_val == prev_sub_obj_val:
        break
    else:
        prev_sub_obj_val = subproblem_obj_val
    
    iteration+=1

for i in range(len(Y)):
    print(f"Y_{i}: {Y[i].X}")

print(remaining_coverage)
print(sum(remaining_coverage))

print(f"In: {iteration} iterazioni")
