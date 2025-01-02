from src.settings import *


def imgload(*path, columns=1, rows=1, scale=R):
    image = pygame.transform.scale_by(
        pygame.image.load(Path(*path)).convert_alpha(), scale
    )
     
    if columns * rows == 1: 
        return image
    else:
        frame_width = image.get_width() / columns
        frame_height = image.get_height() / rows

    ret = []
    if columns > 1 and rows == 1:  # if image is divided into columns
        for i in range(columns):
            frame = image.subsurface(
                i * frame_width,
                0,
                frame_width,
                frame_height,
            )
            ret.append(frame)

    elif rows > 1 and columns == 1:  # if image is divided into rows
        for i in range(rows):
            frame = image.subsurface(
                0,
                i * frame_height,
                frame_width,
                frame_height,
            )
            ret.append(frame)

    elif columns > 1 and rows > 1:  # if image is divided two-dimensinally
        ret = []
        for i in range(rows):
            row = image.subsurface(
                0, i * frame_height, image.get_width(), frame_height
            )
            for j in range(columns):
                frame = row.subsurface(
                    j * frame_width,
                    0,
                    frame_width,
                    frame_height,
                )
                ret.append(frame)
    return ret


class Game:
    def __init__(self):
        self.state = States.MAIN_MENU
        self.countdown_time = 4000
        self.started = False
        self.ended = False
        self.duration = 60000
        self.game_over = False
        self.upgrades = []
        self.upgrade_types = ["speed", "time"]

    def set_state(self, target):
        self.reset()
        self.state = target

    def reset(self):
        self.countdown_time = 4000
        self.started = False
        self.ended = False
        self.duration = 60000
        self.game_over = False
        self.upgrades = []

game = Game()