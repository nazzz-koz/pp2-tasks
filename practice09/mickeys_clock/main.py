from clock import MickeyClock

def main():
    game = MickeyClock()

    running = True
    while running:
        running = game.update()
        game.draw()

    import pygame
    pygame.quit()


main()