# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 12:30:56 2018

@author: Romain
"""

import math        
import pyaudio     #sudo apt-get install python-pyaudio/ !pip install pyaudio
import wave

class soundCard:
    
    
    def __init__(self) :
        self.bitrate = 44100
        self.PyAudio = pyaudio.PyAudio
        print("creation of the soundCard object")
    
    
    def playSound(self, frequency, duration):
        
        if frequency > self.bitrate:
            self.bitrate = frequency+100

        numberOfFrames = int(self.bitrate * duration)
        restframes = numberOfFrames % self.bitrate
        wavedata = ''    

        #creation of the data
        for x in range(numberOfFrames):
            wavedata = wavedata+chr(int(math.sin(x/((self.bitrate/frequency)/math.pi))*127+128))    

        for x in range(restframes): 
            wavedata = wavedata+chr(128)

        p = self.PyAudio()
        stream = p.open(format = p.get_format_from_width(1),
                        channels = 1, 
                        rate = self.bitrate, 
                        output = True)

        stream.write(wavedata)
        stream.stop_stream()
        stream.close()
        p.terminate()
        
    def recordSound(self, time):
        #record
        print("Recording...")
    
    def testDevices():
        """
            Show the audio devices of the computer
        """
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            #if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
        



sound = soundCard()
sound.playSound(500,1)
sound.recordSound()
#second test record

 
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"
 
audio = pyaudio.PyAudio()
 
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
print("recording...")
frames = []
 
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print("finished recording")
 
 
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
 
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

p = pyaudio.PyAudio()

