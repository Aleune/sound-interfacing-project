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
            Estimate frequency over time by counting zero crossings
            Return indexes and associate frequency
        """
        sig = self.data
        # Find all indices right before a rising-edge zero crossing
        indices = find((sig[1:] >= 0) & (sig[:-1] < 0))
    
    
        # More accurate, using linear interpolation to find intersample
        crossings = [i - sig[i] / (sig[i+1] - sig[i]) for i in indices]

        
    
        return (indices, self.sample_rate / np.diff(crossings))
    
    

    def plot_signal(self):
        plt.plot(self.data)
        
    def plot_psd(self, lab='Psd'):
        """
            Plot power spectral density of data
        """
        freq, psd = sg.periodogram(self.data, fs = self.sample_rate, window = 'flattop')
        plt.loglog(freq, psd, label = lab)
        
    
    def plot_auto_correlation(self):
        """
            Calculate and plot the autocorrelation of data
        """        
        result = np.correlate(self.data, self.data, mode='full')
        result = result[len(self.data)-1:]
        result = result/max(result)
        x = np.arange(len(result))/44100
        plt.plot(x,result)
              
        
    def save_signal(self, file):
        np.savetxt(file, self.data)
        

