# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 12:30:56 2018

@author: Romain
"""

import numpy as np
import matplotlib.pyplot as plt

#https://python-sounddevice.readthedocs.io/en/0.3.10/
import sounddevice as sd  #!pip install sounddevice
from scipy import signal as sg #for the square function
from scipy.signal import blackmanharris, fftconvolve
from matplotlib.mlab import find
from numpy.fft import rfft, fft, rfftfreq, irfft
import soundfile as sf
import random



def low_filter_function(f, fc):
    """
    low pass transfert function
    """
    return 1/(1+1j*(f/fc))
    
def high_filter_function(f, fc):
    """
    high pass transfert function
    """
    return 1j*(f/fc)/(1+1j*(f/fc))



class SoundCard(object):
    samplerate = 44100
    channels = 2
    
    
    def __init__(self) :
        print("creation of the soundCard object")
        
    def create_sound(self, frequency, duration):
        """
        create sound with frequency (Hz) for duration (s)
        sin wave or square
        return an array with the data that can be played
        """
        sample = self.samplerate*duration
        x = np.arange(sample)
        
        sinArray = 10*np.sin(2*np.pi*frequency*x/self.samplerate)
        #square_array = 100*sg.square(2*np.pi*frequency*x/self.samplerate)
        return sinArray
    
    def create_random_sound(self, duration):
        """
        random sound
        """
        
        arrayRandom = [random.uniform(-10,10) for i in np.arange(0, self.samplerate*duration)]
        
        return np.asarray(arrayRandom)
    
    def add_delay(self, data, delay):
        """
        add a delay on one channel (add the channel)
        return two dimensional array, data delayed on one
        """
        #get the part of data-duration*samplerate
        dataCroped = data[:-delay*self.samplerate]
        dataDelay = np.asarray([0 for i in range(delay*self.samplerate)])
        dataDelayed = np.concatenate((dataDelay, dataCroped))
        
        
        
        return np.transpose(np.array((data, dataDelayed)))
        #return dataDelayed
        
        
        
    
    def play(self, data):
        """
        play the numpy array
        """
        sd.play(data, self.samplerate)


    def stop(self):
        """
        can be used to stop playing before the end
        """
        sd.stop()
        
    def record_sound(self, duration):
        """
        Record sound for duration (s)
        """
        myrecording = sd.rec(duration * self.samplerate, samplerate=self.samplerate, channels=self.channels)
    
        return myrecording
        
    def set_samplerate(self, samplerate):
        self.samplerate = samplerate
        
    def record_and_play(self, data):
        """
        record and play data at the same time
        #TESTED (working with a laptop)
        """
        myrecording = sd.playrec(data, self.samplerate, self.channels)
        
        return myrecording
    



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
    
        return self.sample_rate / np.mean(np.diff(crossings))
    

    def plot_signal(self):
        plt.plot(self.data)
        
    def plot_psd(self):
        
        freq, psd = sg.periodogram(self.data, fs = self.sample_rate, window = 'flattop')
        plt.loglog(freq, psd)
        

        
    def low_pass_filter(self, fc):
        """
        filtering with low filter, cuttoff frequency fc
        output in temporal space
        maybe not useful if it's for re-ploting in fourier space... ?
        """
        
        #Fourier space
        signal_tilde = rfft(self.data)
        #sample frequencies
        n = self.data.size
        freq = rfftfreq(n, d=1./self.sample_rate)
        H_f = [low_filter_function(i, fc) for i in freq]
        
        signal_filtre_tilde = signal_tilde*(H_f*np.conjugate(H_f))
        
        return irfft(signal_filtre_tilde)
        
        
    def hig_pass_filter(self, fc):
        """
        filtering with high pass filter, cuttoff frequency fc
        output in temporal space
        """
        
        #Fourier space
        signal_tilde = rfft(self.data)
        #sample frequencies
        n = self.data.size
        freq = rfftfreq(n, d=1./self.sample_rate)
        H_f = [high_filter_function(i, fc) for i in freq]
        
        signal_filtre_tilde = signal_tilde*(H_f*np.conjugate(H_f))
        
        return irfft(signal_filtre_tilde)
    
    def plot_auto_correlation(self):
        
        result = np.correlate(self.data, self.data, mode='full')
        result = result[len(self.data)-1:]
        result = result/max(result)
        plt.plot(result)
        

sound = SoundCard()


#Creation of test sound data
test_sound = sound.create_sound(500,2)


#Playing sound
sound.play(test_sound)


#Recording data
#sometimes i have to restart spyder after plunging the micro, tu update the list of device of soundevice maybe
#check devices with sq.query_devices()
myrecording = sound.record_and_play(test_sound)

#test recording
sound.play(myrecording)


#Data Analysis
analysis = SignalAnalysis(myrecording[:,0])

#ƒanalysis.plot_signal()
#filter fonctions are working
#maybe find another way to use the filter, here we need to create another object to analyse the filtered signal
analysis.plot_psd()
signallFiltre = analysis.low_pass_filter(200)


analyis2 = SignalAnalysis(signallFiltre)
analyis2.plot_psd()




 




