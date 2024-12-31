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
theme_song = pygame.mixer.Sound(Path("assets", "sfx", "theme1.wav"))
theme_song.set_volume(0.8)

voicelines = [pygame.mixer.Sound(Path("assets", "sfx", f"voiceline{i}.wav")) for i in range(1, 9)]

class States(Enum):
    LAUNCH = 0  
    MAIN_MENU = 1
    PLAY = 3
    VEHICLES = 4
    SETTINGS = 5