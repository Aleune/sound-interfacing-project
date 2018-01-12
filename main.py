# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 12:30:56 2018

@author: Romain
"""

import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd  #!pip install sounddevice
from scipy import signal as sg #for the square function


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
        #NOT TESTED (no microphone for the moment)
        """
        myrecording = sd.playrec(data, self.samplerate, self.channels)
        
        return myrecording


sound = soundCard()
#Warning, loud, amplitude can be changed in the createSound method
sound.play(sound.createSound(500,5))

#need to be tested with microphone
sound.recordAndPlay(sound.createSound(500,5))






 




