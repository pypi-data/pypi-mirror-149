import numpy as np
import random

def shuffle(shuffling, load_indices, file_indices, N_mol):

    if shuffling:
        if load_indices:
            indices=np.zeros(N_mol,dtype=int)
            f=open(file_indices, 'r')
            indices=[]
            for line in f:
                string=line.split()[0]
                indices.append(int(string))
            f.close()
        else:
            indices=list( random.sample(range(0, N_mol), N_mol) )
            f = open(file_indices, 'w')
            for i_mol in range(N_mol):
                f.write("%06d"%(indices[i_mol])+'\n')
            f.close()

    else:
        if load_indices:
            indices=np.zeros(N_mol,dtype=int)
            f=open(file_indices, 'r')
            indices=[]
            for line in f:
                string=line.split()[0]
                indices.append(int(string))
            f.close()
        else:
            indices = list(i_mol for i_mol in range(N_mol))
            f = open(file_indices, 'w')
            for i_mol in range(N_mol):
                f.write("%06d"%(indices[i_mol])+'\n')
            f.close()


    return indices
