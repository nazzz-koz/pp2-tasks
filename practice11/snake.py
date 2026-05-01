import pygame
from color import *
import random

pygame.init()

WIDTH  = 600
HEIGHT = 600
CELL   = 30          

COLS = WIDTH  // CELL
ROWS = HEIGHT // CELL

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

font = pygame.font.SysFont("Arial", 24)


def draw_grid():
    """Draw a light-gray grid over the entire screen."""
    for i in range(COLS):
        for j in range(ROWS):
            pygame.draw.rect(screen, colorGRAY,
                             (i * CELL, j * CELL, CELL, CELL), 1)


class Point:
    """Simple 2-D grid coordinate."""
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Snake:
    """The player-controlled snake."""

    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1   
        self.dy = 0   

    def move(self):
        """Shift every segment to the position of the one ahead of it, then move head."""
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def draw(self):
        """Draw the head in red and the body segments in yellow."""
        pygame.draw.rect(screen, colorRED,
                         (self.body[0].x * CELL, self.body[0].y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW,
                             (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_wall_collision(self):
        """Return True if the head has left the grid."""
        head = self.body[0]
        return (
            head.x < 0 or head.x >= COLS or
            head.y < 0 or head.y >= ROWS
        )

    def check_self_collision(self):
        """Return True if the head overlaps any body segment."""
        head = self.body[0]
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False

    def check_food_collision(self, food):
        """Return True if the head is on the food; grow the snake if so."""
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            self.body.append(Point(head.x, head.y))
            return True
        return False


FOOD_LIFETIME = 5.0

FOOD_WEIGHTS = {
    1: colorGREEN,         
    3: (255, 165, 0),       
    5: (200,  50, 200),     
}

class Food:
    """A food item that has a random point weight and disappears after a timer."""

    def __init__(self):
        self.pos    = Point(0, 0)
        self.weight = 1                    
        self.color  = colorGREEN           
        self.spawn_time = pygame.time.get_ticks()   

    @property
    def elapsed(self):
        """Seconds since this food was spawned."""
        return (pygame.time.get_ticks() - self.spawn_time) / 1000.0

    @property
    def is_expired(self):
        """True when the food has been on the board longer than FOOD_LIFETIME."""
        return self.elapsed >= FOOD_LIFETIME

    def draw(self):
        """Draw food with colour based on weight; fade it out as it nears expiry."""
        fraction_left = max(0.0, 1.0 - self.elapsed / FOOD_LIFETIME)
        brightness = 0.3 + 0.7 * fraction_left
        r = int(self.color[0] * brightness)
        g = int(self.color[1] * brightness)
        b = int(self.color[2] * brightness)
        pygame.draw.rect(screen, (r, g, b),
                         (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

        weight_surf = pygame.font.SysFont("Arial", 16).render(
            str(self.weight), True, colorWHITE
        )
        screen.blit(weight_surf, (self.pos.x * CELL + 4, self.pos.y * CELL + 6))

    def generate_random_pos(self, snake):
        """Pick a random grid cell not occupied by the snake, choose a random weight."""
        while True:
            x = random.randint(0, COLS - 1)
            y = random.randint(0, ROWS - 1)

            overlap = any(seg.x == x and seg.y == y for seg in snake.body)
            if not overlap:
                self.pos = Point(x, y)
                break

        self.weight = random.choices(
            list(FOOD_WEIGHTS.keys()),
            weights=[60, 30, 10]
        )[0]
        self.color      = FOOD_WEIGHTS[self.weight]
        self.spawn_time = pygame.time.get_ticks()  


snake = Snake()
food  = Food()
food.generate_random_pos(snake)

score       = 0
level       = 1
foods_eaten = 0

FPS   = 5
clock = pygame.time.Clock()

running   = True
game_over = False


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

        if snake.check_wall_collision() or snake.check_self_collision():
            game_over = True

        if snake.check_food_collision(food):
            score       += food.weight   
            foods_eaten += 1
            food.generate_random_pos(snake)

            if foods_eaten % 4 == 0:
                level += 1
                FPS   += 2

        if food.is_expired:
            food.generate_random_pos(snake)

    screen.fill(colorBLACK)
    draw_grid()

    snake.draw()
    food.draw()

    score_text = font.render(f"Score: {score}", True, colorWHITE)
    level_text = font.render(f"Level: {level}", True, colorWHITE)
    timer_secs = max(0.0, FOOD_LIFETIME - food.elapsed)
    timer_text = font.render(f"Food: {timer_secs:.1f}s", True, colorWHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))
    screen.blit(timer_text, (10, 70))

    if game_over:
        game_text = font.render("GAME OVER", True, colorRED)
        screen.blit(game_text, (WIDTH // 2 - 80, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
