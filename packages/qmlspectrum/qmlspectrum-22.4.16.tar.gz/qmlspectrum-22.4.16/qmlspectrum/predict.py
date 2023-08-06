import numpy as np
import qml

def predict(X,alpha,indices,iquery,max_size,sigmas,cut_distance):
    N_train=alpha.shape[0]
    N_bin=alpha.shape[1]
    
    K=np.zeros(N_train)
    for itrain in range(N_train):
   #    if np.mod(itrain,50) == 0:
   #       print(itrain, 'kernel elements between query and training molecules calculated, ', N_train-itrain, 'remaining')
        Xt=X[indices[itrain]]
        Xq=X[indices[iquery]]
        Yt=np.zeros([1,max_size,5,max_size],dtype=float)
        Yq=np.zeros([1,max_size,5,max_size],dtype=float)
        Yt[0]=Xt
        Yq[0]=Xq
        tmp=qml.fchl.get_global_kernels(Yq,Yt,sigmas=sigmas,cut_distance=cut_distance)
        K[itrain]=tmp[0,0,0]

    Int_pred=np.zeros(N_bin)
    for i_bin in range(N_bin):
        Int_pred[i_bin]=np.dot(K,alpha[:,i_bin])

    return Int_pred
