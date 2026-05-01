import pygame, sys
from pygame.locals import *

from persistence import load_settings, save_settings, add_entry
from ui          import main_menu, username_entry, settings_screen, \
                        leaderboard_screen, game_over_screen
from racer       import run_game

WIDTH, HEIGHT = 400, 600


def main():
    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racer – TSIS 3")

    settings = load_settings()
    username = "Player"

    action = "menu"

    while True:
        if action == "menu":
            action = main_menu(display)

        elif action == "play":
            username = username_entry(display)
            action = "game"

        elif action == "game":
            score, distance, coins = run_game(display, settings)
            add_entry(username, score, distance)
            action = game_over_screen(display, score, distance, coins)

        elif action == "retry":
            score, distance, coins = run_game(display, settings)
            add_entry(username, score, distance)
            action = game_over_screen(display, score, distance, coins)

        elif action == "leaderboard":
            leaderboard_screen(display)
            action = "menu"

        elif action == "settings":
            settings = settings_screen(display)
            save_settings(settings)
            action = "menu"

        elif action == "quit":
            pygame.quit()
            sys.exit()

        else:
            action = "menu"


if __name__ == "__main__":
    main()
