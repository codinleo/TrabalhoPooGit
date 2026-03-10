import sys
import os
import pygame


def resource_path(relative_path):
    """
    Ajusta o caminho do arquivo para que funcione tanto em modo de
    desenvolvimento quanto após ser compilado pelo PyInstaller.
    """
    try:
        # O PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Se não estiver rodando como executável, usa o caminho normal da pasta
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# função no módulo 'sys' para que ela fique disponível
# globalmente em todos os outros scripts do projeto.
sys.resource_path = resource_path

# importar o Game
from code.Game import Game

if __name__ == "__main__":
    # Inicialização padrão do Pygame
    pygame.init()

    game = Game()

    try:
        # Inicia o loop principal do jogo
        game.run()
    except Exception as e:
        # Se o jogo fechar por erro de arquivo, ele criará este log para você ler
        with open("error_log.txt", "w") as f:
            f.write(f"Erro detectado: {str(e)}")
        pygame.quit()
        sys.exit()