import pygame
from sys import exit
from random import randint
from pygame.sprite import Group

#Classes

class Game():
    def __init__(self) -> None:
        self.state = 'start'
        self.level = Level(self)

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
            game.state = game.level.next_level()
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

class Operation():
    #Texto para pedir a operação
    def operation_text(self):
        operation_text = operation_screen_font.render(f"Selecione qual Operação você quer jogar!!", False, 'White')
        operation_text_rect = operation_text.get_rect()
        operation_text_rect.center = (SCREEN_WIDTH/2, 150)
        screen.blit(operation_text, operation_text_rect)

        operation_sum_text = operation_screen_font.render(f"Soma", False, 'White')
        operation_sum_text_rect = operation_sum_text.get_rect()
        operation_sum_text_rect.center = (350, 300)
        screen.blit(operation_sum_text, operation_sum_text_rect)

        operation_sub_text = operation_screen_font.render(f"Subtração", False, 'White')
        operation_sub_text_rect = operation_sub_text.get_rect()
        operation_sub_text_rect.center = (850, 300)
        screen.blit(operation_sub_text, operation_sub_text_rect)

        operation_mul_text = operation_screen_font.render(f"Multiplicação", False, 'White')
        operation_mul_text_rect = operation_mul_text.get_rect()
        operation_mul_text_rect.center = (350, 600)
        screen.blit(operation_mul_text, operation_mul_text_rect)

        operation_div_text = operation_screen_font.render(f"Divisão", False, 'White')
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

class Level():
    def __init__(self, game):
        self.current_level = 0
        self.obstacles_counter = 0
        self.all_obstacle_numbers = [1, 2, 3]
        self.obstacles_number = self.all_obstacle_numbers[self.current_level]
        self.game = game

    #Serve para mexer com o contador de obstáculos da fase e passar entre fases/bosses em caso de acerto de pergunta. Retorna o valor atualizado de game_state 
    def next_level(self):
        if self.game.state == 'boss':
            #Se chegar no final do jogo
            if self.current_level >= len(self.all_obstacle_numbers) - 1 :
                return 'game_over'
            #Caso seja em boss mas não no final do jogo
            else:
                self.current_level +=1
                self.obstacles_number = self.all_obstacle_numbers[self.current_level]
                self.obstacles_counter = 0
                return 'running'
            
        self.obstacles_counter += 1

        #Se for passar de fase
        if self.obstacles_counter >= self.obstacles_number: 
            return 'boss'
        
        self.obstacles_counter += 1
        print(self.obstacles_counter, self.obstacles_number)
        #Se fase estiver concluida
        if self.obstacles_counter >= self.obstacles_number:
            game.state = 'boss'
        return 'running'

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

pygame.init()

# Constantes
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GROUND_LEVEL = 555

#Variáveis do Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Mathematic Park')

#Jogo
game = Game()

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
scene_surface = pygame.image.load('img/scene.jpg').convert()

#Loop do jogo
while True:
    
    #Tela Inicial
    if game.state == 'start':
        screen.blit(start_text, start_text_rect)
        pygame.display.flip()
        for key in pygame.event.get():
            if key.type == pygame.QUIT:
                pygame.quit()
                exit()
            if key.type == pygame.KEYUP:
                game.state = 'operation'
                
    #Selecionar o Operador
    elif game.state == 'operation':
        screen.fill('black')
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
                    game.state = 'running'
                if event.key == pygame.K_2:
                    operator.operation_option = '-'
                    game.state = 'running'
                if event.key == pygame.K_3:
                    operator.operation_option = '*'
                    game.state = 'running'
                if event.key == pygame.K_4:
                    operator.operation_option = '/'
                    game.state = 'running'

    #Jogo
    elif game.state == 'running':
        screen.blit(scene_surface, (0, -7))
        player.draw(screen)
        obstacle_group.draw(screen)

        player.sprite.update()
        obstacle_group.update()

        if collision_obstacle():
            game.state = 'game_over'

        if collision_question():
            game.state = 'question'

    #Tela de GameOver
    elif game.state == 'game_over':
        screen.fill('black')
        screen.blit(game_over_text_surface, (400, 150))
        screen.blit(game_over_press_button_text_surface, (150, 400))
        for key in pygame.event.get():
            if key.type == pygame.KEYDOWN:
                game.state = 'running'  
                obstacle_group.add(Obstacle("cone"))
            if key.type == pygame.QUIT:
                pygame.quit()
                exit()        
    
    #Loop da Questão         
    elif game.state == 'question' :
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
                        game.state = 'running'

                        waiting_response = False

                    if event.key == pygame.K_SPACE:
                        for s in obstacle_group.sprites():
                            s.question_checkpoint.kill()
                            s.kill()
                        game.state = 'game_over'
                        waiting_response = False

    elif game.state == 'boss':
        waiting_response = True
        while waiting_response:
            print('BOSS')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.KEYDOWN = False
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_CAPSLOCK:
                        game.state = game.level.next_level()
                        waiting_response = False

                    if event.key == pygame.K_SPACE:
                        for s in obstacle_group.sprites():
                            s.question_checkpoint.kill()
                            s.kill()
                        game.state = 'game_over'
                        waiting_response = False
        
    for key in pygame.event.get():
        if key.type == pygame.QUIT:
            pygame.quit()
            exit()

    #Atualização do Display e FPS
    pygame.display.update()
    clock.tick(30)
    