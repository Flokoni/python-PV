import pygame, sys, random
from racer import Player, Enemy, Collectible, Obstacle, get_asset
from ui import UI
from persistence import load_data, save_data


pygame.init()
pygame.mixer.init()


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer TSIS 3")
clock = pygame.time.Clock()

LB_FILE = "leaderboard.json"
SET_FILE = "settings.json"

def play_safe_sound(sound_name, settings):
    """Безопасное воспроизведение звука (защита от краша при неверном формате)"""
    if settings.get('sound_on', True):
        try:
            path = get_asset(sound_name)
            sound = pygame.mixer.Sound(path)
            sound.set_volume(0.5)
            sound.play()
        except Exception as e:
            print(f"Не удалось воспроизвести {sound_name}: {e}")

def run_game(user_name, settings):
    SCORE = 0
    COINS = 0
    BASE_SPEED = 5 + (settings.get('difficulty', 2) * 1) 
    BG_SPEED = BASE_SPEED
    
    nitro_timer = 0
    nitro_active = False

    P1 = Player(settings.get('car_color', 'green'))
    E1 = Enemy(BASE_SPEED)
    
    enemies = pygame.sprite.Group(E1)
    items = pygame.sprite.Group()
    hazards = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(P1, E1)

    if settings.get('sound_on', True):
        try:
            pygame.mixer.music.load(get_asset("background"))
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except: pass

    road_img = pygame.image.load(get_asset("road"))
    road_img = pygame.transform.scale(road_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_y1, bg_y2 = 0, -SCREEN_HEIGHT

    SPAWN_ITEM = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_ITEM, 1200)
    SPAWN_HAZARD = pygame.USEREVENT + 2
    pygame.time.set_timer(SPAWN_HAZARD, 5000)

    running = True
    while running:
      
        bg_y1 += BG_SPEED
        bg_y2 += BG_SPEED
        if bg_y1 >= SCREEN_HEIGHT: bg_y1 = -SCREEN_HEIGHT
        if bg_y2 >= SCREEN_HEIGHT: bg_y2 = -SCREEN_HEIGHT
        
        DISPLAYSURF.blit(road_img, (0, bg_y1))
        DISPLAYSURF.blit(road_img, (0, bg_y2))

        if nitro_active:
            nitro_timer -= 1
            if nitro_timer <= 0:
                nitro_active = False
                BG_SPEED = BASE_SPEED

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == SPAWN_ITEM:
                t = random.choices(['coin_s', 'coin_b', 'nitro', 'shield', 'repair'], 
                                  weights=[50, 15, 8, 10, 12])[0]
                new_item = Collectible(t)
                items.add(new_item); all_sprites.add(new_item)
            if event.type == SPAWN_HAZARD:
                new_h = Obstacle(BG_SPEED)
                hazards.add(new_h); all_sprites.add(new_h)


        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            if isinstance(entity, Enemy):
                if entity.move(): SCORE += 1
            elif isinstance(entity, (Collectible, Obstacle)):
                entity.move(BG_SPEED)
            else:
                entity.move()

        hit_item = pygame.sprite.spritecollideany(P1, items)
        if hit_item:
            if 'coin' in hit_item.type:
               
                play_safe_sound("money", settings) 
                COINS += hit_item.weight
                BASE_SPEED = 5 + (COINS // 10)
                if not nitro_active: 
                    BG_SPEED = BASE_SPEED
                E1.speed = BASE_SPEED
                
            elif hit_item.type == 'nitro':
                
                play_safe_sound("power", settings) 
                nitro_active = True
                nitro_timer = 180 
                BG_SPEED = BASE_SPEED + 6
                
            elif hit_item.type == 'repair':
            
                play_safe_sound("carrepair", settings) 
                P1.hp = min(100, P1.hp + 20)
                
            elif hit_item.type == 'shield':
               
                play_safe_sound("armour", settings) 
                P1.shield = True
                
            hit_item.kill()
        
        if pygame.sprite.spritecollideany(P1, hazards):
            play_safe_sound("crash", settings)
            P1.hp -= 30
            for h in hazards: h.kill()

        
        if pygame.sprite.spritecollideany(P1, enemies):
            if P1.shield:
                P1.shield = False
                E1.spawn()
            else:
                play_safe_sound("crash", settings)
                P1.hp -= 20
                E1.spawn()
                if P1.hp <= 0:
                    pygame.mixer.music.stop()
                    return COINS

        
        font = pygame.font.SysFont("Verdana", 20)
        DISPLAYSURF.blit(font.render(f"Coins: {COINS}  Score: {SCORE}", True, (0,0,0)), (190, 10))
        pygame.draw.rect(DISPLAYSURF, (255,0,0), (10, 10, 100, 10))
        pygame.draw.rect(DISPLAYSURF, (0,255,0), (10, 10, max(0, P1.hp), 10))
        if P1.shield: pygame.draw.circle(DISPLAYSURF, (0, 255, 255), P1.rect.center, 45, 2)
        if nitro_active: DISPLAYSURF.blit(font.render("NITRO!!!", True, (255, 69, 0)), (10, 30))

        pygame.display.update()
        clock.tick(60)

def main():
    ui = UI(DISPLAYSURF)
    user_name = "Serikbai"
    state = "MENU"
    settings = load_data(SET_FILE, {'sound_on': True, 'car_color': 'green', 'difficulty': 2})
    last_score = 0

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if state == "MENU":
                ui.menu_screen()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: state = "INPUT"
                    if event.key == pygame.K_s: state = "SETTINGS"
                    if event.key == pygame.K_l: state = "LB"

            elif state == "INPUT":
                ui.name_input_screen(user_name)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: state = "GAME"
                    elif event.key == pygame.K_BACKSPACE: user_name = user_name[:-1]
                    else: user_name += event.unicode

            elif state == "SETTINGS":
                ui.settings_screen(settings)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s: settings['sound_on'] = not settings['sound_on']
                    if event.key == pygame.K_c:
                        clrs = ["green", "red", "blue", "black"]
                        settings['car_color'] = clrs[(clrs.index(settings['car_color']) + 1) % 4]
                    if event.key == pygame.K_ESCAPE:
                        save_data(SET_FILE, settings)
                        state = "MENU"

            elif state == "GAMEOVER":
                ui.game_over_screen(last_score)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m: state = "MENU"

            elif state == "LB":
                scores = load_data(LB_FILE, [])
                ui.leaderboard_screen(scores)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: state = "MENU"

        if state == "GAME":
            final_score = run_game(user_name, settings)
            lb_data = load_data(LB_FILE, [])
            lb_data.append({"name": user_name, "score": final_score})
            lb_data = sorted(lb_data, key=lambda x: x['score'], reverse=True)[:10]
            save_data(LB_FILE, lb_data)
            last_score = final_score
            state = "GAMEOVER"

        pygame.display.update()

if __name__ == "__main__":
    main()