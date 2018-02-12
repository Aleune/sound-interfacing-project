# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 16:19:42 2018

@author: Romain

Test file for pendulum experiment & data analysis
"""

import numpy as np
import matplotlib.pyplot as plt
from utils import low_pass, high_pass
from scipy.optimize import curve_fit
from SignalAnalysis import SignalAnalysis
from SoundCard import SoundCard






LENGTH_PENDULUM = 0.54
XPOS_START = 0.28 #cm
START_ANGLE = -np.arctan(XPOS_START/LENGTH_PENDULUM)
DURATION_RECORD = 10 #seconds
SAMPLE_RATE = 44100
FREQUENCY = 2000 #Hertz

def fit_sin(x, ampl, freq, phase):
    """ Fit sinus centered around 2000 """
    return FREQUENCY + ampl*np.sin(2*np.pi*freq*x+phase)


####################################
#### Sound Creation & recording ####

sound = SoundCard()
testSound = sound.create_sound(FREQUENCY,DURATION_RECORD)
myRec = sound.record_and_play(testSound)






##################
#### FILTRAGE ####

#Import file penduleData.txt
#dataRaw = np.loadtxt("Data/penduleData.txt")
#use the recording (delete the firsts values)
dataRaw = myRec[:,1][15000:]

dataFiltered = high_pass(dataRaw, FREQUENCY-100, SAMPLE_RATE)
dataFiltered = low_pass(dataFiltered, FREQUENCY+100, SAMPLE_RATE)

analysisRaw = SignalAnalysis(dataRaw)
analysis = SignalAnalysis(dataFiltered)

plt.figure()
analysisRaw.plot_psd()
analysis.plot_psd()
plt.legend()

plt.figure()
plt.plot(dataRaw)
plt.figure()
plt.plot(dataFiltered)


############################
### SIMULATION PENDULUM ####



omega = np.sqrt(9.81/LENGTH_PENDULUM)

#time (10sec  *44100)
t = np.arange(0,len(dataRaw)/44100,1/44100)
vitesse = -START_ANGLE*omega*np.sin(omega *t)
angle = START_ANGLE*np.cos(omega*t) 
positionx = LENGTH_PENDULUM*np.sin(angle) #position en x
vitesseX = LENGTH_PENDULUM*np.cos(angle)*vitesse

#frequency shift function of time
indices, freq = analysis.freq_from_crossings()
#simulation doppler shift function of time
dopplerTest = FREQUENCY*(1-vitesseX/340)


x = np.arange(0, len(dataRaw))
plt.figure()
plt.plot(indices[:-1], freq)
plt.plot(x, dopplerTest)


#Remove higher frequencies in order to fit correctly
indices2 = []
freq2 = []

for i in np.arange(0,len(freq)):
    if(freq[i] < 2050 and freq[i] > 1950):
        indices2.append(indices[i])
        freq2.append(freq[i])
        
indices2 = np.array(indices2)
freq2 = np.array(freq2)

p_opt, cor_mat = curve_fit(fit_sin, indices2, freq2, (20, 1/150000, 1))
y = fit_sin(indices2, *p_opt)
plt.figure()

plt.plot(indices2, freq2, label = "Data")
plt.plot(indices2, y, label = "Fit")
plt.plot(x, dopplerTest, label = 'Theoretical model')
plt.legend()



#################################
#### Test Lock-In Amplifier #####


n = len(dataFiltered)
Tt = np.arange(n)/44100
f = 2000
X = np.sin(2*np.pi*f*Tt)
Y = np.cos(2*np.pi*f*Tt)
dataX = dataFiltered*X
dataY = dataFiltered*Y
X_filter = low_pass(dataX, 100, 44100)
Y_filter = low_pass(dataY, 100, 44100)
phi = np.arctan2(X_filter, Y_filter)
phi_bis = np.cumsum((phi[1:]-phi[:-1]+np.pi)%(2*np.pi)-np.pi)

plt.figure()
plt.plot(X_filter)
plt.plot(Y_filter)


plt.figure()
plt.plot(phi_bis)