import pygame, sys, time
from pygame.locals import *
import random

pygame.init()

fps = 60
framepersec = pygame.time.Clock()

blue = pygame.Color(0, 0, 255)
green = pygame.Color(0, 255, 0)
red = pygame.Color(255, 0, 0)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

width = 400
height = 600
speed = 5
score = 0
coin = 0

font = pygame.font.SysFont("TimesNewRoman", 60)
font_small = pygame.font.SysFont("TimesNewRoman", 20)
game_over = font.render("Game Over", True, black)

background = pygame.image.load("AnimatedStreet.png")

display = pygame.display.set_mode((width, height))
display.fill(white)
pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, width-40), 0)
    
    def move(self):
        global score
        self.rect.move_ip(0, speed)
        if self.rect.top > height:
            score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, width - 40), 0)
    

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        original = pygame.image.load("coin.png").convert_alpha()
        self.image = pygame.transform.scale(original, (30, 30))  
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(40, width-40), random.randint(-100, -40))

    def move(self):
        self.rect.move_ip(0, speed)
        if self.rect.top > height:
            self.reset()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect_center = (160, 520)
        self.rect.bottom = height
        self.speed = 5

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.right < width:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(speed, 0)
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-speed, 0)


P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group(E1)
coins = pygame.sprite.Group(C1)

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

    display.blit(background, (0,0))
    scores = font_small.render(str(score), True, black)
    display.blit(scores, (10, 10))
    coin_text = font_small.render(str(coin), True, black)
    display.blit(coin_text, (width - 120, 10))
    
    for entity in all_sprites:
        display.blit(entity.image, entity.rect)
        entity.move()

    collect = pygame.sprite.spritecollide(P1, coins, False)
    for c in collect:
        coin += 10
        c.reset()

    if pygame.sprite.spritecollideany(P1, enemies):
        #pygame.mixer.Sound('crash.wav').play()
        #time.sleep(0.5)

        display.fill(red)
        display.blit(game_over, (30, 250))
        pygame.display.update()

        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exist()

    pygame.display.update()
    framepersec.tick(fps)
