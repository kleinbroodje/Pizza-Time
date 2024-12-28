from src.engine import *


class Pizza:
    def __init__(self):
        self.image = imgload("assets", "images", "pizza_box.png")
        self.rect = self.image.get_rect()
    