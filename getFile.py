import os
import subprocess

import pytube

url = 'https://www.youtube.com/watch?v=oNhyLKUjRec'
yt = pytube.YouTube(url)

vids = yt.streams.all()

for i in range(len(vids)):
    print(i,'. ',vids[i])

vnum = 1

vids[vnum].download("./")

new_filename = "fucking.raw"
clean_file = "clean.wav"
final_file ="final.raw"

default_filename = vids[vnum].default_filename
# subprocess.call(['ffmpeg','-i',
#                  os.path.join("./", default_filename),
#                  '-ac',
#                  '2',
#                  '-f',
#                  'wav',
#                  os.path.join("./", new_filename)])
subprocess.call(['ffmpeg','-i',
                 os.path.join("./", default_filename),
                 '-ar',
                 '48000',
                 '-f',
                 's16le',
                 '-acodec',
                 'pcm_s16le',
                 os.path.join("./", new_filename)])
print("ls y")
subprocess.call(['ls','-l'])
print("rnnoise")
subprocess.call([os.path.join("./denoiser","rnnoise_demo"), os.path.join("./", new_filename) , os.path.join("./", final_file)])

subprocess.call(['ffmpeg',
                 '-ar',
                 '96000',
                 '-f',
                 's16le',
                 '-i',
                 os.path.join("./", final_file),
                 '-strict',
                 '-2',
                 '-r',
                 '26',
                 os.path.join("./", clean_file)])

# ffmpeg -ar 96000 -f s16le -i output.raw -strict -2 -r 26 final.wav

print("suck sex")