import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

current_color = BLACK
mode = 'line'  
start_pos = None
drawing = False

canvas = pygame.Surface((800, 600))
canvas.fill(WHITE)

def draw_menu():
    """Рисуем простую инструкцию в углу экрана"""
    font = pygame.font.SysFont("Arial", 18)
    text = font.render("L: Line | R: Rect | C: Circle | E: Eraser | 1: Red | 2: Green | 3: Blue", True, BLACK)
    screen.blit(text, (10, 10))

running = True
while running:
    screen.fill(WHITE) 
    screen.blit(canvas, (0, 0)) 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: current_color = RED
            if event.key == pygame.K_2: current_color = GREEN
            if event.key == pygame.K_3: current_color = BLUE
            if event.key == pygame.K_0: current_color = BLACK
            # Выбор режима
            if event.key == pygame.K_l: mode = 'line'
            if event.key == pygame.K_r: mode = 'rect'
            if event.key == pygame.K_c: mode = 'circle'
            if event.key == pygame.K_e: mode = 'eraser'

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos 
            
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = event.pos
                if mode == 'rect':
                    width = end_pos[0] - start_pos[0]
                    height = end_pos[1] - start_pos[1]
                    pygame.draw.rect(canvas, current_color, (start_pos[0], start_pos[1], width, height), 2)
                elif mode == 'circle':
                    radius = int(((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2)**0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 2)
                drawing = False

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                if mode == 'line':
                    pygame.draw.circle(canvas, current_color, event.pos, 3)
                elif mode == 'eraser':
                    pygame.draw.circle(canvas, WHITE, event.pos, 20)

    if drawing:
        curr_pos = pygame.mouse.get_pos()
        if mode == 'rect':
            w = curr_pos[0] - start_pos[0]
            h = curr_pos[1] - start_pos[1]
            pygame.draw.rect(screen, current_color, (start_pos[0], start_pos[1], w, h), 2)
        elif mode == 'circle':
            r = int(((curr_pos[0] - start_pos[0])**2 + (curr_pos[1] - start_pos[1])**2)**0.5)
            pygame.draw.circle(screen, current_color, start_pos, r, 2)

    draw_menu()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()