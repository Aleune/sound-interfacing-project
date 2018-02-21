import numpy as np
import sounddevice as sd  #!pip install sounddevice
import random
from scipy import signal as sg


class SoundCard(object):
    samplerate = 44100
    channels = 2
    
    
        
    def create_sound(self, frequency, duration):
        """
            Create sound with frequency (Hz) for duration (s)
            Return an array with the recorded data that can be played
        """
        sample = self.samplerate*duration
        x = np.arange(sample)
        
        sinArray = 10*np.sin(2*np.pi*frequency*x/self.samplerate)
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
        dataCroped = data[:-delay*self.samplerate]
        dataDelay = np.asarray([0 for i in range(delay*self.samplerate)])
        dataDelayed = np.concatenate((dataDelay, dataCroped))
        
        
        
        return np.transpose(np.array((data, dataDelayed)))
        
        
        
    
    def play(self, data):
        """
            Play the numpy array data
        """
        sd.play(data, self.samplerate)


    def stop(self):
        """
            Can be used to stop playing before the end
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
            Record and play data at the same time
        """
        myrecording = sd.playrec(data, self.samplerate, self.channels)
        
        return myrecording
    
    def create_chirp(self, frequencyStart, frequencyEnd, durationChirp, durationTot):
        """
            Create a chirp from a given frequency to another one in a given time
            durationChirp
            Add zeros for a time durationTot-durationCHirp
        """
        t  = np.arange(0,1,1/44100)
        sound = sg.chirp(t,5000, 1, 200)
        sound = np.concatenate((sound,np.zeros(44100)))
        
        return sound
    
        