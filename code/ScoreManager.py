# code/ScoreManager.py
import os


class ScoreManager:
    """
    Classe responsável pela Persistência de Dados do jogo.
    Salva e recupera as pontuações dos jogadores em um arquivo de texto local.
    """

    def __init__(self):
        # Define o caminho do arquivo onde as pontuações serão armazenadas
        self.file_path = "DBScore/highscores.txt"

        # Verifica se a pasta DBScore existe; caso contrário, cria a pasta
        # Isso evita erros de 'File Not Found' ao tentar salvar pela primeira vez
        if not os.path.exists("DBScore"):
            os.makedirs("DBScore")

    def save_score(self, name, score):
        """
        Salva uma nova pontuação no arquivo.
        Usa o modo 'a' (append) para adicionar o novo score sem apagar os anteriores.
        """
        with open(self.file_path, "a") as file:
            # Escreve no formato "Nome:Pontuação" seguido de uma quebra de linha
            file.write(f"{name}:{score}\n")

    def get_top_scores(self):
        """
        Lê o arquivo de pontuações, ordena os dados e retorna os 5 melhores resultados.
        """
        # Se o arquivo ainda não existe (primeiro jogo), retorna uma lista vazia
        if not os.path.exists(self.file_path):
            return []

        with open(self.file_path, "r") as file:
            lines = file.readlines()

            # Processa cada linha: remove espaços/quebras e divide pelo caractere ":"
            # Resulta em uma lista de listas: [['Player', '100'], ['Leo', '200']]
            scores = [line.strip().split(":") for line in lines]

            # Lógica de Ordenação:
            # 1. key=lambda x: int(x[1]) -> Usa o segundo elemento (score) convertido para inteiro como chave.
            # 2. reverse=True -> Ordena do maior para o menor.
            # 3. [:5] -> Retorna apenas os 5 primeiros (Top 5).
            return sorted(scores, key=lambda x: int(x[1]), reverse=True)[:5]