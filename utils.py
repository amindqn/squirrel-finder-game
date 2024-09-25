# utils.py

import pygame


def load_image(name, scale=None):
    image = pygame.image.load(name).convert_alpha()
    if scale:
        image = pygame.transform.scale(image, scale)
    return image


def load_font(name, size):
    return pygame.font.Font(name, size)
