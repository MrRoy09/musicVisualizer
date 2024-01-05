import pygame
import wave
import numpy as np
import sys
import os
import random

def drawCircles(screen,num_circles,radius):
    radius=int(radius)
    for _ in range(num_circles):
        x = random.randint(radius, screen_width - radius)
        y = random.randint(radius, screen_height - radius)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pygame.draw.circle(screen, color, (x, y), radius)

def average_energy(frame):
    energy=np.sum(data[int(frame):int(frame+frames)]**2)
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

def init(status,filename):
    global framerate
    global screen_width
    global screen_height
    global fps
    global frames
    global number_bars
    global data 
    global window 
    global black,white
    global energy_history
    energy_history=[]
    screen_width=1200
    screen_height=700
    fps=60

    with wave.open(filename,'rb') as audio_file:
        channels,sample_width,framerate,nframes=audio_file.getparams()[0:4]
        data=np.frombuffer(audio_file.readframes(nframes),np.int32)/2147483647

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    clock=pygame.time.Clock()
    window=pygame.display.set_mode((screen_width,screen_height))
    frames=framerate*1/fps
    pygame.mixer.music.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.unload()
                pygame.quit()
                os.remove('audio.wav')
                sys.exit()
        if len(energy_history)>=int(frames*10):
            energy_history=energy_history[int(frames*8):]
        beatDetect()
        window.fill((0,0,0))
        pygame.display.flip()


