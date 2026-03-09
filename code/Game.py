import pygame
from code.Menu import Menu
from code.Level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Medieval Street Fight - Trabalho POO")
        self.clock = pygame.time.Clock()
        self.state = "MENU" # Estado inicial do jogo
        self.menu = Menu(self.screen)
        self.level = None

    def run(self):
        running = True
        while running:
            if self.state == "MENU":
                self.state = self.menu.run()
            elif self.state == "PLAYING":
                if self.level is None:
                    self.level = Level(self.screen)
                self.state = self.level.run()
                if self.state == "MENU": # Reseta o nível ao voltar ao menu
                    self.level = None
            elif self.state == "QUIT":
                running = False

            pygame.display.flip()
            self.clock.tick(60) # Mantém 60 FPS
        pygame.quit()