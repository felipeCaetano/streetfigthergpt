import pygame


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

# Defina os grupos de sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)

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