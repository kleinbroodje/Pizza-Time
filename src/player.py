from src.engine import *
from src.vehicles import *
from src.pizza import *


class Player:
    def __init__(self):
        self.rect = pygame.Rect(10, 10, 21*R, 21*R)
        self.head = imgload("assets", "images", "head.png")
        self.body = imgload("assets", "images", "body.png")
        self.legs = imgload("assets", "images", "legs.png", columns=12)
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 7
        self.running = False
        self.current_frame = 0
        self.vehicle = vehicles["bike"]
        self.driving = False
        self.mountable = False
        self.pizzas = [Pizza()]
        self.pizza = None

    def keys(self):
        keys = pygame.key.get_pressed()
        self.vel_x, self.vel_y = 0, 0
        self.running = False

        if keys[pygame.K_a]:
            self.vel_x = -self.speed
            self.running = True

        if keys[pygame.K_d]:
            self.vel_x = self.speed
            self.running = True

        if keys[pygame.K_w]:
            self.vel_y = -self.speed
            self.running = True

        if keys[pygame.K_s]:
            self.vel_y = self.speed
            self.running = True

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                if self.mountable:
                    self.driving = True
                else:
                    self.driving = False
            if event.key == pygame.K_e and self.mountable:
                if not self.pizza:
                    self.pizza = self.pizzas[0]
                else:
                    self.pizzas.append(self.pizza)
                    self.pizza = None

    def update(self):
        self.vehicle.update()

        if not self.driving and math.sqrt((self.rect.centerx - self.vehicle.rect.centerx)**2 + (self.rect.centery - self.vehicle.rect.centery)**2) < 20*R:
            self.mountable = True
            text1 = pygame.Font.render(fonts[30], "Press <Q> to drive", True, (255, 255, 255))
            text2 = pygame.Font.render(fonts[30], "Press <E> to grab pizza", True, (255, 255, 255))
            display.blit(text1, (WIDTH/2 - text1.width/2, HEIGHT*2/3))
            display.blit(text2, (WIDTH/2 - text2.width/2, HEIGHT*3/4))
        else:
            self.mountable = False

        self.keys()

        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if self.driving:
            self.running = False
            self.vehicle.keys()
            angle = self.vehicle.angle
            self.rect.centerx = self.vehicle.rect.centerx - R * 4 * math.sin(math.radians(angle))
            self.rect.centery = self.vehicle.rect.centery - R * 4 * math.cos(math.radians(angle))
        else:
            angle = math.degrees(math.atan2(self.rect.centery - pygame.mouse.get_pos()[1], self.rect.centerx - pygame.mouse.get_pos()[0])) * -1 - 90

        legs = self.legs[0]
        if self.running:
            if self.current_frame >= 11:
                self.current_frame = 0
            legs = self.legs[int(self.current_frame)]
            self.current_frame += 0.25

        surf = pygame.Surface((21*R, 31*R))
        surf.set_colorkey((0, 0, 0))
        surf.blit(legs, (0, 0))
        surf.blit(self.body, (0, 0))
        if self.pizza:
            surf.blit(self.pizza.image, (4*R, 18*R))
        surf.blit(self.head, (0, 0))

        surf_copy = pygame.transform.rotate(surf, angle)

        display.blit(surf_copy, (self.rect.centerx - int(surf_copy.width/2), self.rect.centery - int(surf_copy.height/2)))


player = Player()