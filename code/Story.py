import pygame
import sys # Importado para manter o padrão de compatibilidade.

class Story:
    """
    Classe responsável pela introdução narrativa do jogo.
    Implementa um efeito de "Scroll Vertical" inspirado na abertura de Star Wars,
    contando a história do herói Leo e seu objetivo.
    """

    def __init__(self, screen):
        self.screen = screen
        # Configuração da fonte: Amarela, em negrito e com tamanho legível
        self.font = pygame.font.SysFont("Arial", 35, bold=True)
        self.color = (255, 220, 0)  # Amarelo clássico "Star Wars"
        self.background = (0, 0, 0)  # Fundo preto para destaque total do texto

        # Lista de strings que compõem a narrativa do jogo
        self.text = [
            "EPISODIO 1",
            "ATRAVÉS DO TEMPO",
            "",
            "Guerra! Após a invasão do impiedoso Lorde Murgoth",
            "às terras intermédias, nosso herói o persegue no",
            "tempo em busca de justiça por aqueles que caíram",
            "em suas mãos. O mal está por toda a parte e há",
            "heróis em ambos os lados, porém através de uma",
            "manobra surpreendente, nosso herói consegue saltar",
            "no tempo usando magia, identificando um dos grandes",
            "generais das forças inimigas Luci, o devastador de",
            "mundos, que agora busca a destruição em um planeta",
            "distante, chamado Terra.",
            "",
            "Enquanto nossos companheiros tentam reconstruir o",
            "condado que um dia foi símbolo de paz e prosperidade",
            "nosso herói Leo, o RU:1316847 persegue um dos grandes",
            "generais inimigos em tempos distantes. Nosso cavaleiro",
            "nobre luta com toda sua força para libertar a todos",
            "das garras do mal!",
            "",
            "",
            "PRESSIONE QUALQUER TECLA PARA COMEÇAR"
        ]

        # LÓGICA DE POSICIONAMENTO:
        # Começa com o texto na parte de baixo da tela (fora da visão do jogador)
        self.y_pos = self.screen.get_height()
        # Define o quão rápido o texto sobe a cada frame
        self.scroll_speed = 0.8

    def run(self):
        """Loop da tela de história."""
        # Preenche o fundo com a cor preta a cada frame
        self.screen.fill(self.background)

        # Gerenciamento de Eventos (Permite pular a cena)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            # Se o jogador interagir com teclado ou mouse, pula para o jogo
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return "PLAYING"

        # --- RENDERIZAÇÃO DO TEXTO DINÂMICO ---
        for i, line in enumerate(self.text):
            # Renderiza a string atual da lista
            rendered_text = self.font.render(line, True, self.color)

            # Centralização Horizontal Dinâmica:
            # (Largura da Tela - Largura do Texto) / 2
            text_x = (self.screen.get_width() - rendered_text.get_width()) // 2

            # Posicionamento Vertical:
            # Posição base (y_pos) + (índice da linha * espaçamento de 50 pixels)
            text_y = self.y_pos + (i * 50)

            # Desenha o texto na superfície da tela
            self.screen.blit(rendered_text, (text_x, text_y))

        # MOVIMENTO: Diminui o valor de Y para que o texto suba no eixo vertical
        self.y_pos -= self.scroll_speed

        # CONDIÇÃO DE TÉRMINO AUTOMÁTICO:
        # Se a posição do final do texto for menor que zero (sumiu da tela), inicia o jogo
        if self.y_pos < -(len(self.text) * 55):
            return "PLAYING"

        # Mantém o estado atual como STORY enquanto o texto estiver subindo
        return "STORY"