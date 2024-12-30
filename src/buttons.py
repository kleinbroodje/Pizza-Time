from src.engine import *
from src.player import *


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
            rect = text.get_rect(midleft=self.text_rect.midleft)
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

buttons = {
    States.MAIN_MENU: [
        Button((100, 100), 50, "PLAY", (255, 255, 255), [lambda: game.set_state(States.PLAY), lambda: game.reset(), lambda: map_.reset(), lambda: player.reset(), lambda: player.vehicle.reset()]),
        Button((100, 175), 50, "VEHICLES", (255, 255, 255), [lambda: game.set_state(States.PLAY)]),
        Button((100, 255), 50, "SETTINGS", (255, 255, 255), [lambda: game.set_state(States.PLAY)]),
    ],
    States.PLAY: [
        Button((WIDTH/2-160, 300), 30, "CLICK TO CONTINUE", (255, 255, 255), [lambda: game.set_state(States.MAIN_MENU)])
    ]
}