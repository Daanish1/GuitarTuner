#https://swharden.com/blog/2016-07-19-realtime-audio-visualization-in-python/


# import pyaudio
# import numpy as np
# import pylab
# import time

# RATE = 44100
# CHUNK = int(RATE/20) # RATE / number of updates per second

# def soundplot(stream):
#     t1=time.time()
#     data = np.fromstring(stream.read(CHUNK),dtype=np.int16)

#     #Test
#     fft_data = np.fft.fft(data)
#     freqs = np.fft.fftfreq(len(data))

#     peak_coefficient = np.argmax(np.abs(fft_data))
#     peak_freq = freqs[peak_coefficient]

#     print(abs(peak_freq * RATE))
#     #

#     pylab.plot(data)
#     pylab.title(i)
#     pylab.grid()
#     pylab.axis([0,len(data),-2**16/2,2**16/2])
#     pylab.savefig("03.png",dpi=50)
#     pylab.close('all')
#     # print("took %.02f ms"%((time.time()-t1)*1000))

# if __name__=="__main__":
#     p=pyaudio.PyAudio()
#     stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
#                   frames_per_buffer=CHUNK)
#     for i in range(int(20*RATE/CHUNK)): #approx 43 seconds?
#         soundplot(stream)
#     stream.stop_stream()
#     stream.close()
#     p.terminate()


import pyaudio
import numpy as np
np.set_printoptions(suppress=True) # don't use scientific notation

CHUNK = 4096 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)
TARGET = 2100 # show only this one frequency

p=pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK) #uses default input device

# create a numpy array holding a single read of audio data
for i in range(10): #to it a few times just to see
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    fft = abs(np.fft.fft(data).real)
    fft = fft[:int(len(fft)/2)] # keep only first half
    freq = np.fft.fftfreq(CHUNK,1.0/RATE)
    freq = freq[:int(len(freq)/2)] # keep only first half
    assert freq[-1]>TARGET, "ERROR: increase chunk size"
    val = fft[np.where(freq>TARGET)[0][0]]
    print(val)

# close the stream gracefully
stream.stop_stream()
stream.close()
p.terminate()