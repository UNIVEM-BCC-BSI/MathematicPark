import pygame
import sys
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

class Operation(pygame.sprite.Sprite):
    #Texto para pedir a operação
    def operation_text(self):
        operation_text = operation_screen_font.render(f"Selecione a operação", False, 'black')
        operation_text_rect = operation_text.get_rect()
        operation_text_rect.center = (SCREEN_WIDTH/2, 150)
        screen.blit(operation_text, operation_text_rect)

        operation_sum_text = operation_screen_font.render(f"Soma", False, 'black')
        operation_sum_text_rect = operation_sum_text.get_rect()
        operation_sum_text_rect.center = (350, 300)
        screen.blit(operation_sum_text, operation_sum_text_rect)

        operation_sub_text = operation_screen_font.render(f"Subtração", False, 'black')
        operation_sub_text_rect = operation_sub_text.get_rect()
        operation_sub_text_rect.center = (850, 300)
        screen.blit(operation_sub_text, operation_sub_text_rect)

        operation_mul_text = operation_screen_font.render(f"Multiplicação", False, 'black')
        operation_mul_text_rect = operation_mul_text.get_rect()
        operation_mul_text_rect.center = (350, 600)
        screen.blit(operation_mul_text, operation_mul_text_rect)

        operation_div_text = operation_screen_font.render(f"Divisão", False, 'black')
        operation_div_text_rect = operation_div_text.get_rect()
        operation_div_text_rect.center = (850, 600)
        screen.blit(operation_div_text, operation_div_text_rect)
    
    #puxa o operador em string para ser utilizado pela questão
    def option(self, operator):
        self.operation_option = operator

class Question(pygame.sprite.Sprite):

    #Pede a variavel para usar na função calculate
    def __init__(self, operation):
        self.operation = operation
        self.calculate()
        self.show_question()
        self.show_answer()
    
    #Gera números com o randint para fazer a conta e retorna o resultado
    def calculate(self):
        if self.operation == '*':
            self.num1 = randint(1, 10)
            self.num2 = randint(1, 10)
        
        elif self.operation == '/':
            self.num1 = randint(1, 20)
            self.num2 = randint(1, 10)
            while self.num1 % self.num2 != 0:
                self.num1 = randint(1, 20)
                self.num2 = randint(1, 10)
        else:
            self.num1 = randint(1, 100)
            self.num2 = randint(1, 80)

        while self.num2 > self.num1:
            self.num2 = randint(1, 80)

        self.result = int(eval(str(self.num1) + self.operation + str(self.num2)))
        return self.result
   
    #Mostra a pergunta na tela
    def show_question(self):
        question_text = question_font.render(f"{self.num1} {self.operation} {self.num2}", False, 'White')
        question_text_rect = question_text.get_rect()
        question_text_rect.center = (SCREEN_WIDTH/2, 150)
        screen.blit(question_text, question_text_rect)
    
    #Mostra as opções de respostas na tela
    def show_answer(self):
        
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

#Checa a colisão com o obstaculo, se colidir retorna True e deleta o obstaculo e a linha e se não colidir retorna False
def collision_obstacle():
    collided = pygame.sprite.spritecollide(player.sprite, obstacle_group, False)
    if collided:
        collided[0].question_checkpoint.kill()
        collided[0].kill()
        return True
    return False

#Checa a colisão com a linha da pergunta, se colidir retorna True e deleta a linha e se não colidir retorna False
def collision_question():
    collided = pygame.sprite.spritecollide(player.sprite, question_checkpoint_group, False )
    if collided:
        collided[0].kill()
        return True
    return False
        
class Button:
    
    def __init__(self, x, y, image,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width * scale), int(height *scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False 

    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        #check mouseover and clicked condition 
        if  self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True 
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        #draw button on the screen 
        screen.blit(self.image,(self.rect.x, self.rect.y))
        return action
pygame.init()

# Constantes
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GROUND_LEVEL = 555

#Variáveis do Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Mathematic Park')

#Variáveis do jogo
game_state = 'start'

#Variáveis de texto
title_font = pygame.font.Font('ARCADECLASSIC.TTF', 100)
subtitle_font = pygame.font.Font('ARCADECLASSIC.TTF', 50)
start_font = pygame.font.Font('ARCADECLASSIC.TTF', 32)
operation_screen_font = pygame.font.Font('arial.TTF', 32)
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
inicial_surface = pygame.image.load('img/telalogo1.png').convert()
inicial_surface =pygame.transform.scale(inicial_surface, (1280, 720))
operacao_surface = pygame.image.load('img/telalogo1.png')
scene_surface = pygame.image.load('img/scene.jpg').convert()

#variáveis dos botões
start_img = pygame.image.load('img/botaonv.png').convert_alpha()
exit_img = pygame.image.load('img/botaonv.png').convert_alpha()
credits_img = pygame.image.load('img/botaonv.png').convert_alpha()
#button_img = pygame.image.load('img/butao.png').convert_alpha()


# Calcular posições dos botões para centralizá-los na tela
x_centro = SCREEN_WIDTH // 2
y_iniciar = SCREEN_HEIGHT // 2 - 100
y_creditos = SCREEN_HEIGHT // 1.85
y_sair = SCREEN_HEIGHT // 2 + 130
escala_start = 1
escala_cred = 0.75
escala_sair = 0.60

# Instâncias dos botões
button_start = Button(x_centro - int(start_img.get_width()* escala_start)// 2, y_iniciar, start_img,escala_start)
button_credits = Button(x_centro - int(credits_img.get_width()*escala_cred)// 2, y_creditos, credits_img,escala_cred)
button_exit = Button(x_centro - int(exit_img.get_width()*escala_sair)// 2, y_sair, exit_img, escala_sair)
#button_general = Button(-330,-75,button_img,1)

#Loop do jogo
while True: 
    for key in pygame.event.get():
            if key.type == pygame.QUIT:
                pygame.quit()
                exit()
    #Tela Inicial
    if game_state == 'start':
        screen.blit(inicial_surface, (0,0))
        if button_start.draw():
            game_state = 'operation'
        elif button_credits.draw():
            game_state = 'credits'
        elif button_exit.draw():
            pygame.quit()
            sys.exit()
            
            
    
                
    #Selecionar o Operador
    elif game_state == 'operation':
        screen.blit(operacao_surface, (0,0))
        operation_screen_text = Operation()
        operation_screen_text.operation_text()
        operator = Operation()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    operator.operation_option = '+'
                    game_state = 'running'
                elif event.key == pygame.K_2:
                    operator.operation_option = '-'
                    game_state = 'running'
                elif event.key == pygame.K_3:
                    operator.operation_option = '*'
                    game_state = 'running'
                elif event.key == pygame.K_4:
                    operator.operation_option = '/'
                    game_state = 'running'

    #Jogo
    elif game_state == 'running':
        screen.blit(scene_surface, (0, -7))
        player.draw(screen)
        obstacle_group.draw(screen)

        player.sprite.update()
        obstacle_group.update()

        if collision_obstacle():
            game_state = 'game_over'

        if collision_question():
            game_state = 'question'

    #Tela de GameOver
    elif game_state == 'game_over':
        screen.fill('black')
        screen.blit(game_over_text_surface, (400, 150))
        screen.blit(game_over_press_button_text_surface, (150, 400))
        for key in pygame.event.get():
            if key.type == pygame.KEYDOWN:
                game_state = 'running'  
                obstacle_group.add(Obstacle("cone"))
            if key.type == pygame.QUIT:
                pygame.quit()
                exit()        
    
    #Loop da Questão         
    elif game_state == 'question':
        question = Question(operator.operation_option)
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
                        game_state = 'running'
                        waiting_response = False

                    if event.key == pygame.K_SPACE:
                        for s in obstacle_group.sprites():
                            s.question_checkpoint.kill()
                            s.kill()
                        game_state = 'game_over'
                        waiting_response = False

    for key in pygame.event.get():
        if key.type == pygame.QUIT:
            pygame.quit()
            exit()

    #Atualização do Display e FPS
    pygame.display.update()
    clock.tick(30)
    