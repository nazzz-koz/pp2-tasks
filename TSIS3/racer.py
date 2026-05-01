import pygame, random, math
from pygame.locals import *

WIDTH, HEIGHT = 400, 600

BLACK  = (0,   0,   0)
WHITE  = (255, 255, 255)
GRAY   = (160, 160, 160)
DARK   = (30,  30,  30)
ACCENT = (255, 200,  0)
RED    = (220,  50,  50)
GREEN  = (50,  200,  80)
BLUE   = (50,  120, 220)
ORANGE = (255, 140,  0)
TEAL   = (0,   200, 200)
PURPLE = (160,  80, 220)

DIFFICULTY_PRESETS = {
    "easy":   {"base_speed": 4,  "spawn_enemy": 120, "spawn_obs": 180},
    "normal": {"base_speed": 5,  "spawn_enemy": 90,  "spawn_obs": 130},
    "hard":   {"base_speed": 7,  "spawn_enemy": 60,  "spawn_obs": 90},
}

CAR_BODY_COLORS = {
    "red":   (220,  50,  50),
    "blue":  (50,  120, 220),
    "green": (50,  200,  80),
}

LANE_X = [80, 160, 240, 320]   


def _draw_car(surface, x, y, w, h, body_color, window_color=(150, 220, 255)):
    rect = pygame.Rect(x - w // 2, y - h // 2, w, h)
    pygame.draw.rect(surface, body_color, rect, border_radius=5)
    win_w, win_h = w - 8, h // 3
    pygame.draw.rect(surface, window_color,
                     pygame.Rect(rect.x + 4, rect.y + 6, win_w, win_h), border_radius=3)
    pygame.draw.rect(surface, window_color,
                     pygame.Rect(rect.x + 4, rect.bottom - win_h - 6, win_w, win_h), border_radius=3)
    ww, wh = 7, 10
    for dx in [0, w - ww]:
        for dy in [4, h - wh - 4]:
            pygame.draw.rect(surface, BLACK, pygame.Rect(rect.x - 3 + dx, rect.y + dy, ww, wh), border_radius=2)


def _make_car_surf(w, h, body_color):
    surf = pygame.Surface((w + 6, h), pygame.SRCALPHA)
    _draw_car(surf, (w + 6) // 2, h // 2, w, h, body_color)
    return surf


def _make_obstacle_surf(kind):
    if kind == "oil":
        surf = pygame.Surface((44, 24), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (30, 30, 80, 200), surf.get_rect())
        pygame.draw.ellipse(surf, (80, 80, 180, 120), surf.get_rect().inflate(-10, -8))
    elif kind == "pothole":
        surf = pygame.Surface((36, 36), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (50, 40, 40), surf.get_rect())
        pygame.draw.ellipse(surf, (30, 25, 25), surf.get_rect().inflate(-8, -8))
    else:  
        surf = pygame.Surface((50, 18), pygame.SRCALPHA)
        pygame.draw.rect(surf, (220, 60, 60), surf.get_rect(), border_radius=3)
        for i in range(0, 50, 10):
            pygame.draw.rect(surf, WHITE, pygame.Rect(i, 0, 5, 18))
    return surf


def _make_powerup_surf(kind):
    surf = pygame.Surface((30, 30), pygame.SRCALPHA)
    colors = {"nitro": ORANGE, "shield": BLUE, "repair": GREEN}
    symbols = {"nitro": "N", "shield": "S", "repair": "R"}
    pygame.draw.circle(surf, colors[kind], (15, 15), 14)
    pygame.draw.circle(surf, WHITE, (15, 15), 14, 2)
    font = pygame.font.SysFont("Arial", 16, bold=True)
    lbl = font.render(symbols[kind], True, WHITE)
    surf.blit(lbl, lbl.get_rect(center=(15, 15)))
    return surf


def _make_coin_surf(weight):
    surf = pygame.Surface((28, 28), pygame.SRCALPHA)
    color = {1: (212, 175, 55), 2: (192, 192, 192), 5: (0, 200, 200)}[weight]
    pygame.draw.circle(surf, color, (14, 14), 13)
    pygame.draw.circle(surf, WHITE, (14, 14), 13, 2)
    font = pygame.font.SysFont("Arial", 12, bold=True)
    lbl = font.render(str(weight), True, BLACK)
    surf.blit(lbl, lbl.get_rect(center=(14, 14)))
    return surf


def _make_nitro_strip_surf():
    surf = pygame.Surface((60, 20), pygame.SRCALPHA)
    pygame.draw.rect(surf, (0, 255, 180, 180), surf.get_rect(), border_radius=4)
    font = pygame.font.SysFont("Arial", 11, bold=True)
    lbl = font.render("NITRO", True, BLACK)
    surf.blit(lbl, lbl.get_rect(center=(30, 10)))
    return surf


class Road:

    def __init__(self):
        self.y_offset = 0
        self.stripe_h = 40
        self.stripe_gap = 40

    def update(self, speed):
        self.y_offset = (self.y_offset + speed) % (self.stripe_h + self.stripe_gap)

    def draw(self, surface):
        surface.fill((60, 60, 60))
        for x, w, c in [(0, 40, (180, 60, 60)), (WIDTH - 40, 40, (180, 60, 60))]:
            pygame.draw.rect(surface, c, pygame.Rect(x, 0, w, HEIGHT))
        pygame.draw.rect(surface, (80, 80, 80), pygame.Rect(40, 0, WIDTH - 80, HEIGHT))
        for lx in [120, 200, 280]:
            y = -self.stripe_gap + self.y_offset
            while y < HEIGHT:
                pygame.draw.rect(surface, (220, 220, 60),
                                 pygame.Rect(lx - 2, int(y), 4, self.stripe_h))
                y += self.stripe_h + self.stripe_gap


class Player(pygame.sprite.Sprite):
    def __init__(self, car_color="red"):
        super().__init__()
        self.body_color = CAR_BODY_COLORS.get(car_color, RED)
        self.image = _make_car_surf(34, 56, self.body_color)
        self.rect  = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom  = HEIGHT - 10
        self.move_speed = 5
        self.shield_active = False
        self.nitro_active  = False
        self.nitro_timer   = 0

    def update(self, keys):
        dx = 0
        if keys[K_LEFT]  and self.rect.left  > 40:  dx = -self.move_speed
        if keys[K_RIGHT] and self.rect.right < WIDTH - 40: dx = self.move_speed
        self.rect.x += dx
        if self.nitro_active:
            self.nitro_timer -= 1
            if self.nitro_timer <= 0:
                self.nitro_active = False

    def activate_nitro(self, duration_frames):
        self.nitro_active = True
        self.nitro_timer  = duration_frames

    def draw_shield(self, surface):
        if self.shield_active:
            cx, cy = self.rect.centerx, self.rect.centery
            pygame.draw.circle(surface, (*BLUE, 120), (cx, cy), 34, 3)


class EnemyCar(pygame.sprite.Sprite):
    COLORS = [(200, 80, 80), (80, 200, 80), (80, 80, 200),
              (200, 200, 80), (180, 80, 180), (80, 200, 200)]

    def __init__(self, speed, player_rect):
        super().__init__()
        color = random.choice(self.COLORS)
        self.image = _make_car_surf(32, 54, color)
        self.rect  = self.image.get_rect()
        self.speed = speed
        for _ in range(20):
            lx = random.choice(LANE_X)
            self.rect.centerx = lx
            self.rect.bottom  = random.randint(-80, -10)
            if abs(self.rect.centerx - player_rect.centerx) > 60 or \
               self.rect.bottom < player_rect.top - 150:
                break

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    KINDS = ["oil", "pothole", "barrier"]

    def __init__(self, speed, player_rect):
        super().__init__()
        self.kind  = random.choice(self.KINDS)
        self.image = _make_obstacle_surf(self.kind)
        self.rect  = self.image.get_rect()
        self.speed = speed
        for _ in range(20):
            lx = random.choice(LANE_X)
            self.rect.centerx = lx
            self.rect.top     = random.randint(-200, -60)
            if abs(self.rect.centerx - player_rect.centerx) > 50 or \
               self.rect.bottom < player_rect.top - 180:
                break

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class NitroStrip(pygame.sprite.Sprite):

    def __init__(self, speed):
        super().__init__()
        self.image = _make_nitro_strip_surf()
        self.rect  = self.image.get_rect()
        self.rect.centerx = random.choice(LANE_X)
        self.rect.top = random.randint(-300, -80)
        self.speed = speed
        self.timer = 360  

    def update(self):
        self.rect.y += self.speed
        self.timer -= 1
        if self.rect.top > HEIGHT or self.timer <= 0:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.weight = random.choices([1, 2, 5], weights=[60, 30, 10])[0]
        self.image  = _make_coin_surf(self.weight)
        self.rect   = self.image.get_rect()
        self.rect.centerx = random.choice(LANE_X)
        self.rect.top = random.randint(-300, -40)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    KINDS = ["nitro", "shield", "repair"]

    def __init__(self, speed):
        super().__init__()
        self.kind  = random.choice(self.KINDS)
        self.image = _make_powerup_surf(self.kind)
        self.rect  = self.image.get_rect()
        self.rect.centerx = random.choice(LANE_X)
        self.rect.top = random.randint(-400, -100)
        self.speed = speed
        self.timer = 480  

    def update(self):
        self.rect.y += self.speed
        self.timer -= 1
        if self.rect.top > HEIGHT or self.timer <= 0:
            self.kill()


def _draw_hud(surface, score, coins, distance, active_pu, pu_timer, shield, next_boost):
    font_s = pygame.font.SysFont("Arial", 17, bold=True)
    lines = [
        f"Score: {score}",
        f"Coins: {coins}",
        f"Dist:  {distance}m",
        f"Boost @ {next_boost} coins",
    ]
    for i, line in enumerate(lines):
        surf = font_s.render(line, True, WHITE)
        surface.blit(surf, (8, 8 + i * 20))

    if active_pu:
        secs = max(0, pu_timer // 60)
        color = {"nitro": ORANGE, "shield": BLUE, "repair": GREEN}.get(active_pu, WHITE)
        pu_text = f"[{active_pu.upper()}]" + (f" {secs}s" if pu_timer > 0 else "")
        pu_surf = font_s.render(pu_text, True, color)
        surface.blit(pu_surf, (WIDTH - pu_surf.get_width() - 8, 8))


def run_game(display, settings) -> tuple:
    clock = pygame.time.Clock()
    FPS   = 60

    preset     = DIFFICULTY_PRESETS.get(settings.get("difficulty", "normal"), DIFFICULTY_PRESETS["normal"])
    base_speed = preset["base_speed"]
    speed      = float(base_speed)
    car_color  = settings.get("car_color", "red")

    SPEED_BOOST_EVERY = 5
    last_boost_thresh = 0

    road = Road()

    P1 = Player(car_color)
    all_sprites  = pygame.sprite.Group(P1)
    enemies      = pygame.sprite.Group()
    obstacles    = pygame.sprite.Group()
    coins_grp    = pygame.sprite.Group()
    powerups_grp = pygame.sprite.Group()
    nitro_strips = pygame.sprite.Group()

    score    = 0
    coin_val = 0
    distance = 0  

    enemy_timer = 0
    obs_timer   = 0
    pu_timer    = 0
    nitro_strip_timer = 0

    active_pu   = None
    active_timer= 0   

    def _spawn_interval(base, dist):
        reduction = min(dist // 300, 30)   
        return max(base - reduction, 20)

    running = True
    while running:
        dt = clock.tick(FPS)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                import sys; sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        speed += 0.5 / FPS   

        current_thresh = coin_val // SPEED_BOOST_EVERY
        if current_thresh > last_boost_thresh:
            speed += (current_thresh - last_boost_thresh) * 1.0
            last_boost_thresh = current_thresh

        effective_speed = speed * (1.5 if P1.nitro_active else 1.0)

        enemy_timer += 1
        if enemy_timer >= _spawn_interval(preset["spawn_enemy"], distance):
            num = 1 + (distance // 500)  
            for _ in range(min(num, 3)):
                e = EnemyCar(effective_speed + random.uniform(-0.5, 0.5), P1.rect)
                enemies.add(e)
                all_sprites.add(e)
            enemy_timer = 0

        obs_timer += 1
        if obs_timer >= _spawn_interval(preset["spawn_obs"], distance):
            o = Obstacle(effective_speed * 0.7, P1.rect)
            obstacles.add(o)
            all_sprites.add(o)
            obs_timer = 0

        pu_timer += 1
        if pu_timer >= 300:  
            pu = PowerUp(effective_speed * 0.8)
            powerups_grp.add(pu)
            all_sprites.add(pu)
            pu_timer = 0

        nitro_strip_timer += 1
        if nitro_strip_timer >= 400:
            ns = NitroStrip(effective_speed * 0.8)
            nitro_strips.add(ns)
            all_sprites.add(ns)
            nitro_strip_timer = 0

        coin_spawn_rate = max(40, 80 - distance // 200)
        if random.randint(0, coin_spawn_rate) == 0:
            c = Coin(effective_speed * 0.9)
            coins_grp.add(c)
            all_sprites.add(c)

        road.update(effective_speed)
        P1.update(keys)
        for e in enemies:       e.update()
        for o in obstacles:     o.update()
        for c in coins_grp:     c.update()
        for pu in powerups_grp: pu.update()
        for ns in nitro_strips: ns.update()

        distance += int(effective_speed * 0.1)

        if active_timer > 0:
            active_timer -= 1
            if active_timer <= 0 and active_pu not in (None, "shield"):
                active_pu = None

        for c in pygame.sprite.spritecollide(P1, coins_grp, True):
            coin_val += c.weight
            score    += c.weight * 10

        for ns in pygame.sprite.spritecollide(P1, nitro_strips, True):
            P1.activate_nitro(3 * FPS)
            score += 50

        for pu in pygame.sprite.spritecollide(P1, powerups_grp, True):
            if active_pu is None or True:  
                active_pu = pu.kind
                if pu.kind == "nitro":
                    P1.activate_nitro(4 * FPS)
                    active_timer = 4 * FPS
                elif pu.kind == "shield":
                    P1.shield_active = True
                    active_timer = 0   
                elif pu.kind == "repair":
                    obstacles.empty()
                    active_pu    = "repair"
                    active_timer = 2 * FPS

        for o in pygame.sprite.spritecollide(P1, obstacles, True):
            if P1.shield_active:
                P1.shield_active = False
                active_pu = None
            else:
                if o.kind in ("oil", "pothole"):
                    speed = max(base_speed, speed - 1.5)
                    score = max(0, score - 20)
                else:  
                    running = False

        if pygame.sprite.spritecollideany(P1, enemies):
            if P1.shield_active:
                P1.shield_active = False
                active_pu = None
                enemies.empty()
            else:
                running = False

        road.draw(display)
        all_sprites.draw(display)
        P1.draw_shield(display)

        next_boost = (last_boost_thresh + 1) * SPEED_BOOST_EVERY
        _draw_hud(display, score, coin_val, distance, active_pu, active_timer,
                  P1.shield_active, next_boost)

        pygame.display.update()

    score += distance // 10
    return score, distance, coin_val
