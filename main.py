import gurobipy as gp
# Sub-problem: min V(X,Z) + H_2(X,Z) + H_3(X,Z)
# Constrains: 
#             C_V
#             C_H_2
#             C_H_3
#             X_j, Z_{ij} \in {0,1} \forall i \in I, k \in K    
model = gp.Model()


#tour: due settimane
#p: numero di periodi in un giorno
#periods rappresenta il numero dei periodi in cui può iniziare il turno di lavoro
# n = quanti workshift deve fare ognuno nel tour
p = 24
periods = 24
n = 10
l = 3


####### VARIABILI

#X_j = 1 indica che il turno è iniziato al periodo j, 0 altrimenti
X = model.addVars(range(periods), vtype=gp.GRB.BINARY, name="X")

Z = model.addVars(range(periods+l), vtype=gp.GRB.BINARY, name="Z")

s = model.addVars(range(l), vtype=gp.GRB.CONTINUOUS, name="s")


####### VINCOLI

# \sum_j X_j = n --> Ogni tour deve avere esattamente n workshift 
model.addConstr(gp.quicksum(X[j] for j in range(periods)) == n, name="first_constr")

#Z_(j+l) = s_l + X_j   \forall j \in J, \forall l \in L
#TODO: definire bene cosa fa questo maledetto vincolo, come funziona il valore di s ???
model.addConstr(Z[periods+l] == s[l]*X[periods], name="second_constr")

#\sum_(j=j)^(j+p) X_j <= 1   \forall j \in J --> non ci deve essere overlap fra i turni
model.addConstr(gp.quicksum(X[j] for j in range(periods, periods+p)) <= 1, name="third_constr")
