import gurobipy as gp
# Sub-problem: min V(X,Z) + H_2(X,Z) + H_3(X,Z)
# Constrains: \sum_j X_j = n
#             Z_(j+l) = s_l + X_j           \forall j \in J, \forall l \in L
#             \sum_(j=j)^(j+p) X_j <= 1     \forall j \in J
#             C_V
#             C_H_2
#             C_H_3
#             X_j, Z_{ij} \in {0,1} \forall i \in I, k \in K    
model = gp.Model()

#tour: due settimane

#periods rappresenta il numero dei periodi in cui può iniziare il turno di lavoro
periods = 24
#X_j = 1 indica che il turno è iniziato al periodo j
X = model.addVars(range(periods), vtype=gp.GRB.BINARY, name="X")

# n = quanti workshift deve fare ognuno nel tour
n = 10
# Ogni tour deve avere esattamente n workshift 
model.addConstr(gp.quicksum(X[j] for j in range(periods)) == n, name="first_constr")


#Z_(j+l) = s_l + X_j
#TODO: definire bene cosa fa questo maledetto vincolo, come funziona il valore di s ???
l = 3
Z = model.addVars(range(periods+l), vtype=gp.GRB.BINARY, name="X")
s = model.addVars(range(l), vtype=gp.GRB.CONTINUOUS, name="X")

model.addConstr(Z[periods+l] == s[l]*X[j], name="second_constr")

#p: numero di periodi in un giorno
p = 24
# non ci deve essere overlap fra i turni
model.addConstr(gp.quicksum(X[j] for j in range(periods, periods+p)) <= 1, name="third_constr")
