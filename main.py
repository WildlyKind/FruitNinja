import pygame
import os
import sys
import random
import time

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
    arr_rect = []
    for line in intro_text:
        string_rendered = font.render(line, 1, BLACK)
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 250
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        arr_rect.append(intro_rect)

    arr_rect = arr_rect[1:]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if arr_rect[0].collidepoint(event.pos):
                    light()
                elif arr_rect[1].collidepoint(event.pos):
                    medium()
                else:
                    hard()

                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)

def finish_screen():
    intro_text = [" Поздравляю!",
                  "    Ты набрал", ""
                  f"    {result} баллов"]

    fon = pygame.transform.scale(load_image('fon6.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    text_coord = 170
    arr_rect = []
    for line in intro_text:
        string_rendered = font.render(line, 1, BLACK)
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 250
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        arr_rect.append(intro_rect)

    arr_rect = arr_rect[1:]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if arr_rect[0].collidepoint(event.pos):
                    light()
                elif arr_rect[1].collidepoint(event.pos):
                    medium()
                else:
                    hard()

                return
        pygame.display.flip()
        clock.tick(FPS)

tile_width = tile_height = 50

class HalfFruit(pygame.sprite.Sprite):
    def __init__(self, fruit, side, pos_x, pos_y):
        super().__init__(half_fruits, all_sprites)
        self.side = side
        self.image = load_image(fruit)
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def update(self, *args):
        if self.side == 'left':
            self.rect = self.rect.move(-5, 8)
        else:
            self.rect = self.rect.move(5, 8)


class Fruits(pygame.sprite.Sprite):
    def __init__(self, fruit_type, speed):
        super().__init__(fruits_group, all_sprites)
        self.fruit_type = fruit_type
        self.image = load_image(fruit_type + ".png")
        self.rect = self.image.get_rect()
        self.speed = random.randint(1, speed)
        w, h = self.rect.size
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(random.randrange(0, WIDTH - w, 20), 0)

    def update(self, *args):
        self.rect = self.rect.move(0, self.speed)
        if self.rect.y > HEIGHT:
            self.speed = random.randint(1, 5)
            self.rect.y = - self.rect.h
        if args:
            x, y = args[0]
            if self.rect.collidepoint(x, y):
                self.rect.y = -50
                HalfFruit(self.fruit_type + "_left.png", 'left', x, y)
                HalfFruit(self.fruit_type + "_right.png", 'right', x, y)


class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb.png")
    image_boom = load_image("boom.png")

    def __init__(self, speed):
        super().__init__(bomb_group, all_sprites)
        self.image = load_image('bomb.png')
        self.rect = self.image.get_rect()
        w, h = self.rect.size
        self.rect = self.rect.move(random.randrange(0, WIDTH - w, 20), 0)
        self.speed = random.randint(1, speed)

    def update(self, *args, **kwargs):
        self.rect = self.rect.move(0, self.speed)
        if self.rect.y > HEIGHT:
            self.speed = random.randint(1, self.speed)
            self.rect.y = - self.rect.h
        if args:
            x, y = args[0]
            #if flag: self.kill()
            if self.rect.collidepoint(x, y):
                self.image = Bomb.image_boom
                self.speed = random.randint(3, 5)
        if self.rect.y > 590:
            self.image = Bomb.image


fruits_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
half_fruits = pygame.sprite.Group()
bomb_group = pygame.sprite.Group()

d = ('lemon', 'apple', 'pear', 'pineapple', 'watermelon')

def light():
    for i in range(10):
        fruit_type = random.choice(d)
        Fruits(fruit_type, 5)

def medium():
    for i in range(10):
        fruit_type = random.choice(d)
        Fruits(fruit_type, 5)
    for i in range(5):
        Bomb(5)

def hard():
    for i in range(12):
        fruit_type = random.choice(d)
        Fruits(fruit_type, 7)
    for i in range(10):
        Bomb(7)

pygame.init()
timer_interval = 1000 # 0.5 seconds
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, timer_interval)
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption('FRUIT NINJA')
start_screen()
result = 0
count_time = 5


while True:
    for event in pygame.event.get():
        if event.type == timer_event:
            count_time -= 1
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            all_sprites.update(event.pos)
            result += 5
            print(result)
        if count_time == 0:
            finish_screen()

    screen.fill(WHITE)

    f1 = pygame.font.Font(None, 50)
    text1 = f1.render(f'{count_time}', 1, BLACK)
    screen.blit(text1, (750, 550))

    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(FPS)