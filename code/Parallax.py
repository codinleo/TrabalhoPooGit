import pygame


class Parallax:
    """
    Classe responsável pelo efeito de Parallax (fundo infinito).
    """

    def __init__(self, screen):
        self.screen = screen

        # --- CONFIGURAÇÃO DAS CAMADAS ---
        # Cada tupla contém: (Imagem, Velocidade de Deslocamento)
        # Velocidade 0: Fica estático (Céu)
        # Velocidade próxima a 1: Move-se quase na mesma velocidade que o herói (Perto da câmera)
        self.layers = [
            (pygame.image.load('asset/Sky.png').convert(), 0),  # Céu (Fundo infinito estático)
            (pygame.image.load('asset/buildings.png').convert_alpha(), 0.2),  # Prédios distantes (Movem devagar)
            (pygame.image.load('asset/wall2.png').convert_alpha(), 0.5),  # Muro de trás
            (pygame.image.load('asset/wall1.png').convert_alpha(), 0.8),  # Muro da frente
            (pygame.image.load('asset/road&border.png').convert_alpha(), 1.0)  # Estrada e Chão (Velocidade total)
        ]
        self.width = screen.get_width()  # Largura da tela para calcular a repetição da imagem

    def draw(self, scroll):
        """
        Desenha as camadas na tela aplicando o deslocamento infinito.
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