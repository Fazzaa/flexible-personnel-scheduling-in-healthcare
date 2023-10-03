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

#periods rappresenta il numero dei periodi
periods = 8
X = model.addVars(range(periods), vtype=gp.GRB.BINARY, name="X")

# n non so cosa rappresenti
n = 3
model.addConstr(gp.quicksum(X[j] for j in range(periods)) == n, name="first_constr")


#Z_(j+l) = s_l + X_j

l = 3
Z = model.addVars(range(periods+l), vtype=gp.GRB.BINARY, name="X")
s = model.addVars(range(l), vtype=gp.GRB.CONTINUOUS, name="X")

model.addConstr(Z[periods+l] == s[l]*X[j], name="second_constr")

#p: numero di periodi in un giorno
p = 5
model.addConstr(gp.quicksum(X[j] for j in range(periods, periods+p)) <= 1, name="third_constr")
