import pygame, sys, time
from pygame.locals import *
import random

pygame.init()

fps = 60
framepersec = pygame.time.Clock()

blue  = pygame.Color(0, 0, 255)
green = pygame.Color(0, 255, 0)
red   = pygame.Color(255, 0, 0)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

WIDTH  = 400
HEIGHT = 600

SPEED_BOOST_EVERY_N_COINS = 5

speed = 5          
score = 0          
coin  = 0          
last_boost_threshold = 0  

font       = pygame.font.SysFont("TimesNewRoman", 60)
font_small = pygame.font.SysFont("TimesNewRoman", 20)
game_over_text = font.render("Game Over", True, black)

background = pygame.image.load("AnimatedStreet.png")

display = pygame.display.set_mode((WIDTH, HEIGHT))
display.fill(white)
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
    """Enemy car that moves downward and respawns at the top."""

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect  = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH - 40), 0)

    def move(self):
        """Move enemy downward; increment score and respawn when it exits the screen."""
        global score
        self.rect.move_ip(0, speed)
        if self.rect.top > HEIGHT:
            score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH - 40), 0)


class Coin(pygame.sprite.Sprite):
    """Coin sprite with a randomly assigned point weight (1, 2, or 5)."""

    WEIGHT_COLORS = {
        1:  (212, 175, 55),   
        2:  (192, 192, 192),  
        5:  (0,   200, 200),  
    }

    def __init__(self):
        super().__init__()
        original      = pygame.image.load("coin.png").convert_alpha()
        self.original = pygame.transform.scale(original, (30, 30))
        self.image    = self.original.copy()
        self.rect     = self.image.get_rect()
        self.reset()

    def reset(self):
        """Respawn coin at a random position above the screen with a new random weight."""
        self.rect.center = (random.randint(40, WIDTH - 40),
                            random.randint(-100, -40))


        self.weight = random.choices([1, 2, 5], weights=[60, 30, 10])[0]

        self.image = self.original.copy()

        border_color = self.WEIGHT_COLORS[self.weight]
        pygame.draw.rect(self.image, border_color, self.image.get_rect(), 3)

    def move(self):
        """Move coin downward; respawn when it exits the screen."""
        self.rect.move_ip(0, speed)
        if self.rect.top > HEIGHT:
            self.reset()


class Player(pygame.sprite.Sprite):
    """Player car controlled by the left/right arrow keys."""

    def __init__(self):
        super().__init__()
        self.image  = pygame.image.load("Player.png")
        self.rect   = self.image.get_rect()
        self.rect.bottom = HEIGHT
        self.speed  = 5

    def move(self):
        """Respond to keyboard input and move within screen bounds."""
        pressed_keys = pygame.key.get_pressed()

        if self.rect.right < WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(speed, 0)
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-speed, 0)


P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies    = pygame.sprite.Group(E1)
coins      = pygame.sprite.Group(C1)
all_sprites = pygame.sprite.Group(P1, E1, C1)

inc_speed = pygame.USEREVENT + 1
pygame.time.set_timer(inc_speed, 1000)


while True:
    for event in pygame.event.get():
        if event.type == inc_speed:
            speed += 0.5

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    display.blit(background, (0, 0))

    scores     = font_small.render(f"Score: {score}", True, black)
    coin_text  = font_small.render(f"Coins: {coin}",  True, black)
    display.blit(scores,    (10, 10))
    display.blit(coin_text, (10, 30))

    next_boost = (last_boost_threshold + 1) * SPEED_BOOST_EVERY_N_COINS
    hint = font_small.render(
        f"Next speed boost at {next_boost} coins", True, black
    )
    display.blit(hint, (10, 50))

    for entity in all_sprites:
        display.blit(entity.image, entity.rect)
        entity.move()

    collected = pygame.sprite.spritecollide(P1, coins, False)
    for c in collected:
        coin += c.weight   
        c.reset()          

    current_threshold = coin // SPEED_BOOST_EVERY_N_COINS
    if current_threshold > last_boost_threshold:
        boosts_to_apply = current_threshold - last_boost_threshold
        speed += boosts_to_apply * 1.0         
        last_boost_threshold = current_threshold

    if pygame.sprite.spritecollideany(P1, enemies):
        display.fill(red)
        display.blit(game_over_text, (30, 250))
        pygame.display.update()

        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    framepersec.tick(fps)
