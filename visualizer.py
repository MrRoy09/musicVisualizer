import pygame
import wave
import numpy as np
import sys
from scipy.fft import fft
import os

def CreateRectangles():
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

def init(status,filename):
    global framerate
    global screen_width
    global screen_height
    global fps
    global frames
    global number_bars
    global data 
    global window 

    screen_width=1200
    screen_height=700
    fps=60
    number_bars=100
    white=(255,255,255)
    black=(0,0,0)
    current_color=black
    with wave.open(filename,'rb') as audio_file:
        channels,sample_width,framerate,nframes=audio_file.getparams()[0:4]
        data=np.frombuffer(audio_file.readframes(nframes),np.int32)

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    clock=pygame.time.Clock()
    window=pygame.display.set_mode((screen_width,screen_height))
    frames=framerate*1/fps
    pygame.mixer.music.play()
    toggle_bg = pygame.Rect(1050, 10, 100, 30)

    while True:
        window.fill(current_color)
        CreateRectangles()
        pygame.draw.rect(window, (233, 184, 36), toggle_bg)
        font = pygame.font.Font(None, 28)
        text = font.render("Toggle Bg", True, (0, 0, 0))
        text_rect = text.get_rect(center=toggle_bg.center)
        window.blit(text, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.unload()
                pygame.quit()
                os.remove('audio.wav')
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if toggle_bg.collidepoint(event.pos):
                    current_color = black if current_color == white else white
        pygame.display.flip()

        clock.tick(fps)

        








