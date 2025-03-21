import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moving Ball")

ball_radius = 25
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2

move_speed = 20

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and ball_x - ball_radius > 0:
        ball_x -= move_speed
    if keys[pygame.K_RIGHT] and ball_x + ball_radius < SCREEN_WIDTH:
        ball_x += move_speed
    if keys[pygame.K_UP] and ball_y - ball_radius > 0:
        ball_y -= move_speed
    if keys[pygame.K_DOWN] and ball_y + ball_radius < SCREEN_HEIGHT:
        ball_y += move_speed

    screen.fill(WHITE)

    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

    pygame.display.flip()

    pygame.time.Clock().tick(60)
