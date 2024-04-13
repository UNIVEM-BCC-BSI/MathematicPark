import pygame
from sys import exit

pygame.init()

# Constantes
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GROUND_LEVEL = 555
JUMP_VALUE = -35

#Variáveis do Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Mathematic Park')
game_active = False
start_screen = True
question_active = False

#Variáveis de texto
title_font = pygame.font.Font('ARCADECLASSIC.TTF', 100)
subtitle_font = pygame.font.Font('ARCADECLASSIC.TTF', 50)
start_font = pygame.font.Font('ARCADECLASSIC.TTF', 32)

game_over_text_surface = title_font.render('Voce  perdeu', False, 'yellow')
game_over_press_button_text_surface = subtitle_font.render('Pressione  espaco  para  tentar  novamente', False, 'White')
start_text = start_font.render('Pressione  qualquer  tecla  para  jogar', False, 'White')

start_text_rect = start_text.get_rect()
start_text_rect.midtop = (SCREEN_WIDTH/2, 500)

question_text_surface = subtitle_font.render('PERGUNTA Apertes espaço', False, 'Black')

#Variáveis do player
player_surface = pygame.image.load('img/player200.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (160, GROUND_LEVEL))
player_gravity = 0

#Variáveis do cenário
scene_surface = pygame.image.load('img/scene.jpg').convert()

#Variáveis do obstáculo
cone_surface = pygame.image.load('img/cone.png').convert_alpha()
cone_rect = cone_surface.get_rect(midbottom = (1330, GROUND_LEVEL))
question_rect = pygame.Rect(cone_rect.top, cone_rect.left,  4, 1000)
obstacle_count = 0

#Loop do jogo
while True:
    
    #Tela Inicial
    while start_screen:
        screen.blit(start_text, start_text_rect)
        pygame.display.flip()
        for key in pygame.event.get():
            if key.type == pygame.QUIT:
                pygame.quit()
                exit()
            if key.type == pygame.KEYUP:
                start_screen = False
                game_active = True
                
    
    while question_active:
        # screen.blit(question_text_surface, (200, 50))
        screen.blit(start_text, start_text_rect)
        pygame.display.flip()
        for key in pygame.event.get():
            if key.type == pygame.QUIT:
                pygame.quit()
                exit()
            if key.type == pygame.KEYUP:
                question_active = False 
                obstacle_count += 1

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
                    obstacle_count = 0

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

        if obstacle_count == 0:
            if question_rect.colliderect(player_rect):
                question_active = True
        

        #Mecânica de teste do movimento do cone
        cone_rect.x -= 15
        if cone_rect.right <= 0:
            cone_rect.left = 1280
            obstacle_count = 0
        question_rect.midbottom = cone_rect.midtop

        #Atualizações no display
        screen.blit(scene_surface, (0, -7))
        screen.blit(cone_surface, cone_rect)
        screen.blit(player_surface, player_rect)
        pygame.draw.rect(screen, (255, 0, 0), question_rect)
    else:
        screen.fill('black')
        screen.blit(game_over_text_surface, (400, 150))
        screen.blit(game_over_press_button_text_surface, (150, 400))


    pygame.display.update()
    clock.tick(30)
    