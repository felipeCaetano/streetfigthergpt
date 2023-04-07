import pygame

from figther import Fighter

# Defina as dimensões da tela
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Inicie o Pygame
pygame.init()

# Crie a tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Defina o título da janela
pygame.display.set_caption("Street Fighter Pygame")

# Defina as cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


def get_image(sheet, width, height, offset):
    sprite_sheet = pygame.image.load(sheet).convert_alpha()
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sprite_sheet, (0, 0), (offset[0], offset[1], width, height))
    return image


# Crie os personagens
class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, image, mask, offset):
        super().__init__()
        self.images = {
            "idle": get_image(image, mask[0], mask[1], (offset[0], offset[1])),
            # pygame.image.load(image).convert_alpha(),
            "right": pygame.image.load(image).convert_alpha(),
            "left": pygame.image.load(image).convert_alpha(),
            "up": pygame.image.load(image).convert_alpha(),
            "down": pygame.image.load(image).convert_alpha(),
            "punch": get_image(image, mask[0] + 23, mask[1],
                               (offset[0] * 27, offset[1])),
            # pygame.image.load(image).convert_alpha(),
            "kick": pygame.image.load(image).convert_alpha(),
        }
        self.image = self.images["idle"]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.direction = "idle"
        self.attacking = False
        self.attack_timer = 0

    def update(self):
        # Movimenta o personagem
        if self.direction == "right":
            self.rect.x += self.speed
            self.image = self.images["right"]
        elif self.direction == "left":
            self.rect.x -= self.speed
            self.image = self.images["left"]
        elif self.direction == "up":
            self.rect.y -= self.speed
            self.image = self.images["up"]
        elif self.direction == "down":
            self.rect.y += self.speed
            self.image = self.images["down"]
        elif self.attacking:
            if pygame.time.get_ticks() - self.attack_timer > 500:
                self.attacking = False
                self.image = self.images["idle"]
        else:
            self.image = self.images["idle"]

    def punch(self):
        if not self.attacking:
            self.attacking = True
            self.attack_timer = pygame.time.get_ticks()
            self.image = self.images["punch"]

    def kick(self):
        if not self.attacking:
            self.attacking = True
            self.attack_timer = pygame.time.get_ticks()
            self.image = self.images["kick"]


# Defina a posição inicial dos personagens
player1 = Character(50, 400, "ryu.png", (50, 85), (14, 15))
player2 = Character(600, 400, "ken.gif", (40, 80), (4, 2))

# define o background do jogo
bg_image = pygame.image.load(
    "assets/images/background/background.jpg").convert_alpha()
warrior_sheet = pygame.image.load(
    "assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load(
    "assets/images/wizard/Sprites/wizard.png.png").convert_alpha()
WARRIOR_ANIM_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIM_STEPS = [8, 8, 1, 8, 8, 3, 7]


def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))


def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


figther_1 = Fighter(200, 310, warrior_sheet, WARRIOR_ANIM_STEPS)
figther_2 = Fighter(700, 310, wizard_sheet, WIZARD_ANIM_STEPS)

# Defina os grupos de sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)

# Defina o relógio
clock = pygame.time.Clock()

# Loop principal do jogo
running = True
while running:
    # Processa eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_a:
                player1.punch()
            elif event.key == pygame.K_s:
                player1.kick()
    # all_sprites.draw(screen)
    # all_sprites.update()
    draw_bg()
    draw_health_bar(figther_1.health, 20, 20)
    draw_health_bar(figther_2.health, SCREEN_WIDTH - 420, 20)
    figther_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, figther_2)
    # figther_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, figther_1)
    figther_1.draw(screen)
    figther_2.draw(screen)
    clock.tick(60)
    screen.blit(screen, [0, 0])
    pygame.display.update()
