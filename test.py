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

