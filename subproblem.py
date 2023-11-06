from gurobipy import *
import random as rn

def subproblem(remaining_coverage):
    n_workshift = 10 
    morning_ws = 3
    afternoon_ws = 3
    night_ws = 3
    cost = 10
    undercoverage_cost = 50
    overcoverage_cost = 25
    workshift_len = 8
    
    total_time = 336

    service_coverage_value = 1 #quanto
    starting_time = [i for i in range(total_time) if i%8==0] # [0,8,16,24,32,40]
    
    subproblem=Model()

    X = {} # Vale 1 se inizi a lavorare a pedice j

    for idx, value in enumerate(starting_time):
        X[value] = subproblem.addVar(0,1, vtype = GRB.BINARY, name=f"X_{value}")

    subproblem.addConstr(quicksum(X[j] for j in starting_time) == n_workshift)

    morning_penalty = subproblem.addVar(0, vtype=GRB.CONTINUOUS, name="morning_penalty")
    afternoon_penalty = subproblem.addVar(0, vtype=GRB.CONTINUOUS, name="afternoon_penalty")
    night_penalty = subproblem.addVar(0, vtype=GRB.CONTINUOUS, name="night_penalty")


    subproblem.addConstr(quicksum(morning_ws - X[j] for j in starting_time if j % 24 == 8) <= morning_penalty)
    subproblem.addConstr(quicksum(afternoon_ws - X[j] for j in starting_time if j % 24 == 16) <= afternoon_penalty)
    subproblem.addConstr(quicksum(night_ws - X[j] for j in starting_time if j % 24 == 0) <= night_penalty)

    Z = [0]*total_time
    slack_1 = [0]*total_time
    slack_2 = [0]*total_time
    
    for i in range(total_time):
        Z[i] = subproblem.addVar(0, 1, vtype=GRB.BINARY, name=f"Z_{i}")
        slack_1[i] = subproblem.addVar(0, vtype=GRB.CONTINUOUS, name=f"slack_{i}")
        slack_2[i] = subproblem.addVar(0, vtype=GRB.CONTINUOUS, name=f"slack_{i}")

    for j in starting_time:
        for i in range(j,j+workshift_len):
            subproblem.addConstr(Z[i] == (X[j]*service_coverage_value), name="coverage_constraint")
    subproblem.update()
    
    for i in range(len(remaining_coverage)):
        subproblem.addConstr((remaining_coverage[i] - Z[i]) + slack_1[i] >= 0, name=f"over_coverage_constraint_{i}")
        subproblem.addConstr((remaining_coverage[i] - Z[i]) - slack_2[i] <= 0, name=f"under_coverage_constraint_{i}")



    subproblem.setObjective(quicksum(slack_1[i]*overcoverage_cost for i in range(len(slack_1))) + 
                            quicksum(slack_2[i]*undercoverage_cost for i in range(len(slack_2))) +
                            morning_penalty * cost +
                            afternoon_penalty * cost +
                            night_penalty * cost, sense = GRB.MINIMIZE)
 
    for j in starting_time[:-2]:
        somma = 0
        idx = (j+24)
        for i in range(j, idx):
            if i % 8 == 0:
                somma += X[i]

        subproblem.addConstr(somma <= 1, name="secondo_vincolo")
    
    subproblem.update()
    subproblem.optimize()

    if subproblem.status == GRB.INFEASIBLE:
        print("INFEASIBLE")
        return 0, [], []
    else:
        shift = [0]*total_time
        for idx in range(total_time):
            if idx % workshift_len == 0:
                if X[idx].X == 1:
                    shift[idx] = 1

    coverage = [int(elem.X) for elem in Z]
    return shift, coverage

            
    