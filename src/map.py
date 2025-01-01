from src.engine import *
from itertools import product


directions = {"down": (0, 1), "right": (1, 0), "up": (0, -1), "left": (-1, 0)}
opposite = {"up": "down", "down": "up", "left": "right", "right": "left"}


class Tile:
    def __init__(self, position):
        self.connections = {"left": None, "right": None, "up": None, "down": None}
        self.position = position  
        self.image = imgload("assets", "images", "road_0.png")
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0] * 200 * R
        self.rect.y = self.position[1] * 200 * R
    
    def get_connection_type(self):
        combinations = list(product([Tile, type(None)], repeat=4))
        
        self.combination = (type(self.connections["left"]), type(self.connections["right"]), type(self.connections["up"]), type(self.connections["down"]))
        return combinations.index(self.combination)
    
    def connect(self, tile, direction):
        self.connections[direction] = tile
        tile.connections[opposite[direction]] = self

    def update(self):
        display.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))


class House:
    def __init__(self, direction, position):
        self.image = imgload("assets", "images", "house.png")
        self.images = {"right": self.image, 
                       "left": pygame.transform.rotate(self.image, 180), 
                       "up": pygame.transform.rotate(self.image, 90), 
                       "down": pygame.transform.rotate(self.image, 270),
                       }
        self.image = self.images[direction]
        self.position = position
        self.image_rect = self.image.get_rect()
        self.image_rect.x = self.position[0] * 200 * R
        self.image_rect.y = self.position[1] * 200 * R
        self.rect = pygame.Rect(0, 0, 138*R, 138*R)
        self.rect.centerx, self.rect.centery = self.image_rect.centerx, self.image_rect.centery
        self.door_rect = pygame.Rect(0, 0, 30*R, 30*R)

        match direction:
            case "right":
                self.door_rect.centery = self.rect.centery
                self.door_rect.centerx = self.rect.centerx + 82*R
            case "left":
                self.door_rect.centery = self.rect.centery
                self.door_rect.centerx = self.rect.centerx - 82*R
            case "up":
                self.door_rect.centery = self.rect.centery - 82*R
                self.door_rect.centerx = self.rect.centerx 
            case "down":
                self.door_rect.centery = self.rect.centery + 82*R
                self.door_rect.centerx = self.rect.centerx 
        
    def update(self):
        display.blit(self.image, (self.image_rect.x - scroll[0], self.image_rect.y - scroll[1]))


class Puddle():
    def __init__(self, pos) -> None:
        self.pos = pos
        self.image = imgload("assets", "images", "puddle.png")
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        display.blit(self.image, (self.pos[0]-scroll[0], self.pos[1]-scroll[1]))


def generate_road(num_tiles):
    start = Tile((0, 0))
    road = [start]
    position_tile = {start.position: start}

    while len(road) < num_tiles:
        connected_tile = choice(road) 

        directions_list = list(directions.keys())
    
        if (connected_tile.position[0] + 1, connected_tile.position[1] - 1) in position_tile.keys():
            if (connected_tile.position[0] + 1, connected_tile.position[1]) in position_tile.keys():
                directions_list.remove("up")
            if (connected_tile.position[0], connected_tile.position[1] - 1) in position_tile.keys():
                directions_list.remove("right")
        if (connected_tile.position[0] - 1, connected_tile.position[1] + 1) in position_tile.keys():
            if (connected_tile.position[0] - 1, connected_tile.position[1]) in position_tile.keys():
                directions_list.remove("down")
            if (connected_tile.position[0], connected_tile.position[1] + 1) in position_tile.keys():
                directions_list.remove("left")
        if (connected_tile.position[0] - 1, connected_tile.position[1] - 1) in position_tile.keys():
            if (connected_tile.position[0] - 1, connected_tile.position[1]) in position_tile.keys() and ("up" in directions_list):
                directions_list.remove("up")
            if (connected_tile.position[0], connected_tile.position[1] - 1) in position_tile.keys() and ("left" in directions_list):
                directions_list.remove("left")
        if (connected_tile.position[0] + 1, connected_tile.position[1] + 1) in position_tile.keys():
            if (connected_tile.position[0] + 1, connected_tile.position[1]) in position_tile.keys() and ("down" in directions_list):
                directions_list.remove("down")
            if (connected_tile.position[0], connected_tile.position[1] + 1) in position_tile.keys() and ("right" in directions_list):
                directions_list.remove("right")

        for d in directions_list:
            if connected_tile.connections[d]:
                directions_list.remove(d)

        if not directions_list:
            continue

        direction = choice(directions_list)

        new_tile = Tile((connected_tile.position[0] + directions[direction][0], connected_tile.position[1] + directions[direction][1]))  
        if new_tile.position not in position_tile.keys():
            connected_tile.connect(new_tile, direction)
            position_tile[new_tile.position] = new_tile
            road.append(new_tile)
        
    for position, tile in position_tile.items():
        for direction, (dx, dy) in directions.items():
            neighbor_position = (position[0] + dx, position[1] + dy)
            if neighbor_position in position_tile.keys():
                neighbor_room = position_tile[neighbor_position]
                if not tile.connections[direction]:
                    tile.connect(neighbor_room, direction)
    
    for tile in road:
        tile.image =  imgload("assets", "images", f"road_{tile.get_connection_type()}.png")

    return road


def generate_houses(road):
    road_copy = road.copy()
    houses = []
    positions = []

    while road_copy:
        current_tile = choice(road_copy)
        for k, v in current_tile.connections.items():
            if not v:
                new_position = (current_tile.position[0] + directions[k][0], current_tile.position[1] + directions[k][1])
                if new_position not in positions:
                    new_house = House(opposite[k], new_position)
                    houses.append(new_house)
                    positions.append(new_house.position)
        road_copy.remove(current_tile)
        
    return houses


def generate_obstacles(road):
    obstacles = []
    for r in road:
        obstacles.append(Puddle((randint(r.rect.left, r.rect.right-35*R), randint(r.rect.top, r.rect.bottom-32*R))))
    return obstacles


class Map:
    def __init__(self):
        self.road = generate_road(10)
        self.houses = generate_houses(self.road)
        self.obstacles = generate_obstacles(self.road)

    def reset(self):
        self.road = generate_road(10)
        self.houses = generate_houses(self.road)
        self.obstacles = generate_obstacles(self.road)

map_ = Map()