# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 17:03:17 2018

@author: Romain
"""

import numpy as np
import matplotlib.pyplot as plt

from SoundCard import SoundCard
from SignalAnalysis import SignalAnalysis

sound = SoundCard()

#same random noise (5sec) on two channel, second channel delayed by 2sec
test_sound = sound.add_delay(sound.create_random_sound(5),2)
#recording
myRec = sound.record_and_play(test_sound)

#import data example
dataRaw = np.loadtxt("../../Data/distance2SpeakerData.txt")


#Analysis
plt.figure()
dataAnalysis = SignalAnalysis(dataRaw)
#The pike in the autocorrelation -> distance between the speakers
dataAnalysis.plot_auto_correlation()