import pygame


class Fighter:
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.action = 0
        # {
        #   0: "idle", 1: "run", 2: "jump", 3: "attack1", 4: "attack2",
        #   5:"hit", 6:"death"}
        self.frame_index = 0
        self.attack_type = None
        self.attack_cooldown = 0
        self.hit = False
        self.attacking = False
        self.jump = False
        self.flip = flip
        self.vel_y = 0
        self.running = False
        self.health = 100
        self.alive = True
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(x, y, 80, 180)
        self.update_time = pygame.time.get_ticks()

    def load_images(self, sprite_sheet, animation_steps):
        animation_list = [
            [pygame.transform.scale(
                sprite_sheet.subsurface(
                    x * self.size, y * self.size, self.size, self.size
                ), (self.size * self.image_scale, self.size * self.image_scale)
            )
                for x in range(animation)
            ]
            for y, animation in enumerate(animation_steps)
        ]
        return animation_list

    def move(self, screen_width, screen_height, surface, target):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        key = pygame.key.get_pressed()
        if not self.attacking and self.alive:
            if self.player == 1:
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                if key[pygame.K_w] and not self.jump:
                    self.vel_y = -30
                    self.jump = True
                if key[pygame.K_r] or key[pygame.K_t]:
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    else:
                        self.attack_type = 2
                    self.attack(surface, target)
            if self.player == 2:
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                if key[pygame.K_UP] and not self.jump:
                    self.vel_y = -30
                    self.jump = True
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    else:
                        self.attack_type = 2
                    self.attack(surface, target)

        self.vel_y += GRAVITY
        dy += self.vel_y

        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        animation_cooldown = 50
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_animation(6)
        elif self.running:
            self.update_animation(1)
        elif self.jump:
            self.update_animation(2)
        elif self.attacking:
            if self.attack_type == 1:
                self.update_animation(3)
            elif self.attack_type == 2:
                self.update_animation(4)
        elif self.hit:
            self.update_animation(5)
        else:
            self.update_animation(0)
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            if not self.alive:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                if self.action == 5:
                    self.hit = False
                    self.attacking = False
                    self.attack_cooldown = 20

    def update_animation(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def attack(self, surface, target):
        target.hit = False
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect = pygame.Rect(
                self.rect.centerx - (2 * self.rect.width * self.flip),
                self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
            pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - self.offset[0] * self.image_scale,
                           self.rect.y - self.offset[1] * self.image_scale))
