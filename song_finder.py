import sys
from pytube import *
import subprocess
import os
import music_visualize

if len(sys.argv)!=2:
    yt = YouTube(str(input("Enter the URL of the video: \n>> ")))
else:
    yt=YouTube(sys.argv[1])
video = yt.streams.filter(only_audio=True).first() 
out_file = video.download()
base, ext = os.path.splitext(out_file) 
new_file = base + '.mp3'
os.rename(out_file, new_file)

subprocess.call(['ffmpeg', '-i', new_file,'audio.wav'])
os.remove(new_file)

music_visualize.init(True,'audio.wav')

