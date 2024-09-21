import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Клас для керування кулями, випущеними з корабля."""

    def __init__(self, ai_settings, screen, ship):
        """Створити об'єкт кулі на поточній позиції корабля."""
        super(Bullet, self).__init__()
        self.screen = screen

        # Створити rect кулі у (0, 0), а потім встановити правильну позицію.
        self.rect = pygame.Rect(
            0, 0, ai_settings.bullet_width, ai_settings.bullet_height
        )
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Зберігати десяткове значення позиції кулі.
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Перемістити кулю вгору по екрану."""
        # Оновити десяткову позицію кулі.
        self.y -= self.speed_factor
        # Оновити позицію rect.
        self.rect.y = self.y

    def draw_bullet(self):
        """Намалювати кулю на екрані."""
        pygame.draw.rect(self.screen, self.color, self.rect)
