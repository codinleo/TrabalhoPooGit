# code/ScoreManager.py
import os

class ScoreManager:
    def __init__(self):
        self.file_path = "DBScore/highscores.txt"
        if not os.path.exists("DBScore"):
            os.makedirs("DBScore")

    def save_score(self, name, score):
        with open(self.file_path, "a") as file:
            file.write(f"{name}:{score}\n")

    def get_top_scores(self):
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, "r") as file:
            lines = file.readlines()
            # Ordena por pontuação (maior primeiro)
            scores = [line.strip().split(":") for line in lines]
            return sorted(scores, key=lambda x: int(x[1]), reverse=True)[:5]