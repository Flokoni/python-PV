import pygame
import os
from clock import get_time_angles

pygame.init()
WIDTH, HEIGHT = 800, 800 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock Application")
clock = pygame.time.Clock()

BASE_PATH = os.path.dirname(__file__)
IMAGES_PATH = os.path.join(BASE_PATH, "images")

print(f"Путь к папке: {IMAGES_PATH}")
if os.path.exists(IMAGES_PATH):
    print("Файлы в папке:", os.listdir(IMAGES_PATH))
else:
    print("ПАПКА IMAGES НЕ НАЙДЕНА!")

try:
    # 1. Загружаем
    main_clock = pygame.image.load(os.path.join(IMAGES_PATH, "main-clock.png.png")).convert_alpha()
    right_hand_img = pygame.image.load(os.path.join(IMAGES_PATH, "right-hand.png.png")).convert_alpha()
    left_hand_img = pygame.image.load(os.path.join(IMAGES_PATH, "left-hand.png.jpg")).convert_alpha()
    
    main_clock = pygame.transform.scale(main_clock, (WIDTH, HEIGHT))
    
    right_hand_img = pygame.transform.scale(right_hand_img, (60, 350))
    
    left_hand_img = pygame.transform.scale(left_hand_img, (40, 300))
    
except Exception as e:
    print(f"\nОШИБКА: {e}")
    pygame.quit()
    exit()

def blit_rotate_center(surf, image, center_pos, angle):
    """Вращает картинку и рисует её с центром в center_pos"""
    rotated_image = pygame.transform.rotate(image, angle)
    
    new_rect = rotated_image.get_rect(center=image.get_rect(center=center_pos).center)
    surf.blit(rotated_image, new_rect)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    min_angle, sec_angle = get_time_angles()

    screen.fill((255, 255, 255)) 
    screen.blit(main_clock, (0, 0)) 

    blit_rotate_center(screen, right_hand_img, (400, 400), min_angle)
    blit_rotate_center(screen, left_hand_img, (400, 400), sec_angle)

    pygame.display.flip()
    clock.tick(60) 

pygame.quit()