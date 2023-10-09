import gurobipy as gp

L = [8] # due tipi di turni
p = 48 # numero di periodi totali
periods = [i for i in range(p) if i%8==0]
n = 2 # quanti workshift deve fare ognuno nel tour

def subproblem(pi):
    subproblem = gp.Model()
    X = {} #48 ore, ogni 8 ore può iniziare turno
    Z = {}
    s = {}
    
    for j in periods:
        X[j] = subproblem.addVar(obj = pi[j], vtype=gp.GRB.BINARY, name=f"X_{j}")
        Z[j] = subproblem.addVar(vtype=gp.GRB.BINARY, name=f"Z_{j}")

    for l in L:
        s[l] = subproblem.addVar(vtype=gp.GRB.CONTINUOUS, name="s")

    subproblem.update()

    somma = 0
    for j in periods:
        somma += X[j]

    subproblem.addConstr(somma == n, name="primo_vincolo")


    for j in periods:
        if j != 40:
            for l in L:
                subproblem.addConstr(Z[j+l] == s[l]*X[j], name="secondo_vincolo")
    
    
    for j in periods[:-2]: # j = 32
        somma = 0
        idx = (j+16) # idx = 32+12 = 44
        for i in range(j, idx+1):
            if i % 8 == 0:
                somma += X[i]
        subproblem.addConstr(somma <= 1, name="terzo_vincolo")
    
    subproblem.update()
    subproblem.optimize()

    shift = [0]*48
    for i in range(48):
        if i%8==0:
            if X[i].X == 1:
                shift[i:(i+8)] = [1]*8
    print(shift)


if __name__=="__main__":
    import random
    subproblem([random.randint(-10,10) for i in range(48)])
    