import pygame
import random
from code.Parallax import Parallax
from code.Entity import Entity, Enemy
from code.ScoreManager import ScoreManager


class Level:
    def __init__(self, screen):
        self.screen = screen
        self.parallax = Parallax(screen)
        self.player = Entity(100, 500, (0, 0, 255))  # Azul para o jogador
        self.enemies = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.scroll = 0
        self.score_manager = ScoreManager()

        # Sons (Req19)
        self.punch_sound = pygame.mixer.Sound('asset/punch.wav')
        self.kick_sound = pygame.mixer.Sound('asset/kick.wav')
        pygame.mixer.music.load('asset/BackgroundMedievalSong.wav')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

    def spawn_enemy(self):
        if len(self.enemies) < 3:  # Mantém no máximo 3 inimigos na tela
            enemy = Enemy(1300, 500)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

    def run(self):
        self.spawn_enemy()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "QUIT"

            # Ataques (Req7)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Soco
                    self.punch_sound.play()
                    self.attack()
                elif event.button == 3:  # Chute
                    self.kick_sound.play()
                    self.attack()

        # Movimentação (Req7)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]: self.scroll += 5; self.player.rect.x += 2
        if keys[pygame.K_a]: self.scroll -= 5; self.player.rect.x -= 2
        if keys[pygame.K_w]: self.player.rect.y -= 5
        if keys[pygame.K_s]: self.player.rect.y += 5

        # Colisões (Req3)
        enemy_hit = pygame.sprite.spritecollideany(self.player, self.enemies)
        if enemy_hit:
            self.player.hp -= 0.5  # Perde vida se colidir sem atacar

        # Desenho
        self.parallax.draw(self.scroll)
        self.enemies.update(self.player.rect)
        self.all_sprites.draw(self.screen)

        # UI (Req4)
        font = pygame.font.SysFont("Arial", 30)
        self.screen.blit(font.render(f"HP: {int(self.player.hp)}", True, (255, 0, 0)), (20, 20))
        self.screen.blit(font.render(f"Score: {self.player.score}", True, (255, 255, 255)), (20, 60))

        # Fim de Jogo (Req5)
        if self.player.hp <= 0 or self.player.score >= 100:
            self.score_manager.save_score("Player", self.player.score)
            pygame.mixer.music.stop()
            return "MENU"

        return "PLAYING"

    def attack(self):
        # Verifica se há inimigos próximos ao atacar (Req3)
        hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
        for _ in hits:
            self.player.score += 10