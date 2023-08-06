import numpy as np
import qml

def prepare_trainingdata(N_train,load_K,file_kernel,indices,lamd,X,Int_lam,sigmas,cut_distance,max_size):


    N_bin=len(Int_lam[0])

    K=np.zeros([N_train,N_train],dtype=float)
    if load_K:
        K = np.load(file_kernel)
    else:
        print('Calculating FCHL kernel elements'+'\n')
        for itrain in range(N_train):
            K[itrain,itrain]=1.0 + lamd
            if np.mod(itrain,10) == 0:
                print(itrain, 'rows calculated', N_train-itrain, 'remaining')
            for jtrain in range(itrain+1,N_train):
                Xt=X[indices[itrain]]
                Xq=X[indices[jtrain]]
                Yt=np.zeros([1,max_size,5,max_size],dtype=float)
                Yq=np.zeros([1,max_size,5,max_size],dtype=float)
                Yt[0]=Xt
                Yq[0]=Xq
                tmp=qml.fchl.get_global_kernels(Yq,Yt,sigmas=sigmas,cut_distance=cut_distance)
                K[itrain,jtrain]=tmp[0,0,0]
                K[jtrain,itrain]=K[itrain,jtrain]
        np.save(file_kernel, K)

    P=np.zeros([N_train,N_bin],dtype=float)

    for ibin in range(N_bin):
        for itrain in range(N_train):
            P[itrain,ibin]=Int_lam[indices[itrain],ibin]

    return K, P

def prepare_trainingdata_batch(N_train,file_kernel,indices,lamd,X,Int_lam,sigmas,cut_distance,max_size, ini_row, fin_row):


    N_bin=len(Int_lam[0])

    K=np.zeros([fin_row-ini_row,N_train],dtype=float)

    print('Calculating FCHL kernel elements'+'\n')
    for itrain in range(ini_row,fin_row):
        K[itrain,itrain]=1.0 + lamd
        if np.mod(itrain,10) == 0:
            print(itrain, 'rows calculated', N_train-itrain, 'remaining')
        for jtrain in range(itrain+1,N_train):
            Xt=X[indices[itrain]]
            Xq=X[indices[jtrain]]
            Yt=np.zeros([1,max_size,5,max_size],dtype=float)
            Yq=np.zeros([1,max_size,5,max_size],dtype=float)
            Yt[0]=Xt
            Yq[0]=Xq
            tmp=qml.fchl.get_global_kernels(Yq,Yt,sigmas=sigmas,cut_distance=cut_distance)
            K[itrain,jtrain]=tmp[0,0,0]
            K[jtrain,itrain]=K[itrain,jtrain]
    np.save(file_kernel, K)

    P=np.zeros([N_train,N_bin],dtype=float)

    for ibin in range(N_bin):
        for itrain in range(N_train):
            P[itrain,ibin]=Int_lam[indices[itrain],ibin]

    return K, P
