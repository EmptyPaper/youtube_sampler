import librosa
import os
import numpy as np
import matplotlib.pyplot as plt

y, sr = librosa.load(path=os.path.join("./","clean.wav"),sr=92000)
time = np.linspace(0,len(y)/sr,len(y))
real_time = len(y)/sr
hop = int(real_time%7)
yt= librosa.effects.split(y,top_db=70,hop_length=92000,frame_length=3)
out_put_file = "output"
j=0
print(len(yt))
print(yt)
for i in range(len(yt)) :
    if(10>(yt[i][1] - yt[i][0])/sr> 4) :
        print("trimed")
        real = y[yt[i][0]:yt[i][1]]
        librosa.output.write_wav(os.path.join("./trim",out_put_file+str(j)+".wav"),real,sr)
        j+=1


#
# real = y[yt[11][0]:yt[11][1]]
# print(yt)
#
# time = np.linspace(0,yt[11][1]-yt[11][0]/sr,yt[11][1]-yt[11][0])
#
# fig, ax1 = plt.subplots()
# ax1.plot(time,real,color='b',label='speach waveform')
# ax1.set_ylabel("Amplitude")
# ax1.set_xlabel("Time [s]")
# plt.title("trim23ed")
# plt.show()
#
#
# librosa.output.write_wav("trimed_data.wav",real,sr)
print(y)
# print(librosa.get_duration(y),librosa.get_duration(yt))