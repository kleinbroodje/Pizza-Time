from src.engine import *
from src.map import *


class Vehicle:
    def __init__(self, name, speed, r_max_vel, max_vel, rot_vel, offset):
        self.name = name
        self.image = imgload("assets", "images", f"{name}.png")
        self.rect = pygame.Rect(0, 0, 48*R, 48*R)
        self.mask = pygame.mask.from_surface(self.image)
        self.base_speed = speed
        self.speed = self.base_speed
        self.vel = 0
        self.base_max_vel = max_vel
        self.max_vel = self.base_max_vel
        self.r_max_vel = r_max_vel
        self.rot_vel = rot_vel
        self.angle  = 0
        self.offset = offset
        self.slipping_time = 700 
        self.start_slipping = 0
        self.slipping = False
        self.slipping_angle = 0

    def reset(self):
        self.rect.x, self.rect.y = 0, 0
        self.speed = self.base_speed
        self.max_vel = self.base_max_vel
        self.vel = 0
        self.angle = 0
        self.slipping = False

    def keys(self):
        keys = pygame.key.get_pressed()

        if not self.slipping:
            if keys[pygame.K_a]: 
                self.angle += self.rot_vel

            if keys[pygame.K_d]:
                self.angle -= self.rot_vel

            if keys[pygame.K_w]:
                self.vel = min(self.max_vel, self.vel + self.speed)

            if keys[pygame.K_s]:
                self.vel = max(self.r_max_vel, self.vel - self.speed)
            

    def update(self):
        if self.slipping:
            angle = self.slipping_angle
            self.angle += 17
            if pygame.time.get_ticks() - self.start_slipping > self.slipping_time:
                self.slipping = False
        else:
            angle = self.angle
            
        radians = math.radians(angle)

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

        self.vel = max(0, self.vel - 0.5)

        if not self.slipping:
            for o in map_.obstacles:
                if self.mask.overlap(o.mask, (o.pos[0] - self.rect.x - 33/2, o.pos[1] - self.rect.y)):
                    pygame.mixer.Sound.play(slip_sound)
                    self.start_slipping = pygame.time.get_ticks()
                    self.slipping = True
                    self.vel = 25
                    self.slipping_angle = self.angle

        img_copy = pygame.transform.rotate(self.image, self.angle)
        self.mask = pygame.mask.from_surface(img_copy)
        display.blit(img_copy, (self.rect.centerx - int(img_copy.get_width()/2) - scroll[0], self.rect.centery - int(img_copy.get_height()/2) - scroll[1]))
        #pygame.draw.rect(display, (255, 0, 0), pygame.Rect(self.rect.left-scroll[0], self.rect.top-scroll[1], self.rect.width, self.rect.height), 2)


vehicles = {"bike": Vehicle("bike", 2, -4, 15, 3, 4), "scooter": Vehicle("scooter", 4, -2, 17, 4, -3)}