import os
import subprocess
from threading import Thread
from threading import Lock
import pytube
import voiceChop

# url = 'https://www.youtube.com/watch?v=oNhyLKUjRec'
# yt = pytube.YouTube(url)
#
# vids = yt.streams.all()
#
# for i in range(len(vids)):
#     print(i,'. ',vids[i])
#
# vnum = 1
#
# vids[vnum].download("./")





rawNumber = 0
denoiseNumber = 0
wavNum = 0

rawLock = Lock()
denoiseLock = Lock()
wavLock = Lock()

# new_filename = "fucking.raw"
# clean_file = "clean.wav"
# final_file ="final.raw"

# default_filename = vids[vnum].default_filename

# ffmpeg -ar 96000 -f s16le -i output.raw -strict -2 -r 26 final.wav

def Video2Raw(fileName) :
    global rawNumber
    finalFile = "origin"

    rawLock.acquire()
    rawNumber+=1
    number=rawNumber
    rawLock.release()

    subprocess.call(['ffmpeg', '-i',
                     os.path.join("./source", fileName),
                     '-ar',
                     '48000',
                     '-f',
                     's16le',
                     '-acodec',
                     'pcm_s16le',
                     os.path.join("./raws", finalFile+str(number)+".raw")])
    print(finalFile+str(number)+".raw completed")
    denoise(finalFile+str(number)+".raw")

def denoise(fileName) :
    global denoiseNumber
    finalFile="mid"

    denoiseLock.acquire()
    denoiseNumber+=1
    number=denoiseNumber
    denoiseLock.release()

    subprocess.call([os.path.join("./denoiser","rnnoise_demo"),
                     os.path.join("./raws", fileName) ,
                     os.path.join("./denoised", finalFile+str(number)+".raw")])
    print(finalFile + str(number) + ".raw completed")
    Raw2Wav(finalFile + str(number) + ".raw")

def Raw2Wav(fileName) :
    global wavNum
    finalFile = "object"

    wavLock.acquire()
    wavNum+=1
    number = wavNum
    wavLock.release()

    subprocess.call(['ffmpeg',
                     '-ar',
                     '96000',
                     '-f',
                     's16le',
                     '-i',
                     os.path.join("./denoised", fileName),
                     '-strict',
                     '-2',
                     '-r',
                     '26',
                     os.path.join("./object", finalFile+str(number)+".wav")])
    voiceChop.trimer(finalFile+str(number)+".wav")

def job() :
    pl = pytube.Playlist("https://www.youtube.com/watch?v=xottL3JnaQw&list=PLKjihOYfsIYuD-Z5LvtrzLb68EkOcAxz7")
    pl.download_all(os.path.join("./", "source"))
    print("download video  completed")

    threads = []
    file_list = os.listdir("./source")
    file_list.sort()
    # print(file_list[1])
    for file in file_list :
        thread = Thread(target=Video2Raw,args = (file,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    #
    # print("video 2 raws completed")
    #
    # file_list = os.listdir("./raws")
    # file_list.sort()
    #
    # for file in file_list:
    #     thread = Thread(target=denoise, args=(file,))
    #     threads.append(thread)
    #     thread.start()
    #
    # for thread in threads:
    #     thread.join()
    # print("denoising completed")
    #
    # file_list = os.listdir("./denoised")
    # file_list.sort()
    #
    # for file in file_list:
    #     thread = Thread(target=Raw2Wav, args=(file,))
    #     threads.append(thread)
    #     thread.start()
    #
    # for thread in threads:
    #     thread.join()
    #
    # print("raw to wav completed")