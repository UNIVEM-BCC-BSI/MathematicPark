import pygame
from sys import exit

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Mathematic Park')

test_surface = pygame.Surface((100, 100))
test_surface.fill('Red')

floor_surface = pygame.Surface((1280, 450))
floor_surface.fill('Green')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(floor_surface, (0, 550))
    screen.blit(test_surface, (80, 450))

    pygame.display.update()
    clock.tick(30)