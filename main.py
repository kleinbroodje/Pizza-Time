import asyncio #pygbag

from src.settings import *
from src.engine import *
from src.player import *
from src.vehicles import *
from src.map import *
from src.pizza import *
from src.buttons import *


async def main():
    clock = pygame.time.Clock()
    running = True
    prev_countdown = 3
    prev_time = 0

    speed_upgrade_time = 10000
    speed_timer = 0

    upgrade_cooldown = 10000
    last_upgrade = 0

    extra_time = 0

    pygame.mixer.Sound.play(theme_song, -1)
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            player.process_event(event)
            if not (game.state == States.PLAY and not game.game_over):
                for button in buttons[game.state]:
                    if (not(button == vehicle_select.select_button and (player.vehicle == vehicle_select.item or vehicle_select.item not in player.unlocked_vehicles)) and 
                        not(button == vehicle_select.scooter_buy and (vehicles["scooter"] in player.unlocked_vehicles or vehicle_select.item != vehicles["scooter"]))):
                        button.process_event(event)
            if event.type == pygame.QUIT:
                running = False
        
        match game.state:
            
            case States.MAIN_MENU:
                display.fill((0, 0, 0))
                start_time = pygame.time.get_ticks()

            case States.PLAY:
    
                display.fill((84, 143, 43))

                true_scroll[0] += (player.rect.x-true_scroll[0]-WIDTH/2+player.rect.width/2)/10
                true_scroll[1] += (player.rect.y-true_scroll[1]-HEIGHT/2+player.rect.height/2)/10
                scroll[0] = int(true_scroll[0])
                scroll[1] = int(true_scroll[1])
                    
                for tile in map_.road:
                    tile.update()
                
                for obstacle in map_.obstacles:
                    obstacle.update()   

                for house in map_.houses:
                    house.update()
                
                for upgrade in upgrades:
                    upgrade.update() 

                for upgrade in player.upgrades:
                    match upgrade.type:
                        case "speed":
                            player.vehicle.max_vel *= 1.2
                            speed_timer = pygame.time.get_ticks()

                        case "time":
                            extra_time += 5
                    player.upgrades.remove(upgrade)

                if pygame.time.get_ticks() - speed_timer > speed_upgrade_time:
                    player.vehicle.max_vel = player.vehicle.base_max_vel

                player.update(game.started)
                
                minimap_width, minimap_height = 200, 200
                minimap_scale = 0.05
                minimap_scroll[0] += (player.rect.x*minimap_scale-minimap_scroll[0]-minimap_width/2+player.rect.width*minimap_scale/2)
                minimap_scroll[1] += (player.rect.y*minimap_scale-minimap_scroll[1]-minimap_height/2+player.rect.height*minimap_scale/2)
                minimap = pygame.surface.Surface((200, 200))
                for r in map_.road:
                    minimap.blit(pygame.transform.scale_by(r.image, minimap_scale), pygame.Rect(r.position[0]*200*R*minimap_scale-minimap_scroll[0], r.position[1]*200*R*minimap_scale-minimap_scroll[1], 200*R*minimap_scale, 200*R*minimap_scale))
                for h in map_.houses:
                    minimap.blit(pygame.transform.scale_by(h.image, minimap_scale), pygame.Rect(h.position[0]*200*R*minimap_scale-minimap_scroll[0], h.position[1]*200*R*minimap_scale-minimap_scroll[1], 200*R*minimap_scale, 200*R*minimap_scale))
                pygame.draw.rect(minimap, (251, 242, 54), pygame.Rect(player.target_house.position[0]*200*R*minimap_scale-minimap_scroll[0], player.target_house.position[1]*200*R*minimap_scale-minimap_scroll[1], 200*R*minimap_scale, 200*R*minimap_scale), 2)
                if not player.driving:
                    pygame.draw.rect(minimap, (0, 255, 0), pygame.Rect(player.vehicle.rect.x*minimap_scale-minimap_scroll[0], player.vehicle.rect.y*minimap_scale-minimap_scroll[1], player.vehicle.rect.width*minimap_scale, player.vehicle.rect.height*minimap_scale))
                pygame.draw.rect(minimap, (255, 0, 0), pygame.Rect(player.rect.x*minimap_scale-minimap_scroll[0], player.rect.y*minimap_scale-minimap_scroll[1], player.rect.width*minimap_scale, player.rect.height*minimap_scale))
                display.blit(minimap, (1000, 20))

                tips = pygame.Font.render(fonts[30], f"tips: {player.tips}$", True, (255, 255, 255))
                display.blit(tips, (1040, 225))

                if not game.started and not game.ended:
                    countdown = int((game.countdown_time-pygame.time.get_ticks()+start_time)/1000) + extra_time
                    countdown_timer = pygame.Font.render(fonts[50], f"{countdown}", True, (255, 255, 255))
                    display.blit(countdown_timer, (WIDTH/2 - countdown_timer.get_width()/2, HEIGHT/2 - countdown_timer.get_height()/2))
                    if countdown <= 0:
                        game.started = True
                        pygame.mixer.Sound.play(go_sound)
                    elif prev_countdown != countdown and countdown < 3:
                        pygame.mixer.Sound.play(click_sound)
                    prev_countdown = countdown

                if not game.started and game.ended:
                    extra_time = 0
                    time = 1000-pygame.time.get_ticks()+start_time
                    score = pygame.Font.render(fonts[50], f"SCORE: {player.pizzas_delivered}", True, (255, 255, 255))
                    stop_sign = pygame.Font.render(fonts[50], "STOP", True, (255, 255, 255))
                    if time < 0:
                        display.blit(score, (WIDTH/2 - score.get_width()/2, HEIGHT/2 - score.get_height()/2 - 100))
                        game.game_over = True
                    else:
                        display.blit(stop_sign, (WIDTH/2 - stop_sign.get_width()/2, HEIGHT/2 - stop_sign.get_height()/2))

                if game.started:
                    time = int((game.duration-pygame.time.get_ticks()+start_time+game.countdown_time)/1000) + extra_time
                    timer = pygame.Font.render(fonts[30], f"{time}", True, (255, 255, 255))
                    display.blit(timer, (WIDTH/2 - timer.get_width()/2, 0))
                    if time-extra_time > game.duration/1000-1:
                        start_sign = pygame.Font.render(fonts[50], f"GO", True, (255, 255, 255))
                        display.blit(start_sign, (WIDTH/2 - start_sign.get_width()/2, HEIGHT/2 - start_sign.get_height()/2))

    
                    if pygame.time.get_ticks() - last_upgrade > upgrade_cooldown:
                        road = choice(map_.road)
                        upgrades.append(Upgrade(choice(upgrade_types), (randint(road.rect.left, road.rect.right-30*R), randint(road.rect.top, road.rect.bottom-30*R))))
                        last_upgrade = pygame.time.get_ticks()


                    if time <= 0:
                        start_time = pygame.time.get_ticks()
                        pygame.mixer.Sound.play(stop_sound)
                        game.started = False
                        game.ended = True
                    elif prev_time != time and time < 4:
                        pygame.mixer.Sound.play(countdown_sound)

                    prev_time = time

            case States.VEHICLES:
                display.fill((0, 0, 0))
                vehicle_select.update()

            case States.SETTINGS:
                display.fill((0, 0, 0))
        
        if not (game.state == States.PLAY and not game.game_over):
            for button in buttons[game.state]:
                if button == vehicle_select.scooter_buy:
                    if vehicle_select.item != vehicles["scooter"] or vehicles["scooter"] in player.unlocked_vehicles:
                        continue
                if button == vehicle_select.select_button: 
                    if player.vehicle == vehicle_select.item:
                        text = pygame.Font.render(fonts[50], "SELECTED", True, (255, 255, 255))
                        display.blit(text, (WIDTH/2 - 115, 450))
                        continue
                    if vehicle_select.item not in player.unlocked_vehicles:
                        continue
                button.update()

        if game.state != States.PLAY:
            tips = pygame.Font.render(fonts[30], f"tips collected: {player.total_tips}$", True, (255, 255, 255))
            display.blit(tips, (WIDTH/2 - tips.get_width()/2, 0))

        fps = pygame.Font.render(fonts[30], f"{int(clock.get_fps())}", True, (255, 255, 255))
        display.blit(fps, (0, 0))

        window.blit(display, (0, 0))

        pygame.display.update()
        
        await asyncio.sleep(0) #pygbag

    pygame.quit()

asyncio.run(main()) #pygbag