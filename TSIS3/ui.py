import pygame
from pygame.locals import *
from persistence import load_leaderboard, load_settings, save_settings

BLACK  = (0,   0,   0)
WHITE  = (255, 255, 255)
GRAY   = (180, 180, 180)
DARK   = (30,  30,  30)
ACCENT = (255, 200,  0)
RED    = (220,  50,  50)
GREEN  = (50,  200,  80)
BLUE   = (50,  120, 220)

WIDTH, HEIGHT = 400, 600


def _font(size):
    return pygame.font.SysFont("Arial", size, bold=True)


def _draw_button(surface, rect, text, base_color, text_color=BLACK, hover=False):
    color = tuple(min(c + 30, 255) for c in base_color) if hover else base_color
    pygame.draw.rect(surface, color, rect, border_radius=8)
    pygame.draw.rect(surface, BLACK, rect, 2, border_radius=8)
    label = _font(22).render(text, True, text_color)
    surface.blit(label, label.get_rect(center=rect.center))


def _button_hovered(rect):
    return rect.collidepoint(pygame.mouse.get_pos())


def main_menu(display):
    clock = pygame.time.Clock()
    title_font = _font(52)
    buttons = {
        "play":        pygame.Rect(100, 200, 200, 50),
        "leaderboard": pygame.Rect(100, 270, 200, 50),
        "settings":    pygame.Rect(100, 340, 200, 50),
        "quit":        pygame.Rect(100, 410, 200, 50),
    }
    labels = {
        "play": "Play", "leaderboard": "Leaderboard",
        "settings": "Settings", "quit": "Quit",
    }
    colors = {
        "play": GREEN, "leaderboard": BLUE,
        "settings": GRAY, "quit": RED,
    }
    while True:
        display.fill(DARK)
        title = title_font.render("RACER", True, ACCENT)
        display.blit(title, title.get_rect(center=(WIDTH // 2, 110)))
        sub = _font(18).render("Dodge · Collect · Survive", True, GRAY)
        display.blit(sub, sub.get_rect(center=(WIDTH // 2, 165)))

        for key, rect in buttons.items():
            _draw_button(display, rect, labels[key], colors[key],
                         hover=_button_hovered(rect))

        for event in pygame.event.get():
            if event.type == QUIT:
                return "quit"
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                for key, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        return key

        pygame.display.update()
        clock.tick(60)


def username_entry(display):
    clock  = pygame.time.Clock()
    name   = ""
    prompt = _font(26).render("Enter your name:", True, WHITE)
    done_btn = pygame.Rect(125, 360, 150, 48)

    while True:
        display.fill(DARK)
        display.blit(prompt, prompt.get_rect(center=(WIDTH // 2, 220)))

        box = pygame.Rect(80, 270, 240, 48)
        pygame.draw.rect(display, WHITE, box, border_radius=6)
        pygame.draw.rect(display, ACCENT, box, 2, border_radius=6)
        text_surf = _font(28).render(name + "|", True, BLACK)
        display.blit(text_surf, text_surf.get_rect(midleft=(box.x + 8, box.centery)))

        _draw_button(display, done_btn, "Start", GREEN, hover=_button_hovered(done_btn))

        for event in pygame.event.get():
            if event.type == QUIT:
                return "Player"
            if event.type == KEYDOWN:
                if event.key == K_RETURN and name.strip():
                    return name.strip()
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 16 and event.unicode.isprintable():
                    name += event.unicode
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if done_btn.collidepoint(event.pos) and name.strip():
                    return name.strip()

        pygame.display.update()
        clock.tick(60)


def settings_screen(display):
    clock    = pygame.time.Clock()
    settings = load_settings()

    CAR_COLORS    = ["red", "blue", "green"]
    DIFFICULTIES  = ["easy", "normal", "hard"]

    back_btn = pygame.Rect(125, 510, 150, 45)

    def cycle(lst, val, delta=1):
        return lst[(lst.index(val) + delta) % len(lst)]

    arrow_areas = {
        "car_left":   pygame.Rect(60,  260, 40, 35),
        "car_right":  pygame.Rect(300, 260, 40, 35),
        "diff_left":  pygame.Rect(60,  340, 40, 35),
        "diff_right": pygame.Rect(300, 340, 40, 35),
        "sound_btn":  pygame.Rect(150, 420, 100, 35),
    }

    while True:
        display.fill(DARK)
        title = _font(38).render("Settings", True, ACCENT)
        display.blit(title, title.get_rect(center=(WIDTH // 2, 80)))

        label = _font(22).render("Car colour", True, WHITE)
        display.blit(label, label.get_rect(center=(WIDTH // 2, 242)))
        _draw_button(display, arrow_areas["car_left"],  "<", GRAY, hover=_button_hovered(arrow_areas["car_left"]))
        _draw_button(display, arrow_areas["car_right"], ">", GRAY, hover=_button_hovered(arrow_areas["car_right"]))
        val_surf = _font(22).render(settings["car_color"].capitalize(), True, ACCENT)
        display.blit(val_surf, val_surf.get_rect(center=(WIDTH // 2, 277)))

        label2 = _font(22).render("Difficulty", True, WHITE)
        display.blit(label2, label2.get_rect(center=(WIDTH // 2, 322)))
        _draw_button(display, arrow_areas["diff_left"],  "<", GRAY, hover=_button_hovered(arrow_areas["diff_left"]))
        _draw_button(display, arrow_areas["diff_right"], ">", GRAY, hover=_button_hovered(arrow_areas["diff_right"]))
        val_surf2 = _font(22).render(settings["difficulty"].capitalize(), True, ACCENT)
        display.blit(val_surf2, val_surf2.get_rect(center=(WIDTH // 2, 357)))

        sound_label = _font(22).render("Sound", True, WHITE)
        display.blit(sound_label, sound_label.get_rect(center=(WIDTH // 2, 405)))
        sound_text = "ON" if settings["sound"] else "OFF"
        sound_color = GREEN if settings["sound"] else RED
        _draw_button(display, arrow_areas["sound_btn"], sound_text, sound_color,
                     hover=_button_hovered(arrow_areas["sound_btn"]))

        _draw_button(display, back_btn, "Back", GRAY, hover=_button_hovered(back_btn))

        for event in pygame.event.get():
            if event.type == QUIT:
                save_settings(settings)
                return settings
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if arrow_areas["car_left"].collidepoint(pos):
                    settings["car_color"] = cycle(CAR_COLORS, settings["car_color"], -1)
                elif arrow_areas["car_right"].collidepoint(pos):
                    settings["car_color"] = cycle(CAR_COLORS, settings["car_color"], 1)
                elif arrow_areas["diff_left"].collidepoint(pos):
                    settings["difficulty"] = cycle(DIFFICULTIES, settings["difficulty"], -1)
                elif arrow_areas["diff_right"].collidepoint(pos):
                    settings["difficulty"] = cycle(DIFFICULTIES, settings["difficulty"], 1)
                elif arrow_areas["sound_btn"].collidepoint(pos):
                    settings["sound"] = not settings["sound"]
                elif back_btn.collidepoint(pos):
                    save_settings(settings)
                    return settings

        pygame.display.update()
        clock.tick(60)


def leaderboard_screen(display):
    clock   = pygame.time.Clock()
    entries = load_leaderboard()
    back_btn = pygame.Rect(125, 530, 150, 45)

    while True:
        display.fill(DARK)
        title = _font(36).render("Leaderboard", True, ACCENT)
        display.blit(title, title.get_rect(center=(WIDTH // 2, 50)))

        header = _font(16).render(f"{'#':<4}{'Name':<14}{'Score':>7}{'Dist':>8}", True, GRAY)
        display.blit(header, (30, 95))
        pygame.draw.line(display, GRAY, (30, 115), (370, 115), 1)

        for i, e in enumerate(entries[:10]):
            rank_color = [ACCENT, GRAY, (205, 127, 50)] + [WHITE] * 7
            color = rank_color[i]
            row = _font(17).render(
                f"{i+1:<4}{e['name'][:13]:<14}{e['score']:>7}{e.get('distance',0):>8}m",
                True, color
            )
            display.blit(row, (30, 125 + i * 36))

        if not entries:
            no = _font(20).render("No entries yet!", True, GRAY)
            display.blit(no, no.get_rect(center=(WIDTH // 2, 280)))

        _draw_button(display, back_btn, "Back", GRAY, hover=_button_hovered(back_btn))

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if back_btn.collidepoint(event.pos):
                    return
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return

        pygame.display.update()
        clock.tick(60)


def game_over_screen(display, score, distance, coins):
    clock    = pygame.time.Clock()
    retry_btn = pygame.Rect(60,  430, 130, 50)
    menu_btn  = pygame.Rect(210, 430, 130, 50)

    while True:
        display.fill((80, 0, 0))
        title = _font(52).render("GAME OVER", True, RED)
        display.blit(title, title.get_rect(center=(WIDTH // 2, 100)))

        lines = [
            f"Score:    {score}",
            f"Distance: {distance} m",
            f"Coins:    {coins}",
        ]
        for i, line in enumerate(lines):
            surf = _font(26).render(line, True, WHITE)
            display.blit(surf, surf.get_rect(center=(WIDTH // 2, 210 + i * 55)))

        _draw_button(display, retry_btn, "Retry",     GREEN, hover=_button_hovered(retry_btn))
        _draw_button(display, menu_btn,  "Main Menu", BLUE,  hover=_button_hovered(menu_btn))

        for event in pygame.event.get():
            if event.type == QUIT:
                return "quit"
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if retry_btn.collidepoint(event.pos):
                    return "retry"
                if menu_btn.collidepoint(event.pos):
                    return "menu"

        pygame.display.update()
        clock.tick(60)
