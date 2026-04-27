import pygame
import math
from datetime import datetime
from tools import flood_fill  

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("TSIS 2: Advanced Paint")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


current_color = BLACK
mode = 'pencil'
thickness = 2
drawing = False
start_pos = None
last_pos = None


typing = False
text_content = ""
text_pos = (0, 0)

canvas = pygame.Surface((800, 600))
canvas.fill(WHITE)

def draw_menu():
    """Верхняя панель управления"""
    pygame.draw.rect(screen, (230, 230, 230), (0, 0, 800, 45))
    font = pygame.font.SysFont("Arial", 12)
    
    line1 = "Colors: F1:Red F2:Green F3:Blue F4:Black | Size: 1, 2, 3 | Save: Ctrl+S"
    line2 = "Tools: P:Pencil L:Line R:Rect C:Circle S:Square T:Right_Tri G:Equi_Tri H:Rhombus F:Fill X:Text E:Eraser"
    
    img1 = font.render(line1, True, BLACK)
    img2 = font.render(line2, True, BLACK)
    
    pygame.draw.rect(screen, current_color, (10, 10, 25, 25))
    screen.blit(img1, (45, 5))
    screen.blit(img2, (45, 22))

running = True
while running:
    screen.fill(WHITE)
    screen.blit(canvas, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if typing:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    font_text = pygame.font.SysFont("Arial", 20 + thickness * 2)
                    rendered_text = font_text.render(text_content, True, current_color)
                    canvas.blit(rendered_text, text_pos)
                    typing = False
                    text_content = ""
                elif event.key == pygame.K_ESCAPE:
                    typing = False
                    text_content = ""
                elif event.key == pygame.K_BACKSPACE:
                    text_content = text_content[:-1]
                else:
                    text_content += event.unicode
            continue

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_F1: current_color = RED
            if event.key == pygame.K_F2: current_color = GREEN
            if event.key == pygame.K_F3: current_color = BLUE
            if event.key == pygame.K_F4: current_color = BLACK
            
            if event.key == pygame.K_1: thickness = 2
            if event.key == pygame.K_2: thickness = 5
            if event.key == pygame.K_3: thickness = 10
            
            if event.key == pygame.K_p: mode = 'pencil'
            if event.key == pygame.K_l: mode = 'line'
            if event.key == pygame.K_r: mode = 'rect'
            if event.key == pygame.K_c: mode = 'circle'
            if event.key == pygame.K_s: mode = 'square'
            if event.key == pygame.K_t: mode = 'right_tri'
            if event.key == pygame.K_g: mode = 'equi_tri'
            if event.key == pygame.K_h: mode = 'rhombus'
            if event.key == pygame.K_f: mode = 'fill'
            if event.key == pygame.K_x: mode = 'text'
            if event.key == pygame.K_e: mode = 'eraser'

            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                fn = f"paint_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                pygame.image.save(canvas, fn)
                print(f"Canvas saved as {fn}")

        if event.type == pygame.MOUSEBUTTONDOWN:
            if mode == 'fill':
                flood_fill(canvas, event.pos[0], event.pos[1], current_color)
            elif mode == 'text':
                typing = True
                text_pos = event.pos
            else:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos
            
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = event.pos
             
                if mode == 'rect':
                    pygame.draw.rect(canvas, current_color, (min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]), abs(end_pos[0]-start_pos[0]), abs(end_pos[1]-start_pos[1])), thickness)
                elif mode == 'line':
                    pygame.draw.line(canvas, current_color, start_pos, end_pos, thickness)
                elif mode == 'circle':
                    rad = int(math.hypot(end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                    pygame.draw.circle(canvas, current_color, start_pos, rad, thickness)
                elif mode == 'square':
                    side = max(abs(end_pos[0]-start_pos[0]), abs(end_pos[1]-start_pos[1]))
                    pygame.draw.rect(canvas, current_color, (start_pos[0], start_pos[1], side, side), thickness)
                elif mode == 'right_tri':
                    pygame.draw.polygon(canvas, current_color, [start_pos, end_pos, (start_pos[0], end_pos[1])], thickness)
                elif mode == 'equi_tri':
                    h = (end_pos[1] - start_pos[1])
                    pts = [start_pos, (start_pos[0] - h/1.73, end_pos[1]), (start_pos[0] + h/1.73, end_pos[1])]
                    pygame.draw.polygon(canvas, current_color, pts, thickness)
                elif mode == 'rhombus':
                    dx, dy = end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]
                    pts = [(start_pos[0]+dx, start_pos[1]), (start_pos[0], start_pos[1]+dy), (start_pos[0]-dx, start_pos[1]), (start_pos[0], start_pos[1]-dy)]
                    pygame.draw.polygon(canvas, current_color, pts, thickness)
                
                drawing = False

        if event.type == pygame.MOUSEMOTION and drawing:
            if mode == 'pencil':
                pygame.draw.line(canvas, current_color, last_pos, event.pos, thickness)
                last_pos = event.pos
            elif mode == 'eraser':
                pygame.draw.circle(canvas, WHITE, event.pos, thickness * 5)

    if drawing:
        cp = pygame.mouse.get_pos()
        if mode == 'rect':
            pygame.draw.rect(screen, current_color, (min(start_pos[0], cp[0]), min(start_pos[1], cp[1]), abs(cp[0]-start_pos[0]), abs(cp[1]-start_pos[1])), thickness)
        elif mode == 'line':
            pygame.draw.line(screen, current_color, start_pos, cp, thickness)
        elif mode == 'circle':
            r = int(math.hypot(cp[0]-start_pos[0], cp[1]-start_pos[1]))
            pygame.draw.circle(screen, current_color, start_pos, r, thickness)

    if typing:
        f_type = pygame.font.SysFont("Arial", 20 + thickness * 2)
        t_img = f_type.render(text_content + "|", True, current_color)
        screen.blit(t_img, text_pos)

    draw_menu()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()