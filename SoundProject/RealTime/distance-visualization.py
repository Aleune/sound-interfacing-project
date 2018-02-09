# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 15:04:34 2018

@author: admin
"""

import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from SoundProject.SoundCard import SoundCard
from threading import Thread, currentThread
from Utils.utils import low_pass, high_pass

soundObject = SoundCard()
sound = soundObject.create_sound(2000, 5)

RATE = 44100
CHUNK = int(RATE/20) # RATE / number of updates per second
dataWrite = []

def soundplot(stream):
    #t1=time.time()
    data = np.fromstring(stream.read(CHUNK),dtype=np.float32)
    return data
   
p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paFloat32,channels=1,rate=RATE,input=True,output = True,
                  frames_per_buffer=CHUNK) 


def loop_play(arg):
    t = currentThread()
    while getattr(t, "do_run", True):
        stream.write((sound.astype(np.float32)/10).tostring())
    print("Stopping as you wish.")
    
def handle_close(evt):
    global my_thread
    my_thread.do_run = False
    my_thread.join()
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    
    print('Closed Figure!')
   
    

fig, ax = plt.subplots()
fig.canvas.mpl_connect('close_event', handle_close)


line, = ax.plot([], [], 'r', animated=True,linewidth=.5)


a  = []

def animate(frame):
    global a
#    
    data = soundplot(stream)
    dataFiltered = high_pass(data, 1900, 44100)
    dataFiltered = low_pass(dataFiltered, 2100, 44100)
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
    
    a = phi_bis
    line.set_ydata(phi_bis)  # update the data
    line.set_xdata(np.arange(len(phi_bis)))
    return line,


# Init only required for blitting to give a clean slate.
def init():
    #line.set_ydata(np.ma.array(x, mask=True))
    ax.set_ylim([-100, 100])
    ax.set_xlim([0, 2203])
    return line,

my_thread = Thread(target=loop_play, args=("task",))
my_thread.start() 

ani = animation.FuncAnimation(fig, animate, init_func=init,
                              interval=20, blit=True)
plt.show()