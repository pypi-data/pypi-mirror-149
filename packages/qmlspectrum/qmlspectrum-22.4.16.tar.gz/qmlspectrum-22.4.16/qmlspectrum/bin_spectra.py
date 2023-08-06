import numpy as np
import qmlspectrum
import pandas as pd
'''
A module containing functions for various types of binning.
'''
def bin_spectra_uniform(spec_path, read_P, file_P, wavelength_min, wavelength_max, N_bin):
    '''
    A function for binning spectra using a uniform bin width
    '''
    spec_files=qmlspectrum.read_files(spec_path)
    if read_P:
        bin_spectra=np.load(file_P)
        N_file=bin_spectra.shape[0]-2
        Int_lam=bin_spectra[0:N_file,:]         # shouldn't this be Int_lam=bin_spectra[0:N_file,:] ???, fixed 06 May 2022
        lambda_min=bin_spectra[N_file,:]
        dlambda=bin_spectra[N_file+1,:]
    else:
        print('binning spectra')

        lambda_min=[]
        lambda_max=[]
        dlambda = (wavelength_max - wavelength_min)/N_bin
        for i_bin in range(N_bin):
            lambda_min.append( wavelength_min + (i_bin)*dlambda )
            lambda_max.append( wavelength_min + (i_bin+1)*dlambda )

        N_file=len(spec_files)
        i_file=0
        Int_lam=np.zeros([N_file+2,N_bin])
        for spec_csv in spec_files:
            if np.mod(i_file, 100) == 0:
                print(i_file,' out of ', N_file, ' done')
            spec_data=pd.read_csv(spec_path+'/'+spec_csv, names=['wavelength_nm', 'osc_strength'])
            wavelength=np.array(spec_data['wavelength_nm'])
            f=np.array(spec_data['osc_strength'])
            for i_bin in range(N_bin):
                sum_f=0.0
                for i_state in range(f.shape[0]):
                    if wavelength[i_state] > lambda_min[i_bin] and wavelength[i_state] <= lambda_max[i_bin]:
                        sum_f=sum_f+f[i_state]
                Int_lam[i_file,i_bin]=sum_f
            i_file=i_file+1
        Int_lam[N_file,:]=lambda_min
        Int_lam[N_file+1,:]=dlambda
        np.save(file_P, Int_lam)
        print('data saved in ', file_P)

    return Int_lam, lambda_min, dlambda

def bin_spectra_nonuniform(spec_path, indices, read_P, file_P, wavelength_min, wavelength_max, N_train, N_bin):
    '''
    A function for binning spectra using non-uniform bin widths
    '''
    spec_files = qmlspectrum.read_files(spec_path)
    if read_P:
        bin_spectra=np.load(file_P)
        N_file=bin_spectra.shape[0]-2
        N_bin=bin_spectra.shape[1]
        Int_lam=bin_spectra[0:N_file,:]     # shouldn't this be Int_lam=bin_spectra[0:N_file,:] ???, fixed 06 May 2022
        lambda_min=bin_spectra[N_file,:]
        dlambda=bin_spectra[N_file+1,:]
    else:
        print('binning spectra')

        # RR: FIXME, 10 April 2022
        # Should this be done for every training set size, separately? Maybe this should be done for 
        # only 100 examples or so. 
        
        # RR: TODO, 10 April 2022
        # There may be cases when different molecules can have different number of states and we may want
        # to bin uniformly. 

        print (spec_path, read_P, file_P, wavelength_min, wavelength_max, N_train, N_bin)

        all_wavelength = []
        for itrain in range(N_train):
            train_data = pd.read_csv(spec_path+'/'+"%06d"%(indices[itrain]+1)+'.csv', names=['wavelength_nm', 'osc_strength'])
            wavelength = train_data['wavelength_nm'].tolist()
            all_wavelength = all_wavelength + wavelength

        sorted_wavelength = []
        for wavelength in all_wavelength:
            if (wavelength_min <= wavelength <= wavelength_max):
                sorted_wavelength.append(wavelength)

        sorted_wavelength = pd.DataFrame(sorted_wavelength, columns=['wavelength_nm'])
        sorted_wavelength['bins'], bins = pd.qcut(sorted_wavelength['wavelength_nm'], q=N_bin, retbins=True, precision=6)
        counts = sorted_wavelength['bins'].value_counts(sort=False)
        avg_count = counts/N_train
        spec_den = sum(avg_count.values)/N_bin  # Average no. of states per bin per molecule 
        print('Spectral density (i.e. average no. of states per bin per molecule) = ', spec_den)

        lambda_min = []
        lambda_max = []
        dlambda = []
        print(bins)
        for i in range(N_bin):
            lambda_min.append(bins[i])
            lambda_max.append(bins[i+1])
            dlambda.append( bins[i + 1] - bins[i] )
            print(i, bins[i],bins[i+1])

        N_file=len(spec_files)
        i_file=0
        Int_lam=np.zeros([N_file+2,N_bin])
        for spec_csv in spec_files:
            if np.mod(i_file, 100) == 0:
                print(i_file,' out of ', N_file, ' done')
            spec_data=pd.read_csv(spec_path+'/'+spec_csv, names=['wavelength_nm', 'osc_strength'])
            wavelength=np.array(spec_data['wavelength_nm'])
            f=np.array(spec_data['osc_strength'])
            for i_bin in range(N_bin):
                sum_f=0.0
                for i_state in range(f.shape[0]):
                    if wavelength[i_state] > lambda_min[i_bin] and wavelength[i_state] <= lambda_max[i_bin]:
                        sum_f=sum_f+f[i_state]
                Int_lam[i_file,i_bin]=sum_f
                print(i_file,i_bin,sum_f)
            i_file=i_file+1
        Int_lam[N_file,:]=lambda_min
        Int_lam[N_file+1,:]=dlambda
        np.save(file_P, Int_lam)
        print('data saved in ', file_P)

    return Int_lam, lambda_min, dlambda
