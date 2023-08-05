from simple_exact_diagonalization_routines.local_matrix_class import *

# You need to tell local_matrix_class what will be the ultimate system size
L = 3

# This is how to create objects of Pauli operators
X = X_class(L)
Y = Y_class(L)
Z = Z_class(L)
S_plus = S_plus_class(L)
S_minus = S_minus_class(L)

# As an example, use some of these objects to create a hopping Hamiltonian

# Trivial initialization of the right size matrix
H_hopping = 0*np.eye( 2**L ) 

# Iteratively add always more hopping terms
for x in range(1,L-1):
    H_hopping = H_hopping + S_plus.at(x).dot(Z.at(x+1).dot(S_minus.at(x+2))) + S_minus.at(x).dot(Z.at(x+1).dot(S_plus.at(x+2)))


