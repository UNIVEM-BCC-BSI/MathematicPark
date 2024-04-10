import pygame
from sys import exit

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Mathematic Park')

player_surface = pygame.image.load('img/player200.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (160, 555))

scene_surface = pygame.image.load('img/scene.jpg').convert()

cone_surface = pygame.image.load('img/cone.png').convert_alpha()
cone_rect = cone_surface.get_rect(midbottom = (1330, 550))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()



    screen.blit(scene_surface, (0, -7))
    screen.blit(player_surface, player_rect)

    cone_rect.x -= 8
    if cone_rect.right <= 0:
        cone_rect.left = 1280

    screen.blit(cone_surface, cone_rect)

    pygame.display.update()
    clock.tick(30)