import pygame
from code.Menu import Menu
from code.Level import Level
from code.Story import Story  # Importação da classe que gerencia a introdução narrativa


class Game:
    """
    Classe principal que gerencia o loop do jogo e a transição entre telas (Estados).
    Esta classe aplica o conceito de Orquestração, controlando o fluxo do programa.
    """

    def __init__(self):
        # Inicializa todos os módulos do Pygame
        pygame.init()

        # Configura a resolução da janela do jogo (HD)
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Evil Hunt - Demo - Trabalho POO")

        # Objeto para controlar o tempo e taxa de quadros (FPS)
        self.clock = pygame.time.Clock()

        # Variável de Estado: Define qual tela está ativa (MENU, STORY, PLAYING, etc.)
        self.state = "MENU"

        # Inicialização dos objetos das telas
        self.menu = Menu(self.screen)
        self.story = Story(self.screen)  # Cria o objeto da história estilo Star Wars
        self.level = None  # O nível começa como nulo e é criado apenas quando o jogo inicia

    def run(self):
        """Loop principal do jogo (Main Loop)."""
        running = True
        while running:
            # --- GERENCIAMENTO DE ESTADOS ---

            # ESTADO: MENU PRINCIPAL
            if self.state == "MENU":
                # O método run do menu retorna a próxima string de estado
                self.state = self.menu.run()

                # Transição: Se o jogador clicou em iniciar, envia para a História antes do gameplay
                if self.state == "PLAYING":
                    self.state = "STORY"

            # ESTADO: INTRODUÇÃO NARRATIVA
            elif self.state == "STORY":
                # Executa a tela de história e captura o retorno (pode ser STORY ou PLAYING)
                self.state = self.story.run()

            # ESTADO: JOGABILIDADE (O Jogo propriamente dito)
            elif self.state == "PLAYING":
                # Instancia o nível apenas se ele ainda não existir (Lazy Initialization)
                if self.level is None:
                    self.level = Level(self.screen)

                # Executa a lógica do nível (movimentação, combate, HUD)
                self.state = self.level.run()

                # Transição: Se o jogador morrer ou vencer e voltar ao Menu.
                if self.state == "MENU":
                    self.level = None  # Destrói o nível atual para liberar memória e resetar o progresso
                    self.story = Story(self.screen)  # Reinicia o objeto da história para uma nova partida

            # ESTADO: SAIR DO SISTEMA
            elif self.state == "QUIT":
                running = False

            # --- ATUALIZAÇÃO DA TELA ---
            # Atualiza o buffer de vídeo para mostrar as imagens na janela
            pygame.display.flip()

            # Trava a taxa de quadros em 60 por segundo (estabilidade)
            self.clock.tick(60)

        # Finaliza o Pygame ao fechar o loop
        pygame.quit()