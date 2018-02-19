# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 17:25:25 2018

@author: Romain
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as sg #for the square function
from matplotlib.mlab import find


class SignalAnalysis(object):
    
    def __init__(self, data, sample_rate=44100):
        self.data = data
        self.sample_rate = sample_rate
        

    def freq_from_crossings(self):
        """
        Estimate frequency by counting zero crossings
        """
        sig = self.data
        # Find all indices right before a rising-edge zero crossing
        indices = find((sig[1:] >= 0) & (sig[:-1] < 0))
    
        # Naive (Measures 1000.185 Hz for 1000 Hz, for instance)
        # crossings = indices
    
        # More accurate, using linear interpolation to find intersample
        # zero-crossings (Measures 1000.000129 Hz for 1000 Hz, for instance)
        crossings = [i - sig[i] / (sig[i+1] - sig[i]) for i in indices]
    
    
        #np.diff create an array with difference one by one out[n] = a[n+1] - a[n]
        
    
        return (indices, self.sample_rate / np.diff(crossings))
    
    

    def plot_signal(self):
        plt.plot(self.data)
        
    def plot_psd(self, lab='Psd'):
        freq, psd = sg.periodogram(self.data, fs = self.sample_rate, window = 'flattop')
        plt.loglog(freq, psd, label = lab)
        
        

        
    
    def plot_auto_correlation(self):
        
        result = np.correlate(self.data, self.data, mode='full')
        result = result[len(self.data)-1:]
        result = result/max(result)
        x = np.arange(len(result))/44100
        plt.plot(x,result)
              
        
        
        
    def save_signal(self, file):
        np.savetxt(file, self.data)
        
        
    def getData(self):
        return self.data
    
    def set_data(data):
        self.data = data

