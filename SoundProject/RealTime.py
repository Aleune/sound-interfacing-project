import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from SoundProject.SoundCard import SoundCard
from scipy import signal as sg
from SoundProject.SignalAnalysisPendulum import SignalAnalysisPendulum


class RealTime(object):
    RATE = 44100
    CHUNK = int(RATE/42) # RATE / number of updates per second
    
    
    
    
    def sound3d(self, dataToPlay = []):
        """
            Show in real time the soundwaves recorded via the microphone
            and the Power Dessity Spectrum
            Animation stop when the windows is closed
            Play a chirp from 5000Hz to 200Hz
        """
        saveData = []
        count = 0
        if len(dataToPlay) is 0:
            dataToPlay = np.zeros(44100)

        
        
        def callback(in_data, frame_count, time_info, status):
            nonlocal saveData, count
            saveData = np.fromstring(in_data,dtype=np.float32)
            #eache time callback is called play CHUNK of data to play (count save the position)
            data = (dataToPlay[count*self.CHUNK:count*self.CHUNK+self.CHUNK].astype(np.float32)/10).tostring()
            count = count+1
            if count > len(dataToPlay)/self.CHUNK-1: count = 0
            return (data, pyaudio.paContinue)
        
        def handle_close(evt):
            """
                Close the stream when the window is closed
            """
            stream.stop_stream()
            stream.close()
            p.terminate()
   
        
        
        
        p=pyaudio.PyAudio()
        stream=p.open(format=pyaudio.paFloat32,channels=1,rate=self.RATE,input=True,output = True,
                  frames_per_buffer=self.CHUNK, stream_callback = callback)
        
        
        x = np.arange(100)
        y = np.arange(0,40*int(self.CHUNK/2)+1,40)
        y, x = np.meshgrid(y, x)
        z = np.zeros((100,int(self.CHUNK/2)+1))
        z = np.ndarray.tolist(z)
        
        fig2,ax = plt.subplots()
        fig2.canvas.mpl_connect('close_event', handle_close)
        
        lnTest = ax.pcolormesh(x, y, z,  vmin=0., vmax=1E-9)
        
        
        i = 0
        
        
        def initFreq():
            """
                Function used to initialize the window of the plot
                Set dimensions of the window
            """
            ax.set_xlim([0.0, 100])
            ax.set_ylim([0.0, 22000])
            return lnTest,

        def updateFreq(frame):
            """
                Function called by matplotlib FuncAnimation to
                refresh the plot
            """
            nonlocal z, i, saveData
            data = saveData
            freq, psd = sg.periodogram(data, fs = 44100, window = 'flattop')
        
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
        
        ani = animation.FuncAnimation(fig2, updateFreq, interval = 10, init_func=initFreq, blit = True)
        plt.colorbar(lnTest, ax=ax, orientation='vertical', extend='max')
        plt.show()
        return ani
    
    
    def soundPsd(self, dataToPlay):
        """
            Plot in real time the Power Spectrum Desity function of time
            
            Animation stop when the windows is closed
        """
        
        saveData = []
        count = 0
        #check if dataToPlay is empty
        if len(dataToPlay) is 0:
            dataToPlay = np.zeros(44100)
        
        def callback(in_data, frame_count, time_info, status):
            nonlocal saveData, count
            saveData = np.fromstring(in_data,dtype=np.float32)
            data = (dataToPlay[count*self.CHUNK:count*self.CHUNK+self.CHUNK].astype(np.float32)/10).tostring()
            count = count+1
            if count > len(dataToPlay)/self.CHUNK-1: count = 0
            return (data, pyaudio.paContinue)
        
        
        
        
        def handle_close(evt):
            stream.stop_stream()
            stream.close()
            p.terminate()
            
        
        
        p=pyaudio.PyAudio()
        stream=p.open(format=pyaudio.paFloat32,channels=1,rate=self.RATE,input=True,output = True,
                  frames_per_buffer=self.CHUNK, stream_callback = callback)
        
        
        fig, (ax1, ax2) = plt.subplots(2,1)
        fig.canvas.mpl_connect('close_event', handle_close)
        ln, = ax1.plot([], [], 'r', animated=True,linewidth=.5)
        ln2, = ax2.loglog([], [], 'r', animated=True, linewidth=.5)
        line = [ln, ln2]
        dataTot = []
        
        def initSound():
            ax1.set_ylim(-.1,.1)
            ax1.set_xlim(0, 44100*5)
            ax2.set_ylim( 1E-14, 1E-6)
            ax2.set_xlim(20, 23000)
        
            ln2.set_data([],[])
            ln.set_data([],[])
            return line
        
        def updateSound(frame):
            nonlocal dataTot, saveData

            data = saveData
            if len(dataTot) == 44100*5:
                dataTot = dataTot[self.CHUNK:]
            dataTot = np.concatenate((dataTot, data))
            freq, psd = sg.periodogram(data, fs = self.RATE, window = 'flattop')
        
            ln.set_data(np.arange(len(dataTot)), dataTot)
            ln2.set_data(freq, psd)
            
            return line
        
        ani = animation.FuncAnimation(fig, updateSound, interval = 20, init_func=initSound, blit = True)
        plt.show()
        return ani
        
    def distanceVisualisation(self):
        """
           Show in real time the phase of the recorded sound, which
           is proportionnal to the distance between the microphone and
           the speakers.
           Play a continuous sound at 2000Hz.
           Animation stop when the windows is closed
           
           Note : Still some frequency jumps
        """
        soundObject = SoundCard()

        sound = soundObject.create_sound(2000, 1)
        saveData = []
        count = 1
        counter = 0
        time = []
        
        def callback(in_data, frame_count, time_info, status):
            nonlocal saveData, time, count, counter
            saveData = np.fromstring(in_data,dtype=np.float32)
            data = (sound[counter*self.CHUNK:count*self.CHUNK+self.CHUNK].astype(np.float32)/10).tostring()
            time = count*self.CHUNK/self.RATE+np.arange(self.CHUNK)/self.RATE
            count = count+1
            counter = counter+1
            if counter > len(sound)/self.CHUNK-1: counter =0
            return (data, pyaudio.paContinue)
           
        p=pyaudio.PyAudio()
        stream=p.open(format=pyaudio.paFloat32,channels=1,rate=self.RATE,input=True,output = True,
                          frames_per_buffer=self.CHUNK, stream_callback = callback) 
        
        
            
        def handle_close(evt):
            stream.stop_stream()
            stream.close()
            p.terminate()
           
        stream.start_stream()  
        
        fig, ax = plt.subplots()
        fig.canvas.mpl_connect('close_event', handle_close)
        
        
        line, = ax.plot([], [], 'r', animated=True,linewidth=.5,  markersize=1)
        
        
        i = 0
        z = []
        savePhi = 0
        
 
        
        def animate(frame):
            nonlocal i,z, savePhi, saveData, time

            analysis = SignalAnalysisPendulum(saveData)
            phi_bis = analysis.extractDistance(2000)
            
        
            
            if i == 100:
                z = z[len(phi_bis):]
                z = np.ndarray.tolist(z)
                z = np.concatenate((z,phi_bis))
                
            else : 
                z = np.concatenate((z,phi_bis))
                i = i+1
            z = np.asarray(z)
            
            line.set_ydata(z)  # update the data
            line.set_xdata(np.arange(len(z)))
            savePhi = phi_bis
            return line,
        
        
        # Init only required for blitting to give a clean slate.
        def init():
            ax.set_ylim([-1, 1])
            ax.set_xlim([0, self.CHUNK*100])
            return line,
        
        
        ani = animation.FuncAnimation(fig, animate, init_func=init,
                                      interval=50, blit=True)
        plt.show()
        return ani