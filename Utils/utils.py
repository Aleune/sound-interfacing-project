# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 17:27:25 2018

@author: Romain
"""

import numpy as np
from numpy.fft import rfft, rfftfreq, irfft


def high_pass(data, fc, sample_rate):
    """
    filtering with high pass filter, cuttoff frequency fc
    output in temporal space
    """
    
    #Fourier space
    signal_tilde = rfft(data)
    #sample frequencies
    n = data.size
    freq = rfftfreq(n, d=1./sample_rate)
    
    H_f = 1j*(freq/fc)/(1+1j*(freq/fc))
    #H_f = [high_filter_function(i, fc) for i in freq]
    
    signal_filtre_tilde = signal_tilde*(H_f*np.conjugate(H_f))
        
    return irfft(signal_filtre_tilde)

def low_pass(data, fc, sample_rate):
    """
    filtering with low filter, cuttoff frequency fc
    output in temporal space
    maybe not useful if it's for re-ploting in fourier space... ?
    """
        
        
    #Fourier space
    signal_tilde = rfft(data)
    #sample frequencies
    n = data.size
    freq = rfftfreq(n, d=1./sample_rate)
    
    H_f = 1/(1+1j*(freq/fc))
    #H_f = [low_filter_function(i, fc) for i in freq]
    
    #signal*module carré de la fonction de transfert
    signal_filtre_tilde = signal_tilde*(H_f*np.conjugate(H_f))
    
    return irfft(signal_filtre_tilde)



####Fonction de lissage
def lissage(Lx,Ly,p):
    '''Fonction qui débruite une courbe par une moyenne glissante
    sur 2P+1 points'''
    Lxout=[]
    Lyout=[]
    Lxout = Lx[p: -p]
    for index in range(p, len(Ly)-p):
        average = np.mean(Ly[index-p : index+p+1])
        Lyout.append(average)
    return Lxout,Lyout
  

 