import pygame

class Ball:
    def __init__(self, x, y, radius, color, screen_width, screen_height):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.step = 20  

    def move(self, direction):
        """Move the ball in the given direction if within screen boundaries."""
        if direction == 'up' and self.y - self.radius - self.step >= 0:
            self.y -= self.step
        elif direction == 'down' and self.y + self.radius + self.step <= self.screen_height:
            self.y += self.step
        elif direction == 'left' and self.x - self.radius - self.step >= 0:
            self.x -= self.step
        elif direction == 'right' and self.x + self.radius + self.step <= self.screen_width:
            self.x += self.step

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
