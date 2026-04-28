import pygame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (50, 150, 255)

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font_main = pygame.font.SysFont("Verdana", 40)
        self.font_small = pygame.font.SysFont("Verdana", 20)

    def draw_text(self, text, font, color, x, y):
        img = font.render(text, True, color)
        rect = img.get_rect(center=(x, y))
        self.screen.blit(img, rect)

    def menu_screen(self):
        """Главное меню"""
        self.screen.fill(BLUE)
        self.draw_text("SUPER RACER", self.font_main, WHITE, 200, 150)
        self.draw_text("Press SPACE to Start", self.font_small, WHITE, 200, 300)
        self.draw_text("Press L for Leaderboard", self.font_small, WHITE, 200, 350)
        pygame.display.update()

    def name_input_screen(self, name):
        """Экран ввода имени"""
        self.screen.fill(BLACK)
        self.draw_text("Enter Your Name:", self.font_small, WHITE, 200, 200)
        
        
        pygame.draw.rect(self.screen, WHITE, (100, 250, 200, 40))
        self.draw_text(name, self.font_small, BLACK, 200, 270)
        
        self.draw_text("Press ENTER to Confirm", self.font_small, GRAY, 200, 350)
        pygame.display.update()

    def game_over_screen(self, score):
        """Экран проигрыша"""
        self.screen.fill((150, 0, 0))
        self.draw_text("GAME OVER", self.font_main, WHITE, 200, 150)
        self.draw_text(f"Your Score: {score}", self.font_small, WHITE, 200, 250)
        self.draw_text("Press M for Main Menu", self.font_small, WHITE, 200, 400)
        pygame.display.update()

    def leaderboard_screen(self, scores):
        """Таблица лидеров"""
        self.screen.fill(BLACK)
        self.draw_text("TOP 10 PLAYERS", self.font_small, WHITE, 200, 50)
        
        for i, entry in enumerate(scores):
           
            txt = f"{i+1}. {entry['name']} - {entry['score']}"
            self.draw_text(txt, self.font_small, WHITE, 200, 100 + i*30)
            
        self.draw_text("Press ESC to Back", self.font_small, GRAY, 200, 500)
        pygame.display.update()