import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf


def run_game():
    # Ініціалізація pygame, налаштувань і об'єкта екрану.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    # Створення кнопки "Play".
    play_button = Button(ai_settings, screen, "Play")

    # Створення екземпляра для збереження статистики гри та табло для очок.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Встановлення кольору фону.
    bg_color = (230, 230, 230)

    # Створення корабля, групи куль та групи прибульців.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # Створення флоту прибульців.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Запуск основного циклу гри.
    while True:
        gf.check_events(
            ai_settings, screen, stats, sb, play_button, ship, aliens, bullets
        )

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)

        gf.update_screen(
            ai_settings, screen, stats, sb, ship, aliens, bullets, play_button
        )


run_game()
