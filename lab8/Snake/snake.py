import pygame
import sys
import random

pygame.init()

# Настройки экрана
width, height = 500, 500
cell_size = 10
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simple Snake')

# Цвета
black = (0, 0, 0)
green = (0, 255, 0)
red = (213, 50, 80)
blue = (50, 153, 213)
white = (255, 255, 255)

# Параметры змейки
snake_pos = [100, 100]  # Начальная позиция головы змейки
snake_body = [[100, 100], [80, 100], [60, 100]]  # Тело змейки
direction = 'RIGHT'
change_to = direction

# Начальные параметры игры
score = 0
level = 1
speed = 10  # Начальная скорость игры
food_x = 0
food_y = 0
level_up_threshold = 4  # Уровень увеличивается после съеденных 4 еды
food_eaten = 0  # Счётчик съеденных продуктов

# Часы и шрифты
clock = pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Функция для отображения счёта и уровня
def your_score(score, level):
    value = score_font.render("Score: " + str(score) + " Level: " + str(level), True, white)
    screen.blit(value, [0, 0])

# Функция для отрисовки змейки
def draw_snake(snake_block, snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, green, pygame.Rect(block[0], block[1], snake_block, snake_block))

# Функция для генерации еды, чтобы она не пересекалась с телом змейки
def generate_food(snake_list):
    food_x = random.randrange(0, width - cell_size, cell_size)
    food_y = random.randrange(0, height - cell_size, cell_size)
    
    # Проверка, чтобы еда не появлялась на теле змейки
    while [food_x, food_y] in snake_list:
        food_x = random.randrange(0, width - cell_size, cell_size)
        food_y = random.randrange(0, height - cell_size, cell_size)
    
    return food_x, food_y

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
    
    direction = change_to

    # Обновляем позицию головы змейки в зависимости от направления
    if direction == 'UP':
        snake_pos[1] -= cell_size
    elif direction == 'DOWN':
        snake_pos[1] += cell_size
    elif direction == 'LEFT':
        snake_pos[0] -= cell_size
    elif direction == 'RIGHT':
        snake_pos[0] += cell_size

    # Проверка на столкновение с границей экрана (стены)
    if snake_pos[0] < 0 or snake_pos[0] >= width or snake_pos[1] < 0 or snake_pos[1] >= height:
        running = False  # Игра заканчивается, если змейка вышла за пределы

    # Добавляем новую голову змейки
    snake_body.insert(0, list(snake_pos))

    # Если змейка съела еду
    if snake_pos == [food_x, food_y]:
        food_x, food_y = generate_food(snake_body)  # Генерируем новую еду
        food_eaten += 1  # Увеличиваем счётчик съеденной еды
        score += 10  # Увеличиваем счёт

        # Если съедено достаточно еды, увеличиваем уровень и скорость
        if food_eaten >= level_up_threshold:
            level += 1
            speed += 2  # Увеличиваем скорость игры

            # Сбросим счётчик съеденной еды для следующего уровня
            food_eaten = 0

    else:
        snake_body.pop()  # Убираем последний блок (хвост), если змейка не съела еду

    # Отображаем экран
    screen.fill(black)
    pygame.draw.rect(screen, red, pygame.Rect(food_x, food_y, cell_size, cell_size))  # Отрисовываем еду
    draw_snake(cell_size, snake_body)  # Отрисовываем змейку
    your_score(score, level)  # Отображаем счёт и уровень

    pygame.display.flip()  # Обновляем экран

    clock.tick(speed)  # Управляем скоростью игры

# Завершаем игру
pygame.quit()
sys.exit() 