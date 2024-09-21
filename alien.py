import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Клас для представлення одного прибульця у флоті."""

    def __init__(self, ai_settings, screen):
        """Ініціалізувати прибульця та задати його початкову позицію."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Завантажити зображення прибульця та встановити його атрибут rect.
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # Почати кожного нового прибульця біля верхнього лівого кута екрану.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Зберегти точну позицію прибульця.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Повернути True, якщо прибулець знаходиться на краю екрану."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Переміщати прибульця вправо або вліво."""
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def blitme(self):
        """Намалювати прибульця у його поточному місці."""
        self.screen.blit(self.image, self.rect)
