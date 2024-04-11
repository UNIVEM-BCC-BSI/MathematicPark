import pygame
from sys import exit

pygame.init()

# Constantes
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GROUND_LEVEL = 555
JUMP_VALUE = -30

#Variáveis do Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Mathematic Park')
game_active = True

#Variáveis de texto
title_font = pygame.font.Font(None, 100)
subtitle_font = pygame.font.Font(None, 50)

game_over_text_surface = title_font.render('Você perdeu', False, 'White')
game_over_press_button_text_surface = subtitle_font.render('Pressione espaço para tentar novamente', False, 'White')

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
        
        if game_active:
            #Eventos de pulo
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom == GROUND_LEVEL:
                    player_gravity = JUMP_VALUE

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_PAGEUP or pygame.K_w) and player_rect.bottom == GROUND_LEVEL: 
                    player_gravity = JUMP_VALUE

        else:
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE):
                    game_active = True
                    cone_rect.left = 1280

    if game_active:
        #Funcionalidade da gravidade
        player_gravity += 2
        player_rect.y += player_gravity

        #Funcionalidade do chão
        if player_rect.bottom > GROUND_LEVEL:
            player_rect.bottom = GROUND_LEVEL

        #Colisões
        if cone_rect.colliderect(player_rect):
            game_active = False

        #Mecânica de teste do movimento do cone
        cone_rect.x -= 15
        if cone_rect.right <= 0:
            cone_rect.left = 1280

        #Atualizações no display
        screen.blit(scene_surface, (0, -7))
        screen.blit(cone_surface, cone_rect)
        screen.blit(player_surface, player_rect)
    else:
        screen.fill('black')
        screen.blit(game_over_text_surface, (400, 150))
        screen.blit(game_over_press_button_text_surface, (300, 400))



    pygame.display.update()
    clock.tick(30)
    