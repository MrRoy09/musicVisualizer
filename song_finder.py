import sys
from pytube import *
import subprocess
import os
import fttmode
import visualizer
import energy

if len(sys.argv)!=3:
    yt = YouTube(str(input("Enter the URL of the video you want to visualize: \n>> ")))
    mode=int(input("Enter mode of visuals"))
else:
    yt=YouTube(sys.argv[1])
    mode=int(sys.argv[2])
video = yt.streams.filter(only_audio=True).first() 
out_file = video.download()
base, ext = os.path.splitext(out_file) 
new_file = base + '.mp3'
print(new_file)
os.rename(out_file, new_file)

subprocess.call(['ffmpeg', '-i', new_file,
                   'audio.wav'])
os.remove(new_file)

if mode==1:
    fttmode.init(True,'audio.wav')
elif mode==2:
    visualizer.init(True,'audio.wav')
elif mode==3:
    energy.init(True,'audio.wav')
else:
    print("wrong mode")
