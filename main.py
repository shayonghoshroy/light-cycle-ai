import os
import neat
import pygame
from pygame import mixer
from pygame.locals import *
#flags = DOUBLEBUF
pygame.init()
mixer.init()
import time
import numpy as np
import pickle


WIN_WIDTH = 1920
WIN_HEIGHT = 960
TILE_SIZE = 20  # common factors of window are 10, 12, 15, 16, 20, 24, 30, 32, 40, 48, 60, 64
BIKE_SPEED = TILE_SIZE
MUSIC_DELAY = 1.15
LIGHTGREY = (25, 25, 25)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 20, 147)
WHITE = (255, 255, 255)
FONT = 'freesansbold.ttf'
FONT_SIZE = 72
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
ROTATE = 90
BLUE_BIKE = pygame.transform.scale(pygame.image.load("imgs/blue_bike.png"), (TILE_SIZE, TILE_SIZE))
PINK_BIKE = pygame.transform.scale(pygame.image.load("imgs/pink_bike.png"), (TILE_SIZE, TILE_SIZE))
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
WIN.set_alpha(None)


# draw lines for grid
def spawn_grid():
    for x in range(0, WIN_WIDTH, TILE_SIZE):
        pygame.draw.line(WIN, LIGHTGREY, (x, 0), (x, WIN_HEIGHT))
    for y in range(0, WIN_HEIGHT, TILE_SIZE):
        pygame.draw.line(WIN, LIGHTGREY, (0, y), (WIN_WIDTH, y))


# draw visited squares for each bike
def draw_visited(blue_bike, pink_bike):
    for (x, y) in blue_bike.visited:
        pygame.draw.rect(WIN, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
    for (x, y) in pink_bike.visited:
        pygame.draw.rect(WIN, PINK, (x, y, TILE_SIZE, TILE_SIZE))


# bike object
class Bike:
    def __init__(self, x, y, IMG, X_VEL, Y_VEL):
        self.x = x
        self.y = y
        self.IMG = IMG
        self.X_VEL = X_VEL
        self.Y_VEL = Y_VEL
        self.visited = []
        self.direction = ""
        if self.X_VEL == 0 and self.Y_VEL == -BIKE_SPEED:
            self.direction = UP
        elif self.X_VEL == 0 and self.Y_VEL == BIKE_SPEED:
            self.direction = DOWN
        elif self.X_VEL == -BIKE_SPEED and self.Y_VEL == 0:
            self.direction = LEFT
        elif self.X_VEL == BIKE_SPEED and self.Y_VEL == 0:
            self.direction = RIGHT

    # move bike along current path, add coordinate to list of visited places
    def move(self):
        self.visited += [(self.x, self.y)]
        pygame.draw.rect(WIN, BLUE, (self.x, self.y, TILE_SIZE, TILE_SIZE))
        self.x += self.X_VEL
        self.y += self.Y_VEL

    # draw bike img at new location
    def draw(self):
        if self.direction == UP:
            WIN.blit(pygame.transform.rotate(self.IMG, -ROTATE), (self.x, self.y))
        elif self.direction == DOWN:
            WIN.blit(pygame.transform.rotate(self.IMG, ROTATE), (self.x, self.y))
        elif self.direction == LEFT:
            WIN.blit(pygame.transform.rotate(self.IMG, -(ROTATE*2)), (self.x, self.y))
        else:
            WIN.blit(self.IMG, (self.x, self.y))
        pygame.display.update()

    # if a new direction is chosen, reset the bike img and direction
    def set_direction(self, direction):
        self.direction = direction
        if self.direction == UP:
            self.X_VEL = 0
            self.Y_VEL = -BIKE_SPEED
        elif self.direction == DOWN:
            self.X_VEL = 0
            self.Y_VEL = BIKE_SPEED
        elif self.direction == LEFT:
            self.X_VEL = -BIKE_SPEED
            self.Y_VEL = 0
        elif self.direction == RIGHT:
            self.X_VEL = BIKE_SPEED
            self.Y_VEL = 0


# draw all elements in the window
def draw_window(blue_bike, pink_bike, blue_score, pink_score):
    write_scores(str(blue_score), str(pink_score))
    blue_bike.move()
    pink_bike.move()
    draw_visited(blue_bike, pink_bike)
    blue_bike.draw()
    pink_bike.draw()
    pygame.display.update()


# write a word in the center of the window
def write(word, color):
    font = pygame.font.Font(FONT, FONT_SIZE)
    text = font.render(word, True, color, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (WIN_WIDTH // 2, WIN_HEIGHT // 2)
    WIN.fill(BLACK)
    WIN.blit(text, text_rect)
    pygame.display.update()


# write the current score for each bike
def write_scores(blue_score, pink_score):
    font = pygame.font.Font(FONT, FONT_SIZE)
    text = font.render(blue_score, True, BLUE)
    text.set_alpha(200)
    text_rect = text.get_rect()
    text_rect.center = (WIN_WIDTH - text.get_width(), text.get_height())
    WIN.blit(text, text_rect)
    text = font.render(pink_score, True, PINK)
    text.set_alpha(200)
    text_rect = text.get_rect()
    text_rect.center = (WIN_WIDTH - text.get_width(), text.get_height() * 2)
    WIN.blit(text, text_rect)


# after a death, reset to start
def reset_players(blue_bike, pink_bike, blue_score, pink_score):
    WIN.fill(BLACK)
    spawn_grid()
    blue_bike.visited = []
    pink_bike.visited = []
    blue_bike.x = 0
    blue_bike.y = 0
    blue_bike.set_direction(RIGHT)
    pink_bike.x = WIN_WIDTH
    pink_bike.y = WIN_HEIGHT-TILE_SIZE
    pink_bike.set_direction(LEFT)
    draw_window(blue_bike, pink_bike, blue_score, pink_score)


# check for collisions
def check_collisions(blue_bike, pink_bike, blue_score, pink_score):
    if (blue_bike.x, blue_bike.y) in pink_bike.visited or (blue_bike.x, blue_bike.y) in blue_bike.visited\
            or blue_bike.x < 0 or blue_bike.x > WIN_WIDTH or blue_bike.y < 0 or blue_bike.y > WIN_HEIGHT:
        pink_score += 1
        write_scores(str(blue_score), str(pink_score))
        reset_players(blue_bike, pink_bike, blue_score, pink_score)
    elif (pink_bike.x, pink_bike.y) in blue_bike.visited or (pink_bike.x, pink_bike.y) in pink_bike.visited \
            or pink_bike.x < 0 or pink_bike.x > WIN_WIDTH or pink_bike.y < 0 or pink_bike.y > WIN_HEIGHT:
        blue_score += 1
        write_scores(str(blue_score), str(pink_score))
        reset_players(blue_bike, pink_bike, blue_score, pink_score)
    return blue_score, pink_score


# display title, play music
def start_screen():
    mixer.music.load("sound/son_of_flynn.mp3")
    mixer.music.play()

    display_word_with_delay("T", MUSIC_DELAY/4)
    display_word_with_delay("TR", MUSIC_DELAY/4)
    display_word_with_delay("TRO", MUSIC_DELAY/4)
    display_word_with_delay("TRON", MUSIC_DELAY/4)


# display a word and add delay for it
def display_word_with_delay(word, delay):
    write(word, WHITE)
    pygame.display.update()
    clock = pygame.time.Clock()
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    time.sleep(delay)
    WIN.fill(BLACK)


# main game loop
def game():
    WIN.fill(BLACK)
    start_screen()
    spawn_grid()

    blue_bike = Bike(0, 0, BLUE_BIKE, BIKE_SPEED, 0)
    pink_bike = Bike(WIN_WIDTH, WIN_HEIGHT-TILE_SIZE, PINK_BIKE, -BIKE_SPEED, 0)
    blue_score = 0
    pink_score = 0

    while True:
        clock = pygame.time.Clock()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    blue_bike.set_direction(DOWN)
                if event.key == pygame.K_UP:
                    blue_bike.set_direction(UP)
                if event.key == pygame.K_RIGHT:
                    blue_bike.set_direction(RIGHT)
                if event.key == pygame.K_LEFT:
                    blue_bike.set_direction(LEFT)
                if event.key == pygame.K_s:
                    pink_bike.set_direction(DOWN)
                if event.key == pygame.K_w:
                    pink_bike.set_direction(UP)
                if event.key == pygame.K_d:
                    pink_bike.set_direction(RIGHT)
                if event.key == pygame.K_a:
                    pink_bike.set_direction(LEFT)

        draw_window(blue_bike, pink_bike, blue_score, pink_score)
        blue_score, pink_score = check_collisions(blue_bike, pink_bike, blue_score, pink_score)


if __name__ == '__main__':
    game()
































