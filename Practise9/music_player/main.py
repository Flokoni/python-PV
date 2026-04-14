import pygame
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Music Player")

font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)

player = MusicPlayer("music")

running = True
while running:
    screen.fill((30, 30, 30)) # Темный фон

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: # Play
                player.play()
            elif event.key == pygame.K_s: # Stop
                player.stop()
            elif event.key == pygame.K_n: # Next
                player.next_track()
            elif event.key == pygame.K_b: # Back/Previous
                player.prev_track()
            elif event.key == pygame.K_q: # Quit
                running = False

    status = "Playing" if player.is_playing else "Stopped"
    track_info = player.get_current_track_name()

    img_status = font.render(f"Status: {status}", True, (255, 255, 255))
    img_track = font.render(f"Track: {track_info}", True, (0, 255, 0))
    img_hint = small_font.render("P: Play | S: Stop | N: Next | B: Back | Q: Quit", True, (150, 150, 150))

    screen.blit(img_status, (50, 100))
    screen.blit(img_track, (50, 150))
    screen.blit(img_hint, (50, 300))

    pygame.display.flip()

pygame.quit()