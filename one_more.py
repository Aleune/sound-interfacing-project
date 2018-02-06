# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 11:14:56 2018

@author: THHUuummmbbB
"""

import numpy as np
import matplotlib.pyplot as plt

#https://python-sounddevice.readthedocs.io/en/0.3.10/
import sounddevice as sd  #!pip install sounddevice
from scipy import signal as sg #for the square function
from matplotlib.mlab import find
from numpy.fft import rfft, rfftfreq, irfft
import random
from scipy.optimize import curve_fit
from scipy.signal import hilbert
from scipy.interpolate import spline




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

def test_pendule_fit(x, amplSign, freqCarrier, freqSignal):
    #return amplCar*np.cos(2*np.pi*freqCarrier*x)*(1+amplSign*np.cos(2*np.pi*freqSignal*x))
    return np.cos(2*np.pi*freqCarrier*x)*amplSign*np.cos(2*np.pi*freqSignal*x)
    #return np.cos(2*np.pi*freqCarrier*x)
    
def load_signal(file):
    data = np.loadtxt(file)
    return data

def fit_sin(x, ampl, freq, phase):
    return 2000 + ampl*np.sin(2*np.pi*freq*x+phase)

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

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
        
    
        return (indices, self.sample_rate / np.diff(crossings))
    

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
        
        
    def save_signal(self, file):
        np.savetxt(file, self.data)
        
        
    def getData(self):
        return self.data
    
    def lock_in(self,t):
        sig_loc = self.data*np.cos(2*np.pi*4000*t)
        return sig_loc


#sound = SoundCard()
#test_sound = sound.create_sound(2000,15)
#myRec = sound.record_and_play(test_sound)
#
#analysis = SignalAnalysis(myRec[:,0])
#analysis.save_signal('gravity.txt')

data=load_signal("C:/Users/THHUuummmbbB/Desktop/sound_interfacing_project_master/pendulum.txt")
t = np.arange(0,15,1/44100)
analysis = SignalAnalysis(data)
#analysis_1 = SignalAnalysis(data)
#indice_1,freq_1=analysis_1.freq_from_crossings()
#plt.figure()
#plt.plot(indice_1[:-1],freq_1)
#sig_l=analysis_1.lock_in(t)
#analysis=SignalAnalysis(sig_l)
filtre = analysis.hig_pass_filter(1900)
analysis3 = SignalAnalysis(filtre)
filtre2 = analysis3.low_pass_filter(2100)
#exclude 11500 first values
#analysis = SignalAnalysis(filtre2[11500:])
analysis4 = SignalAnalysis(filtre2)
plt.figure()
analysis.plot_psd()
analysis4.plot_psd()

plt.figure()
plt.plot(filtre2)

indices, freq = analysis4.freq_from_crossings()
plt.figure()
plt.plot(indices[:-1], freq)

omega = np.sqrt(9.81/1.4)
#start angle (degres)
theta0 = -0.18
#time (10sec  *44100)

vitesse = -theta0*omega*np.sin(omega *t)
angle = theta0*np.cos(omega*t) 

positionx = 1.4*np.sin(angle) #position en x

#Envelop with exponential attenuation (exp(-alpha r))
#different values of alpha
#0.024 bottom
#0.01 top
ampl = 0.12*np.exp(-0.01*positionx)
#combining envelop and theoretical cos
singlalTest = ampl*np.cos(2*np.pi*2000*t)

#speed on x axis
vitesseX = 1.4*np.cos(angle)*vitesse
#frequency shift function of time
indices, freq = analysis4.freq_from_crossings()
#simulation doppler shift function of time
dopplerTest = 2000*(1-vitesseX/340)
x = np.arange(0, 15*44100)
plt.figure()
plt.plot(indices[:-1], freq)
plt.plot(x, dopplerTest)

indices2 = []
freq2 = []

for i in np.arange(0,len(freq)):
    if(freq[i] < 2050 and freq[i] > 1950):
        indices2.append(indices[i])
        freq2.append(freq[i])
        
indices2 = np.array(indices2)
freq2 = np.array(freq2)
indice_smooth=np.linspace(indices2.min(),indices2.max(),len(indices2))
freq_smooth=smooth(freq2, 5)
plt.figure()
plt.plot(indices2, freq2)
plt.plot(indice_smooth,freq_smooth,color='red')
#p_opt, cor_mat = curve_fit(fit_sin, indice_smooth, freq_smooth,(10,1/80000,1))
p_opt, cor_mat = curve_fit(fit_sin, indice_smooth, freq_smooth,(10,1/80000,1))
y = fit_sin(indices2, *p_opt)
plt.figure()

plt.plot(indice_smooth,freq_smooth)
plt.plot(indices2, y)