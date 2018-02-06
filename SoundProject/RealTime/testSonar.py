import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, writers
from scipy import signal as sg #for the square function
from threading import Thread, currentThread
from findPeak import detect_peaks

FRAME_DURATION_CHIRP = 60
SAMPLE_RATE = 44100
BASIS_FREQ = 16000

t  = np.arange(0,FRAME_DURATION_CHIRP/SAMPLE_RATE,1/SAMPLE_RATE)
sound = sg.chirp(t,BASIS_FREQ, FRAME_DURATION_CHIRP/SAMPLE_RATE, BASIS_FREQ)*(np.hanning(60))



CHUNK = int(SAMPLE_RATE/20) # RATE / number of updates per second

def genPulse(nbFrames, f0, f1, sampleRate=44100):
    t  = np.arange(0,nbFrames/sampleRate,1/sampleRate)
    sound = sg.chirp(t,f0, nbFrames/sampleRate, f1)*np.sqrt(np.hanning(nbFrames))
    return sound
    

def genPulseTrain(pulse, nbPulses, nbFrames):
    
    nbFramesSilences = int((nbFrames-len(pulse)*nbPulses)/nbPulses)
    print(nbFramesSilences)
    fin = []
    for i in range(nbPulses):
        fin = np.concatenate([fin,np.concatenate([pulse, np.zeros(nbFramesSilences)])])
    return fin

a = genPulse(60, BASIS_FREQ, BASIS_FREQ)

sound = genPulseTrain(a, 10,4096)


def soundplot(stream):
    data = np.fromstring(stream.read(CHUNK),dtype=np.float32)
    return data
   
p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paFloat32,channels=1,rate=SAMPLE_RATE,input=True,output = True,
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
        
def echoOrNot(data):
    """regarder si on a la bonne freq dans le spectrogramme"""
    freq, psd = sg.periodogram(data, fs = 44100, window = 'flattop')
    t  = detect_peaks(psd[600:800], mph = (psd.max()+psd.min())/10, mpd = 20)
    if len(t)>0 :
        return True
    else :
        return False
    
    
def extractDistance(data):
    """verifier qu'il y a au moins trois grands pics"""
    
    #selectionne le deuxieme pic
    dataE = data[205:615]
    #enveloppe
    t = detect_peaks(dataE, mpd = 5)
    #plt.plot(dataE)
    xr = np.arange(len(dataE))[t]
    #plt.plot( xr, dataE[t])
    u = detect_peaks(dataE[t], mph = 0.01)
    xu = xr[u]
    #plt.plot( np.arange(len(dataE))[xu], dataE[t][u], 'x')
    indices = np.arange(len(dataE))[xu]
    peaks = np.stack((dataE[t][u], indices))
    peaks = peaks.transpose()
    peaks = peaks[np.argsort(peaks[:, 0])]
    peaks = peaks[::-1]
    
    if peaks[0,0] < 0.6:
        return 0
    else :
        distance = np.abs(peaks[1,1] - peaks[2,1])/44100*340
        distance = distance/4
        return distance


fig, ax3= plt.subplots(1,1)
fig.canvas.mpl_connect('close_event', handle_close)
ln3, = ax3.plot([], [], 'r', animated=True,linewidth=.5)
line = ln3,

FFMpegWriter = writers['ffmpeg']
metadata = dict(title='Movie Test', artist='Matplotlib',
                comment='Movie support!')
writer = FFMpegWriter(fps=15, metadata=metadata)


i=0
saveDat = []
saveDist = []

def initSound():

    ax3.set_ylim(-0.2,1)
    ax3.set_xlim(0,2200)
    ln3.set_data([],[])
    return line

def updateSound(frame):
    global i
    global saveDat
    global saveDist
    data = soundplot(stream)
    i = i+1
    result = np.correlate(data, data, mode='full')
    #result = sg.fftconvolve(data, sound)
    #saveDat = result
    result = result[len(data)-1:]
    result = result/max(result)
    saveDat = np.concatenate([saveDat,np.abs(result)])
    ln3.set_data(np.arange(len(data)), result)
    #print(echoOrNot(data))
    if echoOrNot(data) :
        dist = extractDistance(result)
        print(dist)
        if dist is not 0:
            saveDist.append(dist)
#    else :
#        saveDist.append(0)
    #print(str(len(saveDat)))
    #plt.savefig("test"+str(i))
    return line

my_thread = Thread(target=loop_play, args=("task",))
my_thread.start() 
   

ani = FuncAnimation(fig, updateSound, interval = 20, init_func=initSound, blit = True)

#ani.save("test.mp4", writer=writer)
plt.show()

##test autocorrelation
#testDecal80 = np.concatenate([np.zeros(80),sound])
#testDecal80 = testDecal80[:-80]
#testSum = sound+testDecal80
#plt.figure()
#plt.plot(testSum)
#result = np.correlate(testSum, testSum, mode='full')
#result = result[len(testSum)-1:]
#result = result/max(result)
#plt.figure()
#plt.plot(np.abs(result))

##test enveloppe
#yes = yes[205:615]
#t = detect_peaks(yes, mpd = 5)
#plt.plot(yes)
#xr = np.arange(len(yes))[t]
#plt.plot( xr, yes[t])
#u = detect_peaks(yes[t], mph = 0.01)
#xu = xr[u]
#plt.plot( np.arange(len(yes))[xu], yes[t][u], 'x')
#indices = np.arange(len(yes))[xu]
#peaks = np.stack((yes[t][u], indices))
#peaks = peaks.transpose()
#peaks = peaks[np.argsort(peaks[:, 0])]
#peaks = peaks[::-1]
#
#distance = np.abs(peaks[1,1] - peaks[2,1])/44100*340
#distance = distance/4


