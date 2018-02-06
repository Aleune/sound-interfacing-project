import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from SoundCard import SoundCard
from scipy import signal as sg #for the square function
from threading import Thread, currentThread





RATE = 44100
cDivide = 40
CHUNK = int(RATE/cDivide) # RATE / number of updates per second
soundCard = SoundCard()

t  =np.arange(0,0.05,0.05/2205)
t  =np.arange(0,1,1/44100)
sound = sg.chirp(t,5000, 0.05, 200)
sound = sg.chirp(t,5000, 1, 200)


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
        stream.write(sound.astype(np.float32).tostring())
        stream.write(np.zeros(44100).astype(np.float32).tostring())
    print("Stopping as you wish.")
        



x = np.arange(100)
y = np.arange(0,cDivide*int(CHUNK/2)+1,cDivide)
y, x = np.meshgrid(y, x)
z = np.zeros((100,int(CHUNK/2)+1))
z = np.ndarray.tolist(z)

fig2,ax = plt.subplots()
fig2.canvas.mpl_connect('close_event', handle_close)

lnTest = ax.pcolormesh(x, y, z,  vmin=0., vmax=1E-9)
#ax.set_yscale('log')

i = 0

def initFreq():
    ax.set_xlim([0.0, 100])
    ax.set_ylim([0.0, 22000])
    return lnTest,

def updateFreq(frame):
    
    global z
    global i
    
    data = soundplot(stream)
    freq, psd = sg.periodogram(data, fs = 44100, window = 'flattop')
    #print(str(len(z[0])))
    if i == 100:
        z = z[1:]        
        z = np.ndarray.tolist(z)
        z.append(psd)
    else :
        z[i] = psd
        i = i+1
    z = np.asarray(z)
    lnTest.set_array(z[:-1,:-1].ravel())
    return lnTest,



my_thread = Thread(target=loop_play, args=("task",))
my_thread.start()  

ani = FuncAnimation(fig2, updateFreq, interval = 10, init_func=initFreq, blit = True)
plt.colorbar(lnTest, ax=ax, orientation='vertical', extend='max')
plt.show()



#loop_play()
    







