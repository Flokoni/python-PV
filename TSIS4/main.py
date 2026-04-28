import pygame, sys, json, random
from config import *
import db, game



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake KBTU Edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)

def load_set():
    """Загрузка настроек с защитой от ошибок (KeyError)"""
    try:
        with open("settings.json", "r") as f:
            data = json.load(f)
        
            if "color" not in data: data["color"] = [0, 255, 0]
            if "grid" not in data: data["grid"] = True
            return data
    except:
        return {"color": [0, 255, 0], "grid": True}

def main():
    db.init_db()
    sets = load_set()
    state = "MENU"
    user = "Serikbai"
    score = 0
    lvl = 1
    pb = 0


    s = None
    w = None
    foods = []

    while True:
        screen.fill(BLACK)
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if state == "MENU":
            screen.blit(font.render(f"PLAYER: {user}", True, WHITE), (150, 180))
            screen.blit(font.render("Type name & press ENTER to set", True, (120, 120, 120)), (150, 210))
            screen.blit(font.render("SPACE - START GAME", True, GREEN), (150, 300))
            screen.blit(font.render("L - Leaderboard | S - Settings", True, WHITE), (150, 350))
            
            for e in events:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                   
                        score = 0
                        lvl = 1
                        pb = db.get_pb(user)
                        s = game.Snake(sets.get('color', [0, 255, 0]))
                        w = game.Obstacle(lvl, s.body)
                        foods = [game.Food(s.body, w.blocks)]
                        state = "GAME"
                    elif e.key == pygame.K_l: state = "LB"
                    elif e.key == pygame.K_s: state = "SET"
                    elif e.key == pygame.K_BACKSPACE: user = user[:-1]
                    elif e.key == pygame.K_RETURN: pass 
                    else: 
                        if len(user) < 15: user += e.unicode

        elif state == "GAME":
            
            if sets.get('grid', True):
                for x in range(0, WIDTH, CELL):
                    pygame.draw.line(screen, (35, 35, 35), (x, 0), (x, HEIGHT))
                    pygame.draw.line(screen, (35, 35, 35), (0, x), (WIDTH, x))


            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and s.dir[1] == 0: s.dir = [0, -CELL]
                    elif event.key == pygame.K_DOWN and s.dir[1] == 0: s.dir = [0, CELL]
                    elif event.key == pygame.K_LEFT and s.dir[0] == 0: s.dir = [-CELL, 0]
                    elif event.key == pygame.K_RIGHT and s.dir[0] == 0: s.dir = [CELL, 0]

            s.move(grow=False)
            head = s.body[0]

            if (head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT or 
                head in s.body[1:] or head in w.blocks):
                db.save_res(user, score, lvl)
                state = "OVER"

            for f in foods[:]:
                if head == f.pos:
                    if f.type == "poison":
                        if len(s.body) <= 2: 
                            db.save_res(user, score, lvl); state = "OVER"
                        else: 
                            s.body.pop(); s.body.pop()
                    else:
                        score += 1
                        s.body.append(s.body[-1])
                        if score % 5 == 0:
                            lvl += 1
                            w = game.Obstacle(lvl, s.body) 
                    foods.remove(f)
                    foods.append(game.Food(s.body, w.blocks, random.choice(["normal", "normal", "poison"])))

            
            for b in s.body: pygame.draw.rect(screen, s.color, (b[0], b[1], CELL-2, CELL-2))
            for b in w.blocks: pygame.draw.rect(screen, RED, (b[0], b[1], CELL, CELL))
            for f in foods: pygame.draw.rect(screen, f.colors[f.type], (f.pos[0], f.pos[1], CELL, CELL))
            
            screen.blit(font.render(f"Score: {score}  Lvl: {lvl}  Best: {pb}", True, WHITE), (10, 10))
            pygame.display.update()
            clock.tick(FPS + (lvl * 1)) 
            continue 

        elif state == "OVER":
            screen.blit(font.render("GAME OVER", True, RED), (230, 200))
            screen.blit(font.render(f"Your Score: {score}", True, WHITE), (230, 250))
            screen.blit(font.render("Press M for Menu", True, GREEN), (210, 350))
            for e in events:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_m:
                    state = "MENU"

        elif state == "LB":
            top = db.get_top()
            screen.blit(font.render("TOP 10 PLAYERS", True, YELLOW), (200, 50))
            if top:
                for i, r in enumerate(top[:10]):
                    screen.blit(font.render(f"{i+1}. {r[0]} - {r[1]} (Lvl {r[2]})", True, WHITE), (150, 100 + i*35))
            screen.blit(font.render("Press ESC to Back", True, GREEN), (150, 520))
            for e in events:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE: state = "MENU"

        elif state == "SET":
            screen.blit(font.render("SETTINGS", True, YELLOW), (220, 50))
            screen.blit(font.render(f"1. Toggle Grid: {'ON' if sets['grid'] else 'OFF'}", True, WHITE), (150, 200))
            screen.blit(font.render(f"2. Snake Color: {sets['color']}", True, WHITE), (150, 250))
            screen.blit(font.render("ESC - Save & Back", True, GREEN), (150, 400))
            for e in events:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_1: sets['grid'] = not sets['grid']
                    if e.key == pygame.K_2: sets['color'] = [random.randint(50,255) for _ in range(3)]
                    if e.key == pygame.K_ESCAPE:
                        with open("settings.json", "w") as f: json.dump(sets, f)
                        state = "MENU"

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()