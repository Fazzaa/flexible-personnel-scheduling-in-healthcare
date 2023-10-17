'''MP
COVERAGE RICHIESTA = [5,5,5.....]
SOLUZIONE CHE COPRE  [2,2,1,.....]

SUBPROBLEM [[5,5,5.....]-[2,2,1,.....]]


SP ([3,3,3,3....])

s = 1
X = [1,0,0....,1,0....]
X[j]


Z = [1,0,0,0,0]
Z[j]
j+d = X*s

Z = s*X'''

'''
tour_pool = [([1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0], [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]), 
             ([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0])]

Y = [1,1]
requested_coverage = [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
def diff(a,b):
    if b != []:
        result = []
        for i in range(len(a)):
            result.append(a[i]-b[i])
        return result
    return a

def compute_vec_distance(tour_pool, requested_coverage):
    #tour = (tour, Z) ([1,0,0,0,0,0], [1,1,1,1,1,1,1,0,0,0])
    remaining_coverage = requested_coverage
    for i in range(len(tour_pool)):
        remaining_coverage = diff(remaining_coverage, tour_pool[i][1]*Y[i])
    return sum(remaining_coverage)

print(compute_vec_distance(tour_pool, requested_coverage))

'''
import gurobipy as grb

# Definisci la lista di elementi 1
lista1 = [10, 20, 30, 40, 50]

# Definisci la lista 2 come una lista di tuple, ognuna con due liste
lista2 = [(5, [8, 18, 28, 38, 48]), (10, [11, 21, 31, 41, 51]), (15, [14, 24, 34, 44, 54])]

# Crea un oggetto Model
model = grb.Model()

# Crea variabili di decisione per ponderare il secondo elemento di ogni tupla nella lista 2
variabili_decisione = [model.addVar(vtype=grb.GRB.CONTINUOUS, name=f'x{i}') for i in range(len(lista2))]

# Aggiorna il modello
model.update()

# Crea la funzione obiettivo per minimizzare la distanza tra lista 1 e il secondo elemento di ogni tupla nella lista 2
funzione_obiettivo = grb.quicksum((lista1[i] - variabili_decisione[j] * tupla[1][i]) ** 2 for i in range(len(lista1)) for j, tupla in enumerate(lista2))

# Imposta il modello per minimizzare la funzione obiettivo
model.setObjective(funzione_obiettivo, grb.GRB.MINIMIZE)

# Risolvi il problema di ottimizzazione
model.optimize()

# Ottieni i valori ottimali delle variabili decisionali
valori_variabili = [variabile.x for variabile in variabili_decisione]

# Stampi i risultati
print("Valori ottimali delle variabili decisionali:")
for i, valore in enumerate(valori_variabili):
    print(f'x{i}: {valore}')
