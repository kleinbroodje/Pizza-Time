from src.engine import *
from src.player import *


def buy_vehicle(price, vehicle): 
    if player.total_tips < price:
        return
    player.total_tips -= price
    player.unlocked_vehicles.append(vehicle)


class Button:
    def __init__(self, pos, size, text, color, funcs):
        self.size = size
        self.color = color
        self.text = text
        self.pos = pos
        self.font = pygame.Font.render(fonts[self.size], self.text, True, self.color)
        self.text_rect = self.font.get_rect(topleft=self.pos)
        self.funcs = funcs
        self.hover_sound_played = False

    def update(self):
        if self.text_rect.collidepoint(pygame.mouse.get_pos()):
            if not self.hover_sound_played:
                pygame.mixer.Sound.play(hover_sound)
                self.hover_sound_played = True
            size = self.size+10
            text = pygame.Font.render(fonts[size], self.text, True, self.color)
            rect = text.get_rect(center=self.text_rect.center)
            display.blit(text, rect)
        else:
            self.hover_sound_played = False
            display.blit(self.font, self.text_rect)

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.text_rect.collidepoint(pygame.mouse.get_pos()):
                 pygame.mixer.Sound.play(click_sound)
                 for func in self.funcs:
                    func()


class Select():
    def __init__(self, pos, lpos, rpos, arrow_size, items):
        self.pos = pos
        self.right_arrow = Button(rpos, arrow_size, ">", (255, 255, 255), [lambda: self.right()])
        self.left_arrow = Button(lpos, arrow_size, "<", (255, 255, 255), [lambda: self.left()])
        self.select_button = Button((WIDTH/2 - 85, 450), 50, "SELECT", (255, 255, 255), [lambda: player.switch_vehicle(self.items[self.index].name)])
        self.scooter_buy = Button((WIDTH/2 - 60, 450), 50, "500$", (255, 255, 255), [lambda: buy_vehicle(500, vehicles["scooter"])])
        self.items = items
        self.index = 0
        self.item = self.items[self.index]

    def right(self):
        if self.index == len(self.items) - 1:
            self.index = 0
        else:
            self.index += 1

    def left(self):
        if self.index == 0:
            self.index = len(self.items) - 1
        else:
            self.index -= 1

    def update(self):
        self.item = self.items[self.index]
        image = self.item.image
        display.blit(image, (self.pos[0]-image.get_width()/2, self.pos[1]))


vehicle_select = Select((WIDTH/2, HEIGHT/2 - 150), (WIDTH/2 - 130, HEIGHT/2 - 60), (WIDTH/2 + 105, HEIGHT/2 - 60), 50, list(vehicles.values()))


buttons = {
    States.MAIN_MENU: [
        Button((100, 200), 75, "PLAY", (255, 255, 255), [lambda: game.set_state(States.PLAY), lambda: game.reset(), lambda: map_.reset(), lambda: player.reset(), lambda: player.vehicle.reset()]),
        Button((100, 300), 50, "VEHICLES", (255, 255, 255), [lambda: game.set_state(States.VEHICLES)]),
        Button((100, 375), 50, "SETTINGS", (255, 255, 255), [lambda: game.set_state(States.SETTINGS)]),
    ],
    States.PLAY: [
        Button((WIDTH/2-156, 300), 30, "CLICK TO CONTINUE", (255, 255, 255), [lambda: game.set_state(States.MAIN_MENU)])
    ],
    States.VEHICLES: [
        Button((100, 100), 40, "BACK", (255, 255, 255), [lambda: game.set_state(States.MAIN_MENU)]),
        vehicle_select.select_button,
        vehicle_select.right_arrow,
        vehicle_select.left_arrow,
        vehicle_select.scooter_buy,
    ],
    States.SETTINGS: [
        Button((100, 100), 40, "BACK", (255, 255, 255), [lambda: game.set_state(States.MAIN_MENU)])
    ]
}

