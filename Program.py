import pygame
from sys import exit

from pygame.sprite import Group

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('img/testplayer.png').convert_alpha()
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
        self.question_checkpoint = QuestionCheckpoint(self)
        question_checkpoint_group.add(self.question_checkpoint)
        
    def update(self):
        self.rect.x -= 12
        if self.rect.right <= 0:
            self.question_checkpoint.kill()
            self.kill()
            obstacle_group.add(Obstacle("cone"))
            del self
        else:
            self.question_checkpoint.update()

class QuestionCheckpoint(pygame.sprite.Sprite):
    def __init__(self, Obstacle):
        super().__init__()
        self.obstacle = Obstacle
        self.image = pygame.Surface((4, 1000))
        self.rect = pygame.Rect(0, 0, 4, 1000)

    def update(self):
        self.rect.midbottom = self.obstacle.rect.midtop
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

def collision_obstacle():
    collided = pygame.sprite.spritecollide(player.sprite, obstacle_group, False)
    if collided:
        collided[0].question_checkpoint.kill()
        collided[0].kill()
        return False
    return True

def collision_question():
    if pygame.sprite.spritecollide(player.sprite, question_checkpoint_group, True ):
        return True
    return False


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

question_checkpoint_group = pygame.sprite.Group()

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
        screen.blit(start_text, start_text_rect)
        pygame.display.flip()
        for key in pygame.event.get():
            if key.type == pygame.QUIT:
                pygame.quit()
                exit()
            if key.type == pygame.KEYUP:
                question_active = False 

    if game_active:
        screen.blit(scene_surface, (0, -7))
        player.draw(screen)
        obstacle_group.draw(screen)
        question_checkpoint_group.draw(screen)

        player.sprite.update()
        obstacle_group.update()

        game_active = collision_obstacle()
        question_active = collision_question()

    else:
        screen.fill('black')
        screen.blit(game_over_text_surface, (400, 150))
        screen.blit(game_over_press_button_text_surface, (150, 400))
        for key in pygame.event.get():
            if key.type == pygame.KEYUP:
                game_active = True
                obstacle_group.add(Obstacle("cone"))
            if key.type == pygame.QUIT:
                pygame.quit()
                exit()

    for key in pygame.event.get():
        if key.type == pygame.QUIT:
            pygame.quit()
            exit()


    pygame.display.update()
    clock.tick(30)
    