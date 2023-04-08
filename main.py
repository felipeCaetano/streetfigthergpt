import pygame

from figther import Fighter

# Defina as dimensões da tela
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
# Defina as cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

WARRIOR_ANIM_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIM_STEPS = [8, 8, 1, 8, 8, 3, 7]
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]
ROUND_OVER_COOLDOWN = 2000


def game_ticks():
    return pygame.time.get_ticks()


intro_count = 3
last_count_update = game_ticks()
score = [0, 0]
round_over = False

# Inicie o Pygame
pygame.init()

# Crie a tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Defina o título da janela
pygame.display.set_caption("Street Fighter Pygame")

# define o background do jogo
bg_image = pygame.image.load(
    "assets/images/background/background.jpg").convert_alpha()
warrior_sheet = pygame.image.load(
    "assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load(
    "assets/images/wizard/Sprites/wizard.png").convert_alpha()


def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))


def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


figther_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet,
                    WARRIOR_ANIM_STEPS)
figther_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet,
                    WIZARD_ANIM_STEPS)

# Defina o relógio
clock = pygame.time.Clock()

# Loop principal do jogo
running = True

count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


while running:
    # Processa eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    draw_bg()
    draw_health_bar(figther_1.health, 20, 20)
    draw_health_bar(figther_2.health, SCREEN_WIDTH - 420, 20)
    if intro_count <= 0:
        figther_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, figther_2)
        figther_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, figther_1)
    else:
        draw_text(
            str(intro_count), count_font, WHITE, SCREEN_WIDTH // 2,
                                                 SCREEN_HEIGHT // 2
        )
        if game_ticks() - last_count_update >= 1000:
            last_count_update = game_ticks()
            intro_count -= 1

    figther_1.update()
    figther_2.update()
    figther_1.draw(screen)
    figther_2.draw(screen)

    if not round_over:
        if not figther_1.alive:
            score[1] += 1
            round_over = True
            round_over_time = game_ticks()
        elif not figther_2.alive:
            score[0] += 1
            round_over = True
            round_over_time = game_ticks()

    clock.tick(60)
    screen.blit(screen, [0, 0])
    pygame.display.update()
