import gurobipy as gp
# Sub-problem: min V(X,Z) + H_2(X,Z) + H_3(X,Z)
# Constrains: 
#             C_V
#             C_H_2
#             C_H_3
#             X_j, Z_{ij} \in {0,1} \forall i \in I, k \in K    
subproblem = gp.Model()
masterproblem = gp.Model()


#tour: due settimane
#p: numero di periodi in un giorno
#periods rappresenta il numero dei periodi in cui può iniziare il turno di lavoro, ipotizzato 3 [7.00-15.00-23.00]
# n = quanti workshift deve fare ognuno nel tour
# I indica il numero dei dipendenti
L = [4,8]
I = 5
p = 24
periods = 3
n = 10
l = 2

def v(Y):
    return 0

def H1(Y):
    return 0

def H2(Y):
    return 0

def H3(Y):
    return 0

####### VARIABILI

#X_j = 1 indica che il turno è iniziato al periodo j, 0 altrimenti
X = subproblem.addVars(range(periods), vtype=gp.GRB.BINARY, name="X")

Z = subproblem.addVars(range(periods+l), vtype=gp.GRB.BINARY, name="Z")

s = subproblem.addVars(range(l), vtype=gp.GRB.CONTINUOUS, name="s")

Y = masterproblem.addVars(range(I), vtype=gp.GRB.BINARY, name="Y")
####### VINCOLI

# \sum_j X_j = n --> Ogni tour deve avere esattamente n workshift 
subproblem.addConstr(gp.quicksum(X[j] for j in range(periods)) == n, name="first_constr")

#Z_(j+l) = s_l + X_j   \forall j \in J, \forall l \in L 
#subproblem.addConstr(((Z[p+l1] == s[l1]*X[p]) for p in range(periods) for l1 in range(L)), name="second_constr")

#\sum_(j=j)^(j+p) X_j <= 1   \forall j \in J --> non ci deve essere overlap fra i turni
#subproblem.addConstr(gp.quicksum(X[j] for j in range(periods, periods+p)) <= 1, name="third_constr")

#funzione obiettivo del sub problem
subproblem.setObjective(v(Y)+H2(Y)+H3(Y), gp.GRB.MINIMIZE)

#funzione obiettivo del master problem
masterproblem.setObjective(v(Y)+H1(Y)+H2(Y)+H3(Y), gp.GRB.MINIMIZE)

# Y_i <= 1
masterproblem.addConstr((Y[i] <= 1 for i in range(I)) , name="master_constr")

subproblem.update()

subproblem.optimize()
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