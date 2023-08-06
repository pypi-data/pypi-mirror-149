import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np

def plot_stem(lam,Int,label,filename):
    plt.stem(lam, Int, label=label, linewidth=1.0, linefmt='r-', markerfmt=' ')
    plt.legend()
    plt.xlabel('Wavelength (nm)', fontsize = 15)
    plt.ylabel('Oscillator strength (au)', fontsize = 15)
    plt.savefig(filename,bbox_inches='tight')
    plt.clf()
    return 1

def plot_smooth(lam,Int,label,filename):
    dx=(max(lam)-min(lam))/1000.0
    lam_smooth=np.zeros(1000)
    for i in range(0,1000):
        lam_smooth[i]=min(lam)+i*dx+dx/2
    f=interpolate.interp1d(lam, Int, kind='cubic')
    Int_smooth=f(lam_smooth)
    plt.plot(lam_smooth, Int_smooth, label=label, linewidth=1.0, color='blue')
    plt.legend()
    plt.xlabel('Wavelength (nm)', fontsize = 15)
    plt.ylabel('Oscillator strength (au)', fontsize = 15)
    plt.savefig(filename,bbox_inches='tight')
    plt.clf()
    return 1

def plot_stem_smooth(lam,Int1,Int2,label,filename):
    label1=label[0]
    label2=label[1]
    dx=(max(lam)-min(lam))/1000.0
    lam_smooth=np.zeros(1000)
    for i in range(0,1000):
        lam_smooth[i]=min(lam)+i*dx+dx/2
    f=interpolate.interp1d(lam, Int2, kind='cubic')
    Int_smooth=f(lam_smooth)
    plt.stem(lam, Int1, label=label1, linefmt='r-', markerfmt=' ')
    plt.plot(lam_smooth, Int_smooth, label=label2, linewidth=1.0, color='blue')
    plt.legend()
    plt.xlabel('Wavelength (nm)', fontsize = 15)
    plt.ylabel('Oscillator strength (au)', fontsize = 15)
    plt.savefig(filename,bbox_inches='tight')
    plt.clf()
    return 1

def plot_bar(lambda_min, Int, dlambda, label, filename):
    plt.bar(lambda_min, Int, width = dlambda, label=label, color='red', alpha=0.7, align='edge')
    plt.legend()
    plt.xlabel('Wavelength (nm)', fontsize = 15)
    plt.ylabel('Oscillator strength (au)', fontsize = 15)
    plt.savefig(filename,bbox_inches='tight')
    plt.clf()
    return 1

def plot_bar_compare(lambda_min, Int1, Int2, dlambda, label, filename):
    label1=label[0]
    label2=label[1]
    plt.bar(lambda_min, Int1, width = dlambda, label=label1,  color='red', alpha=0.2, align='edge', edgecolor='red')
    plt.bar(lambda_min, Int2, width = dlambda, label=label2,  alpha=1.0, align='edge', fill=False, edgecolor='red')
    plt.legend()
    plt.xlabel('Wavelength (nm)', fontsize = 15)
    plt.ylabel('Oscillator strength (au)', fontsize = 15)
    plt.savefig(filename,bbox_inches='tight')
    plt.clf()
    return 1


