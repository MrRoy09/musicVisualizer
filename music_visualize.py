import pygame
import wave
import numpy as np
import sys
from scipy.fft import fft,fftfreq,fftshift
import matplotlib.pyplot as plt
import os
import math
import random

colors=[(0,0,225),(225,0,0),(0,255,0),(255,0,0),(0,0,255)]

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
        if rect_h>screen_height-10:
            rect_h=screen_height-30
            rect_y=screen_height-rect_h
        rect_dim=(rect_x,rect_y,rect_w,rect_h)
        pygame.draw.rect(window,colors[random.randint(0,4)],rect_dim)
        pygame.draw.rect(window,(0,0,0),rect_dim,width=2)
    pygame.display.flip()

def CreateRectangles_Visualizer():
    current_frame = pygame.mixer.music.get_pos() * framerate // 1000
    rectangle_width=screen_width/frames
    for i in range(0,int(frames),int(frames/number_bars)):
        if 0 <= current_frame - i < len(data):
            amplitude = data[current_frame + i] 
            if amplitude>0:
                rectangle_dim=(i*rectangle_width,screen_height/2-screen_height/3*amplitude/2147483647 ,rectangle_width,screen_height/3*amplitude/2147483647 )
                pygame.draw.rect(window,(33,156,144),rectangle_dim)
                pygame.draw.circle(window,(255,255,255),(i*rectangle_width,screen_height/2-amplitude/(2147483647 )*screen_height/3),1)
            else:
                rectangle_dim=(i*rectangle_width,screen_height/2,rectangle_width,amplitude/(-2147483647 )*screen_height/3)
                pygame.draw.rect(window,(255,0,0),rectangle_dim)
                pygame.draw.circle(window,(255,255,255),(i*rectangle_width,screen_height/2+amplitude/(-2147483647 )*screen_height/3),1)
    pygame.display.flip()

def drawCircles(screen,num_circles,radius):
    radius=int(radius)
    for _ in range(num_circles):
        x = random.randint(radius, screen_width - radius)
        y = random.randint(radius, screen_height - radius)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pygame.draw.circle(screen, color, (x, y), radius)

def average_energy(frame):
    energy=np.sum(beat_data[int(frame):int(frame+frames)]**2)
    energy_history.append(energy)
    return energy

def beatDetect():
    current_frame = pygame.mixer.music.get_pos() * framerate // 1000
    energy=average_energy(current_frame)
    energy_set=np.array([energy])
    for i in range(1,11):
        energy_set=np.append(energy_set,average_energy(current_frame+i*frames))
    average_energy_set=np.mean(energy_set)
    c=-0.0000015*np.var(energy_history)+1.5123
    if energy>average_energy_set*c:
        drawCircles(window,40,energy/2)
    pygame.display.flip()

def init(status,filename,pos=0.0):
    global screen_height
    global screen_width
    global number_bars
    global frames
    global fps
    global framerate
    global data 
    global beat_data
    global window
    global mode
    global energy_history
    global black,white
    mode=0
    number_bars=80
    energy_history=[]

    if status==True:
        screen_width=1200
        screen_height=700
        with wave.open(filename,'rb') as audio_file:
            channels,sample_width,framerate,nframes=audio_file.getparams()[0:4]
            data=np.frombuffer(audio_file.readframes(nframes),np.int32)
            beat_data=data/2147483647

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        clock=pygame.time.Clock()
        window=pygame.display.set_mode((screen_width,screen_height))

       
        pygame.mixer.music.play()
        while True:
            window.fill((0,0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.unload()
                    pygame.quit()
                    os.remove('audio.wav')
                    sys.exit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        mode=(mode+1)%3
            if mode==0:
                fps=30
                frames=framerate*1/fps
                signalProducer()
                clock.tick(fps) 
            elif mode==1:
                fps=60
                frames=framerate*1/fps
                CreateRectangles_Visualizer()
                clock.tick(fps) 
            elif mode==2:
                fps=60
                frames=framerate*1/fps
                if len(energy_history)>=int(frames*10):
                    energy_history=energy_history[int(frames*8):]
                beatDetect()
                window.fill((0,0,0))
                pygame.display.flip()
            
            
