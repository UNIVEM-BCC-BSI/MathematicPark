#Variáveis do cenário
inicial_surface = pygame.image.load('img/telalogo1.png').convert()
inicial_surface =pygame.transform.scale(inicial_surface, (1280, 720))
operacao_surface = pygame.image.load('img/telalogo1.png')
scene_surface = pygame.image.load('img/scene.jpg').convert()
#variáveis dos botões
start_img = pygame.image.load('img/começarbotao.png').convert_alpha()
exit_img = pygame.image.load('img/sairbotao.png').convert_alpha()
credits_img = pygame.image.load('img/créditosbotao.png').convert_alpha()
#button_img = pygame.image.load('img/butao.png').convert_alpha()

class Button:
    def __init__(self, x, y, image,scale):
        width = image.get_width()
        height = image.get_height()
        image = pygame.transform.scale(image,(int(width * scale), int(height *scale)))
        self.image = image 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False 

    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        #check mouseover and clicked condition 
        if  self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True 
        if pygame.mouse.get_pressed()[0] ==0:
            self.clicked = False
        #draw button on the screen 
        screen.blit(self.image,(self.rect.x, self.rect.y))
        return action
# button instances
button_start = Button(-330,-200, start_img,1)
button_exit = Button(-330,-75, exit_img,1)
button_credits = Button(-330,30,credits_img,1)
#button_general = Button(-330,-75,button_img,1)
#Loop do jogo
while True: 
    
    #Tela Inicial
    if game_state == 'start':
        screen.blit(inicial_surface, (0,0))
        screen.blit(start_text, start_text_rect)
        if button_start.draw() == True :
            print('clicked')
        for key in pygame.event.get():
            if key.type == pygame.QUIT:
                pygame.quit()
                exit()
        if button_credits.draw()== True:
            print('clicked')