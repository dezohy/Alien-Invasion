import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Відповідь на натискання клавіш."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Відповідь на відпускання клавіш."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Відповідь на натискання клавіш та події миші."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(
                ai_settings,
                screen,
                stats,
                sb,
                play_button,
                ship,
                aliens,
                bullets,
                mouse_x,
                mouse_y,
            )


def check_play_button(
    ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y
):
    """Почати нову гру, коли гравець натискає 'Play'."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Скинути налаштування гри.
        ai_settings.initialize_dynamic_settings()

        # Сховати курсор миші.
        pygame.mouse.set_visible(False)

        # Скинути статистику гри.
        stats.reset_stats()
        stats.game_active = True

        # Оновити табло.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Очистити список прибульців і куль.
        aliens.empty()
        bullets.empty()

        # Створити новий флот і вирівняти корабель.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Вистрілити кулею, якщо ліміт не досягнуто."""
    # Створити нову кулю та додати її до групи куль.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Оновити зображення на екрані та переключити на новий екран."""
    # Перемалювати екран на кожному проході циклу.
    screen.fill(ai_settings.bg_color)

    # Перемалювати всі кулі, за кораблем та прибульцями.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Відобразити інформацію про рахунок.
    sb.show_score()

    # Відобразити кнопку "Play", якщо гра не активна.
    if not stats.game_active:
        play_button.draw_button()

    # Зробити видимим найсвіжіший екран.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Оновити позицію куль та позбутися старих куль."""
    # Оновити позиції куль.
    bullets.update()

    # Позбутися куль, що зникли.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_high_score(stats, sb):
    """Перевірити, чи є новий рекорд."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_bullet_alien_collisions(
    ai_settings, screen, stats, sb, ship, aliens, bullets
):
    """Відповідь на зіткнення куль з прибульцями."""
    # Видалити всі кулі та прибульців, що зіткнулися.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Якщо весь флот знищено, почати новий рівень.
        bullets.empty()
        ai_settings.increase_speed()

        # Підвищити рівень.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def check_fleet_edges(ai_settings, aliens):
    """Відповідь на досягнення краю екрану флотом прибульців."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Опустити весь флот і змінити напрямок флоту."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Відповідь на зіткнення корабля з прибульцем."""
    if stats.ships_left > 0:
        # Зменшити кількість кораблів.
        stats.ships_left -= 1

        # Оновити табло.
        sb.prep_ships()

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    # Очистити список прибульців та куль.
    aliens.empty()
    bullets.empty()

    # Створити новий флот і вирівняти корабель.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    # Пауза.
    sleep(0.5)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Перевірити, чи не досягли прибульці нижньої частини екрану."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Вважати це так само, як зіткнення корабля з прибульцем.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Перевірити, чи флот на краю,
    потім оновити позиції всіх прибульців у флоті.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Шукати зіткнення корабля з прибульцем.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Шукати, чи не досягли прибульці нижньої частини екрану.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def get_number_aliens_x(ai_settings, alien_width):
    """Визначити кількість прибульців, що помістяться в ряд."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Визначити кількість рядів прибульців, що помістяться на екрані."""
    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Створити прибульця та розмістити його в ряді."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Створити повний флот прибульців."""
    # Створити прибульця і знайти кількість прибульців в ряді.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Створити флот прибульців.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
