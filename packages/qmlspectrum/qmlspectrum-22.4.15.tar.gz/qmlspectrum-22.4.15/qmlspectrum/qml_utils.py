import qml
import numpy as mp

def max_size(geom_path, geom_files):
    N_file=len(geom_files)
    N_at=[]
    for i_geom in range(N_file):
        xyz_file=geom_path+'/'+geom_files[i_geom]
        mol=qml.Compound(xyz=xyz_file)
        N_at.append( len(mol.nuclear_charges) )
    max_size = max(N_at) 
    return max_size
