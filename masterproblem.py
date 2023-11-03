from gurobipy import *
from subproblem import subproblem
import time
import numpy as np
import random as rn
import matplotlib.pyplot as plt 

def diff(a,b):
    return [a[i]-b[i] for i in range(len(a))]

def compute_vec_distance(tour_pool, requested_coverage, Y):
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

def masterproblem(n_workers, requested_coverage):
    remaining_coverage = requested_coverage
    tour_pool = []
    masterproblem = Model()

    #* Y[i] = 1 se il tour i-esimo è selezionato, 0 altrimenti
    Y = {}
    for i in range(n_workers):
        Y[i] = masterproblem.addVar(0,1, vtype=GRB.BINARY, name=f"Y_{i}") 
        
    masterproblem.update()

    iteration = 0
    prev_mp_obj_val = 0.1
    while True:
        print(f"Iterazione numero: {iteration}")
        
        if iteration >= n_workers:
            Y[iteration] = masterproblem.addVar(0,1, vtype=GRB.BINARY, name=f"Y_{iteration}")
        
        tour, Z = subproblem(remaining_coverage)
        tour_pool.append((tour, Z))

        masterproblem.setObjective(objfn(requested_coverage, tour_pool, Y), sense=GRB.MINIMIZE)
        masterproblem.addConstr(quicksum(Y[i] for i in range(len(Y))) <= n_workers)

        masterproblem.update()
        masterproblem.optimize()
        remaining_coverage = compute_vec_distance(tour_pool, requested_coverage, Y)
        
        if (masterproblem.objVal / prev_mp_obj_val) < 1.05:
            break
        else:
            prev_mp_obj_val = masterproblem.objVal
        
        iteration+=1

    for i in range(len(Y)):
        print(f"Y_{i}: {Y[i].X}")

    print(requested_coverage)
    
    print("---------------------PRINTING REMAINING COVERAGE AFTER SCHEDULING---------------------------")
    for j in range(0, len(remaining_coverage)):
        if j % 24 != 0:
            print(f"[{remaining_coverage[j]}]", end="")
        else:
            print("\n")
            print(f"[{remaining_coverage[j]}]", end ="")
    
    print(sum(remaining_coverage))
    print(f"In: {iteration} iterazioni")
    return remaining_coverage


if __name__ == "__main__":
    n_workers = 13
    requested_coverage = [3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,4,4,4,4,4,4,4,4]*14
    #requested_coverage = get_random_coverage(14)
    
    t1=time.time()
    output = masterproblem(n_workers, requested_coverage)
    t2 = time.time()
    print(f"In: {round(t2-t1, 2)} secondi")
    output = [output[i] for i in range(len(output)) if i % 8 == 0]
    
    colors = []
    for elem in output:
        if elem < 0:
            colors.append('g')
        elif elem == 0:
            colors.append('b')
        else:
            colors.append('r')
    
    plt.scatter(list(range(1,43)), output, c=colors)
    plt.axhline(y=0, color='#999999', linestyle='-') 
    plt.ylim(-4, 4)
    plt.xlabel("Work shift")
    plt.text(0.5, 0.9, 'Undercoverage', color='red', ha='center', va='center', transform=plt.gca().transAxes)
    plt.text(0.5, 0.1, 'Overcoverage', color='green', ha='center', va='center', transform=plt.gca().transAxes)

    plt.title("Work shift for planning horizon")
    plt.show()