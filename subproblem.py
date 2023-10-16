from gurobipy import *

'''def cost(slack_five_days):
    somma = 0
    for j in starting_time[:-15]:
        somma += slack_five_days[j].X
    return somma'''

def subproblem(pi):
     
    n = 10 # numero di turni che devono essere lavorati nel periodo analizzato
    workshift_len = 8
    p = 24
    total_time = 336
    sevendays = 168

    starting_time = [i for i in range(total_time) if i%8==0] # [0,8,16,24,32,40]
    print(starting_time)
    #make subproblem
    subproblem=Model()
    
    X = {} # Vale 1 se inizi a lavorare a pedice j
    for idx, value in enumerate(starting_time):
        X[value] = subproblem.addVar(0,1, 1-pi[idx], vtype = GRB.BINARY, name=f"X_{value}")

    subproblem.addConstr(quicksum(X[j] for j in starting_time) == n)
    
    for j in starting_time[:-2]: # j = 32
        somma = 0
        idx = (j+p) # idx = 32+12 = 44
        for i in range(j, idx):
            if i % 8 == 0:
                somma += X[i]
        subproblem.addConstr(somma <= 1, name="secondo_vincolo")
    
    slack_five_days = {}
    for j in starting_time[:-21]:
        slack_five_days[j] = subproblem.addVar(0, vtype=GRB.CONTINUOUS, name="slack_var")
        subproblem.update()
        somma = 0
        idx = (j+sevendays)
        for i in range(j, sevendays):
            if i % workshift_len == 0:
                somma += X[i]
        subproblem.addConstr(somma-slack_five_days[j] <= 5, name="terzo_vincolo")

    subproblem.setObjective(quicksum(slack_five_days[i] for i in starting_time[:-21]), sense=GRB.MINIMIZE)

    subproblem.update()
    subproblem.optimize()
    
    shift = [0]*total_time
    for idx in range(total_time):
        if idx % workshift_len == 0:
            if X[idx].X == 1:
                shift[idx] = 1
    
    for i in range(len(shift)):
        if i != 0 and i % 24 == 0:
            print("\n")    
        
        print(shift[i], end="")
    #print(shift)
    print(slack_five_days)
    return subproblem.objVal, shift
    
    
    
    
if __name__ == '__main__':
    import random
    total_time = 336
    starting_time = [i for i in range(total_time) if i%8==0]
    shift = subproblem([random.randint(-10,10) for i in range(len(starting_time))])
    #print(shift)
    
