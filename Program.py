import pygame
from sys import exit
from random import randint
from pygame.sprite import Group

#Classes

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('img/testplayer.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (160, GROUND_LEVEL))
        self.gravity = 0
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_PAGEUP]) and self.rect.bottom >= GROUND_LEVEL:
            self.gravity = -23

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= GROUND_LEVEL:
            self.rect.bottom = GROUND_LEVEL

    #Verifica os movimentos do player e aplica a gravidade
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

    #Faz o movimento do obstaculo e atualiza a linha, se o obstaculo sair da tela ele é deletado e é adicionado outro 
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

    #Faz o movimento da linha acompanhar o obstaculo e desenha a linha
    def update(self):
        self.rect.midbottom = self.obstacle.rect.midtop
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

#Checa a colisão com o obstaculo, se colidir retorna True e deleta o obstaculo e a linha e se não colidir retorna False
def collision_obstacle():
    collided = pygame.sprite.spritecollide(player.sprite, obstacle_group, False)
    if collided:
        collided[0].question_checkpoint.kill()
        collided[0].kill()
        return False
    return True

#Checa a colisão com a linha da pergunta, se colidir retorna True e deleta a linha e se não colidir retorna False
def collision_question():
    collided = pygame.sprite.spritecollide(player.sprite, question_checkpoint_group, False )
    if collided:
        collided[0].kill()
        return True
    return False

class question(pygame.sprite.Sprite):
    #Pede a variavel para usar na função calculate
    def __init__(self, operation):
        self.operation = operation 
    
    #Gera números com o randint para fazer a conta e retorna o resultado
    def calculate(self):
        self.num1 = randint(1, 50)
        self.num2 = randint(1, 50)
        while self.num2 > self.num1:
            self.num2 = randint(1, 50)
        if self.operation == '+':
            print(self.num1)
            print(self.num2)
            self.result = self.num1 + self.num2
            return self.result
    
    #Mostra a pergunta na tela
    def question(self):
        if self.operation == '+':
            question_text = question_font.render(f"{self.num1}  +  {self.num2}", False, 'White')
            question_text_rect = question_text.get_rect()
            question_text_rect.center = (SCREEN_WIDTH/2, 150)
            screen.blit(question_text, question_text_rect)
    
    #Mostra as opções de respostas na tela
    def answer(self):
        if self.operation == '+':
            resp1_text = question_font.render(f"{self.result}", False, 'White')
            resp1_text_rect = question_text.get_rect()
            resp1_text_rect.midtop = (450, 350)
            screen.blit(resp1_text, resp1_text_rect)

            resp2_text = question_font.render(f"{self.result + 5}", False, 'White')
            resp2_text_rect = question_text.get_rect()
            resp2_text_rect.midtop = (650, 350)
            screen.blit(resp2_text, resp2_text_rect)

            resp3_text = question_font.render(f"{self.result + 2}", False, 'White')
            resp3_text_rect = question_text.get_rect()
            resp3_text_rect.midtop = (850, 350)
            screen.blit(resp3_text, resp3_text_rect)

            resp4_text = question_font.render(f"{self.result - 3}", False, 'White')
            resp4_text_rect = question_text.get_rect()
            resp4_text_rect.midtop = (1050, 350)
            screen.blit(resp4_text, resp4_text_rect)     

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
operation_screen = True
question_active = False

#Variáveis de texto
title_font = pygame.font.Font('ARCADECLASSIC.TTF', 100)
subtitle_font = pygame.font.Font('ARCADECLASSIC.TTF', 50)
start_font = pygame.font.Font('ARCADECLASSIC.TTF', 32)
question_font = pygame.font.Font('arial.TTF', 32)

game_over_text_surface = title_font.render('Voce  perdeu', False, 'yellow')
game_over_press_button_text_surface = subtitle_font.render('Pressione  espaco  para  tentar  novamente', False, 'White')
start_text = start_font.render('Pressione  qualquer  tecla  para  jogar', False, 'White')
question_text_surface = subtitle_font.render("Pergunta", False, 'Black')
question_text = question_font.render('Digite um Número', False, 'White')

start_text_rect = start_text.get_rect()
start_text_rect.midtop = (SCREEN_WIDTH/2, 500)
question_text_rect = question_text.get_rect()
question_text_rect.center = (SCREEN_WIDTH/2, 400)

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

    #Loop da Questão         
    while question_active:
        questão = question("+")
        questão.calculate()
        questão.question()
        questão.answer()
        pygame.display.flip()
        waiting_response = True
        while waiting_response:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.KEYDOWN = False
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_CAPSLOCK:
                        question_active = False
                        waiting_response = False
                    if event.key == pygame.K_SPACE:
                        for s in obstacle_group.sprites():
                            s.question_checkpoint.kill()
                            s.kill()
                        question_active = False
                        game_active = False
                        waiting_response = False
       
    #Jogo
    if game_active:
        screen.blit(scene_surface, (0, -7))
        player.draw(screen)
        obstacle_group.draw(screen)

        player.sprite.update()
        obstacle_group.update()

        game_active = collision_obstacle()
        question_active = collision_question()

    #Tela de GameOver
    else:
        screen.fill('black')
        screen.blit(game_over_text_surface, (400, 150))
        screen.blit(game_over_press_button_text_surface, (150, 400))
        for key in pygame.event.get():
            if key.type == pygame.KEYDOWN:
                game_active = True     
                obstacle_group.add(Obstacle("cone"))
            if key.type == pygame.QUIT:
                pygame.quit()
                exit()        

    for key in pygame.event.get():
        if key.type == pygame.QUIT:
            pygame.quit()
            exit()

    #Atualização do Display e FPS
    pygame.display.update()
    clock.tick(30)
    