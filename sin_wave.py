import pygame
import wave
import numpy as np
import sys
import os

    

def init(status,filename):
    global screen_height
    global screen_width
    global frames
    global fps
    global framerate
    global data 
    global window

    if status==True:
        screen_width=1200
        screen_height=600
        fps=30
        with wave.open(filename,'rb') as audio_file:
            channels,sample_width,framerate,nframes=audio_file.getparams()[0:4]
            print(channels, sample_width)
            data=np.frombuffer(audio_file.readframes(nframes),np.int32)

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        clock=pygame.time.Clock()
        window=pygame.display.set_mode((screen_width,screen_height))

        frames=framerate*1/fps
        pygame.mixer.music.play()
        while True:
            window.fill((0,0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.unload()
                    pygame.quit()
                    os.remove('audio.wav')
                    sys.exit()
            sinwave()
            clock.tick(fps) 