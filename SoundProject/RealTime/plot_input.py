import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy import signal as sg #for the square function
from threading import Thread, currentThread

t  =np.arange(0,0.05,0.05/2205)
sound = sg.chirp(t,10000, 0.05, 5000)

t  =np.arange(0,60/44100,1/44100)
sound = sg.chirp(t,15000, 60/44100, 15000)*np.sqrt(np.hanning(60))

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

def handle_close(evt):
    global my_thread
    my_thread.do_run = False
    my_thread.join()
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    
    print('Closed Figure!')
    
def loop_play(arg):
    t = currentThread()
    while getattr(t, "do_run", True):        
        stream.write((sound.astype(np.float32)/10).tostring())
        print('test')
        #stream.write(np.zeros(44100).astype(np.float32).tostring())
        
    print("Stopping as you wish.")
        



fig, (ax1, ax2, ax3) = plt.subplots(3,1)
fig.canvas.mpl_connect('close_event', handle_close)
ln, = ax1.plot([], [], 'r', animated=True,linewidth=.5)
ln2, = ax2.loglog([], [], 'r', animated=True, linewidth=.5)
ln3, = ax3.plot([], [], 'r', animated=True,linewidth=.5)
line = [ln, ln2, ln3]
dataTot = []
test = []




def initSound():
    ax1.set_ylim(-.1,.1)
    ax1.set_xlim(0, 44100*0.1)
    ax2.set_ylim( 1E-14, 1E-6)
    ax2.set_xlim(20, 23000)
    ax3.set_ylim(-0.2,1)
    ax3.set_xlim(0,2205)
    ln2.set_data([],[])
    ln.set_data([],[])
    ln3.set_data([],[])
    return line

def updateSound(frame):
    global dataTot
    global test
    data = soundplot(stream)
    if len(dataTot) == 44100*5:
        dataTot = dataTot[CHUNK:]
    dataTot = np.concatenate((dataTot, data))
    freq, psd = sg.periodogram(data, fs = 44100, window = 'flattop')

    ln.set_data(np.arange(len(dataTot)), dataTot)
    ln2.set_data(freq, psd)
    
    result = np.correlate(data,data, mode='full')
    result = result[len(data)-1:]
    result = result/max(result)
    test = data
    ln3.set_data(np.arange(len(data)), result)
    return line

my_thread = Thread(target=loop_play, args=("task",))
my_thread.start() 
   

ani = FuncAnimation(fig, updateSound, interval = 20, init_func=initSound, blit = True)
plt.show()



