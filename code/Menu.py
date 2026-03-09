import pygame
import sys
from code.ScoreManager import ScoreManager


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont("Arial", 60, bold=True)
        self.font_menu = pygame.font.SysFont("Arial", 36)
        self.font_small = pygame.font.SysFont("Arial", 24)

        self.score_manager = ScoreManager()
        self.options = ["Iniciar Novo Jogo", "Pontuação", "Sair"]
        self.index = 0  # Para controlar qual opção está selecionada

        # Cores
        self.color_white = (255, 255, 255)
        self.color_yellow = (255, 215, 0)  # Cor para destaque

    def draw_text(self, text, font, color, x, y):
        img = font.render(text, True, color)
        self.screen.blit(img, (x, y))

    def run(self):
        running_menu = True
        while running_menu:
            # Fundo escuro para o menu
            self.screen.fill((30, 30, 30))

            # Título do Jogo
            self.draw_text("MEDIEVAL STREET FIGHT", self.font_title, self.color_yellow, 300, 100)

            # Renderização das Opções (Req13)
            for i, option in enumerate(self.options):
                color = self.color_yellow if i == self.index else self.color_white
                self.draw_text(option, self.font_menu, color, 500, 250 + (i * 60))

            # Instruções de Controle (Req14)
            self.draw_text("CONTROLES:", self.font_small, self.color_yellow, 50, 500)
            self.draw_text("W/S/A/D - Movimentação", self.font_small, self.color_white, 50, 530)
            self.draw_text("Botão Esquerdo Mouse - Soco", self.font_small, self.color_white, 50, 560)
            self.draw_text("Botão Direito Mouse - Chute", self.font_small, self.color_white, 50, 590)

            # Eventos do Menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:  # Navegar para cima
                        self.index = (self.index - 1) % len(self.options)
                    elif event.key == pygame.K_s:  # Navegar para baixo
                        self.index = (self.index + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:  # Selecionar com ENTER
                        if self.index == 0:
                            return "PLAYING"
                        elif self.index == 1:
                            self.show_score_screen()
                        elif self.index == 2:
                            return "QUIT"

            pygame.display.flip()

    def show_score_screen(self):
        """Tela secundária para exibir o Ranking (Req13)"""
        viewing_scores = True
        while viewing_scores:
            self.screen.fill((20, 20, 20))
            self.draw_text("TOP 5 PONTUAÇÕES", self.font_menu, self.color_yellow, 450, 100)

            scores = self.score_manager.get_top_scores()
            for i, (name, val) in enumerate(scores):
                self.draw_text(f"{i + 1}. {name} - {val} pts", self.font_menu, self.color_white, 500, 200 + (i * 50))

            self.draw_text("Pressione ESC para voltar", self.font_small, self.color_yellow, 500, 550)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        viewing_scores = False

            pygame.display.flip()