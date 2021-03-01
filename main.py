import pygame, sys, random
from pygame import mixer
from pygame.locals import *
#flags = DOUBLEBUF
pygame.init()
mixer.init()
import time

WIN_WIDTH = 1920
WIN_HEIGHT = 960
TILE_SIZE = 20  # common factors of window are 10, 12, 15, 16, 20, 24, 30, 32, 40, 48, 60, 64
BIKE_SPEED = TILE_SIZE
LIGHTGREY = (25, 25, 25)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 20, 147)
BLUE_BIKE = pygame.transform.scale(pygame.image.load("imgs/blue_bike.png"), (TILE_SIZE, TILE_SIZE))
PINK_BIKE = pygame.transform.scale(pygame.image.load("imgs/pink_bike.png"), (TILE_SIZE, TILE_SIZE))
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
WIN.set_alpha(None)


class Grid:
    def __init__(self):
        for x in range(0, WIN_WIDTH, TILE_SIZE):
            for y in range(0, WIN_HEIGHT, TILE_SIZE):
                pygame.draw.line(WIN, LIGHTGREY, (x, 0), (x, WIN_HEIGHT))
                pygame.draw.line(WIN, LIGHTGREY, (0, y), (WIN_WIDTH, y))

    def draw_grid(self, blue_bike, pink_bike):
        for (x, y) in blue_bike.visited:
            pygame.draw.rect(WIN, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
        for (x, y) in pink_bike.visited:
            pygame.draw.rect(WIN, PINK, (x, y, TILE_SIZE, TILE_SIZE))

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
            self.direction = "up"
        elif self.X_VEL == 0 and self.Y_VEL == BIKE_SPEED:
            self.direction = "down"
        elif self.X_VEL == -BIKE_SPEED and self.Y_VEL == 0:
            self.direction = "left"
        elif self.X_VEL == BIKE_SPEED and self.Y_VEL == 0:
            self.direction = "right"

    def move(self):
        self.visited += [(self.x, self.y)]
        #self.visited += [((self.x*2+self.X_VEL)/2, (self.y*2+self.Y_VEL)/2)]  # fill in the midpoint
        self.x += self.X_VEL
        self.y += self.Y_VEL

    def draw(self):
        if self.direction == "up":
            WIN.blit(pygame.transform.rotate(self.IMG, -90), (self.x, self.y))
        elif self.direction == "down":
            WIN.blit(pygame.transform.rotate(self.IMG, 90), (self.x, self.y))
        elif self.direction == "left":
            WIN.blit(pygame.transform.rotate(self.IMG, -180), (self.x, self.y))
        else:
            WIN.blit(self.IMG, (self.x, self.y))
        pygame.display.update()

    def set_direction(self, direction):
        self.direction = direction
        if self.direction == "up":
            self.X_VEL = 0
            self.Y_VEL = -BIKE_SPEED
        elif self.direction == "down":
            self.X_VEL = 0
            self.Y_VEL = BIKE_SPEED
        elif self.direction == "left":
            self.X_VEL = -BIKE_SPEED
            self.Y_VEL = 0
        elif self.direction == "right":
            self.X_VEL = BIKE_SPEED
            self.Y_VEL = 0


def draw_window(grid, blue_bike, pink_bike, blue_score, pink_score):
    write_scores(str(blue_score), str(pink_score))
    blue_bike.move()
    pink_bike.move()
    grid.draw_grid(blue_bike, pink_bike)
    blue_bike.draw()
    pink_bike.draw()
    pygame.display.update()

def write(word, color):
    font = pygame.font.Font('freesansbold.ttf', 72)
    text = font.render(word, True, color, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (WIN_WIDTH // 2, WIN_HEIGHT // 2)
    WIN.fill(BLACK)
    WIN.blit(text, text_rect)
    pygame.display.update()


def write_scores(blue_score, pink_score):
    font = pygame.font.Font('freesansbold.ttf', 48)
    text = font.render(blue_score, True, BLUE, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (WIN_WIDTH - text.get_width(), text.get_height())
    WIN.blit(text, text_rect)
    text = font.render(pink_score, True, PINK, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (WIN_WIDTH - text.get_width(), text.get_height() * 2)
    WIN.blit(text, text_rect)


def reset_players(grid, blue_bike, pink_bike, blue_score, pink_score):
    WIN.fill(BLACK)
    grid = Grid()
    blue_bike.visited = []
    pink_bike.visited = []
    blue_bike.x = 0
    blue_bike.y = 0
    blue_bike.set_direction("right")
    pink_bike.x = WIN_WIDTH
    pink_bike.y = WIN_HEIGHT-TILE_SIZE
    pink_bike.set_direction("left")
    draw_window(grid, blue_bike, pink_bike, blue_score, pink_score)


def check_collisions(grid, blue_bike, pink_bike, blue_score, pink_score):
    if (blue_bike.x, blue_bike.y) in pink_bike.visited or (blue_bike.x, blue_bike.y) in blue_bike.visited\
            or blue_bike.x < 0 or blue_bike.x > WIN_WIDTH or blue_bike.y < 0 or blue_bike.y > WIN_HEIGHT:
        pink_score += 1
        write_scores(str(blue_score), str(pink_score))
        reset_players(grid, blue_bike, pink_bike, blue_score, pink_score)
    elif (pink_bike.x, pink_bike.y) in blue_bike.visited or (pink_bike.x, pink_bike.y) in pink_bike.visited \
            or pink_bike.x < 0 or pink_bike.x > WIN_WIDTH or pink_bike.y < 0 or pink_bike.y > WIN_HEIGHT:
        blue_score += 1
        write_scores(str(blue_score), str(pink_score))
        reset_players(grid, blue_bike, pink_bike, blue_score, pink_score)
    return blue_score, pink_score

# TODO: MAKE A DUPLICATE OF GAME FUNCTION FOR AI VERSION, HAVE PLAYER CHOOSE AGAINST CPU OR 2 PLAYER

def game():
    WIN.fill(BLACK)
    grid = Grid()
    blue_bike = Bike(0, 0, BLUE_BIKE, BIKE_SPEED, 0)
    pink_bike = Bike(WIN_WIDTH, WIN_HEIGHT-TILE_SIZE, PINK_BIKE, -BIKE_SPEED, 0)
    blue_score = 0
    pink_score = 0

    #mixer.music.load("sound/son_of_flynn.mp3")
    #mixer.music.play()

    while True:
        clock = pygame.time.Clock()
        clock.tick(120)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    blue_bike.set_direction("down")
                if event.key == pygame.K_UP:
                    blue_bike.set_direction("up")
                if event.key == pygame.K_RIGHT:
                    blue_bike.set_direction("right")
                if event.key == pygame.K_LEFT:
                    blue_bike.set_direction("left")
                if event.key == pygame.K_s:
                    pink_bike.set_direction("down")
                if event.key == pygame.K_w:
                    pink_bike.set_direction("up")
                if event.key == pygame.K_d:
                    pink_bike.set_direction("right")
                if event.key == pygame.K_a:
                    pink_bike.set_direction("left")

        draw_window(grid, blue_bike, pink_bike, blue_score, pink_score)
        blue_score, pink_score = check_collisions(grid, blue_bike, pink_bike, blue_score, pink_score)


if __name__ == '__main__':
    game()
