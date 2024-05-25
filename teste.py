import pygame

pygame.init()

# Configurações da tela
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Exemplo de get_rect')

# Carregar a imagem da seta
arrow_img = pygame.image.load('img/seta.png').convert_alpha()
arrow_rect = arrow_img.get_rect()  # Obter o Rect da imagem da seta

# Definir a posição inicial da seta (por exemplo, no centro da tela)
arrow_rect.center = (400, 300)

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limpar a tela
    screen.fill((0, 0, 0))

    # Desenhar a seta na posição do rect
    screen.blit(arrow_img, arrow_rect)

    # Atualizar a tela
    pygame.display.flip()

pygame.quit()
