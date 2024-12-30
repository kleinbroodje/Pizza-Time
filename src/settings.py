import pygame
import math
from random import choice
from pathlib import Path
from enum import Enum

pygame.init()

WIDTH, HEIGHT = 1280, 720
window = pygame.display.set_mode((WIDTH, HEIGHT))
display = pygame.Surface((WIDTH, HEIGHT))
R = 5
true_scroll = [0, 0]
scroll = [0, 0]
minimap_scroll = [0, 0]
fonts = [
    pygame.font.Font(Path("assets", "fonts", "Chicago.ttf"), i) for i in range(101)
]
click_sound = pygame.mixer.Sound(Path("assets", "sfx", "click.wav"))
point_sound = pygame.mixer.Sound(Path("assets", "sfx", "point.wav"))
hover_sound = pygame.mixer.Sound(Path("assets", "sfx", "select.wav"))
go_sound = pygame.mixer.Sound(Path("assets", "sfx", "go.wav"))
countdown_sound = pygame.mixer.Sound(Path("assets", "sfx", "count.wav"))
stop_sound = pygame.mixer.Sound(Path("assets", "sfx", "stop.wav"))

class States(Enum):
    LAUNCH = 0  
    MAIN_MENU = 1
    PLAY = 3