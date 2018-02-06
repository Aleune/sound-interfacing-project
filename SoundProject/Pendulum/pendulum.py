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



def fit_sin(x, ampl, freq, phase):
    """ Fit sinus centered around 2000 """
    return 2000 + ampl*np.sin(2*np.pi*freq*x+phase)


LENGTH_PENDULUM = 2.82
START_ANGLE = -0.18 #degrees


#### FILTRAGE HF & LOW F####
#Import file penduleData.txt
dataRaw = np.loadtxt("Data/penduleData.txt")


dataFiltered = high_pass(dataRaw, 1000, 44100)
dataFiltered = low_pass(dataFiltered, 4000, 44100)

analysisRaw = SignalAnalysis(dataRaw)
analysis = SignalAnalysis(dataFiltered)

plt.figure()
analysisRaw.plot_psd()
analysis.plot_psd()
plt.legend()

plt.figure()
plt.plot(dataRaw)




#SIMULATION PENDULUM
#pulsation
omega = np.sqrt(9.81/LENGTH_PENDULUM)

#time (10sec  *44100)
t = np.arange(0,10,1/44100)
vitesse = START_ANGLE*omega*np.sin(omega *t)
angle = -START_ANGLE*np.cos(omega*t) 

positionx = LENGTH_PENDULUM*np.sin(angle) #position en x


#speed on x axis
vitesseX = LENGTH_PENDULUM*np.cos(angle)*vitesse
#frequency shift function of time
indices, freq = analysis.freq_from_crossings()
#simulation doppler shift function of time
dopplerTest = 2000*(1-vitesseX/340)
x = np.arange(0, 10*44100)
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

p_opt, cor_mat = curve_fit(fit_sin, indices2, freq2, (20, 1/150000, 1))
y = fit_sin(indices2, *p_opt)
plt.figure()

plt.plot(indices2, freq2)
plt.plot(indices2, y)