import pygame
from player import MusicPlayer

pygame.init()
screen = pygame.display.set_mode((500, 200))
pygame.display.set_caption("🎶 Music Player")
font = pygame.font.Font(None, 36)

player = MusicPlayer("music")

running = True
clock = pygame.time.Clock()

while running:
    screen.fill((30, 30, 30))
    
    track_text = font.render(f"Track: {player.get_current_track_name()}", True, (255, 255, 255))
    screen.blit(track_text, (20, 50))
    
    if player.is_playing:
        pos_text = font.render(f"Position: {player.get_position():.2f}s", True, (180, 180, 180))
        screen.blit(pos_text, (20, 100))
    
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next_track()
            elif event.key == pygame.K_b:
                player.prev_track()
            elif event.key == pygame.K_q:
                running = False

    clock.tick(30)

pygame.quit()
