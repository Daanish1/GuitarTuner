import numpy as np
from scipy.io import wavfile



samplerate, data = wavfile.read("sounds/a.wav")
fft_data = np.fft.fft(data)
freqs = np.fft.fftfreq(len(data))

peak_coefficient = np.argmax(np.abs(fft_data))
peak_freq = freqs[peak_coefficient]

print(abs(peak_freq * samplerate))