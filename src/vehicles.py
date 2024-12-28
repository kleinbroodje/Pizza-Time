from src.engine import *


class Vehicle:
    def __init__(self, name, speed, r_max_vel, max_vel, rot_vel):
        self.image = imgload("assets", "images", f"{name}.png")
        self.rect = self.image.get_rect()
        self.speed = speed
        self.vel = 0
        self.max_vel = max_vel
        self.r_max_vel = r_max_vel
        self.rot_vel = rot_vel
        self.angle  = 0

    def keys(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]: 
            self.angle += self.rot_vel

        if keys[pygame.K_d]:
            self.angle -= self.rot_vel

        if keys[pygame.K_w]:
            self.vel = min(self.max_vel, self.vel + self.speed)

        if keys[pygame.K_s]:
            self.vel = max(self.r_max_vel, self.vel - self.speed)

    def update(self):
        radians = math.radians(self.angle)
        self.rect.x += math.sin(radians) * self.vel
        self.rect.y += math.cos(radians) * self.vel
        self.vel = max(0, self.vel - 0.1)

        img_copy = pygame.transform.rotate(self.image, self.angle)
        display.blit(img_copy, (self.rect.centerx - int(img_copy.width/2), self.rect.centery - int(img_copy.height/2)))

vehicles = {"bike": Vehicle("bike", 2, 0, 10, 3)}