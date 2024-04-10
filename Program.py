import pygame
from sys import exit

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Mathematic Park')

player_surface = pygame.image.load('img/player200.png').convert_alpha()
scene_surface = pygame.image.load('img/scene.jpg').convert()

cone_surface = pygame.image.load('img/cone.png').convert_alpha()
cone_xpos = 1280

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()



    screen.blit(scene_surface, (0, -7))
    screen.blit(player_surface, (80, 356))

    cone_xpos -= 8
    if cone_xpos < -100:
        cone_xpos = 1280

    screen.blit(cone_surface, (cone_xpos, 450))

    pygame.display.update()
    clock.tick(30)