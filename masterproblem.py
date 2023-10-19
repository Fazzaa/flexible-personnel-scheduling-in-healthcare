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
        print(Y[i])
        temp = np.array(tour_pool[i][1])*int(Y[i].X)

        remaining_coverage = diff(remaining_coverage, temp)

    return remaining_coverage

def objfn(requested_coverage, tour_pool, Y):
    return quicksum((requested_coverage[i] - tupla[1][i] * Y[j]) ** 2 for i in range(len(requested_coverage)) for j, tupla in enumerate(tour_pool))


t1=time.time()
I = 10
periods = 336

requested_coverage = [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1]*7
remaining_coverage = requested_coverage

tour_pool = []
masterproblem = Model()

#* VINCOLI

#* Y[i] = 1 se il tour i-esimo è selezionato, 0 altrimenti
Y = {}
for i in range(I):
    Y[i] = masterproblem.addVar(0,1, vtype=GRB.BINARY, name=f"Y_{i}")
    masterproblem.addConstr(Y[i] <= 1)

#* Somma di Y[i] <= I
masterproblem.addConstr(quicksum(Y[i] for i in range(len(Y))) <= I)

#* Funzione Obiettivo
masterproblem.setObjective(objfn(requested_coverage, tour_pool, Y), sense=GRB.MINIMIZE)

masterproblem.update()


iteration = 0
while iteration < 15:

    print(f"Iterazione numero: {iteration}")
    
    if iteration >= 10:
        Y[iteration] = masterproblem.addVar(0,1, vtype=GRB.BINARY, name=f"Y_{iteration}")

    masterproblem.update()
    masterproblem.optimize()
    n, tour, Z = subproblem(remaining_coverage)

    if tour == [] and Z == []:
        break

    tour_pool.append((tour, Z))
    masterproblem.setObjective(objfn(requested_coverage, tour_pool, Y), sense=GRB.MINIMIZE)
    iteration+=1

remaining_coverage = compute_vec_distance(tour_pool, remaining_coverage)
print(remaining_coverage)
print(f"In: {iteration} iterazioni")