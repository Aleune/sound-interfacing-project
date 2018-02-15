import numpy as np
from numpy.fft import rfft, rfftfreq, irfft


def high_pass(data, fc, sample_rate):
    """
        Filtering with second order high pass filter            
        fc cutoff frequency
        
        return data filtered
    """
    
    signal_tilde = rfft(data)
    n = data.size
    freq = rfftfreq(n, d=1./sample_rate)
    
    H_f = 1j*(freq/fc)/(1+1j*(freq/fc))
    
    signal_filtre_tilde = signal_tilde*(H_f*np.conjugate(H_f))
        
    return irfft(signal_filtre_tilde)

def low_pass(data, fc, sample_rate):
    """
        filtering with second order low pass filter
        cuttoff frequency fc
    """

    signal_tilde = rfft(data)
    n = data.size
    freq = rfftfreq(n, d=1./sample_rate)
    
    H_f = 1/(1+1j*(freq/fc))
    
    signal_filtre_tilde = signal_tilde*(H_f*np.conjugate(H_f))
    
    return irfft(signal_filtre_tilde)


def lissage(Lx,Ly,p):
    """
        Moving average function over 2p+1 points
        Lx, Ly, sets of data
        p number of points
    """
    Lxout=[]
    Lyout=[]
    Lxout = Lx[p: -p]
    for index in range(p, len(Ly)-p):
        average = np.mean(Ly[index-p : index+p+1])
        Lyout.append(average)
    return Lxout,Lyout
  

 