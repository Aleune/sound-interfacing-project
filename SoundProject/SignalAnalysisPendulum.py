import numpy as np
from SoundProject.SignalAnalysis import SignalAnalysis
from Utils.utils import low_pass, high_pass



class SignalAnalysisPendulum(SignalAnalysis):
    
    
    def extractDistance(self, freq):
        """
            Extract distance between microphoner and speaker for a pendulum
            experiment using the phase of the signal.
            
            Parameters :
                
            freq : frequency of the signal used for the recording
        """
        dataFiltered = high_pass(self.data, freq-100, self.sample_rate)
        dataFiltered = low_pass(dataFiltered, freq+100, self.sample_rate)
        n = len(dataFiltered)
        Tt = np.arange(n)/44100
        X = np.sin(2*np.pi*freq*Tt)
        Y = np.cos(2*np.pi*freq*Tt)
        dataX = dataFiltered*X
        dataY = dataFiltered*Y
        X_filter = low_pass(dataX, 100, 44100)
        Y_filter = low_pass(dataY, 100, 44100)
        phi = np.arctan2(X_filter, Y_filter)
        phi_bis = np.cumsum((phi[1:]-phi[:-1]+np.pi)%(2*np.pi)-np.pi)
        dist = phi_bis*340/(freq*2*np.pi)
        return dist
    

        