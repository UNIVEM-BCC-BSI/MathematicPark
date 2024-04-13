import pygame
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('img/player200.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (160, GROUND_LEVEL))
        self.gravity = 0
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_PAGEUP]) and self.rect.bottom >= GROUND_LEVEL:
            self.gravity = -33

    def apply_gravity(self):
        self.gravity += 2
        self.rect.y += self.gravity
        if self.rect.bottom >= GROUND_LEVEL:
            self.rect.bottom = GROUND_LEVEL

    def update(self):
        self.player_input()
        self.apply_gravity()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "cone":
            self.image = pygame.image.load('img/cone.png').convert_alpha()

        self.rect = self.image.get_rect(midbottom = (1330, GROUND_LEVEL))
        self.count = 0
        self.question_rect = pygame.Rect(self.rect.top, self.rect.left,  4, 1000)
        
        

    def update(self):
        self.rect.x -= 12
        if self.rect.right <= 0:
            self.rect.left = 1280
        self.question_rect.x = self.rect.x
        pygame.draw.rect(screen, (255, 0, 0), self.question_rect)

pygame.init()

# Constantes
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GROUND_LEVEL = 555

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

#Grupos
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()
obstacle_group.add(Obstacle("cone"))


#Variáveis do cenário
scene_surface = pygame.image.load('img/scene.jpg').convert()

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
                obstacle_group.count += 1

    for event in pygame.event.get():
        #Funcionalidade de fechar o jogo
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if game_active:
        #Colisões
        # if cone_rect.colliderect(player_rect):
        #     game_active = False

        # if obstacle_count == 0:
        #     if question_rect.colliderect(player_rect):
        #         question_active = True
        
        #Atualizações no display
        screen.blit(scene_surface, (0, -7))
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        for sprite in obstacle_group:
             question_rect = pygame.Rect(0, 0,  4, 1000)
             question_rect.x = sprite.rect.x
             question_rect.midbottom = sprite.rect.midtop
             pygame.draw.rect(screen, (255, 0, 0), question_rect)
        obstacle_group.update()


        # pygame.draw.rect(screen, (255, 0, 0), question_rect)
    else:
        screen.fill('black')
        screen.blit(game_over_text_surface, (400, 150))
        screen.blit(game_over_press_button_text_surface, (150, 400))


    pygame.display.update()
    clock.tick(30)
    