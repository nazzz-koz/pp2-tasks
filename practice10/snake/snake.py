import pygame
from color import *
import random

pygame.init()

WIDTH = 600
HEIGHT = 600
CELL = 30

COLS = WIDTH // CELL
ROWS = HEIGHT // CELL

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

font = pygame.font.SysFont("Arial", 24)

def draw_grid():
    for i in range(COLS):
        for j in range(ROWS):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def draw(self):
        pygame.draw.rect(screen, colorRED,
                         (self.body[0].x * CELL, self.body[0].y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW,
                             (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_wall_collision(self):
        head = self.body[0]
        return (
            head.x < 0 or head.x >= COLS or
            head.y < 0 or head.y >= ROWS
        )

    def check_self_collision(self):
        head = self.body[0]
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False

    def check_food_collision(self, food):
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            self.body.append(Point(head.x, head.y))
            return True
        return False

class Food:
    def __init__(self):
        self.pos = Point(0, 0)

    def draw(self):
        pygame.draw.rect(screen, colorGREEN,
                         (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self, snake):
        while True:
            x = random.randint(0, COLS - 1)
            y = random.randint(0, ROWS - 1)

            overlap = False
            for segment in snake.body:
                if segment.x == x and segment.y == y:
                    overlap = True
                    break

            if not overlap:
                self.pos = Point(x, y)
                break

snake = Snake()
food = Food()
food.generate_random_pos(snake)

score = 0
level = 1
foods_eaten = 0

FPS = 5
clock = pygame.time.Clock()

running = True
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
            score += 1
            foods_eaten += 1
            food.generate_random_pos(snake)

            if foods_eaten % 4 == 0:
                level += 1
                FPS += 2  

    screen.fill(colorBLACK)
    draw_grid()

    snake.draw()
    food.draw()

    score_text = font.render(f"Score: {score}", True, colorWHITE)
    level_text = font.render(f"Level: {level}", True, colorWHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    if game_over:
        game_text = font.render("GAME OVER", True, colorRED)
        screen.blit(game_text, (WIDTH // 2 - 80, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()