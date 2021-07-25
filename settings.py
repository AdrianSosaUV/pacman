import pygame
import random
import sys
from pygame.math import Vector2 as vec

# SCREEN SETTINGS
TOP_BOTTOM_BUFFER = 50
WIDTH, HEIGHT = 610, 670
MAZE_WIDTH, MAZE_HEIGHT = WIDTH-TOP_BOTTOM_BUFFER, HEIGHT-TOP_BOTTOM_BUFFER
FPS = 60
COLS = 28
ROWS = 30

# COLOUR SETTINGS
BLACK = (0, 0, 0)
ORANGE = (170, 132, 58)
BLUE1 = (33, 137, 156)
WHITE = (255, 255, 255)
RED = (208, 22, 22)
GRAY = (107, 107, 107)
PURPLE = (112, 55, 163)
PLAYER_COLOUR = (204, 204, 0)
GOLD = (255, 255, 204)
CHERRY = (220, 20, 60)

# FONT SETTINGS
START_TEXT_SIZE = 18
START_FONT = 'arial_black'
# PLAYER SETTINGS
PLAYER_START_POS = vec(1, 1)
# NPC SETTINGS
OIKAKE = (255, 0, 0)
MACHIBUSE = (255, 192, 203)
KIMAGURE = (0, 255, 255)
OTOBOKE = (255, 165, 0)
