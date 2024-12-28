from src.settings import *
from src.engine import *
from src.player import *
from src.vehicles import *


def main():
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)

        display.fill((0, 150, 8))

        for event in pygame.event.get():
            player.process_event(event)
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
        
        player.update()
        
        window.blit(display, (0, 0))

    pygame.quit()

main()