import gurobipy as gp
from subproblem import subproblem

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

#tour: due settimane

L = [8] # due tipi di turni
I = 3 # numero dei dipendenti
p = 48 # numero di periodi totali
periods = [i for i in range(p) if i%8==0]
n = 2 # quanti workshift deve fare ognuno nel tour

####### VARIABILI

#X_j = 1 indica che il turno è iniziato al periodo j, 0 altrimenti
X = {} 
Z =     [1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0]
s = {}

tour0 = [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
tour1 = [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0]
#tour2 = [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0]
tour2 = [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

masterproblem = gp.Model()

Y = masterproblem.addVars(range(I), vtype=gp.GRB.CONTINUOUS, name="Y")

masterproblem.update()


####### VINCOLI

# Y_i <= 1
for i in range(I):
    masterproblem.addConstr(Y[i] <= 1, name="master_constr")

# Z_j <= \sum_j Y_i*tour_j
for j in periods:
    masterproblem.addConstr(Y[0] * tour0[j] + Y[1] * tour1[j] + Y[2] * tour2[j] >= Z[j], name=f"coverage_constraint{j}")
    

masterproblem.update()

n_iter = 0 
while True:

    masterproblem.optimize()

    if masterproblem.status == gp.GRB.INFEASIBLE:
        print("UNFEASIBLE !!!")
    elif masterproblem.status == gp.GRB.OPTIMAL:
        print("FOUND SOLUTION !!!")

    constraint = masterproblem.getConstrs()

    pi = [c.Pi for c in constraint]

    res,tour = subproblem(pi)

    if res >= 0:
        print("OTTIMO CONTINUO")
        break
    else: 
        print(f"N_ITER {n_iter}")
        n_iter += 1
        col = gp.Column()

        for k in range(p):
            if tour[k] != 0:
                col.addTerm(tour[k], constraint[k])
        
        Y.append(masterproblem.addVar(vtype=gp.GRB.CONTINUOUS))
        
        masterproblem.update()

print([Y[i] for i in Y])