import pygame
from settings import GRAVITY, SPEED


class Fighter:
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sfx):
        self.player = player
        self.rect = pygame.Rect(x, y, 80, 180)
        self.flip = flip
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.sfx = sfx
        self.action = 0
        self.action_dict = {
            0: "idle", 1: "run", 2: "jump", 3: "attack1", 4: "attack2", 5: "hit", 6: "death"
        }
        self.frame_index = 0
        self.attack_cooldown = 0
        self.vel_y = 0
        self.health = 100
        self.attack_type = None
        self.hit = False
        self.attacking = False
        self.jump = False
        self.running = False
        self.alive = True
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.image = self.animation_list[self.action][self.frame_index]
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

    def move(self, screen_width, screen_height, target, round_over):
        """
        movimenta o personagem pela tela, verificando sua posição em relação ao inimigo
        """
        dy = 0
        self.running = False
        self.attack_type = 0
        dx = self.fighter_handle(target, round_over)
        self.vel_y += GRAVITY
        dy += self.vel_y
        dy, dx = self.constrange_figther(screen_width, screen_height, dy, dx)
        self.get_horizon_flip(target)
        self.decrease_attack_cooldown()
        self.rect.x += dx
        self.rect.y += dy

    def constrange_figther(self, screen_width, screen_height, dy, dx):
        """
        restringe o personagem a não sair da área visível do jogo.
        """
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom
        return dy, dx

    def decrease_attack_cooldown(self):
        """
        decrementa o contador de ataque para que seja possível atacar novamente
        """
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def get_horizon_flip(self, target):
        """
        Verifica se houve a ultrpassagem do target pelo persongam e troca de lado.
        """
        if target.rect.centerx >= self.rect.centerx and self.alive:
            self.flip = False
        else:
            self.flip = True

    def fighter_handle(self, target, round_over):
        dx = 0
        key = pygame.key.get_pressed()

        key_actions_p1 = {
            pygame.K_a: ('running', -SPEED),
            pygame.K_d: ('running', SPEED),
            pygame.K_w: ('jump', -30),
            pygame.K_r: ('attack_type', 1),
            pygame.K_t: ('attack_type', 2),
        }

        key_actions_p2 = {
            pygame.K_LEFT: ('running', -SPEED),
            pygame.K_RIGHT: ('running', SPEED),
            pygame.K_UP: ('jump', -30),
            pygame.K_KP1: ('attack_type', 1),
            pygame.K_KP2: ('attack_type', 2)
        }

        if not self.attacking and self.alive and not round_over:
            if self.player == 1:
                dx = self.handle_keys(target, key, key_actions_p1)
            else:
                dx = self.handle_keys(target, key, key_actions_p2)
        return dx

    def handle_keys(self, target, key, key_actions_p1):
        dx = 0
        for k, v in key_actions_p1.items():
            if key[k]:
                attr, val = v
                if attr == 'running':
                    dx = val
                    self.running = True
                elif attr == 'jump' and not self.jump:
                    self.vel_y = val
                    self.jump = True
                elif attr == 'attack_type':
                    self.attack_type = val
                    self.attack(target)
        return dx

    def update(self):
        animation_cooldown = 50
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_animation(6)
            self.frame_index = len(self.animation_list[self.action]) - 1
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
            self.frame_index = 0
            if self.action == 3 or self.action == 4:
                self.reset_attack()
            if self.action == 5:
                self.hit = False
                self.reset_attack()

    def reset_attack(self):
        self.attacking = False
        self.attack_cooldown = 20

    def update_animation(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        target.hit = False
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect = pygame.Rect(
                self.rect.centerx - (2 * self.rect.width * self.flip),
                self.rect.y, 2 * self.rect.width, self.rect.height)
            self.sfx.play()
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
                self.running = False
                self.jump = False
            else:
                self.attacking = True
                self.running = False
                self.jump = False

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - self.offset[0] * self.image_scale,
                           self.rect.y - self.offset[1] * self.image_scale))
