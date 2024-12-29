from src.settings import *
from src.engine import *
from src.player import *
from src.vehicles import *
from src.map import *


def main():
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)

        display.fill((0, 150, 8))

        true_scroll[0] += (player.rect.x-true_scroll[0]-WIDTH/2+player.rect.width/2)/10
        true_scroll[1] += (player.rect.y-true_scroll[1]-HEIGHT/2+player.rect.height/2)/10
        scroll[0] = int(true_scroll[0])
        scroll[1] = int(true_scroll[1])

        for event in pygame.event.get():
            player.process_event(event)
            if event.type == pygame.QUIT:
                running = False
        
        for tile in road:
            tile.update()

        for house in houses:
            house.update()
        
        player.update()

        fps = pygame.Font.render(fonts[30], f"{int(clock.get_fps())}", True, (255, 255, 255))
        display.blit(fps, (0, 0))
        
        window.blit(display, (0, 0))

        for r in road:
            pygame.draw.rect(window, (0, 0, 0), pygame.Rect(r.position[0]*20 + 1100, r.position[1]*20+100, 20, 20), 2)

        pygame.display.update()

    pygame.quit()

main()