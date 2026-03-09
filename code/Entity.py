import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        # Placeholder visual para personagem/inimigo (Req16)
        self.image = pygame.Surface((60, 120))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hp = 100
        self.score = 0

    def update(self):
        pass

class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, (200, 0, 0)) # Cor vermelha para inimigos
        self.speed = 2

    def update(self, player_rect):
        # IA simples: inimigo persegue o jogador horizontalmente
        if self.rect.x < player_rect.x:
            self.rect.x += self.speed
        elif self.rect.x > player_rect.x:
            self.rect.x -= self.speed