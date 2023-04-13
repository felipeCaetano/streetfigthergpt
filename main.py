import pygame
from pygame import mixer

from figther import Fighter
from settings import *


mixer.init()
# Inicie o Pygame
pygame.init()


class Game:
    def __init__(self) -> None:
        self.fighter_2 = None
        self.fighter_1 = None
        self.round_over_time = None
        self.magic_fx = None
        self.sword_fx = None
        self.victory_img = None
        self.wizard_sheet = None
        self.warrior_sheet = None
        self.bg_image = None
        self.score_font = None
        self.count_font = None
        self.intro_count = 3
        self.score = [0, 0]
        self.round_over = False
        self.running = True
        self.last_count_update = self.game_ticks()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(GAME_TITLE)
        self.create_fonts()
        self.load_images()
        self.load_sounds()
        self.create_players()

    def create_fonts(self):
        self.count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
        self.score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

    def create_players(self):
        self.fighter_1 = Fighter(
            1, 200, 310, False, WARRIOR_DATA, self.warrior_sheet, WARRIOR_ANIM_STEPS, self.sword_fx)
        self.fighter_2 = Fighter(
            2, 700, 310, True, WIZARD_DATA, self.wizard_sheet, WIZARD_ANIM_STEPS, self.magic_fx)

    def draw_bg(self):
        scaled_bg = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(scaled_bg, (0, 0))

    def draw_health_bar(self, health, x, y):
        ratio = health / 100
        pygame.draw.rect(self.screen, WHITE, (x - 2, y - 2, 404, 34))
        pygame.draw.rect(self.screen, RED, (x, y, 400, 30))
        pygame.draw.rect(self.screen, YELLOW, (x, y, 400 * ratio, 30))

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    @staticmethod
    def game_ticks():
        return pygame.time.get_ticks()

    def load_images(self):
        self.bg_image = pygame.image.load(
            "assets/images/background/background.jpg").convert_alpha()
        self.warrior_sheet = pygame.image.load(
            "assets/images/warrior/Sprites/warrior.png").convert_alpha()
        self.wizard_sheet = pygame.image.load(
            "assets/images/wizard/Sprites/wizard.png").convert_alpha()
        self.victory_img = pygame.image.load(
            "assets/images/icons/victory.png").convert_alpha()

    def load_sounds(self):
        mixer.music.load("assets/audio/music.mp3")
        mixer.music.set_volume(.5)
        self.sword_fx = mixer.Sound("assets/audio/sword.wav")
        self.sword_fx.set_volume(.5)
        self.magic_fx = mixer.Sound("assets/audio/magic.wav")
        self.magic_fx.set_volume(.75)

    @staticmethod
    def play_music():
        mixer.music.play(-1, 0, 5000)

    def run(self):
        self.play_music()
        while self.running:
            # Processa eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.draw_bg()
            self.draw_health_bar(self.fighter_1.health, 20, 20)
            self.draw_health_bar(self.fighter_2.health, SCREEN_WIDTH - 420, 20)
            self.draw_text(f"P1: {self.score[0]}", self.score_font, RED, 20, 60)
            self.draw_text(f"P2: {self.score[1]}", self.score_font, RED, 580, 60)

            if self.intro_count <= 0:
                self.fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, self.fighter_2, self.round_over)
                self.fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, self.fighter_1, self.round_over)
            else:
                self.draw_text(
                    str(self.intro_count), self.count_font, WHITE, MIDDLE_WIDTH, MIDDLE_HEIGHT
                )
                if self.game_ticks() - self.last_count_update >= 1000:
                    self.last_count_update = self.game_ticks()
                    self.intro_count -= 1

            self.fighter_1.update()
            self.fighter_2.update()
            self.fighter_1.draw(self.screen)
            self.fighter_2.draw(self.screen)

            if not self.round_over:
                if not self.fighter_1.alive:
                    self.score[1] += 1
                    self.round_over = True
                    self.round_over_time = self.game_ticks()
                elif not self.fighter_2.alive:
                    self.score[0] += 1
                    self.round_over = True
                    self.round_over_time = self.game_ticks()
            else:
                self.draw_text("K.O", self.count_font, WHITE, MIDDLE_WIDTH - 50, MIDDLE_HEIGHT - 50)
                if (self.score[0] < 2) and (self.score[1] < 2):
                    self.round_reset()
                else:
                    self.screen.blit(self.victory_img, (360, 150))

            self.clock.tick(60)
            pygame.display.update()

    def round_reset(self):
        if self.game_ticks() - self.round_over_time > ROUND_OVER_COOLDOWN:
            self.round_over = False
            self.intro_count = 3
            self.fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, self.warrior_sheet,
                                     WARRIOR_ANIM_STEPS, self.sword_fx)
            self.fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, self.wizard_sheet,
                                     WIZARD_ANIM_STEPS, self.magic_fx)


Game().run()
