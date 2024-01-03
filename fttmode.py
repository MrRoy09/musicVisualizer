import pygame
import wave
import numpy as np
import sys
from scipy.fft import fft
import matplotlib.pyplot as plt

screen_width=1200
screen_height=600
fps=100
number_bars=25
with wave.open('song3.wav','rb') as audio_file:
    channels,sample_width,framerate,nframes=audio_file.getparams()[0:4]
    print(channels, sample_width)
    data=np.frombuffer(audio_file.readframes(nframes),np.int32)

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('song3.wav')
clock=pygame.time.Clock()
window=pygame.display.set_mode((screen_width,screen_height))

frames=framerate*1/fps
print("approx number of frames is",frames)

def signalProducer():
    current_frame = pygame.mixer.music.get_pos() * framerate // 1000
    signal=np.array(data[current_frame:current_frame+int(frames)])
    transformed=fft(signal)
    transformed=np.abs(transformed)
    transformed=transformed.astype(np.int32)/2147483647
    CreateRectangles(transformed)

def CreateRectangles(transformed):
    transformed=transformed[0:len(transformed):5]
    rectangle_width=screen_width/len(transformed)
    for i in range(len(transformed)):
        rect_dim=(i*rectangle_width,screen_height/1.5-screen_height/2*transformed[i],rectangle_width,screen_height/2*transformed[i])
        pygame.draw.rect(window,(255,0,0),rect_dim)
        pygame.draw.rect(window,(0,0,0),rect_dim,width=2)


pygame.mixer.music.play()
while True:
    window.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.unload()
            pygame.quit()
            sys.exit()
    signalProducer()
    pygame.display.flip()

    clock.tick(fps)
