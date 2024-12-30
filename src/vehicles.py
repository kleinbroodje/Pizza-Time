from src.engine import *
from src.map import *


class Vehicle:
    def __init__(self, name, speed, r_max_vel, max_vel, rot_vel):
        self.image = imgload("assets", "images", f"{name}.png")
        self.rect = pygame.Rect(0, 0, 48*R, 48*R)
        self.base_speed = speed
        self.speed = self.base_speed
        self.vel = 0
        self.base_max_vel = max_vel
        self.max_vel = self.base_max_vel
        self.r_max_vel = r_max_vel
        self.rot_vel = rot_vel
        self.angle  = 0

    def reset(self):
        self.rect.x, self.rect.y = 0, 0
        self.speed = self.base_speed
        self.max_vel = self.base_max_vel
        self.vel = 0
        self.angle = 0

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

        self.vel_x = math.sin(radians) * self.vel
        self.rect.x +=  self.vel_x

        for o in map_.houses:
            if self.rect.colliderect(o.rect): 
                if self.vel_x > 0:
                    self.rect.right = o.rect.left
                if self.vel_x < 0:
                    self.rect.left = o.rect.right

        self.vel_y = math.cos(radians) * self.vel
        self.rect.y += self.vel_y

        for o in map_.houses:
            if self.rect.colliderect(o.rect): 
                if self.vel_y > 0:
                    self.rect.bottom = o.rect.top
                if self.vel_y < 0:
                    self.rect.top = o.rect.bottom

        self.vel = max(0, self.vel - 0.1)

        img_copy = pygame.transform.rotate(self.image, self.angle)
        display.blit(img_copy, (self.rect.centerx - int(img_copy.width/2) - scroll[0], self.rect.centery - int(img_copy.height/2) - scroll[1]))


vehicles = {"bike": Vehicle("bike", 2, 0, 10, 3)}