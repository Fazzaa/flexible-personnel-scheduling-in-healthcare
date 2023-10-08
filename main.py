import gurobipy as gp

subproblem = gp.Model()
masterproblem = gp.Model()

#tour: due settimane

L = [8] # due tipi di turni
I = 5 # numero dei dipendenti
p = 24 # numero di periodi in un giorno
#periods = 3 # numero dei periodi in cui può iniziare il turno di lavoro -> [00.00-8.00-16.00]
periods = [0,8,16]
n = 10 # quanti workshift deve fare ognuno nel tour

def vs(X,Z):
    return 0

def vm(Y):
    return 0

def H1m(Y):
    return 0

def H2s(X,Z):
    return 0

def H2m(Y):
    return 0

def H3s(X,Z):
    return 0

def H3m(Y):
    return 0

####### VARIABILI

#X_j = 1 indica che il turno è iniziato al periodo j, 0 altrimenti
#X = subproblem.addVars(range(periods), vtype=gp.GRB.BINARY, name="X")
X = {}
Z = {}
s = {}
for j in periods:
    X[j] = subproblem.addVar(vtype=gp.GRB.BINARY, name=f"X_{j}")
    Z[j] = subproblem.addVar(vtype=gp.GRB.BINARY, name=f"Z_{j}")

for l in L:
    s[l] = subproblem.addVar(vtype=gp.GRB.CONTINUOUS, name=f"s_{l}")

subproblem.update()
print(X)
print(Z)
print(s)

Y = masterproblem.addVars(range(I), vtype=gp.GRB.BINARY, name="Y")

masterproblem.update()
print(Y)


####### VINCOLI

# \sum_j X_j = n --> Ogni tour deve avere esattamente n workshift 
somma = 0
for j in periods:
    somma += X[j]

subproblem.addConstr(somma == n, name="primo_vincolo")

for j in periods:
    for l in L:
        index = (j+l)%24
        subproblem.addConstr(Z[index] == s[l]*X[j], name="secondo_vincolo")

# non da errore ma non fa quello che deve secondo me
# anche perchè non ho capito bene quello che deve fare
# La copertura di un turno deve essere uguale al grado di copertura (quante peprsone servono per ogni ora) durante quel turno moltiplcato per l'esistenza di un turno che inizia a quell'ora (per semplicità s[l] = 1)
somma = 0
for j in periods:
    idx = (j+p)%24
    for i in range(j, idx+1):
        somma += X[i]
    subproblem.addConstr(somma <= 1, name="terzo_vincolo")

#funzione obiettivo del sub problem
subproblem.setObjective(vs(X,Z)+H2s(X,Z)+H3s(X,Z), gp.GRB.MINIMIZE)

#funzione obiettivo del master problem
masterproblem.setObjective(vm(Y)+H1m(Y)+H2m(Y)+H3m(Y), gp.GRB.MINIMIZE)

# Y_i <= 1
for i in range(I):
    masterproblem.addConstr(Y[i] <= 1, name="master_constr")

subproblem.update()
masterproblem.update()
subproblem.optimize()
masterproblem.optimize()


'''Subproblem
For each shift to assign:
    Add a shift starting at the period j which minimizes the cost function
Next shift to assign
Return tour
'''

'''Master problem
Do
    For each local search structure:
        Do:
            Execute current local search (SUBPROBLEM)
        Repeat until no improvements are found
    Next local search structure (NEW TOUR)
Repeat until no more improvements have been found with any local search'''