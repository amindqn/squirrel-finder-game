# sprites.py

import pygame
import random
import assets
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Player(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = assets.koala_img
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = speed
        self.slow_timer = 0

    def update(self, keys_pressed):
        current_speed = self.speed if self.slow_timer == 0 else max(1, self.speed // 2)
        if self.slow_timer > 0:
            self.slow_timer -= 1

        dx, dy = 0, 0
        if keys_pressed[pygame.K_LEFT]:
            dx -= current_speed
        if keys_pressed[pygame.K_RIGHT]:
            dx += current_speed
        if keys_pressed[pygame.K_UP]:
            dy -= current_speed
        if keys_pressed[pygame.K_DOWN]:
            dy += current_speed

        self.rect.x += dx
        self.rect.y += dy

        # Keep player on screen
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def slow_down(self):
        self.slow_timer = 120  # Slow down for 2 seconds


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, speed_multiplier):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        speed = speed_multiplier
        self.speedx = random.choice([-speed, speed])
        self.speedy = random.choice([-speed, speed])

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Bounce off edges
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speedx *= -1
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speedy *= -1
