import pygame
import wave
import numpy as np
import sys
from scipy.fft import fft,fftfreq,fftshift
import matplotlib.pyplot as plt
import os
import math


def signalProducer():
    global start
    global end
    current_frame = pygame.mixer.music.get_pos() * framerate // 1000
    signal=np.array(data[current_frame:current_frame+int(frames)])
    transformed=fftshift(fft(signal))
    freq = np.fft.fftshift(np.fft.fftfreq(len(signal), d=1/framerate))
    transformed=np.abs(transformed)
    transformed=transformed/10000000000
    CreateRectangles(transformed)

def CreateRectangles(transformed):
    transformed=transformed[0:len(transformed):10]
    rectangle_width=screen_width/len(transformed)
    for i in range(len(transformed)):
        rect_x,rect_y,rect_w,rect_h=i*rectangle_width,screen_height-screen_height/8*transformed[i],rectangle_width,screen_height/8*transformed[i]
        if rect_h>screen_height:
            rect_h=screen_height-10
            rect_y=screen_height-rect_h
        rect_dim=(rect_x,rect_y,rect_w,rect_h)
        pygame.draw.rect(window,(255, 0, 0),rect_dim)
        pygame.draw.rect(window,(0,0,0),rect_dim,width=2)
    pygame.display.flip()

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
            signalProducer()
            clock.tick(fps) 

