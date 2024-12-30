from src.engine import *
from src.vehicles import *
from src.pizza import *
from src.map import *


class Player:
    def __init__(self):
        self.rect = pygame.Rect(10, 10, 21*R, 21*R)
        self.head = imgload("assets", "images", "head.png")
        self.body = imgload("assets", "images", "body.png")
        self.legs = imgload("assets", "images", "legs.png", columns=12)
        self.arrow = imgload("assets", "images", "arrow.png")
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 7
        self.running = False
        self.current_frame = 0
        self.vehicle = vehicles["bike"]
        self.driving = False
        self.mountable = False
        self.pizza = None
        self.deliverable = False
        self.target_house = choice(houses)
        self.pizzas_delivered = 0
        self.angle = 0

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
                if self.mountable and not self.pizza:
                    self.driving = True
                else:
                    self.driving = False
            if event.key == pygame.K_e:
                if self.deliverable:
                    pygame.mixer.Sound.play(point_sound)
                    self.pizza = None
                    self.pizzas_delivered += 1
                    self.target_house = choice(houses)
                elif self.mountable:
                    if not self.pizza:
                        self.pizza = Pizza()
                    else:
                        self.pizza = None

    def draw_arrow(self):
        angle = math.degrees(math.atan2(self.rect.centery - self.target_house.rect.centery, self.rect.centerx - self.target_house.rect.centerx))*-1+90
        arrow = pygame.transform.rotate(self.arrow, angle)
        dx = R * 40 * math.sin(math.radians(angle))
        dy  = R * 40 * math.cos(math.radians(angle))
        display.blit(arrow, (self.rect.centerx - dx - int(arrow.width/2) - scroll[0], self.rect.centery - dy - int(arrow.height/2) - scroll[1]))

    def draw(self):
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

        surf_copy = pygame.transform.rotate(surf, self.angle)

        display.blit(surf_copy, (self.rect.centerx - int(surf_copy.width/2) - scroll[0], self.rect.centery - int(surf_copy.height/2) - scroll[1]))

    def update(self, game_started):
        self.vehicle.update()

        self.running = False
        self.draw_arrow()
        if game_started:
            if not self.driving and math.sqrt((self.rect.centerx - self.vehicle.rect.centerx)**2 + (self.rect.centery - self.vehicle.rect.centery)**2) < 20*R:
                self.mountable = True
                if not self.pizza:
                    text1 = pygame.Font.render(fonts[30], "Press <Q> to drive", True, (255, 255, 255))
                    display.blit(text1, (WIDTH/2 - text1.width/2, HEIGHT*2/3))
                    text2 = pygame.Font.render(fonts[30], "Press <E> to grab pizza", True, (255, 255, 255))
                    display.blit(text2, (WIDTH/2 - text2.width/2, HEIGHT*3/4))
                elif not self.deliverable:
                    text2 = pygame.Font.render(fonts[30], "Press <E> to put back pizza", True, (255, 255, 255))
                    display.blit(text2, (WIDTH/2 - text2.width/2, HEIGHT*3/4))
            else:
                self.mountable = False

            self.keys()

            self.rect.x += self.vel_x

            for o in houses:
                if self.rect.colliderect(o.rect): 
                    if self.vel_x > 0:
                        self.rect.right = o.rect.left
                    if self.vel_x < 0:
                        self.rect.left = o.rect.right

            self.rect.y += self.vel_y

            for o in houses:
                if self.rect.colliderect(o.rect): 
                    if self.vel_y > 0:
                        self.rect.bottom = o.rect.top
                    if self.vel_y < 0:
                        self.rect.top = o.rect.bottom
            
            self.deliverable = False
            if self.rect.colliderect(self.target_house.door_rect) and self.pizza:
                text2 = pygame.Font.render(fonts[30], "Press <E> to deliver pizza", True, (255, 255, 255))
                display.blit(text2, (WIDTH/2 - text2.width/2, HEIGHT*3/4))
                self.deliverable = True

            if self.driving:
                self.running = False
                self.vehicle.keys()
                self.angle = self.vehicle.angle
                self.rect.centerx = self.vehicle.rect.centerx - R * 4 * math.sin(math.radians(self.angle))
                self.rect.centery = self.vehicle.rect.centery - R * 4 * math.cos(math.radians(self.angle))
            else:
                self.angle = math.degrees(math.atan2(self.rect.centery - (pygame.mouse.get_pos()[1]+scroll[1]), self.rect.centerx - (pygame.mouse.get_pos()[0]+scroll[0]))) * -1 - 90
        
        self.draw()

player = Player()