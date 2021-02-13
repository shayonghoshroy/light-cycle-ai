import pygame

WIN_WIDTH = 1920
WIN_HEIGHT = 960
TILE_SIZE = 16
LIGHTGREY = (100, 100, 100)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 20, 147)
BLUE_BIKE = pygame.transform.scale(pygame.image.load("imgs/blue_bike.png"), (TILE_SIZE, TILE_SIZE))
PINK_BIKE = pygame.transform.scale(pygame.image.load("imgs/pink_bike.png"), (TILE_SIZE, TILE_SIZE))
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


class Grid:
    def draw_grid(self, blue_bike, pink_bike):
        for x in range(0, WIN_WIDTH, TILE_SIZE):
            for y in range(0, WIN_HEIGHT, TILE_SIZE):
                pygame.draw.line(WIN, LIGHTGREY, (x, 0), (x, WIN_HEIGHT))
                pygame.draw.line(WIN, LIGHTGREY, (0, y), (WIN_WIDTH, y))
                if (x, y) in blue_bike.visited:
                    pygame.draw.rect(WIN, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
                if (x, y) in pink_bike.visited:
                    pygame.draw.rect(WIN, PINK, (x, y, TILE_SIZE, TILE_SIZE))


class Bike:
    def __init__(self, x, y, IMG, X_VEL):
        self.x = x
        self.y = y
        self.IMG = IMG
        self.X_VEL = X_VEL
        self.Y_VEL = 0
        self.visited = []

    def move(self):
        self.visited += [(self.x, self.y)]
        self.x += self.X_VEL
        self.y += self.Y_VEL

    def draw(self):
        WIN.blit(self.IMG, (self.x, self.y))
        pygame.display.update()


grid = Grid()
blue_bike = Bike(0, 0, BLUE_BIKE, TILE_SIZE)
pink_bike = Bike(WIN_WIDTH, WIN_HEIGHT-TILE_SIZE, PINK_BIKE, -TILE_SIZE)


def draw_window(grid, blue_bike, pink_bike):
    WIN.fill(BLACK)
    grid.draw_grid(blue_bike, pink_bike)
    blue_bike.draw()
    pink_bike.draw()
    pygame.display.update()


def main():
    while True:
        clock = pygame.time.Clock()
        clock.tick(60)

        blue_bike.move()
        pink_bike.move()

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    blue_bike.X_VEL = 0
                    blue_bike.Y_VEL = TILE_SIZE
                if event.key == pygame.K_UP:
                    blue_bike.X_VEL = 0
                    blue_bike.Y_VEL = -TILE_SIZE
                if event.key == pygame.K_RIGHT:
                    blue_bike.X_VEL = TILE_SIZE
                    blue_bike.Y_VEL = 0
                if event.key == pygame.K_LEFT:
                    blue_bike.X_VEL = -TILE_SIZE
                    blue_bike.Y_VEL = 0

                if event.key == pygame.K_s:
                    pink_bike.X_VEL = 0
                    pink_bike.Y_VEL = TILE_SIZE
                if event.key == pygame.K_w:
                    pink_bike.X_VEL = 0
                    pink_bike.Y_VEL = -TILE_SIZE
                if event.key == pygame.K_d:
                    pink_bike.X_VEL = TILE_SIZE
                    pink_bike.Y_VEL = 0
                if event.key == pygame.K_a:
                    pink_bike.X_VEL = -TILE_SIZE
                    pink_bike.Y_VEL = 0

        draw_window(grid, blue_bike, pink_bike)


if __name__ == '__main__':
    main()
