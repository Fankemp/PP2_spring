import pygame
import sys
import math

# ------------ Initialization ------------
pygame.init()

# ------------ Screen settings ------------
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Paint Extended')

# ------------ Colors ------------
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (200, 200, 200)

# ------------ Brush and shape settings ------------
drawing = False
brush_color = black
shape = 'brush'

# ------------ Button class ------------
class Button:
    def __init__(self, x, y, width, height, text, color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, white)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def check_action(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.action()

# ------------ Shape and color selection functions ------------
def set_black():  global brush_color; brush_color = black
def set_green():  global brush_color; brush_color = green
def set_red():    global brush_color; brush_color = red
def set_blue():   global brush_color; brush_color = blue
def set_brush():  global shape; shape = 'brush'
def set_rectangle(): global shape; shape = 'rectangle'
def set_circle(): global shape; shape = 'circle'
def set_eraser(): global shape; shape = 'eraser'
def set_square(): global shape; shape = 'square'
def set_right_triangle(): global shape; shape = 'right_triangle'
def set_equilateral_triangle(): global shape; shape = 'equilateral_triangle'
def set_rhombus(): global shape; shape = 'rhombus'
def clear_screen(): screen.fill(white)
def exit_app(): pygame.quit(); sys.exit()

# ------------ Button definitions ------------
buttons = [
    Button(10, 10, 70, 30, 'Black', black, set_black),
    Button(80, 10, 70, 30, 'Green', green, set_green),
    Button(150, 10, 70, 30, 'Red', red, set_red),
    Button(220, 10, 70, 30, 'Blue', blue, set_blue),
    Button(290, 10, 70, 30, 'Brush', gray, set_brush),
    Button(360, 10, 70, 30, 'Eraser', gray, set_eraser),
    Button(430, 10, 70, 30, 'Rect', gray, set_rectangle),
    Button(500, 10, 70, 30, 'Circle', gray, set_circle),
    Button(570, 10, 70, 30, 'Square', gray, set_square),
    Button(640, 10, 70, 30, 'R-Tri', gray, set_right_triangle),
    Button(710, 10, 85, 30, 'Eq-Tri', gray, set_equilateral_triangle),
    Button(10, 50, 85, 30, 'Rhombus', gray, set_rhombus),
    Button(100, 50, 70, 30, 'Clear', gray, clear_screen),
    Button(170, 50, 70, 30, 'Exit', gray, exit_app)
]

# ------------ Initial screen clear ------------
clear_screen()

# ------------ Main game loop ------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_app()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            drawing = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            drawing = False
        for button in buttons:
            button.check_action(event)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    # ------------ Drawing shapes when mouse is pressed below toolbar ------------
    if drawing and mouse_y > 90:
        if shape == 'brush':
            pygame.draw.circle(screen, brush_color, (mouse_x, mouse_y), 5)
        elif shape == 'rectangle':
            pygame.draw.rect(screen, brush_color, (mouse_x - 50, mouse_y - 25, 100, 50), 2)
        elif shape == 'circle':
            pygame.draw.circle(screen, brush_color, (mouse_x, mouse_y), 40, 2)
        elif shape == 'square':
            pygame.draw.rect(screen, brush_color, (mouse_x - 40, mouse_y - 40, 80, 80), 2)
        elif shape == 'right_triangle':
            points = [(mouse_x, mouse_y), (mouse_x, mouse_y + 80), (mouse_x + 80, mouse_y + 80)]
            pygame.draw.polygon(screen, brush_color, points, 2)
        elif shape == 'equilateral_triangle':
            height_triangle = int(80 * math.sqrt(3) / 2)
            points = [
                (mouse_x, mouse_y - height_triangle // 2),
                (mouse_x - 40, mouse_y + height_triangle // 2),
                (mouse_x + 40, mouse_y + height_triangle // 2)
            ]
            pygame.draw.polygon(screen, brush_color, points, 2)
        elif shape == 'rhombus':
            points = [
                (mouse_x, mouse_y - 50),
                (mouse_x - 30, mouse_y),
                (mouse_x, mouse_y + 50),
                (mouse_x + 30, mouse_y)
            ]
            pygame.draw.polygon(screen, brush_color, points, 2)
        elif shape == 'eraser':
            pygame.draw.circle(screen, white, (mouse_x, mouse_y), 10)

    # ------------ Draw the toolbar ------------
    pygame.draw.rect(screen, gray, (0, 0, width, 90))
    for button in buttons:
        button.draw(screen)

    pygame.display.flip()
