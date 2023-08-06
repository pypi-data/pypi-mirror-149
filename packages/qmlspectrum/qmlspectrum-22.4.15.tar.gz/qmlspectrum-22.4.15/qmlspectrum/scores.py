import numpy as np

def confidence_score(fpred,fDFT):

    fpred=np.array(fpred) 
    fDFT=np.array(fDFT)

    df = np.abs(fpred/np.sum(fpred)-fDFT/np.sum(fDFT))

    error = np.sum(df)

    phi=100 * ( 1 - error )

    return phi
