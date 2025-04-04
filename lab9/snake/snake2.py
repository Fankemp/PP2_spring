import pygame
import sys
import random
import time

pygame.init()

# ------------ Screen and grid settings ------------
width, height = 500, 500
cell_size = 10
hud_height = 40
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake with Bonus Apples')

# ------------ Colors ------------
black = (0, 0, 0)
green = (0, 255, 0)
red = (213, 50, 80)
gold = (255, 215, 0)
blue = (50, 153, 213)
white = (255, 255, 255)

# ------------ Snake parameters ------------
snake_pos = [100, 100]
snake_body = [[100, 100], [90, 100], [80, 100]]
direction = 'RIGHT'
change_to = direction

# ------------ Score and speed ------------
score = 0
level = 1
speed = 10
food_eaten = 0
level_up_threshold = 4

# ------------ Fonts and timer ------------
clock = pygame.time.Clock()
font = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# ------------ Food list (only 1 at a time) ------------
foods = []

# ------------ Food class ------------
class Food:
    def __init__(self):
        self.spawn()

    def spawn(self):
        self.x = random.randrange(0, width - cell_size, cell_size)
        self.y = random.randrange(hud_height, height - cell_size, cell_size)
        self.weight = random.choices([10, 30], weights=[0.8, 0.2])[0]
        self.color = red if self.weight == 10 else gold
        self.created_time = time.time()

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, cell_size, cell_size))

    def is_expired(self, timeout=6):
        return time.time() - self.created_time > timeout

# ------------ Show score and level ------------
def show_score(score, level):
    value = score_font.render(f"Score: {score}  Level: {level}", True, white)
    screen.blit(value, (10, 5))

# ------------ Draw the snake ------------
def draw_snake(snake_block, snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, green, pygame.Rect(block[0], block[1], snake_block, snake_block))

# ------------ Generate food NOT on snake ------------
def generate_food():
    while True:
        food = Food()
        if [food.x, food.y] not in snake_body:
            foods.clear()         # ensure only one apple at a time
            foods.append(food)
            break

# ------------ First food ------------
generate_food()

# ------------ Game loop ------------
running = True
while running:
    # --- Input handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'

    direction = change_to

    # --- Move the snake ---
    if direction == 'UP':
        snake_pos[1] -= cell_size
    elif direction == 'DOWN':
        snake_pos[1] += cell_size
    elif direction == 'LEFT':
        snake_pos[0] -= cell_size
    elif direction == 'RIGHT':
        snake_pos[0] += cell_size

    # --- Wall / HUD collision ---
    if (snake_pos[0] < 0 or
        snake_pos[0] >= width or
        snake_pos[1] < hud_height or
        snake_pos[1] >= height):
        running = False

    # --- Update snake body ---
    snake_body.insert(0, list(snake_pos))

    # --- Check food collision ---
    eaten = False
    for food in foods[:]:
        if snake_pos == [food.x, food.y]:
            score += food.weight
            food_eaten += 1
            foods.remove(food)
            generate_food()  # immediately add new one
            eaten = True
            if food_eaten >= level_up_threshold:
                level += 1
                speed += 2
                food_eaten = 0
            break

    if not eaten:
        snake_body.pop()

    # --- Check food expiration ---
    for food in foods[:]:
        if food.is_expired():
            foods.remove(food)
            generate_food()  # add new one immediately

    # --- Drawing ---
    screen.fill(black)
    pygame.draw.rect(screen, blue, (0, 0, width, hud_height))  # HUD
    draw_snake(cell_size, snake_body)
    for food in foods:
        food.draw()
    show_score(score, level)

    pygame.display.flip()
    clock.tick(speed)

# --- End the game ---
pygame.quit()
sys.exit()
