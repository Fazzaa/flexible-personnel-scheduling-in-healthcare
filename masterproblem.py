import gurobipy as gp
from subproblem import subproblem


#tour: due settimane

L = [8] # due tipi di turni
I = 3 # numero dei dipendenti
p = 48 # numero di periodi totali
periods = [i for i in range(p) if i%8==0]
n = 2 # quanti workshift deve fare ognuno nel tour


def vm(Y):
    return 0

def H1m(Y):
    return 0

def H2m(Y):
    return 0

def H3m(Y):
    return 0

####### VARIABILI

#X_j = 1 indica che il turno è iniziato al periodo j, 0 altrimenti
X = {} 
Z = {}
s = {}

tour1 = [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0]
tour2 = [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0]
tour3 = [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0]

masterproblem = gp.Model()

Y = masterproblem.addVars(range(I), vtype=gp.GRB.BINARY, name="Y")

masterproblem.update()
#print(Y)


####### VINCOLI

#funzione obiettivo del master problem
masterproblem.setObjective(vm(Y)+H1m(Y)+H2m(Y)+H3m(Y), gp.GRB.MINIMIZE)

# Y_i <= 1
for i in range(I):
    masterproblem.addConstr(Y[i] <= 1, name="master_constr")

masterproblem.update()
masterproblem.optimize()
constraint = masterproblem.getConstrs()

pi = [c.Pi for c in constraint]

_,_ = subproblem(pi)

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