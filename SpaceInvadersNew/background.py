import pygame
from config import *
from assets import load_image
    
def draw_background(screen, background, y1, y2, speed):
    y1 += speed
    y2 += speed
    if y1 >= HEIGHT:
        y1 = -HEIGHT
    if y2 >= HEIGHT:
        y2 = -HEIGHT
    screen.blit(background, (0, y1))
    screen.blit(background, (0, y2))
    return y1, y2
