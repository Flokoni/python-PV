import pygame
import random
import time


pygame.init()

WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)

WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game PP2')

clock = pygame.time.Clock()

font_style = pygame.font.SysFont("Arial", 25)
score_font = pygame.font.SysFont("Arial", 35)

def display_score(score, level):
    """Функция для вывода счета и уровня на экран"""
    value = score_font.render(f"Score: {score}  Level: {level}", True, YELLOW)
    screen.blit(value, [10, 10])

def draw_snake(block_size, snake_list):
    """Рисуем каждый сегмент змейки"""
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], block_size, block_size])

def gameLoop():
    game_over = False
    
    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    snake_speed = 10
    score = 0
    level = 1

    def generate_food():
        while True:
            fx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 20.0) * 20.0
            fy = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 20.0) * 20.0
            
            if [fx, fy] not in snake_List:
                return fx, fy

    foodx, foody = generate_food()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_over = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)

        
        pygame.draw.rect(screen, RED, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])
        
        
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_over = True

        draw_snake(BLOCK_SIZE, snake_List)
        display_score(score, level) 

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food() 
            Length_of_snake += 1
            score += 1
            
            if score % 3 == 0:
                level += 1
                snake_speed += 3 

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()