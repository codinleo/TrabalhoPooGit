import pygame

class Parallax:
    def __init__(self, screen):
        self.screen = screen
        # Carregamento das camadas conforme Req15
        self.layers = [
            (pygame.image.load('asset/Sky.png').convert(), 0),
            (pygame.image.load('asset/buildings.png').convert_alpha(), 0.2),
            (pygame.image.load('asset/wall2.png').convert_alpha(), 0.5),
            (pygame.image.load('asset/wall1.png').convert_alpha(), 0.8),
            (pygame.image.load('asset/road&border.png').convert_alpha(), 1.0)
        ]
        self.width = screen.get_width()

    def draw(self, scroll):
        for img, speed in self.layers:
            # Calcula o deslocamento baseado no scroll global e velocidade da camada
            offset = (scroll * speed) % self.width
            self.screen.blit(img, (-offset, 0))
            self.screen.blit(img, (self.width - offset, 0))