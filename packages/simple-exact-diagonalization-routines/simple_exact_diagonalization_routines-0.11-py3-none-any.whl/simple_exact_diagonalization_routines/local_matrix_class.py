import numpy as np
class local_matrix:
    def __init__(self, local_matrix, L, operator_name = 'O'):
        self.local_matrix = local_matrix
        self.L = L
        self.operator_name = operator_name

    def at( self, pos_x ):        
        return np.kron( np.kron( np.eye( 2**(pos_x-1) ), self.local_matrix ), np.eye( 2**(self.L-pos_x) ) )

    def diagonalize( self, A, verbose = None ):
        eig, U = np.linalg.eigh( A )
        if verbose is not None:
            print(eig) 

    def word( self, str_name ):
        W_idx = np.eye( 2**self.L ) 
        ret_str = '' #This allows you to use different instances of the class to transform the same type of index
        for i, s in enumerate(str_name):
            if  s != '1':
                W_idx = W_idx.dot( self.at(i+1) )
                ret_str += self.operator_name
            else:
                ret_str += '1'
        return W_idx, ret_str
    # if test_funcs is not None:
    #     for idx in itertools.product(*[ [0,1] for s in range(3)]):
    #         print(Z_word( idx) )
    def compute_HS_overlaps( A, verbose = False ):
        import itertools
        overlaps = []
        for idx in itertools.product(*[ [0,1] for s in range(2*L)]):

            W_idx = np.eye( 2**L ) 
            for i in range(L):
                if idx[2*i] == 1:
                    W_idx = W_idx.dot( Z.at(i+1) )
                if idx[2*i+1] == 1:
                    W_idx = W_idx.dot( X.at(i+1) )
            overlap = np.trace( W_idx.dot(A)) / (A.shape[0])
            if self.verbose is not False:       
                print( sum( [idx[i]*2**(2*L-i-1) for i in range(2*L)]), idx, overlap)
            overlaps.append( overlap )
        return overlaps

sigma_z = [[1,0],[0,-1]]
sigma_y = 1j*np.array([[0,-1],[1,0]])
sigma_x = [[0,1],[1,0]]
sigma_plus = [[0,1],[0,0]]
sigma_minus = [[0,0],[1,0]]

class X_class(local_matrix):
    def __init__(self, L):
        local_matrix.__init__(self, sigma_x, L)
        self.operator_name = 'X'
class Y_class(local_matrix):
    def __init__(self, L):
        local_matrix.__init__(self, sigma_y, L)
        self.operator_name = 'Y'
class Z_class(local_matrix):
    def __init__(self, L):
        local_matrix.__init__(self, sigma_z, L)
        self.operator_name = 'Z'
class S_plus_class(local_matrix):
    def __init__(self, L):
        local_matrix.__init__(self, sigma_plus, L)
        self.operator_name = '+'
class S_minus_class(local_matrix):
    def __init__(self, L):
        local_matrix.__init__(self, sigma_minus, L)
        self.operator_name = '-'

class Pauli_algebra:
    def compute_Pauli_base_decomposition( A, verbose = False ):
        import itertools
        def __init__(self, L):
            self.Z = Z_class(L)
            self.X = X_class(L)
        overlaps = []
    
        for idx in itertools.product(*[ [0,1] for s in range(2*self.L)]):

            W_idx = np.eye( 2**self.L ) 
            for i in range(self.L):
                if idx[2*i] == 1:
                    W_idx = W_idx.dot( self.Z.at(i+1) )
                if idx[2*i+1] == 1:
                    W_idx = W_idx.dot( self.X.at(i+1) )
            overlap = np.trace( W_idx.dot(A)) / (A.shape[0]) / 2**self.L
            if self.verbose is not False:       
                print( sum( [idx[i]*2**(2*L-i-1) for i in range(2*L)]), idx, overlap)
            overlaps.append( overlap )
        return overlaps



