import pygame
import random
import sys  # Necessário para acessar sys.resource_path.
from code.Parallax import Parallax
from code.Entity import Player, EnemyB, Luci
from code.ScoreManager import ScoreManager


class Level:
    """
    Classe responsável por gerenciar a mecânica do nível, incluindo o spawn de inimigos,
    detecção de colisões, interface do usuário (HUD) e sons.
    """

    def __init__(self, screen):
        self.screen = screen
        self.parallax = Parallax(screen)  # Gerencia o fundo com efeito de profundidade
        self.player = Player(100, 450)  # Instancia o herói Leo

        # Grupos de Sprites para facilitar a atualização e o desenho em massa
        self.enemies = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)

        self.scroll = 0  # Controla o deslocamento do cenário
        self.score_manager = ScoreManager()  # Gerencia o salvamento de pontuações
        self.boss_spawned = False  # Flag para garantir que o Boss nasça apenas uma vez
        self.boss_reference = None  # Referência direta ao Boss Luci

        # Gerenciamento de Timers e Resultados
        self.start_timer = 60  # Tempo de espera no início (1 segundo)
        self.end_game_timer = 0  # Tempo de exibição da mensagem final
        self.game_result = ""  # Armazena se o jogador ganhou ou perdeu

        # --- AJUSTE: Inicialização do sistema de áudio com resource_path ---
        try:
            self.punch_sound = pygame.mixer.Sound(sys.resource_path('asset/punch.wav'))
            self.kick_sound = pygame.mixer.Sound(sys.resource_path('asset/kick.wav'))

            pygame.mixer.music.load(sys.resource_path('asset/BackgroundMedievalSong.wav'))
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(-1)  # Loop infinito
        except Exception as e:
            print(f"Aviso: Erro ao carregar sons no Level: {e}")
            self.punch_sound = self.kick_sound = None

    def draw_hud(self):
        """Desenha as barras de vida e os nomes dos personagens na tela."""
        font_hud = pygame.font.SysFont("Arial", 22, bold=True)
        text_color = (0, 255, 0)  # Verde para os nomes conforme solicitado

        # --- HUD DO JOGADOR ---
        pygame.draw.rect(self.screen, (0, 0, 0), (50, 30, 304, 24))  # Borda preta
        pygame.draw.rect(self.screen, (50, 0, 0), (52, 32, 300, 20))  # Fundo vermelho escuro
        health_w = (self.player.hp / self.player.max_hp) * 300
        if health_w > 0:
            # A cor da barra muda para laranja se a vida estiver crítica
            color_bar = (0, 255, 100) if self.player.hp > 30 else (255, 200, 0)
            pygame.draw.rect(self.screen, color_bar, (52, 32, health_w, 20))
        self.screen.blit(font_hud.render("Leo", True, text_color), (50, 5))

        # --- HUD DO BOSS (Aparece apenas quando o Boss Luci é spawnado) ---
        if self.boss_spawned and self.boss_reference and self.boss_reference.alive():
            pygame.draw.rect(self.screen, (0, 0, 0), (800, 30, 404, 24))
            pygame.draw.rect(self.screen, (50, 50, 50), (802, 32, 400, 20))
            b_health_w = (self.boss_reference.hp / self.boss_reference.max_hp) * 400
            if b_health_w > 0:
                pygame.draw.rect(self.screen, (255, 50, 0), (802, 32, b_health_w, 20))

            boss_name = "Luci O Devastador"
            boss_surf = font_hud.render(boss_name, True, text_color)
            self.screen.blit(boss_surf, (1204 - boss_surf.get_width(), 5))

    def draw_messages(self):
        """Desenha mensagens de sistema centralizadas (Início, Vitória, Derrota)."""
        font_msg = pygame.font.SysFont("Arial", 80, bold=True)
        c_x, c_y = self.screen.get_width() // 2, self.screen.get_height() // 2

        if self.start_timer > 0:
            txt = font_msg.render("JOGO COMEÇANDO", True, (255, 255, 0))
            self.screen.blit(txt, (c_x - txt.get_width() // 2, c_y - 40))
            self.start_timer -= 1

        if self.game_result == "WIN":
            txt = font_msg.render("VOCÊ VENCEU!", True, (0, 255, 0))
            self.screen.blit(txt, (c_x - txt.get_width() // 2, c_y - 40))
        elif self.game_result == "LOSE":
            txt = font_msg.render("VOCÊ MORREU!", True, (255, 0, 0))
            self.screen.blit(txt, (c_x - txt.get_width() // 2, c_y - 40))

    def spawn_enemy(self):
        """Gerencia o surgimento de inimigos comuns e do Boss baseado no Score."""
        if self.game_result != "" or self.start_timer > 0: return

        if self.player.score < 80:
            if len(self.enemies) < 3:
                e = EnemyB(1400, 450 + random.randint(-50, 50))
                self.enemies.add(e)
                self.all_sprites.add(e)
        elif self.player.score >= 80 and not self.boss_spawned:
            for e in self.enemies: e.kill()
            self.boss_reference = Luci(1400, 450)
            self.enemies.add(self.boss_reference)
            self.all_sprites.add(self.boss_reference)
            self.boss_spawned = True

    def run(self):
        """Método principal do nível executado a cada frame."""
        self.spawn_enemy()

        if self.player.status not in ['attack', 'hurt']: self.player.status = 'idle'

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "QUIT"
            if self.start_timer <= 0 and self.game_result == "":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.player.status != 'attack':
                        self.player.status = 'attack'
                        self.player.frame_index = 0
                        if self.punch_sound: self.punch_sound.play()
                        self.attack()

        if self.start_timer <= 0 and self.game_result == "":
            keys = pygame.key.get_pressed()
            moving = False
            if self.player.status != 'attack':
                v = 5
                if keys[pygame.K_d]: self.scroll += 5; self.player.rect.x += v; self.player.direction = 1; moving = True
                if keys[
                    pygame.K_a]: self.scroll -= 5; self.player.rect.x -= v; self.player.direction = -1; moving = True
                if keys[pygame.K_w]: self.player.rect.y -= v; moving = True
                if keys[pygame.K_s]: self.player.rect.y += v; moving = True
                if moving: self.player.status = 'run'

        self.player.update()
        self.enemies.update(self.player.rect)

        for e in self.enemies:
            if self.player.rect.inflate(-80, -40).colliderect(e.rect.inflate(-80, -40)):
                if self.player.status != 'attack' and self.game_result == "":
                    self.player.hp -= 0.3
                    if self.player.status != 'hurt': self.player.status = 'hurt'

        self.parallax.draw(self.scroll)
        self.all_sprites.draw(self.screen)
        self.draw_hud()
        self.draw_messages()

        font_score = pygame.font.SysFont("Arial", 25, bold=True)
        score_surf = font_score.render(f"Score: {self.player.score}", True, (0, 255, 0))
        self.screen.blit(score_surf, (50, 60))

        if self.player.hp <= 0 and self.game_result == "":
            self.game_result = "LOSE"
            self.end_game_timer = 180
            pygame.mixer.music.stop()

        if self.boss_spawned and not self.boss_reference.alive() and self.game_result == "":
            self.game_result = "WIN"
            self.end_game_timer = 180
            pygame.mixer.music.stop()

        if self.game_result != "":
            self.end_game_timer -= 1
            if self.end_game_timer <= 0:
                self.score_manager.save_score("Player", self.player.score)
                return "MENU"

        return "PLAYING"

    def attack(self):
        """Verifica se o ataque do jogador atingiu algum inimigo."""
        attack_rect = self.player.rect.inflate(100, 50)
        for enemy in self.enemies:
            if attack_rect.colliderect(enemy.rect):
                if hasattr(enemy, 'hp'):
                    dano = 10 if not isinstance(enemy, Luci) else 5
                    enemy.hp -= dano
                    if enemy.hp <= 0:
                        self.player.score += 10 if not isinstance(enemy, Luci) else 100
                        enemy.kill()