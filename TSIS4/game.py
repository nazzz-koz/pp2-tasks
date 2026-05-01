import pygame
import random
from color import *
from config import *


class Point:
    """2-D grid coordinate."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def draw_grid(screen):
    for i in range(COLS):
        for j in range(ROWS):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)


def _small_font():
    return pygame.font.SysFont("Arial", 16)



class Snake:
    MIN_LENGTH = 2   

    def __init__(self, color=(50, 220, 50)):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0
        self.color = color

        self.shield_active   = False
        self.speed_end_time  = 0   
        self.slow_end_time   = 0   


    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        self.body[0].x += self.dx
        self.body[0].y += self.dy


    def draw(self, screen):
        head_color = colorCYAN if self.shield_active else colorRED
        pygame.draw.rect(screen, head_color,
                         (self.body[0].x * CELL, self.body[0].y * CELL, CELL, CELL))
        for seg in self.body[1:]:
            pygame.draw.rect(screen, self.color,
                             (seg.x * CELL, seg.y * CELL, CELL, CELL))


    def check_wall_collision(self):
        h = self.body[0]
        return h.x < 0 or h.x >= COLS or h.y < 0 or h.y >= ROWS

    def check_self_collision(self):
        h = self.body[0]
        return any(h.x == s.x and h.y == s.y for s in self.body[1:])

    def check_obstacle_collision(self, obstacles):
        h = self.body[0]
        return any(h.x == o.x and h.y == o.y for o in obstacles)

    def check_food_collision(self, food):
        h = self.body[0]
        if h.x == food.pos.x and h.y == food.pos.y:
            self.body.append(Point(self.body[-1].x, self.body[-1].y))
            return True
        return False

    def check_poison_collision(self, poison):
        h = self.body[0]
        if h.x == poison.pos.x and h.y == poison.pos.y:
            return True
        return False

    def shorten(self, amount=2):
        """Remove `amount` tail segments. Returns True if snake is still alive."""
        self.body = self.body[: max(self.MIN_LENGTH, len(self.body) - amount)]
        return len(self.body) >= self.MIN_LENGTH

    def check_powerup_collision(self, powerup):
        h = self.body[0]
        return h.x == powerup.pos.x and h.y == powerup.pos.y


    def apply_powerup(self, kind):
        now = pygame.time.get_ticks()
        if kind == "speed":
            self.speed_end_time = now + 5000
            self.slow_end_time  = 0
        elif kind == "slow":
            self.slow_end_time  = now + 5000
            self.speed_end_time = 0
        elif kind == "shield":
            self.shield_active = True

    def effective_fps(self, base_fps):
        now = pygame.time.get_ticks()
        if self.speed_end_time > now:
            return base_fps + 5
        if self.slow_end_time > now:
            return max(2, base_fps - 3)
        return base_fps

    def use_shield(self):
        if self.shield_active:
            self.shield_active = False
            return True
        return False


class Food:
    def __init__(self):
        self.pos        = Point(0, 0)
        self.weight     = 1
        self.color      = colorGREEN
        self.spawn_time = pygame.time.get_ticks()

    @property
    def elapsed(self):
        return (pygame.time.get_ticks() - self.spawn_time) / 1000.0

    @property
    def is_expired(self):
        return self.elapsed >= FOOD_LIFETIME

    def draw(self, screen):
        fraction_left = max(0.0, 1.0 - self.elapsed / FOOD_LIFETIME)
        b = 0.3 + 0.7 * fraction_left
        r, g, c = (int(self.color[i] * b) for i in range(3))
        pygame.draw.rect(screen, (r, g, c),
                         (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))
        surf = _small_font().render(str(self.weight), True, colorWHITE)
        screen.blit(surf, (self.pos.x * CELL + 4, self.pos.y * CELL + 6))

    def generate_random_pos(self, snake, obstacles=None):
        blocked = {(s.x, s.y) for s in snake.body}
        if obstacles:
            blocked |= {(o.x, o.y) for o in obstacles}
        while True:
            x = random.randint(0, COLS - 1)
            y = random.randint(0, ROWS - 1)
            if (x, y) not in blocked:
                self.pos = Point(x, y)
                break
        self.weight     = random.choices([1, 3, 5], weights=[60, 30, 10])[0]
        self.color      = FOOD_WEIGHTS[self.weight]
        self.spawn_time = pygame.time.get_ticks()



class PoisonFood:
    LIFETIME = 6.0

    def __init__(self):
        self.pos        = Point(-1, -1)
        self.spawn_time = pygame.time.get_ticks()
        self.active     = False

    @property
    def elapsed(self):
        return (pygame.time.get_ticks() - self.spawn_time) / 1000.0

    @property
    def is_expired(self):
        return self.elapsed >= self.LIFETIME

    def spawn(self, snake, food, obstacles=None):
        blocked = {(s.x, s.y) for s in snake.body}
        blocked.add((food.pos.x, food.pos.y))
        if obstacles:
            blocked |= {(o.x, o.y) for o in obstacles}
        for _ in range(200):
            x = random.randint(0, COLS - 1)
            y = random.randint(0, ROWS - 1)
            if (x, y) not in blocked:
                self.pos        = Point(x, y)
                self.spawn_time = pygame.time.get_ticks()
                self.active     = True
                return
        self.active = False

    def deactivate(self):
        self.active = False

    def draw(self, screen):
        if not self.active:
            return
        fraction = max(0.0, 1.0 - self.elapsed / self.LIFETIME)
        b = 0.4 + 0.6 * fraction
        color = (int(180 * b), 0, 0)
        pygame.draw.rect(screen, color,
                         (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))
        surf = _small_font().render("☠", True, colorWHITE)
        screen.blit(surf, (self.pos.x * CELL + 4, self.pos.y * CELL + 5))



POWERUP_KINDS = {
    "speed":  {"color": colorCYAN,   "symbol": "▲"},
    "slow":   {"color": colorBLUE,   "symbol": "▼"},
    "shield": {"color": colorYELLOW, "symbol": "⬡"},
}

class PowerUp:
    def __init__(self):
        self.pos        = Point(-1, -1)
        self.kind       = "speed"
        self.spawn_time = pygame.time.get_ticks()
        self.active     = False

    @property
    def elapsed(self):
        return (pygame.time.get_ticks() - self.spawn_time) / 1000.0

    @property
    def is_expired(self):
        return self.elapsed >= POWERUP_LIFETIME

    def spawn(self, snake, food, poison, obstacles=None):
        blocked = {(s.x, s.y) for s in snake.body}
        blocked.add((food.pos.x, food.pos.y))
        if poison.active:
            blocked.add((poison.pos.x, poison.pos.y))
        if obstacles:
            blocked |= {(o.x, o.y) for o in obstacles}
        for _ in range(200):
            x = random.randint(0, COLS - 1)
            y = random.randint(0, ROWS - 1)
            if (x, y) not in blocked:
                self.pos        = Point(x, y)
                self.kind       = random.choice(list(POWERUP_KINDS.keys()))
                self.spawn_time = pygame.time.get_ticks()
                self.active     = True
                return
        self.active = False

    def deactivate(self):
        self.active = False

    def draw(self, screen):
        if not self.active:
            return
        info  = POWERUP_KINDS[self.kind]
        frac  = max(0.0, 1.0 - self.elapsed / POWERUP_LIFETIME)
        b     = 0.4 + 0.6 * frac
        color = tuple(int(c * b) for c in info["color"])
        pygame.draw.rect(screen, color,
                         (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))
        surf = _small_font().render(info["symbol"], True, colorWHITE)
        screen.blit(surf, (self.pos.x * CELL + 4, self.pos.y * CELL + 5))



class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.rect(screen, colorLTGRAY,
                         (self.x * CELL, self.y * CELL, CELL, CELL))
        pygame.draw.rect(screen, colorWHITE,
                         (self.x * CELL, self.y * CELL, CELL, CELL), 2)


def generate_obstacles(level, snake):
    count   = min(4 + (level - 3) * 2, 20)
    blocked = {(s.x, s.y) for s in snake.body}
    head = snake.body[0]
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            blocked.add((head.x + dx, head.y + dy))

    obstacles = []
    attempts  = 0
    while len(obstacles) < count and attempts < 500:
        attempts += 1
        x = random.randint(0, COLS - 1)
        y = random.randint(0, ROWS - 1)
        if (x, y) not in blocked:
            blocked.add((x, y))
            obstacles.append(Obstacle(x, y))
    return obstacles
