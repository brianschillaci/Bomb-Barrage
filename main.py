import os

import pygame

from constants import WIDTH, HEIGHT, TITLE
from modes.lan_mode import lan_mode

# Center the window on the screen of a 1920x1080p monitor
x = 720
y = 332
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

# Initialization function needed by Pygame
pygame.init()

# Creating a screen for the game
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption(TITLE)

# Runs the main game
lan_mode(screen)
