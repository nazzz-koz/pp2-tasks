import pygame
import random
import sys

from color  import *
from config import *
from game   import (Snake, Food, PoisonFood, PowerUp, Obstacle,
                    draw_grid, generate_obstacles)
import db
import settings as settings_module

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

font_lg = pygame.font.SysFont("Arial", 36, bold=True)
font_md = pygame.font.SysFont("Arial", 24)
font_sm = pygame.font.SysFont("Arial", 18)

db.init_db()

cfg = settings_module.load()


def draw_text(surf, text, font, color, cx, cy):
    s = font.render(text, True, color)
    r = s.get_rect(center=(cx, cy))
    surf.blit(s, r)


class Button:
    def __init__(self, text, cx, cy, w=200, h=44):
        self.text = text
        self.rect = pygame.Rect(cx - w // 2, cy - h // 2, w, h)

    def draw(self, surf, hover=False):
        color = (80, 80, 200) if hover else (50, 50, 150)
        pygame.draw.rect(surf, color, self.rect, border_radius=8)
        pygame.draw.rect(surf, colorWHITE, self.rect, 2, border_radius=8)
        draw_text(surf, self.text, font_md, colorWHITE,
                  self.rect.centerx, self.rect.centery)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and
                self.rect.collidepoint(event.pos))



def screen_main_menu():
    username     = ""
    input_active = True

    btn_play   = Button("Play",        WIDTH // 2, 310)
    btn_lead   = Button("Leaderboard", WIDTH // 2, 370)
    btn_set    = Button("Settings",    WIDTH // 2, 430)
    btn_quit   = Button("Quit",        WIDTH // 2, 490)
    buttons    = [btn_play, btn_lead, btn_set, btn_quit]

    clock = pygame.time.Clock()
    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", ""

            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_RETURN:
                    input_active = False
                elif len(username) < 20 and event.unicode.isprintable():
                    username += event.unicode

            if btn_play.clicked(event) and username.strip():
                return "play", username.strip()
            if btn_lead.clicked(event):
                return "leaderboard", username.strip()
            if btn_set.clicked(event):
                return "settings", username.strip()
            if btn_quit.clicked(event):
                return "quit", ""

        screen.fill(colorBLACK)
        draw_text(screen, "🐍  SNAKE GAME", font_lg, colorGREEN, WIDTH // 2, 80)
        draw_text(screen, "Enter your username:", font_sm, colorLTGRAY, WIDTH // 2, 170)

        box_color = colorCYAN if input_active else colorLTGRAY
        box_rect  = pygame.Rect(WIDTH // 2 - 130, 195, 260, 40)
        pygame.draw.rect(screen, (20, 20, 40), box_rect, border_radius=6)
        pygame.draw.rect(screen, box_color, box_rect, 2, border_radius=6)
        name_surf = font_md.render(username + ("|" if input_active else ""), True, colorWHITE)
        screen.blit(name_surf, (box_rect.x + 8, box_rect.y + 6))

        if not username.strip():
            draw_text(screen, "(enter username to play)", font_sm,
                      (150, 150, 150), WIDTH // 2, 248)

        for btn in buttons:
            btn.draw(screen, btn.is_hovered((mx, my)))

        pygame.display.flip()
        clock.tick(30)



def screen_leaderboard(username=""):
    rows   = db.get_top10()
    btn_bk = Button("Back", WIDTH // 2, 560)
    clock  = pygame.time.Clock()

    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if btn_bk.clicked(event):
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        screen.fill(colorBLACK)
        draw_text(screen, "🏆  LEADERBOARD", font_lg, colorYELLOW, WIDTH // 2, 40)

        headers = ["#", "Username", "Score", "Lvl", "Date"]
        col_xs  = [30, 80, 300, 390, 450]
        y_start = 90

        for h, x in zip(headers, col_xs):
            s = font_sm.render(h, True, colorCYAN)
            screen.blit(s, (x, y_start))

        pygame.draw.line(screen, colorGRAY, (20, y_start + 24),
                         (WIDTH - 20, y_start + 24), 1)

        if not rows:
            draw_text(screen, "(no records yet — DB not connected?)",
                      font_sm, colorLTGRAY, WIDTH // 2, y_start + 50)
        else:
            for rank, row in enumerate(rows, 1):
                y    = y_start + 30 + (rank - 1) * 30
                vals = [str(rank), row["username"], str(row["score"]),
                        str(row["level_reached"]), str(row.get("date", ""))]
                color = colorYELLOW if row["username"] == username else colorWHITE
                for val, x in zip(vals, col_xs):
                    s = font_sm.render(val, True, color)
                    screen.blit(s, (x, y))

        btn_bk.draw(screen, btn_bk.is_hovered((mx, my)))
        pygame.display.flip()
        clock.tick(30)


COLOR_PRESETS = [
    ("Green",  (50, 220, 50)),
    ("Yellow", (220, 220, 50)),
    ("Cyan",   (50, 220, 220)),
    ("Blue",   (50, 100, 220)),
    ("White",  (220, 220, 220)),
]

def screen_settings():
    global cfg
    local = dict(cfg)    

    btn_save = Button("Save & Back", WIDTH // 2, 530)
    clock    = pygame.time.Clock()

    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if btn_save.clicked(event):
                cfg = local
                settings_module.save(cfg)
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                grid_rect = pygame.Rect(WIDTH // 2 + 60, 199, 40, 24)
                if grid_rect.collidepoint(event.pos):
                    local["grid_overlay"] = not local["grid_overlay"]
                sound_rect = pygame.Rect(WIDTH // 2 + 60, 249, 40, 24)
                if sound_rect.collidepoint(event.pos):
                    local["sound"] = not local["sound"]
                for i, (_, preset_color) in enumerate(COLOR_PRESETS):
                    cx  = 120 + i * 80
                    crect = pygame.Rect(cx - 18, 329, 36, 36)
                    if crect.collidepoint(event.pos):
                        local["snake_color"] = list(preset_color)

        screen.fill(colorBLACK)
        draw_text(screen, "⚙  SETTINGS", font_lg, colorCYAN, WIDTH // 2, 50)

        draw_text(screen, "Grid overlay:", font_md, colorWHITE, WIDTH // 2 - 60, 210)
        tog_col = colorGREEN if local["grid_overlay"] else (100, 100, 100)
        tog_lbl = "ON" if local["grid_overlay"] else "OFF"
        pygame.draw.rect(screen, tog_col, (WIDTH // 2 + 60, 199, 40, 24), border_radius=5)
        draw_text(screen, tog_lbl, font_sm, colorWHITE, WIDTH // 2 + 80, 211)

        draw_text(screen, "Sound:", font_md, colorWHITE, WIDTH // 2 - 60, 260)
        stog_col = colorGREEN if local["sound"] else (100, 100, 100)
        stog_lbl = "ON" if local["sound"] else "OFF"
        pygame.draw.rect(screen, stog_col, (WIDTH // 2 + 60, 249, 40, 24), border_radius=5)
        draw_text(screen, stog_lbl, font_sm, colorWHITE, WIDTH // 2 + 80, 261)

        draw_text(screen, "Snake color:", font_md, colorWHITE, WIDTH // 2, 305)
        for i, (name, preset_color) in enumerate(COLOR_PRESETS):
            cx     = 120 + i * 80
            crect  = pygame.Rect(cx - 18, 329, 36, 36)
            sel    = (list(preset_color) == local["snake_color"])
            pygame.draw.rect(screen, preset_color, crect, border_radius=5)
            if sel:
                pygame.draw.rect(screen, colorWHITE, crect, 3, border_radius=5)
            lbl = font_sm.render(name, True, colorWHITE)
            screen.blit(lbl, (cx - lbl.get_width() // 2, 370))

        btn_save.draw(screen, btn_save.is_hovered((mx, my)))
        pygame.display.flip()
        clock.tick(30)



def screen_game_over(score, level, personal_best):
    btn_retry = Button("Retry",     WIDTH // 2, 380)
    btn_menu  = Button("Main Menu", WIDTH // 2, 440)
    clock     = pygame.time.Clock()

    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if btn_retry.clicked(event):
                return "retry"
            if btn_menu.clicked(event):
                return "menu"

        screen.fill(colorBLACK)
        draw_text(screen, "GAME OVER", font_lg, colorRED, WIDTH // 2, 220)
        draw_text(screen, f"Score : {score}",      font_md, colorWHITE, WIDTH // 2, 285)
        draw_text(screen, f"Level : {level}",      font_md, colorWHITE, WIDTH // 2, 320)
        draw_text(screen, f"Best  : {personal_best}", font_md, colorYELLOW, WIDTH // 2, 355)

        btn_retry.draw(screen, btn_retry.is_hovered((mx, my)))
        btn_menu.draw(screen,  btn_menu.is_hovered((mx, my)))
        pygame.display.flip()
        clock.tick(30)



def run_game(username, player_id, personal_best_ref):
    snake       = Snake(color=tuple(cfg["snake_color"]))
    food        = Food()
    food.generate_random_pos(snake)
    poison      = PoisonFood()
    powerup     = PowerUp()
    obstacles   = []

    score       = 0
    level       = 1
    foods_eaten = 0
    fps         = BASE_FPS
    game_over   = False

    last_poison_spawn  = pygame.time.get_ticks()
    last_powerup_spawn = pygame.time.get_ticks()
    POISON_INTERVAL    = 7000   
    POWERUP_INTERVAL   = 12000  

    clock = pygame.time.Clock()

    while True:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and snake.dx != -1:
                    snake.dx, snake.dy = 1, 0
                elif event.key == pygame.K_LEFT and snake.dx != 1:
                    snake.dx, snake.dy = -1, 0
                elif event.key == pygame.K_DOWN and snake.dy != -1:
                    snake.dx, snake.dy = 0, 1
                elif event.key == pygame.K_UP and snake.dy != 1:
                    snake.dx, snake.dy = 0, -1

        if not game_over:
            snake.move()

            hit_wall = snake.check_wall_collision()
            hit_self = snake.check_self_collision()
            hit_obs  = snake.check_obstacle_collision(obstacles)

            if hit_wall or hit_self or hit_obs:
                if snake.use_shield():
                    h = snake.body[0]
                    h.x = max(0, min(COLS - 1, h.x))
                    h.y = max(0, min(ROWS - 1, h.y))
                else:
                    game_over = True

            if snake.check_food_collision(food):
                score       += food.weight
                foods_eaten += 1
                food.generate_random_pos(snake, obstacles)

                if foods_eaten % 4 == 0:
                    level += 1
                    fps   += 2
                    if level >= 3:
                        obstacles = generate_obstacles(level, snake)
                        food.generate_random_pos(snake, obstacles)
                        poison.deactivate()

            if food.is_expired:
                food.generate_random_pos(snake, obstacles)

            if now - last_poison_spawn > POISON_INTERVAL and not poison.active:
                poison.spawn(snake, food, obstacles)
                last_poison_spawn = now

            if poison.active:
                if poison.is_expired:
                    poison.deactivate()
                elif snake.check_poison_collision(poison):
                    poison.deactivate()
                    if not snake.shorten(2):
                        game_over = True

            if now - last_powerup_spawn > POWERUP_INTERVAL and not powerup.active:
                powerup.spawn(snake, food, poison, obstacles)
                last_powerup_spawn = now

            if powerup.active:
                if powerup.is_expired:
                    powerup.deactivate()
                elif snake.check_powerup_collision(powerup):
                    snake.apply_powerup(powerup.kind)
                    powerup.deactivate()
                    last_powerup_spawn = now   

        screen.fill(colorBLACK)

        if cfg.get("grid_overlay", True):
            draw_grid(screen)

        for obs in obstacles:
            obs.draw(screen)

        snake.draw(screen)
        food.draw(screen)
        if poison.active:
            poison.draw(screen)
        if powerup.active:
            powerup.draw(screen)

        timer_secs = max(0.0, FOOD_LIFETIME - food.elapsed)
        lines = [
            (f"Score: {score}",           colorWHITE),
            (f"Level: {level}",           colorWHITE),
            (f"Food:  {timer_secs:.1f}s", colorWHITE),
            (f"Best:  {personal_best_ref[0]}", colorYELLOW),
        ]
        for i, (txt, col) in enumerate(lines):
            screen.blit(font_md.render(txt, True, col), (10, 10 + i * 28))

        hud_x = WIDTH - 160
        if snake.speed_end_time > now:
            rem = (snake.speed_end_time - now) / 1000
            screen.blit(font_sm.render(f"⚡ Speed {rem:.1f}s", True, colorCYAN), (hud_x, 10))
        if snake.slow_end_time > now:
            rem = (snake.slow_end_time - now) / 1000
            screen.blit(font_sm.render(f"🐢 Slow {rem:.1f}s", True, colorBLUE), (hud_x, 30))
        if snake.shield_active:
            screen.blit(font_sm.render("🛡 Shield", True, colorYELLOW), (hud_x, 50))

        if game_over:
            go = font_lg.render("GAME OVER", True, colorRED)
            screen.blit(go, (WIDTH // 2 - go.get_width() // 2, HEIGHT // 2 - 20))

        pygame.display.flip()
        clock.tick(snake.effective_fps(fps))

        if game_over:
            pygame.time.delay(800)
            return score, level


def main():
    action   = "menu"
    username = ""
    player_id       = None
    personal_best   = [0]    

    while True:
        if action in ("menu", "retry_to_menu"):
            action, username = screen_main_menu()

        if action == "quit":
            break

        if action == "leaderboard":
            screen_leaderboard(username)
            action = "menu"
            continue

        if action == "settings":
            screen_settings()
            action = "menu"
            continue

        if action == "play":
            player_id     = db.get_or_create_player(username) if username else None
            personal_best[0] = db.get_personal_best(player_id)

            score, level  = run_game(username, player_id, personal_best)

            db.save_session(player_id, score, level)

            if score > personal_best[0]:
                personal_best[0] = score

            result = screen_game_over(score, level, personal_best[0])
            if result == "retry":
                action = "play"
            else:
                action = "menu"
            continue

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
