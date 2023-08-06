import numpy as np
from scipy import linalg
from scipy.linalg import cho_factor, cho_solve

def linalg_solve(N_bin,K,P,solver='cholesky',file_train_prop='scr1',file_train_coef='scr2'):

    N_train=K.shape[0]

    alpha=np.zeros([N_train,N_bin]) 

    if solver == 'cholesky':
        Klow, low = cho_factor(K)
        for ibin in range(N_bin):
            alpha[:,ibin] = cho_solve((Klow, low), P[:,ibin])
    else:
        for ibin in range(N_bin):
            alpha[:,ibin] =linalg.solve(K, P[:,ibin])

    return alpha

    f = open(file_train_prop, 'w')
    for i_mol in range(N_train):
        for i_bin in range(N_bin):
            f.write(str(P[i_mol,i_bin])+' ')
        f.write('\n')
    f.close()

    f = open(file_train_coef, 'w')
    for i_mol in range(N_train):
        for i_bin in range(N_bin):
            f.write(str(alpha[i_mol,i_bin])+' ')
        f.write('\n')
    f.close()
