import pygame.font


class Button:
    def __init__(self, ai_settings, screen, msg):
        """Ініціалізувати атрибути кнопки."""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Встановити розміри та властивості кнопки.
        self.width, self.height = 200, 50
        self.button_color = (75, 0, 130)  # Темно-фіолетовий колір
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Створити об'єкт rect для кнопки і вирівняти його по центру.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Повідомлення на кнопці потрібно підготувати лише один раз.
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Перетворити повідомлення на зображення та вирівняти текст по центру кнопки."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Намалювати порожню кнопку, потім намалювати повідомлення.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
