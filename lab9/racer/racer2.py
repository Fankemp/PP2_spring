# ------------------- Imports -------------------
import pygame, sys
from pygame.locals import *
import random, time

# ------------------- Initialization -------------------
pygame.init()

# ------------------- Game Constants -------------------
FPS = 60
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0
COIN_TARGET_FOR_SPEEDUP = 5  # Каждые 5 очков монет — увеличение скорости
ENEMY_SPEED_INCREMENT = 1

# ------------------- Colors -------------------
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# ------------------- Fonts -------------------
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("GAME OVER", True, BLACK)

# ------------------- Assets -------------------
background = pygame.image.load("AnimatedStreet.png")
original_coin = pygame.image.load("coin.png")
coin_image = pygame.transform.scale(original_coin, (30, 30))  # уменьшенная монета

# ------------------- Display Setup -------------------
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racer")

# ------------------- Enemy Class -------------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# ------------------- Player Class -------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

# ------------------- Coin Class with Weights -------------------
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_image
        self.rect = self.image.get_rect()
        self.weight = random.choice([1, 2, 3])  # Вес монеты
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-100, 0))

    def respawn(self):
        # Случайный вес и новая позиция
        self.weight = random.choice([1, 2, 3])
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-100, 0))

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.respawn()

# ------------------- Setup Game Entities -------------------
P1 = Player()
E1 = Enemy()

# Создаём группы
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# Генерируем 3 монеты
for _ in range(3):
    coin = Coin()
    coins.add(coin)
    all_sprites.add(coin)

# ------------------- Speed Increase Timer Event -------------------
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# ------------------- Main Game Loop -------------------
FramePerSec = pygame.time.Clock()

while True:
    # ------------------- Event Handling -------------------
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # ------------------- Drawing Background -------------------
    DISPLAYSURF.blit(background, (0, 0))

    # ------------------- Display Score and Coins -------------------
    score_text = font_small.render(f"Score: {SCORE}", True, BLACK)
    coins_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - 100, 10))

    # ------------------- Update and Draw Sprites -------------------
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # ------------------- Collision with Enemy -------------------
    if pygame.sprite.spritecollideany(P1, enemies):
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # ------------------- Collecting Coins -------------------
    collected_coins = pygame.sprite.spritecollide(P1, coins, False)
    for coin in collected_coins:
        COINS_COLLECTED += coin.weight  # Добавляем вес
        coin.respawn()
        # Увеличение скорости при достижении кратного количества монет
        if COINS_COLLECTED % COIN_TARGET_FOR_SPEEDUP == 0:
            SPEED += ENEMY_SPEED_INCREMENT

    # ------------------- Refresh Screen -------------------
    pygame.display.update()
    FramePerSec.tick(FPS)
