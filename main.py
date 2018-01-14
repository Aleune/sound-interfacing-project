# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 12:30:56 2018

@author: Romain
"""

import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd  #!pip install sounddevice
from scipy import signal as sg #for the square function
from scipy.signal import blackmanharris, fftconvolve
from matplotlib.mlab import find
from numpy.fft import rfft, fft


import soundfile as sf



class soundCard:
    
    
    def __init__(self) :
        self.samplerate = 44100
        self.channels = 2
        print("creation of the soundCard object")
        
    def createSound(self, frequency, duration):
        """
        create sound with frequency (Hz) for duration (s)
        sin wave or square
        return an array with the data that can be played
        """
        sample = self.samplerate*duration
        x = np.arange(sample)
        
        sin_array = 10*np.sin(2*np.pi*frequency*x/self.samplerate)
        #square_array = 100*sg.square(2*np.pi*frequency*x/self.samplerate)
        return sin_array
    
    def play(self, data):
        """
        play the numpy array
        """
        sd.play(data, self.samplerate)

    @staticmethod
    def stop():
        """
        can be used to stop playing before the end
        """
        sd.stop()
        
    def recordSound(self, duration):
        """
        Record sound for duration (s)
        """
        myrecording = sd.rec(duration * self.samplerate, samplerate=self.samplerate, channels=self.channels)
    
        return myrecording
        
    def setsamplerate(self, samplerate):
        self.samplerate = samplerate
        
    def recordAndPlay(self, data):
        """
        record and play data at the same time
        #TESTED (working with a laptop)
        """
        myrecording = sd.playrec(data, self.samplerate, self.channels)
        
        return myrecording
    
    @staticmethod
    def freq_from_crossings(sig, fs):
        """
        Estimate frequency by counting zero crossings
        """
        # Find all indices right before a rising-edge zero crossing
        indices = find((sig[1:] >= 0) & (sig[:-1] < 0))
    
        # Naive (Measures 1000.185 Hz for 1000 Hz, for instance)
        # crossings = indices
    
        # More accurate, using linear interpolation to find intersample
        # zero-crossings (Measures 1000.000129 Hz for 1000 Hz, for instance)
        crossings = [i - sig[i] / (sig[i+1] - sig[i]) for i in indices]
    
        # Some other interpolation based on neighboring points might be better.
        # Spline, cubic, whatever
    
        return fs / np.mean(np.diff(crossings))
    
    @staticmethod
    def frequency_plot(signal, sf):
        """
            plot the power vs frequency
            source : http://samcarcagno.altervista.org/blog/basic-sound-processing-python/
        """
        n =len(signal)
        fftSignal = fft(signal) # calculate fourier transform (complex numbers list)
        
        nUniquePts = int(np.ceil((n+1)/2.0))
        fftSignal = fftSignal[0:nUniquePts]
        fftSignal = abs(fftSignal) #amplitude Part
        
        fftSignal = fftSignal / float(n) # scale by the number of points so that
                 # the magnitude does not depend on the length 
                 # of the signal or on its sampling frequency  
        fftSignal = fftSignal**2  # square it to get the power
        
        # multiply by two (see technical document for details)
        # odd nfft excludes Nyquist point
        if n % 2 > 0: # we've got odd number of points fft
            fftSignal[1:len(fftSignal)] = fftSignal[1:len(fftSignal)] * 2
        else:
            fftSignal[1:len(fftSignal) -1] = fftSignal[1:len(fftSignal) - 1] * 2 # we've got even number of points fft
        
        freqArray = np.arange(0, nUniquePts, 1.0) * (sf / n);
        plt.plot(freqArray/1000, 10*np.log10(fftSignal), color='b', alpha = 0.7)
        plt.fill_between(freqArray/1000, 10*np.log10(fftSignal), np.min(10*np.log10(fftSignal)), color = 'b', alpha = 0.7)
        plt.xlabel('Frequency (kHz)')
        plt.ylabel('Power (dB)')

        
    @staticmethod
    def signal_plot(signal):
        plt.plot(signal)




sound = soundCard()
#Warning, loud, amplitude can be changed in the createSound method
signal , sample = sf.read('E:/Documents/Cours/LUMI/Projet Prog/sound-interfacing-project/sound-interfacing-project/test.wav')
sound.play(signal)
sound.stop()

a = sound.createSound(500,5)
sound.freq_from_crossings(a, 44100)
sound.play(sound.createSound(500,5))

sound.signal_plot(a)
sound.frequency_plot(a, 44100)

#need to be tested with microphone
myrecording = sound.recordAndPlay(sound.createSound(500,5))
sound.play(myrecording)





 




