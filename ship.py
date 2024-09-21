import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """Ініціалізувати корабель та задати його початкову позицію."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Завантажити зображення корабля та отримати його rect.
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Почати кожен новий корабель у нижній центральній частині екрану.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Зберігати десяткове значення для центру корабля.
        self.center = float(self.rect.centerx)

        # Прапори для руху.
        self.moving_right = False
        self.moving_left = False

    def center_ship(self):
        """Вирівняти корабель по центру екрану."""
        self.center = self.screen_rect.centerx

    def update(self):
        """Оновити позицію корабля на основі прапорів руху."""
        # Оновити значення центру корабля, а не rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Оновити об'єкт rect на основі self.center.
        self.rect.centerx = self.center

    def blitme(self):
        """Намалювати корабель у його поточному місці."""
        self.screen.blit(self.image, self.rect)
