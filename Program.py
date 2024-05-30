import pygame
import sys
from sys import exit
from random import randint
from time import sleep
from pygame.sprite import Group

#Classes

class Game():
    def __init__(self) -> None:
        self.state = 'start'
        self.level = Level(self)
        self.scene = Scene()

    def kill_all_obstacles(self):
        for s in obstacle_group.sprites():
            s.question_checkpoint.kill()
            s.kill()

    def reset(self):
        self.level.current_level = self.level.current_level
        self.level.obstacles_counter = 0


class Scene():
    def __init__(self):
        self.scene_pos = 0
        self.scene = pygame.image.load('img/scenes/scene.png').convert()
        self.HOUSES = [
            pygame.image.load('img/scenes/casas/casa_1.png'),
            pygame.image.load('img/scenes/casas/casa_2.png'),
            pygame.image.load('img/scenes/casas/casa_3.png'),
            pygame.image.load('img/scenes/casas/casa_4.png'),
            pygame.image.load('img/scenes/casas/casa_5.png'),
            pygame.image.load('img/scenes/casas/casa_6.png'),
            pygame.image.load('img/scenes/casas/casa_7.png')
        ]
        self.start_house_active = False
        self.end_house_active = False
        self.start_house = self.HOUSES[0]
        self.end_house = self.HOUSES[1]
        self.spawn_house(True)

    def update(self):
        self.scene_pos -= 12
        screen.blit(self.scene, (self.scene_pos, 0))
        screen.blit(self.scene, (self.scene_pos + self.scene.get_width(), 0))
        if self.scene_pos <= -self.scene.get_width():
            self.scene_pos = 0
        
        #houses
        if self.start_house_active:
            self.start_house_rect.centerx -= 12
            if self.start_house_rect.centerx < -100:
                self.start_house_active = False
            screen.blit(self.start_house, self.start_house_rect)
        if self.end_house_active:
            self.end_rect.centerx -= 12
            screen.blit(self.start_house, self.end_house_rect)

    def spawn_house(self, on_start: bool = False):
        if on_start:
            self.start_house_active = True
            self.start_house_rect = self.start_house.get_rect()
            self.start_house_rect.bottom = GROUND_LEVEL - 101
            self.start_house_rect.centerx = 160
        else:
            self.end_house_active = True
            self.end_house_rect = self.end_house.get_rect()
            self.end_house_rect.bottom = GROUND_LEVEL - 101
            self.end_house_rect.left = 1280
    
    def change_house(self, level : int):
        self.start_house = self.HOUSES[level]
        self.end_house = self.HOUSES[level + 1]
        self.end_house_active = False
        self.spawn_house(True)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.running_sprites = []
        self.running_sprites.append(pygame.image.load('img/characters/sheldon_correr1.png').convert_alpha())
        self.running_sprites.append(pygame.image.load('img/characters/sheldon_correr2.png').convert_alpha())
        self.running_sprites.append(pygame.image.load('img/characters/sheldon_correr3.png').convert_alpha())
        self.jumping_sprites = []
        self.jumping_sprites.append(pygame.image.load('img/characters/sheldon_pular1.png').convert_alpha())
        self.jumping_sprites.append(pygame.image.load('img/characters/sheldon_pular2.png').convert_alpha())
        self.jumping_sprites.append(pygame.image.load('img/characters/sheldon_correr3.png').convert_alpha())

        self.current_sprite = 0
        self.image = self.running_sprites[self.current_sprite]
        self.is_jumping = False

        self.rect = self.image.get_rect(midbottom = (160, GROUND_LEVEL))
        self.gravity = 0
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_PAGEUP]) and self.rect.bottom >= GROUND_LEVEL:
            self.gravity = -23
            self.is_jumping = True

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= GROUND_LEVEL:
            self.is_jumping = False
            self.rect.bottom = GROUND_LEVEL

    #Verifica os movimentos do player e aplica a gravidade
    def update(self):
        self.player_input()
        self.apply_gravity()

        if self.is_jumping:
            if self.gravity < -2:
                self.current_sprite = 0
            elif self.gravity > 2:
                self.current_sprite = 1
            else: self.current_sprite = 2
            self.image = self.jumping_sprites[self.current_sprite]
        else:
            self.current_sprite += 0.25
            if self.current_sprite >= 3.0:
                self.current_sprite = 0
            self.image = self.running_sprites[int(self.current_sprite)]

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "cone":
            self.image = pygame.transform.scale_by(pygame.image.load('img/obstacles/cone.png').convert_alpha(), 1.4)
        elif type == "boss":
            self.image = BOSSES[game.level.current_level]

        self.rect = self.image.get_rect(midbottom = (1330, GROUND_LEVEL))

        self.question_checkpoint = QuestionCheckpoint(self)
        question_checkpoint_group.add(self.question_checkpoint)

    #Faz o movimento do obstaculo e atualiza a linha, se o obstaculo sair da tela ele é deletado e é adicionado outro 
    def update(self):
        self.rect.x -= 12
        if self.rect.right <= 0:
            self.question_checkpoint.kill()
            game.level.next_level()
            self.kill()
            if game.state == 'running':
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
        # pygame.draw.rect(screen, (255, 0, 0), self.rect)

class Start():
    def start_text(self):
        start_text = start_font.render(f"Jogar", False, 'white')
        start_text_rect = start_text.get_rect()
        start_text_rect.midtop = (SCREEN_WIDTH/2, 325)
        screen.blit(start_text, start_text_rect)

        start_text = start_font.render(f"Creditos", False, 'white')
        start_text_rect = start_text.get_rect()
        start_text_rect.midtop = (SCREEN_WIDTH/2, 425)
        screen.blit(start_text, start_text_rect)

        start_text = start_font.render(f"Sair", False, 'white')
        start_text_rect = start_text.get_rect()
        start_text_rect.midtop = (SCREEN_WIDTH/2, 525)
        screen.blit(start_text, start_text_rect)

class Game_Over():
    def game_over_text(self):
        game_over_text_surface = title_font.render('VOCE PERDEU', False, 'yellow')
        screen.blit(game_over_text_surface, (440, 150))

        game_over_press_button_text_surface = game_over_font.render('Quer Jogar Novamente?', False, 'White')
        screen.blit(game_over_press_button_text_surface, (445, 350))

        button_game_over_text = game_over_font.render(f"Recomecar", False, 'white')
        button_game_over_text_rect = button_game_over_text.get_rect()
        button_game_over_text_rect.midtop = (350, 530)
        screen.blit(button_game_over_text, button_game_over_text_rect)

        button_game_over_text = game_over_font.render(f"Sair", False, 'white')
        button_game_over_text_rect = button_game_over_text.get_rect()
        button_game_over_text_rect.midtop = (650, 530)
        screen.blit(button_game_over_text, button_game_over_text_rect)

        button_game_over_text = game_over_font.render(f"Inicio", False, 'white')
        button_game_over_text_rect = button_game_over_text.get_rect()
        button_game_over_text_rect.midtop = (950, 530)
        screen.blit(button_game_over_text, button_game_over_text_rect)
        
class Operation():
    #Texto para pedir a operação
    def operation_text(self):
        operation_text = operation_screen_font.render(f"Selecione a operacao", False, 'white')
        operation_text_rect = operation_text.get_rect()
        operation_text_rect.center = (SCREEN_WIDTH/2, 300)
        screen.blit(operation_text, operation_text_rect)

        operation_sum_text = operation_screen_font.render(f"+", False, 'white')
        operation_sum_text_rect = operation_sum_text.get_rect()
        operation_sum_text_rect.center = (400, 440)
        screen.blit(operation_sum_text, operation_sum_text_rect)

        operation_sub_text = operation_screen_font.render(f"-", False, 'white')
        operation_sub_text_rect = operation_sub_text.get_rect()
        operation_sub_text_rect.center = (800, 440)
        screen.blit(operation_sub_text, operation_sub_text_rect)

        operation_mul_text = operation_screen_font.render(f"x", False, 'white')
        operation_mul_text_rect = operation_mul_text.get_rect()
        operation_mul_text_rect.center = (400, 540)
        screen.blit(operation_mul_text, operation_mul_text_rect)

        operation_div_text = operation_screen_font.render(f"/", False, 'white')
        operation_div_text_rect = operation_div_text.get_rect()
        operation_div_text_rect.center = (800, 540)
        screen.blit(operation_div_text, operation_div_text_rect)
    
    #puxa o operador em string para ser utilizado pela questão
    def option(self, operator):
        self.operation_option = operator

class Question(pygame.sprite.Sprite):

    #Pede a variavel para usar na função calculate
    def __init__(self, operation):
        self.operation = operation
        self.calculate()
        self.random_answer()
        self.show_question()
        self.show_answer()
    
    #Gera números com o randint para fazer a conta e retorna o resultado
    def calculate(self):
        if self.operation == '*' and not game.state == 'boss':
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
   
    #Faz a aleatoriedade das questões
    def random_answer(self):
        self.answer = randint(1, 4)
        print(self.answer)
        if self.answer == 1:
            self.response1 = self.result
            self.response2 = self.result + 5
            self.response3 = self.result - 3
            self.response4 = self.result - 1
        elif self.answer == 2:
            self.response2 = self.result
            self.response1 = self.result + 2
            self.response3 = self.result - 3
            self.response4 = self.result - 1
        elif self.answer == 3:
            self.response3 = self.result 
            self.response1 = self.result + 4
            self.response2 = self.result - 1
            self.response4 = self.result - 2
        else:
            self.response4 = self.result
            self.response1 = self.result + 1
            self.response2 = self.result + 2
            self.response3 = self.result - 1

    #Mostra a pergunta na tela
    def show_question(self):
        screen.blit(popup_question, popup_rect)
        question_text = question_font.render(f"Quanto é {self.num1} { 'x' if self.operation == '*' else self.operation } {self.num2}?", False, 'White')
        question_text_rect = question_text.get_rect()
        question_text_rect.center = (SCREEN_WIDTH/2, 150)
        screen.blit(question_text, question_text_rect)

        question_text = question_font.render(f"Pergunta {  f'do {BOSSES_NAMES[game.level.current_level]}' if game.state == 'boss' else game.level.obstacles_counter + 1 }", False, 'White')
        question_text_rect = question_text.get_rect()
        question_text_rect.center = (SCREEN_WIDTH/2, 80)
        screen.blit(question_text, question_text_rect)
    #Mostra as opções de respostas na tela
    def show_answer(self):
        
        resp1_text = question_font.render(f"{self.response1}", False, 'White')
        resp1_text_rect = question_text.get_rect()
        resp1_text_rect.midtop = (515, 358)
        screen.blit(resp1_text, resp1_text_rect)

        resp2_text = question_font.render(f"{self.response2}", False, 'White')
        resp2_text_rect = question_text.get_rect()
        resp2_text_rect.midtop = (715, 358)
        screen.blit(resp2_text, resp2_text_rect)

        resp3_text = question_font.render(f"{self.response3}", False, 'White')
        resp3_text_rect = question_text.get_rect()
        resp3_text_rect.midtop = (915, 358)
        screen.blit(resp3_text, resp3_text_rect)

        resp4_text = question_font.render(f"{self.response4}", False, 'White')
        resp4_text_rect = question_text.get_rect()
        resp4_text_rect.midtop = (1115, 358)
        screen.blit(resp4_text, resp4_text_rect)

    
    def resp_incorrect(self):
        for s in obstacle_group.sprites():
            s.question_checkpoint.kill()
            s.kill()
        game.state = 'game_over'
        print('incorrect')   

    def resp_correct(self):
            if game.state == 'question':
                game.state = 'running'
                print('correct')
            else:
                game.level.next_level()
                print('correct')
class Level():
    def __init__(self, game):
        self.current_level = 0
        self.obstacles_counter = 0
        self.all_obstacle_numbers = [1, 1, 1]
        self.obstacles_number = self.all_obstacle_numbers[self.current_level]
        self.game = game
        self.level_state = True
        self.count_level = 1

    def screen_level(self):
        if self.level_state:
            screen.fill('black')
            level_text = level_font.render(f"Fase {self.count_level}", False, 'White')
            level_text_rect = level_text.get_rect()
            level_text_rect.midtop = (620, SCREEN_HEIGHT/2)
            screen.blit(level_text, level_text_rect)
            pygame.display.flip()
            sleep(1.5)
            self.count_level += 1
            self.level_state = False

    #Serve para mexer com o contador de obstáculos da fase e passar entre fases/bosses em caso de acerto de pergunta. Retorna o valor atualizado de game_state 
    def next_level(self):
        print("Entrnado na funcao", self.obstacles_counter, self.obstacles_number)
        if self.game.state == 'boss':
            #Se chegar no final do jogo
            if self.current_level >= len(self.all_obstacle_numbers) - 1 :
                self.game.state = 'final'
            #Caso seja em boss mas não no final do jogo
            else:
                self.current_level +=1
                #TODO: Update house
                self.obstacles_number = self.all_obstacle_numbers[self.current_level]
                self.obstacles_counter = 0
                self.game.kill_all_obstacles()
                obstacle_group.add(Obstacle("cone"))
                self.level_state = True
                self.game.state = 'running'
        else:
            self.obstacles_counter += 1

            #Se for passar de fase
            if self.obstacles_counter >= self.obstacles_number: 
                
                self.game.state = 'boss'
                self.game.kill_all_obstacles()
                obstacle_group.add(Obstacle("boss"))
                
            else:
                #Se fase estiver concluida
                if self.obstacles_counter >= self.obstacles_number:
                    self.game.state = 'boss'
                else: self.game.state = 'running'
        print("saindo da funcao", self.obstacles_counter, self.obstacles_number)

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

#Jogo
game = Game()

#Variáveis de texto
title_font = pygame.font.Font('press-start.regular.ttf', 40)
subtitle_font = pygame.font.Font('press-start.regular.ttf', 30)
start_font = pygame.font.Font('press-start.regular.ttf', 24)
operation_screen_font = pygame.font.Font('press-start.regular.ttf', 24)
level_font = pygame.font.Font('press-start.regular.ttf', 100)
question_font = pygame.font.Font('press-start.regular.ttf', 24)
game_over_font = pygame.font.Font('press-start.regular.ttf', 20)
final_font = pygame.font.Font('press-start.regular.ttf',20)

game_over_text_surface = title_font.render('VOCE PERDEU', False, 'yellow')
game_over_press_button_text_surface = game_over_font.render('Pressione o botao Recomecar para iniciar o jogo', False, 'White')
game_over_press_button_text_surface = game_over_font.render('ou o botao Sair para sair do jogo', False, 'White')
start_text = start_font.render('Pressione  qualquer  tecla  para  jogar', False, 'White')
credits_text = start_font.render('Voltar', False, 'White')
level_text = level_font.render(f"Fase", False, 'White')
question_text_surface = subtitle_font.render("Pergunta", False, 'Black')
question_text = question_font.render('Digite um Número', False, 'White')
final_text = final_font.render("Parabéns você venceu todos os desafios !!", False, 'yellow')
final_start_text = final_font.render("Inicio", False, 'white')
final_exit_text = final_font.render("Sair", False, 'white')

start_text_rect = start_text.get_rect()
start_text_rect.midtop = (SCREEN_WIDTH/2, 500)
credits_text_rect = credits_text.get_rect()
credits_text_rect.center = (SCREEN_WIDTH/2, 640)
level_text_rect = level_text.get_rect()
level_text_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
question_text_rect = question_text.get_rect()
question_text_rect.center = (SCREEN_WIDTH/2, 400)
final_text_rect = final_text.get_rect()
final_text_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
final_start_text_rect = final_start_text.get_rect()
final_start_text_rect.center = (450, 540)
final_exit_text_rect = final_exit_text.get_rect()
final_exit_text_rect.center = (850, 540)

#Grupos
player = pygame.sprite.GroupSingle()
player.add(Player())

question_checkpoint_group = pygame.sprite.Group()

obstacle_group = pygame.sprite.Group()
obstacle_group.add(Obstacle("cone"))

scene = Scene()

BOSSES = [
    pygame.transform.scale_by(pygame.image.load('img/characters/billy.png').convert_alpha(), 1.1),
    pygame.transform.scale_by(pygame.image.load('img/characters/alberto.png').convert_alpha(), 1.4),
    pygame.transform.scale_by(pygame.image.load('img/characters/policialterry.png').convert_alpha(), 1.75),
]
BOSSES_NAMES = [
    'Billy',
    'Alberto',
    'Policial Terry'
]
#Variáveis do cenário
inicial_surface = pygame.image.load('img/telalogo1.png').convert()
inicial_surface =pygame.transform.scale(inicial_surface, (1280, 720))
operacao_surface = pygame.image.load('img/telalogo1.png')
popup_question = pygame.transform.scale(pygame.image.load('img/screen/quadrado_nv.png').convert_alpha(), (600, 200))
popup_rect = popup_question.get_rect()
popup_rect.centerx = SCREEN_WIDTH // 2
popup_rect.y = 50


#variáveis dos botões
start_img = pygame.image.load('img/botaonv.png').convert_alpha()
exit_img = pygame.image.load('img/botaonv.png').convert_alpha()
credits_img = pygame.image.load('img/botaonv.png').convert_alpha()
operation_img = pygame.image.load('img/botaonv.png').convert_alpha()
question_img = pygame.image.load('img/botaonv.png').convert_alpha()
seta_img = pygame.image.load('img/seta.png').convert_alpha()
seta_rect = seta_img.get_rect()


# Calcular posições dos botões para centralizá-los na tela
x_centro = SCREEN_WIDTH // 2
y_iniciar = 300
y_creditos = 400
y_sair = 500
x_soma = 400
x_sub = 800
y_soma_sub = 400
x_mul = 400
x_div = 800
y_mul_div = 500
x_q1 = 345
x_q2 = 545
x_q3 = 745
x_q4 = 945
y_q = 345
x_game_over1 = 350
x_game_over2 = 650
x_game_over3 = 950
y_credits = 600
x_final1 = 450
x_final2 = 850

#Escalas dos Botões
escala_start = 1
escala_cred = 0.75
escala_sair = 0.60
escala_operation = 0.80
escala_question = 0.45

# fonte do botoes e cor
font = pygame.font.Font('press-start.regular.ttf',40)
font_color = (255,255,255)

# Instâncias dos botões
button_start = Button(x_centro - int(start_img.get_width()* escala_cred)// 2, y_iniciar, start_img,escala_cred)
button_credits = Button(x_centro - int(credits_img.get_width()*escala_cred)// 2, y_creditos, credits_img,escala_cred)
button_exit = Button(x_centro - int(exit_img.get_width()*escala_cred)// 2, y_sair, exit_img, escala_cred)
button_soma = Button(x_soma - int(operation_img.get_width()*escala_operation)// 2, y_soma_sub, operation_img, escala_operation)
button_sub = Button(x_sub - int(operation_img.get_width()*escala_operation)// 2, y_soma_sub, operation_img, escala_operation)
button_mul = Button(x_mul - int(operation_img.get_width()*escala_operation)// 2, y_mul_div, operation_img, escala_operation)
button_div = Button(x_div - int(operation_img.get_width()*escala_operation)// 2, y_mul_div, operation_img, escala_operation)
button_question1 = Button(x_q1 - int(question_img.get_width()* escala_question)// 2, y_q, question_img,escala_question)
button_question2 = Button(x_q2 - int(question_img.get_width()* escala_question)// 2, y_q, question_img,escala_question)
button_question3 = Button(x_q3 - int(question_img.get_width()* escala_question)// 2, y_q, question_img,escala_question)
button_question4 = Button(x_q4 - int(question_img.get_width()* escala_question)// 2, y_q, question_img,escala_question)
button_gameover = Button(x_game_over1 - int(exit_img.get_width()* escala_cred)// 2, y_sair, exit_img,escala_cred)
button_inicio = Button(x_game_over3 - int(exit_img.get_width()*escala_cred)// 2, y_sair, exit_img, escala_cred)
button_exit_game_over = Button(x_game_over2 - int(exit_img.get_width()*escala_cred)// 2, y_sair, exit_img, escala_cred)
button_return = Button(x_centro - int(credits_img.get_width()*escala_cred)// 2, y_credits, credits_img,escala_cred)
button_final_start = Button(x_final1 - int(credits_img.get_width()*escala_cred)// 2, y_sair, exit_img,escala_cred)
button_final_exit = Button(x_final2 - int(credits_img.get_width()*escala_cred)// 2, y_sair, exit_img,escala_cred)
#button_general = Button(-330,-75,button_img,1)

#Loop do jogo
while True: 
    for key in pygame.event.get():
            if key.type == pygame.QUIT:
                pygame.quit()
                exit()
    mouse_pos = pygame.mouse.get_pos()            
    #Tela Inicial
    if game.state == 'start':
        screen.blit(inicial_surface, (0,0))
        screen.blit(seta_img, seta_rect)

        if button_start.draw():
            game.state = 'operation'
        elif button_credits.draw():
            game.state = 'credits'
        elif button_exit.draw():
            pygame.quit()
            sys.exit()
        start_screen_text = Start()
        start_screen_text.start_text()
        #seta dos botoes
        if button_start.rect.collidepoint(mouse_pos):
            seta_rect.midright = (button_start.rect.left - 10, button_start.rect.centery)
        elif button_credits.rect.collidepoint(mouse_pos):
            seta_rect.midright = (button_credits.rect.left - 10, button_credits.rect.centery)
        elif button_exit.rect.collidepoint(mouse_pos):
            seta_rect.midright = (button_exit.rect.left - 10, button_exit.rect.centery)
        else:
            seta_rect.midright = (-100, -100)
    
    #Tela de Creditos
    elif game.state == 'credits':
        screen.blit(operacao_surface, (0,0))
        screen.blit(seta_img, seta_rect)
        if button_return.draw():
            game.state = 'start'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit()
                 exit()
        screen.blit(credits_text, credits_text_rect)
        #seta dos botoes
        if button_return.rect.collidepoint(mouse_pos):
            seta_rect.midright = (button_return.rect.left - 10, button_return.rect.centery)
        
        else:
            seta_rect.midright = (-100, -100)

    #Selecionar o Operador
    elif game.state == 'operation':
        screen.blit(operacao_surface, (0,0))
        screen.blit(seta_img, seta_rect)
        operator = Operation()

        if button_soma.draw():
            operator.operation_option = '+'
            game.state = 'running'
        elif button_sub.draw():
            operator.operation_option = '-'
            game.state = 'running'
        elif button_mul.draw():
            operator.operation_option = '*'
            game.state = 'running'
        elif button_div.draw():
            operator.operation_option = '/'
            game.state = 'running'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit()
                 exit()
        operation_screen_text = Operation()
        operation_screen_text.operation_text()

        #Seta dos Botões
        if button_soma.rect.collidepoint(mouse_pos):
            seta_rect.midright = (button_soma.rect.left - 10, button_soma.rect.centery)
        elif button_sub.rect.collidepoint(mouse_pos):
            seta_rect.midright = (button_sub.rect.left - 10, button_sub.rect.centery)
        elif button_mul.rect.collidepoint(mouse_pos):
            seta_rect.midright = (button_mul.rect.left - 10, button_mul.rect.centery)
        elif button_div.rect.collidepoint(mouse_pos):
            seta_rect.midright = (button_div.rect.left - 10, button_div.rect.centery)
        else:
            seta_rect.midright = (-100, -100) 


    #Jogo
    elif game.state == 'running':
        game.level.screen_level()
        scene.update()
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
        game.kill_all_obstacles()
        screen.fill('black')
        #screen.blit(game_over_text_surface, (400, 150))
        #screen.blit(game_over_press_button_text_surface, (150, 400))
        if button_gameover.draw():
            game.state = 'running'
            obstacle_group.add(Obstacle("cone"))
            game.reset()
        elif button_exit_game_over.draw():
            pygame.quit()
            exit()
        elif button_inicio.draw():
            game.state = 'start'
            obstacle_group.add(Obstacle("cone"))
        game_over_text = Game_Over()
        game_over_text.game_over_text()
             
    #Tela Final
    elif game.state == 'final':
        screen.fill('black')
        screen.blit(final_text, final_text_rect)
        if button_final_start.draw():
            game.state = 'start'
            obstacle_group.add(Obstacle("cone"))
        elif button_final_exit.draw():
            pygame.quit()
            exit()
        screen.blit(final_start_text, final_start_text_rect)
        screen.blit(final_exit_text, final_exit_text_rect)

    #Loop da Questão         
    elif game.state == 'question' :
        button_question1.draw()
        button_question2.draw()
        button_question3.draw()
        button_question4.draw()
        question = Question(operator.operation_option)
        pygame.display.flip()
        waiting_response = True
        while waiting_response:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.KEYDOWN = False
                    pygame.quit()
                    exit()

                elif button_question1.draw():
                    if question.answer == 1:
                        print('botao 1')
                        question.resp_correct()
                        waiting_response = False
                    else:
                        question.resp_incorrect()
                        waiting_response = False

                elif button_question2.draw():
                    print('botao 2')
                    if question.answer == 2:
                        question.resp_correct()
                        waiting_response = False
                    else:
                        question.resp_incorrect()
                        waiting_response = False

                elif button_question3.draw():
                    print('botao 3')
                    if question.answer == 3:
                        question.resp_correct()
                        waiting_response = False
                    else:
                        question.resp_incorrect()
                        waiting_response = False
                elif button_question4.draw():
                    print('botao 4')
                    if question.answer == 4:
                        question.resp_correct()
                        waiting_response = False
                    else:
                        question.resp_incorrect()
                        waiting_response = False
        
    elif game.state == 'boss':
            scene.update()
            player.draw(screen)
            obstacle_group.draw(screen)

            player.sprite.update()
            obstacle_group.update()

            if collision_obstacle() or collision_question():
                button_question1.draw()
                button_question2.draw()
                button_question3.draw()
                button_question4.draw()
                question = Question(operator.operation_option)
                pygame.display.flip()
                waiting_response = True
                while waiting_response:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.KEYDOWN = False
                            pygame.quit()
                            exit()
                        elif button_question1.draw():
                            if question.answer == 1:
                                print('botao 1')
                                question.resp_correct()
                                waiting_response = False
                            else:
                                question.resp_incorrect()
                                waiting_response = False

                        elif button_question2.draw():
                            print('botao 2')
                            if question.answer == 2:
                                question.resp_correct()
                                waiting_response = False
                            else:
                                question.resp_incorrect()
                                waiting_response = False

                        elif button_question3.draw():
                            print('botao 3')
                            if question.answer == 3:
                                question.resp_correct()
                                waiting_response = False
                            else:
                                question.resp_incorrect()
                                waiting_response = False
                        elif button_question4.draw():
                            print('botao 4')
                            if question.answer == 4:
                                question.resp_correct()
                                waiting_response = False
                            else:
                                question.resp_incorrect()
                                waiting_response = False
        
    for key in pygame.event.get():
        if key.type == pygame.QUIT:
            pygame.quit()
            exit()
    #Atualização do Display e FPS
    pygame.display.update()
    clock.tick(30)
    