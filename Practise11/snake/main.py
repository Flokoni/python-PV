import pygame
import random
import time

pygame.init()


WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)      
ORANGE = (255, 165, 0)   
GREEN = (0, 255, 0)

WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game Practise 11')

clock = pygame.time.Clock()
score_font = pygame.font.SysFont("Arial", 35)

def display_score(score, level):
    value = score_font.render(f"Score: {score}  Level: {level}", True, YELLOW)
    screen.blit(value, [10, 10])

def draw_snake(block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], block_size, block_size])

def gameLoop():
    game_over = False
    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_change, y1_change = 0, 0

    snake_List = []
    Length_of_snake = 1
    snake_speed = 10
    score, level = 0, 1

    def generate_food():
        fx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 20.0) * 20.0
        fy = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 20.0) * 20.0
        
        if random.random() < 0.2:
            f_color = ORANGE
            f_weight = 3
        else:
            f_color = RED
            f_weight = 1
            
        f_time = pygame.time.get_ticks() 
        return fx, fy, f_color, f_weight, f_time

    foodx, foody, food_color, food_weight, food_spawn_time = generate_food()
    FOOD_TIMEOUT = 5000 

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change, y1_change = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change, y1_change = BLOCK_SIZE, 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change, x1_change = -BLOCK_SIZE, 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change, x1_change = BLOCK_SIZE, 0

        current_time = pygame.time.get_ticks()
        if current_time - food_spawn_time > FOOD_TIMEOUT:
            foodx, foody, food_color, food_weight, food_spawn_time = generate_food()

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_over = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)
        
        pygame.draw.rect(screen, food_color, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])
        
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
            score += food_weight
            Length_of_snake += food_weight 
            
            if score // 5 >= level: 
                level += 1
                snake_speed += 2 
            
            foodx, foody, food_color, food_weight, food_spawn_time = generate_food()

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()