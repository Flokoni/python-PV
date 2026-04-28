import pygame
import random
import os

def get_asset(name):
    """
    Универсальная функция поиска ассетов.
    Проверяет разные варианты расширений, которые могут быть у файлов.
    """
    for ext in ["", ".png", ".png.png", ".mp3", ".mp3.mp3"]:
        path = os.path.join("assets", name + ext)
        if os.path.exists(path):
            return path
    return os.path.join("assets", name)

class Player(pygame.sprite.Sprite):
    def __init__(self, color_name="green"):
        super().__init__()

        img = pygame.image.load(get_asset("Player")).convert_alpha()
        img = pygame.transform.rotate(img, 180)
        img = pygame.transform.scale(img, (40, 80))
        

        self.image = img.copy()
        colors = {
            "red": (255, 0, 0, 255), 
            "blue": (0, 0, 255, 255), 
            "black": (50, 50, 50, 255)
        }
        
        if color_name in colors:
            tint = pygame.Surface(self.image.get_size()).convert_alpha()
            tint.fill(colors[color_name])

            self.image.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
        self.rect = self.image.get_rect(center=(200, 520))
        self.hp = 100
        self.shield = False

    def move(self):
        """Управление игроком"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 7
        if keys[pygame.K_RIGHT] and self.rect.right < 400:
            self.rect.x += 7

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        img = pygame.image.load(get_asset("Enemy")).convert_alpha()
        self.image = pygame.transform.scale(img, (40, 80))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.spawn()

    def spawn(self):
        """Появление врага в случайной позиции сверху"""
        self.rect.center = (random.randint(40, 360), -100)

    def move(self):
        """Движение врага вниз"""
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.spawn()
            return True 
        return False

class Collectible(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        
        fname = "Coin" if "coin" in type else type
        
        img = pygame.image.load(get_asset(fname)).convert_alpha()
        size = (40, 40) if type == "coin_b" else (30, 30)
        
        self.image = pygame.transform.scale(img, size)
        self.rect = self.image.get_rect(center=(random.randint(40, 360), -50))
        self.weight = 5 if type == "coin_b" else 1

    def move(self, speed_val):
        """Предметы летят со скоростью дороги (BG_SPEED)"""
        self.rect.y += speed_val
        if self.rect.top > 600:
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        img = pygame.image.load(get_asset("barrier")).convert_alpha()
        self.image = pygame.transform.scale(img, (50, 30))
        self.rect = self.image.get_rect(center=(random.randint(50, 350), -100))
        self.speed = speed

    def move(self, speed_val):
        """
        ИСПРАВЛЕНО: Теперь метод принимает скорость дороги.
        Барьеры будут улетать вниз синхронно с разметкой.
        """
        self.rect.y += speed_val
        if self.rect.top > 600:
            self.kill()