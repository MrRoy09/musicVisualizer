import pygame
import wave
import numpy as np
import sys

screen_width=1200
screen_height=700
fps=60
number_bars=100
with wave.open('song4.wav','rb') as audio_file:
    channels,sample_width,framerate,nframes=audio_file.getparams()[0:4]
    print(channels, sample_width)
    data=np.frombuffer(audio_file.readframes(nframes),np.int32)

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('song4.wav')
clock=pygame.time.Clock()

window=pygame.display.set_mode((screen_width,screen_height))
frames=framerate*1/fps

def CreateRectangles():
    current_frame = pygame.mixer.music.get_pos() * framerate // 1000
    rectangle_width=screen_width/frames
    for i in range(0,int(frames),int(frames/number_bars)):
        if 0 <= current_frame - i < len(data):
            amplitude = data[current_frame + i] 
            if amplitude>0:
                rectangle_dim=(i*rectangle_width,screen_height/2-screen_height/3*amplitude/2147483647 ,rectangle_width,screen_height/3*amplitude/2147483647 )
                pygame.draw.rect(window,(33,156,144),rectangle_dim)
            else:
                rectangle_dim=(i*rectangle_width,screen_height/2,rectangle_width,amplitude/(-2147483647 )*screen_height/3)
                pygame.draw.rect(window,(255,0,0),rectangle_dim)

pygame.mixer.music.play()
while True:
    window.fill((0,0,0))
    CreateRectangles()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.unload()
            pygame.quit()
            sys.exit()
    pygame.display.flip()

    clock.tick(fps)

        








