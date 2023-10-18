from gurobipy import *

  

def subproblem(pi):
    #print(pi)
    n = 10 # numero di turni che devono essere lavorati nel periodo analizzato
    workshift_len = 8
    p = 24
    total_time = 336
    sevendays = 168
    service_coverage_value = 1 #quanto
    starting_time = [i for i in range(total_time) if i%8==0] # [0,8,16,24,32,40]
    subproblem=Model()

    X = {} # Vale 1 se inizi a lavorare a pedice j

    for idx, value in enumerate(starting_time):
        X[value] = subproblem.addVar(0,1, vtype = GRB.BINARY, name=f"X_{value}")

    subproblem.addConstr(quicksum(X[j] for j in starting_time) == n)

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

    #X [1,0,0,0,0,0,0,0] -> Z=[1,1,1,1,1,1,1,1]

    #pi = [3,3,3,3,3,3,3,3] - [1,1,1,1,1,1,1,1] + [..............] = 0
    for i in range(len(pi)):
        subproblem.addConstr(pi[i] - Z[i] + slack_1[i] >= 0, name=f"under_coverage_constraint_{i}")
        subproblem.addConstr(pi[i] - Z[i] - slack_2[i]<= 0, name=f"over_coverage_constraint_{i}")

    subproblem.setObjective(quicksum(slack_1[i] for i in range(len(slack_1)))*1 + quicksum(slack_2[i] for i in range(len(slack_2)))*1, sense = GRB.MINIMIZE)

    for j in starting_time[:-2]:
        somma = 0
        idx = (j+p)
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
    print(f"\nObjVal: {subproblem.objVal}")
    return subproblem.objVal, shift, coverage

if __name__ == '__main__':
    import random
    total_time = 336
    starting_time = [i for i in range(total_time) if i%8==0]
    shift = subproblem([random.randint(0,10) for i in range(len(starting_time))])
    #print(shift)