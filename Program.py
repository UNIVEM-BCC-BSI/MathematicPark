import pygame
from sys import exit

pygame.init()

# Constantes
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GROUND_LEVEL = 555
JUMP_VALUE = -25

#Variáveis do Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Mathematic Park')

#Variáveis do player
player_surface = pygame.image.load('img/player200.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (160, GROUND_LEVEL))
player_gravity = 0

#Variáveis do cenário
scene_surface = pygame.image.load('img/scene.jpg').convert()

#Variáveis do obstáculo
cone_surface = pygame.image.load('img/cone.png').convert_alpha()
cone_rect = cone_surface.get_rect(midbottom = (1330, GROUND_LEVEL))

#Loop do jogo
while True:
    for event in pygame.event.get():

        #Funcionalidade de fechar o jogo
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        #Eventos de pulo
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos):
                player_gravity = JUMP_VALUE

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_PAGEUP: 
                player_gravity = JUMP_VALUE

    #Funcionalidade da gravidade
    player_gravity += 2
    player_rect.y += player_gravity

    #Funcionalidade do chão
    if player_rect.bottom > GROUND_LEVEL:
        player_rect.bottom = GROUND_LEVEL

    #Mecânica de teste do movimento do cone
    cone_rect.x -= 12
    if cone_rect.right <= 0:
        cone_rect.left = 1280

    #Atualizações no display
    screen.blit(scene_surface, (0, -7))
    screen.blit(cone_surface, cone_rect)
    screen.blit(player_surface, player_rect)



    pygame.display.update()
    clock.tick(30)
    