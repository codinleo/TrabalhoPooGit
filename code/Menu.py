import pygame
import sys
from code.ScoreManager import ScoreManager


class Menu:
    """
    Classe responsável pela interface inicial do jogo, exibição de pontuações,
    instruções de comandos e identificação do autor.
    """

    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()

        # --- CARREGAMENTO VISUAL ---
        try:
            # Carrega e redimensiona a imagem de fundo para preencher a tela
            self.bg_image = pygame.image.load("asset/City2.png").convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))
        except Exception as e:
            print(f"Erro ao carregar City2.png: {e}")
            self.bg_image = pygame.Surface((self.width, self.height))
            self.bg_image.fill((30, 30, 30))

        # --- SISTEMA DE ÁUDIO ---
        try:
            # Inicia a trilha sonora caso ainda não esteja tocando
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load('asset/BackgroundMedievalSong.wav')
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.play(-1)
        except:
            print("Aviso: Música não encontrada.")

        # --- CONFIGURAÇÃO DE FONTES E CORES ---
        self.font_title = pygame.font.SysFont("Arial", 60, bold=True)
        self.font_menu = pygame.font.SysFont("Arial", 36)
        self.font_small = pygame.font.SysFont("Arial", 20)

        self.score_manager = ScoreManager()
        self.options = ["Iniciar Novo Jogo", "Pontuação", "Sair"]
        self.option_rects = []  # Armazena os retângulos das opções para detectar cliques
        self.index = 0  # Controla qual opção está selecionada no teclado

        self.color_white = (255, 255, 255)
        self.color_yellow = (255, 215, 0)

    def draw_text(self, text, font, color, x, y):
        """
        Método auxiliar para desenhar texto com efeito de sombra.
        Retorna o retângulo (rect) do texto para uso em colisões de mouse.
        """
        shadow = font.render(text, True, (0, 0, 0))  # Sombra preta
        img = font.render(text, True, color)  # Texto principal
        self.screen.blit(shadow, (x + 2, y + 2))  # Desenha sombra com leve deslocamento
        self.screen.blit(img, (x, y))
        return img.get_rect(topleft=(x, y))

    def run(self):
        """Loop principal do Menu."""
        clock = pygame.time.Clock()
        running_menu = True

        while running_menu:
            # Desenha o fundo estático
            self.screen.blit(self.bg_image, (0, 0))

            # --- TÍTULO ---
            self.draw_text("EVIL HUNT - DEMO", self.font_title, self.color_yellow, 300, 80)

            # --- OPÇÕES DO MENU ---
            self.option_rects = []
            for i, option in enumerate(self.options):
                # Destaca em amarelo a opção atualmente selecionada
                color = self.color_yellow if i == self.index else self.color_white
                rect = self.draw_text(option, self.font_menu, color, 500, 250 + (i * 60))
                self.option_rects.append(rect)

            # --- INSTRUÇÕES E COMANDOS ---
            self.draw_text("CONTROLES DO JOGO:", self.font_small, self.color_yellow, 50, 480)
            controles = [
                "W - Mover para Cima", "S - Mover para Baixo", "A - Mover para Trás",
                "D - Mover para Frente", "Mouse Esq. - Soco", "Mouse Dir. - Chute",
                "ENTER - Confirmar Seleção"
            ]
            for i, txt in enumerate(controles):
                self.draw_text(txt, self.font_small, self.color_white, 50, 510 + (i * 25))

            # --- IDENTIFICAÇÃO DO AUTOR ---
            id_text = "Leonardo Cesar Dias - RU: 1316847"
            id_surf = self.font_small.render(id_text, True, self.color_white)
            self.screen.blit(id_surf, (self.width - id_surf.get_width() - 20, self.height - 40))

            # Captura a posição atual do mouse
            mouse_pos = pygame.mouse.get_pos()

            # --- PROCESSAMENTO DE EVENTOS ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                # Interação com Mouse: Hover (passar por cima)
                if event.type == pygame.MOUSEMOTION:
                    for i, rect in enumerate(self.option_rects):
                        if rect.collidepoint(mouse_pos):
                            self.index = i

                # Interação com Mouse: Clique
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Botão esquerdo do mouse
                        for i, rect in enumerate(self.option_rects):
                            if rect.collidepoint(mouse_pos):
                                if i == 0:
                                    return "PLAYING"
                                elif i == 1:
                                    self.show_score_screen()
                                elif i == 2:
                                    return "QUIT"

                # Interação com Teclado
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_w, pygame.K_UP]:
                        self.index = (self.index - 1) % len(self.options)
                    elif event.key in [pygame.K_s, pygame.K_DOWN]:
                        self.index = (self.index + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:  # Selecionar com ENTER
                        if self.index == 0:
                            return "PLAYING"
                        elif self.index == 1:
                            self.show_score_screen()
                        elif self.index == 2:
                            return "QUIT"

            pygame.display.flip()
            clock.tick(60)

    def show_score_screen(self):
        """Sub-loop para exibir as pontuações gravadas."""
        viewing_scores = True
        while viewing_scores:
            self.screen.blit(self.bg_image, (0, 0))

            # Cria um efeito de 'overlay' escurecido para facilitar a leitura
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # Preto com transparência
            self.screen.blit(overlay, (0, 0))

            self.draw_text("TOP 5 PONTUAÇÕES", self.font_menu, self.color_yellow, 450, 100)

            # Busca os dados no ScoreManager
            scores = self.score_manager.get_top_scores()
            for i, (name, val) in enumerate(scores):
                self.draw_text(f"{i + 1}. {name} - {val} pts", self.font_menu, self.color_white, 500, 200 + (i * 50))

            self.draw_text("Pressione ESC para voltar", self.font_small, self.color_yellow, 500, 550)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Retorna ao menu principal
                        viewing_scores = False

            pygame.display.flip()