# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 17:23:10 2018

@author: Romain
"""

import numpy as np
import sounddevice as sd  #!pip install sounddevice
import random


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
    
    def create_pulses(self, nbPulses, durationPulse, durationPause, frequency):
        
        pulses = 10*np.sin(2*np.pi*frequency*np.arange(durationPulse*self.samplerate)/self.samplerate)
        pauses = np.zeros(int(durationPause*44100))
        data = np.concatenate((pauses, pulses))
        
        for i in np.arange(nbPulses-1):
            data = np.concatenate((data, np.concatenate((pauses, pulses))))
    
        return data
        