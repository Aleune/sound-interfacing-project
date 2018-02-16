import numpy as np
from SoundProject.SignalAnalysis import SignalAnalysis

class SignalAnalysisDistSpeakers(SignalAnalysis):
    
    
    def extractDistance(self, timeDelay):
        """
            Extract distance between two speakers from data
            The two speakers had emitted the same white noise with
            timeDelay between the two
            
            result is the difference of path in meter between the
            speakers and the microphone
        """        
        result = np.correlate(self.data, self.data, mode='full')
        result = result[len(self.data)-1:]
        result = result/max(result)

        result = result[self.sample_rate*timeDelay-1000:self.sample_rate*timeDelay+1000]
        ind = np.argmax(result)-1000
        time = ind/self.sample_rate
        dist = time*340
        return dist
        