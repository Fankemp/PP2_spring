import pygame
import sys
import random
import time
import psycopg2
import json

# Инициализация PostgreSQL
def create_tables():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="fank_emp2005",
        host="localhost"
    )
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_scores (
        score_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(user_id),
        level INTEGER NOT NULL,
        score INTEGER NOT NULL,
        saved_state JSONB,
        saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

def get_or_create_user(username):
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="fank_emp2005",
        host="localhost",
        client_encoding="utf-8"
    )
    cursor = conn.cursor()
    
    cursor.execute("SELECT user_id FROM users WHERE username = %s;", (username,))
    user = cursor.fetchone()
    
    if not user:
        cursor.execute("INSERT INTO users (username) VALUES (%s) RETURNING user_id;", (username,))
        user_id = cursor.fetchone()[0]
        print(f"New user created: {username}")
    else:
        user_id = user[0]
        cursor.execute("""
        SELECT level, score FROM user_scores 
        WHERE user_id = %s ORDER BY saved_at DESC LIMIT 1;
        """, (user_id,))
        last_game = cursor.fetchone()
        if last_game:
            print(f"Welcome back, {username}! Level: {last_game[0]}, Score: {last_game[1]}")
    
    conn.commit()
    cursor.close()
    conn.close()
    return user_id

def save_game_state(user_id, level, score, snake_body, direction):
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="fank_emp2005",
        host="localhost"
    )
    cursor = conn.cursor()
    
    game_state = {
        "snake_body": snake_body,
        "direction": direction,
        "speed": 10 + (level-1)*2
    }
    
    cursor.execute("""
    INSERT INTO user_scores (user_id, level, score, saved_state)
    VALUES (%s, %s, %s, %s);
    """, (user_id, level, score, json.dumps(game_state)))
    
    conn.commit()
    cursor.close()
    conn.close()


# (инициализация pygame, настройки, класс Food, вспомогательные функции)

def game_loop():
    create_tables()
    
    username = input("Enter your username: ")
    user_id = get_or_create_user(username)
    
    # Инициализация игровых переменных
    snake_pos = [100, 100]
    snake_body = [[100, 100], [90, 100], [80, 100]]
    direction = 'RIGHT'
    change_to = direction
    score = 0
    level = 1
    food_eaten = 0
    level_up_threshold = 4
    paused = False
    
    # Инициализация pygame
    pygame.init()
    width, height = 500, 500
    cell_size = 10
    hud_height = 40
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Snake Game with User Progress')
    
    # Цвета
    black = (0, 0, 0)
    green = (0, 255, 0)
    red = (213, 50, 80)
    gold = (255, 215, 0)
    blue = (50, 153, 213)
    white = (255, 255, 255)
    
    # Уровни
    LEVELS = {
        1: {"walls": [], "speed": 10},
        2: {"walls": [[50,50,400,20], [50,430,400,20]], "speed": 12},
        3: {"walls": [[50,50,20,400], [430,50,20,400]], "speed": 14},
    }
    
    # Создаем первую еду
    foods = []
    def generate_food():
        while True:
            food = Food()
            if [food.x, food.y] not in snake_body:
                foods.clear()
                foods.append(food)
                break
    
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
    
    generate_food()
    
    clock = pygame.time.Clock()
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
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'
                elif event.key == pygame.K_p:  # Пауза по клавише P
                    paused = not paused
                    if paused:
                        save_game_state(user_id, level, score, snake_body, direction)
        
        if paused:
            continue
            
        direction = change_to
        
        # Движение змейки
        if direction == 'UP':
            snake_pos[1] -= cell_size
        elif direction == 'DOWN':
            snake_pos[1] += cell_size
        elif direction == 'LEFT':
            snake_pos[0] -= cell_size
        elif direction == 'RIGHT':
            snake_pos[0] += cell_size
        
        # Проверка столкновений с границами
        if (snake_pos[0] < 0 or snake_pos[0] >= width or
            snake_pos[1] < hud_height or snake_pos[1] >= height):
            running = False
            
        # Проверка столкновений со стенами уровня
        for wall in LEVELS[level].get("walls", []):
            wall_rect = pygame.Rect(*wall)
            if wall_rect.collidepoint(snake_pos[0], snake_pos[1]):
                running = False
        
        snake_body.insert(0, list(snake_pos))
        
        # Проверка съедения еды
        eaten = False
        for food in foods[:]:
            if snake_pos == [food.x, food.y]:
                score += food.weight
                food_eaten += 1
                foods.remove(food)
                generate_food()
                eaten = True
                if food_eaten >= level_up_threshold:
                    level += 1
                    food_eaten = 0
                break

        if not eaten:
            snake_body.pop()
        
        # Проверка истечения срока еды
        for food in foods[:]:
            if food.is_expired():
                foods.remove(food)
                generate_food()
        
        # Отрисовка
        screen.fill(black)
        pygame.draw.rect(screen, blue, (0, 0, width, hud_height))
        
        # Отрисовка стен уровня
        for wall in LEVELS[level].get("walls", []):
            pygame.draw.rect(screen, white, pygame.Rect(*wall))
        
        # Отрисовка змейки и еды
        for block in snake_body:
            pygame.draw.rect(screen, green, pygame.Rect(block[0], block[1], cell_size, cell_size))
        
        for food in foods:
            food.draw()
        
        # Отрисовка счета
        font = pygame.font.SysFont("comicsansms", 35)
        score_text = font.render(f"Score: {score}  Level: {level}", True, white)
        screen.blit(score_text, (10, 5))
        
        pygame.display.flip()
        clock.tick(LEVELS[level]["speed"])
    
    # Сохранение при завершении игры
    save_game_state(user_id, level, score, snake_body, direction)
    pygame.quit()
    sys.exit()

# Запуск игры
if __name__ == "__main__":
    game_loop()