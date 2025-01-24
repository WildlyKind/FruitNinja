import pygame
import os
import sys
from random import choice
import random

WHITE = pygame.Color("#ffffff")
BLACK = pygame.Color("#000000")
SIZE = WIDTH, HEIGHT = (800, 600)
FPS = 80

def terminate():
    pygame.quit()
    sys.exit()

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def start_screen():
    intro_text = [" FRUIT NINJA",
                  "Легкий уровень", ""
                  "Средний уровень", ""
                  "Сложный уровень"]

    fon = pygame.transform.scale(load_image('fon.jfif'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 170
    for line in intro_text:
        string_rendered = font.render(line, 1, BLACK)
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 250
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


tile_width = tile_height = 50
#images = [load_image('apple1.png'), load_image('lemon1.png'), load_image('pear1.png'),
#          load_image('pineapple1.png'), load_image('watermelon1.png')]


class HalfFruit(pygame.sprite.Sprite):
    def __init__(self, fruit, side, pos_x, pos_y):
        super().__init__(half_fruits, all_sprites)
        self.side = side
        self.image = load_image(fruit)
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def update(self, *args):
        if self.side == 'left':
            self.rect = self.rect.move(-5, 10)
        else:
            self.rect = self.rect.move(5, 10)


class Fruits(pygame.sprite.Sprite):
    def __init__(self, fruit_type):
        super().__init__(fruits_group, all_sprites)
        self.fruit_type = fruit_type
        self.image = load_image(fruit_type + ".png")
        self.rect = self.image.get_rect()
        self.speed = random.randint(1, 5)
        w, h = self.rect.size
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(random.randrange(0, WIDTH - w, 20), 0)


    def update(self, *args):
        self.rect = self.rect.move(0, self.speed)
        if self.rect.y > HEIGHT:
            self.speed = random.randint(1, 6)
            self.rect.y = - self.rect.h
        if args:
            x, y = args[0]
            if self.rect.collidepoint(x, y):
                self.rect.y = -50
                HalfFruit(self.fruit_type + "_left.png", 'left', x, y)
                HalfFruit(self.fruit_type + "_right.png", 'right', x, y)
                #self.image = load_image('apple2.png')


fruits_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
half_fruits = pygame.sprite.Group()

d = ('lemon', 'apple', 'pear', 'pineapple', 'watermelon')

for i in range(10):
    fruit_type = random.choice(d)
    Fruits(fruit_type)

pygame.init()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption('FRUIT NINJA')
start_screen()
#f = Fruits()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            all_sprites.update(event.pos)
    screen.fill(WHITE)
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(FPS)