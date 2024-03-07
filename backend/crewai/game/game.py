import pygame
import sys
import random

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 75))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=(820, random.randint(0, 600)))
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Projectile, self).__init__()
        self.surf = pygame.Surface((10, 5))
        self.surf.fill((0, 0, 255))
        self.rect = self.surf.get_rect(center = (x, y))

    def update(self):
        self.rect.move_ip(5, 0)
        if self.rect.left > 800:
            self.kill()

pygame.init()

# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors
WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Setup a 800x600 window
DISPLAYSURF = pygame.display.set_mode((800,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# Creating our player
player = Player()

# Creating groups
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
projectiles = pygame.sprite.Group()

# Adding a new user event
NEWENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(NEWENEMY, 250)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == NEWENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                projectile = Projectile(player.rect.midright[0], player.rect.midright[1])
                projectiles.add(projectile)
                all_sprites.add(projectile)

    DISPLAYSURF.fill(WHITE)
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    enemies.update()
    projectiles.update()
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.surf, entity.rect)
    for projectile in projectiles:
        if pygame.sprite.spritecollideany(projectile, enemies):
            projectile.kill()
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()

    pygame.display.update()
    FramePerSec.tick(FPS)

pygame.quit()
sys.exit()