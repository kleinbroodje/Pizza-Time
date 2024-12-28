from src.engine import *
from src.vehicles import *

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
            if event.key == pygame.K_e:
                if not self.driving and math.sqrt((self.rect.centerx - self.vehicle.rect.centerx)**2 + (self.rect.centery - self.vehicle.rect.centery)**2) < 20*R:
                    self.driving = True
                else:
                    self.driving = False

    def update(self):
        self.vehicle.update()
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
    
        surf = pygame.Surface((21*R, 29*R))
        surf.set_colorkey((0, 0, 0))
        surf.blit(legs, (0, 0))
        surf.blit(self.body, (0, 0))
        surf.blit(self.head, (0, 0))

        surf_copy = pygame.transform.rotate(surf, angle)

        display.blit(surf_copy, (self.rect.centerx - int(surf_copy.width/2), self.rect.centery - int(surf_copy.height/2)))


player = Player()