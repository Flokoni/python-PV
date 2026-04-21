import pygame
import math

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
    """Инструкция: отображаем текущий цвет и режим"""
    font = pygame.font.SysFont("Arial", 16)
    text = "Цвета: 1:Red 2:Green 3:Blue 0:Black | Фигуры: L:Line R:Rect S:Square T:Right_Tri G:Equi_Tri H:Rhombus E:Eraser"
    img = font.render(text, True, BLACK)
    
    pygame.draw.rect(screen, current_color, (10, 35, 20, 20)) 
    screen.blit(img, (10, 10))

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
            
            
            if event.key == pygame.K_l: mode = 'line'
            if event.key == pygame.K_r: mode = 'rect'
            if event.key == pygame.K_c: mode = 'circle'
            if event.key == pygame.K_s: mode = 'square'
            if event.key == pygame.K_t: mode = 'right_tri'
            if event.key == pygame.K_g: mode = 'equi_tri'
            if event.key == pygame.K_h: mode = 'rhombus'
            if event.key == pygame.K_e: mode = 'eraser'

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos 
            
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = event.pos
        
                if mode == 'rect':
                    pygame.draw.rect(canvas, current_color, (start_pos[0], start_pos[1], end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]), 2)
                elif mode == 'square':
                    side = max(abs(end_pos[0]-start_pos[0]), abs(end_pos[1]-start_pos[1]))
                    pygame.draw.rect(canvas, current_color, (start_pos[0], start_pos[1], side, side), 2)
                elif mode == 'circle':
                    radius = int(math.hypot(end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 2)
                elif mode == 'right_tri':
                    pygame.draw.polygon(canvas, current_color, [start_pos, end_pos, (start_pos[0], end_pos[1])], 2)
                elif mode == 'equi_tri':
                    h = (end_pos[1] - start_pos[1])
                    pts = [start_pos, (start_pos[0] - h/1.73, end_pos[1]), (start_pos[0] + h/1.73, end_pos[1])]
                    pygame.draw.polygon(canvas, current_color, pts, 2)
                elif mode == 'rhombus':
                    dx, dy = end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]
                    pts = [(start_pos[0]+dx, start_pos[1]), (start_pos[0], start_pos[1]+dy), (start_pos[0]-dx, start_pos[1]), (start_pos[0], start_pos[1]-dy)]
                    pygame.draw.polygon(canvas, current_color, pts, 2)
                drawing = False

        if event.type == pygame.MOUSEMOTION and drawing:
            if mode == 'line': pygame.draw.circle(canvas, current_color, event.pos, 3)
            elif mode == 'eraser': pygame.draw.circle(canvas, WHITE, event.pos, 20)

    if drawing:
        cp = pygame.mouse.get_pos()
        if mode == 'rect':
            pygame.draw.rect(screen, current_color, (start_pos[0], start_pos[1], cp[0]-start_pos[0], cp[1]-start_pos[1]), 2)
        elif mode == 'square':
            s = max(abs(cp[0]-start_pos[0]), abs(cp[1]-start_pos[1]))
            pygame.draw.rect(screen, current_color, (start_pos[0], start_pos[1], s, s), 2)
        elif mode == 'rhombus':
            dx, dy = cp[0]-start_pos[0], cp[1]-start_pos[1]
            pygame.draw.polygon(screen, current_color, [(start_pos[0]+dx, start_pos[1]), (start_pos[0], start_pos[1]+dy), (start_pos[0]-dx, start_pos[1]), (start_pos[0], start_pos[1]-dy)], 2)

    draw_menu()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()