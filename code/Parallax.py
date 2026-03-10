import pygame
import sys # Necessário para acessar sys.resource_path

class Parallax:
    """
    Classe responsável pelo efeito de Parallax (fundo infinito).
    A técnica consiste em mover camadas de imagens em velocidades diferentes
    para criar uma ilusão de profundidade.
    """

    def __init__(self, screen):
        self.screen = screen

        # --- CONFIGURAÇÃO DAS CAMADAS COM RESOURCE_PATH ---
        # Ajustado para que o PyInstaller encontre as imagens no executável compactado
        self.layers = [
            (pygame.image.load(sys.resource_path('asset/Sky.png')).convert(), 0),
            (pygame.image.load(sys.resource_path('asset/buildings.png')).convert_alpha(), 0.2),
            (pygame.image.load(sys.resource_path('asset/wall2.png')).convert_alpha(), 0.5),
            (pygame.image.load(sys.resource_path('asset/wall1.png')).convert_alpha(), 0.8),
            (pygame.image.load(sys.resource_path('asset/road&border.png')).convert_alpha(), 1.0)
        ]
        self.width = screen.get_width()  # Largura da tela para calcular a repetição da imagem

    def draw(self, scroll):
        """
        Desenha as camadas na tela aplicando o deslocamento infinito.
        O parâmetro 'scroll' vem da movimentação do jogador no Level.
        """
        for img, speed in self.layers:
            # Calcula o deslocamento da camada atual
            # O operador '%' (módulo) garante que o valor do offset nunca ultrapasse a largura da imagem
            offset = (scroll * speed) % self.width

            # Desenha a primeira cópia da imagem deslocada para a esquerda
            self.screen.blit(img, (-offset, 0))

            # Desenha a segunda cópia da imagem logo após a primeira para preencher o vazio
            # Isso cria o efeito de fundo infinito (looping contínuo)
            self.screen.blit(img, (self.width - offset, 0))