import pygame
import random
import sys  # Necessário para acessar sys.resource_path.


# --- CLASSE BASE (ABSTRATA) PARA TODAS AS ENTIDADES DO JOGO ---
class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frame_index = 0  # Índice atual da animação
        self.animation_speed = 0.15  # Velocidade de troca de frames
        self.direction = 1  # 1: Direita, -1: Esquerda
        self.status = 'idle'  # Estado atual (idle, walk, attack, etc)
        self.animations = {}  # Dicionário que armazenará as listas de imagens

    def load_animation(self, path, num_frames, scale=2):
        """
        Método para carregar uma Sprite Sheet (tira de imagens).
        Recorta a imagem em partes iguais e redimensiona.
        """
        try:
            # AJUSTE: sys.resource_path aplicado ao caminho da folha de sprites
            full_path = sys.resource_path(path)
            sprite_sheet = pygame.image.load(full_path).convert_alpha()

            frame_width = sprite_sheet.get_width() // num_frames  # Calcula largura de cada frame
            sheet_height = sprite_sheet.get_height()
            frames = []

            for i in range(num_frames):
                # Define a área de recorte para cada frame
                rect = pygame.Rect(i * frame_width, 0, frame_width, sheet_height)
                frame = sprite_sheet.subsurface(rect)  # Recorta
                # Aplica o escalonamento dinâmico (tamanho no jogo)
                frame = pygame.transform.smoothscale(frame, (int(frame_width * scale), int(sheet_height * scale)))
                frames.append(frame)
            return frames
        except Exception as e:
            print(f"Erro ao carregar {path}: {e}")
            # Caso a imagem falhe, retorna um quadrado rosa (placeholder de erro)
            surf = pygame.Surface((64, 64))
            surf.fill((255, 0, 255))
            return [surf]

    def animate(self):
        """Gerencia a troca de frames baseada no status e direção."""
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed  # Incrementa o progresso da animação

        # Reinicia a animação ou muda de status ao chegar no fim da lista
        if self.frame_index >= len(animation):
            # Se terminou um ataque ou dano, volta para o estado neutro (idle ou walk)
            if self.status in ['attack', 'hurt', 'attack1', 'run_attack']:
                self.status = 'idle' if 'idle' in self.animations else 'walk'
            elif self.status == 'dead':
                self.frame_index = len(animation) - 1  # Trava no último frame se estiver morto
            else:
                self.frame_index = 0  # Reinicia o loop (ex: caminhada)

            if self.frame_index >= len(animation): self.frame_index = 0

        img = animation[int(self.frame_index)]
        old_center = self.rect.center  # Salva o centro para evitar "pulos" visuais

        # Inverte a imagem horizontalmente se estiver olhando para a esquerda
        self.image = pygame.transform.flip(img, True, False) if self.direction == -1 else img
        # Atualiza o retângulo de colisão mantendo a posição centralizada
        self.rect = self.image.get_rect(center=old_center)


# --- CLASSE DO JOGADOR (HERÓI LEO) ---
class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.animations = {
            'idle': self.load_animation('asset/knightIdle.png', 4),
            'run': self.load_animation('asset/knightRun.png', 7),
            'attack': self.load_animation('asset/knightAttack1.png', 5),
            'hurt': self.load_animation('asset/knightHurt.png', 2),
            'dead': self.load_animation('asset/knightDead.png', 6)
        }
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.max_hp = 100
        self.hp = 100
        self.score = 0

    def update(self):
        self.animate()


# --- CLASSE DO INIMIGO COMUM ---
class EnemyB(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.status = 'walk'
        self.animations = {
            'walk': self.load_animation('asset/EnemyBwalk.png', 12),
            'run': self.load_animation('asset/EnemyBrun.png', 9),
            'attack1': self.load_animation('asset/EnemyBattack1.png', 6),
            'run_attack': self.load_animation('asset/EnemyBrun+attack.png', 7)
        }
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 4
        self.hp = 40

    def update(self, player_rect):
        self.animate()
        dist_x = player_rect.centerx - self.rect.centerx
        dist_y = player_rect.centery - self.rect.centery

        if self.status in ['walk', 'run']:
            self.status = 'run' if abs(dist_x) > 250 else 'walk'

            if abs(dist_x) > 50 or abs(dist_y) > 20:
                self.direction = 1 if dist_x > 0 else -1
                if abs(dist_x) > 50: self.rect.x += self.speed * self.direction
                if abs(dist_y) > 20: self.rect.y += self.speed * (1 if dist_y > 0 else -1)
            else:
                self.status = 'run_attack' if self.status == 'run' else 'attack1'
                self.frame_index = 0


# --- CLASSE DO CHEFE FINAL (LUCI) ---
class Luci(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.status = 'idle'
        self.animations = {
            'idle': self.load_animation('asset/MainEnemyIdle.png', 6, 2.5),
            'walk': self.load_animation('asset/MainEnemyWalk.png', 12, 2.5),
            'attack': self.load_animation('asset/MainEnemyAttack1.png', 10, 2.5),
            'hurt': self.load_animation('asset/MainEnemyHurt.png', 4, 2.5),
            'dead': self.load_animation('asset/MainEnemyDead.png', 4, 2.5)
        }
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 1.5
        self.max_hp = 200
        self.hp = 200

    def update(self, player_rect):
        self.animate()
        if self.status not in ['attack', 'hurt', 'dead']:
            dist_x = player_rect.centerx - self.rect.centerx
            dist_y = player_rect.centery - self.rect.centery
            if abs(dist_x) > 70 or abs(dist_y) > 30:
                self.status = 'walk'
                self.direction = 1 if dist_x > 0 else -1
                if abs(dist_x) > 70: self.rect.x += self.speed * self.direction
                if abs(dist_y) > 30: self.rect.y += self.speed * (1 if dist_y > 0 else -1)
            else:
                self.status = 'attack'
                self.frame_index = 0