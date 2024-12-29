import pygame
import math
from random import choice
from pathlib import Path


pygame.init()

WIDTH, HEIGHT = 1280, 720
window = pygame.display.set_mode((WIDTH, HEIGHT))
display = pygame.Surface((WIDTH, HEIGHT))
R = 5
true_scroll = [0, 0]
scroll = [0, 0]
fonts = [
    pygame.font.Font(Path("assets", "fonts", "Chicago.ttf"), i) for i in range(101)
]