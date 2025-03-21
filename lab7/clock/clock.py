import pygame
import time
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

pygame.display.set_caption("Mickey Mouse Clock")

mainclock = pygame.image.load('D:\\PP2\\PP2_spring\\lab7\\clock\\clock.png')
leftarm = pygame.image.load('D:\\PP2\\PP2_spring\\lab7\\clock\\leftarm.png')
rightarm = pygame.image.load('D:\\PP2\\PP2_spring\\lab7\\clock\\rightarm.png')

mainclock = pygame.transform.scale(mainclock, (800, 600))

done = False

while not done: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    current_time = time.localtime()
    minute = current_time.tm_min
    second = current_time.tm_sec

    second_angle = -second * 6
    minute_angle = -minute * 6 - (second / 60) * 6 - 50

    screen.blit(mainclock, (0, 0))

    rotated_rightarm = pygame.transform.rotate(
        pygame.transform.scale(rightarm, (800, 600)), minute_angle
    )
    rightarm_rect = rotated_rightarm.get_rect(center=(400, 300))
    screen.blit(rotated_rightarm, rightarm_rect)

    rotated_leftarm = pygame.transform.rotate(
        pygame.transform.scale(leftarm, (40, 600)), second_angle
    )
    leftarm_rect = rotated_leftarm.get_rect(center=(400, 300))
    screen.blit(rotated_leftarm, leftarm_rect)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()

