import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien
from buttons import Buttons
from alien_bullet import AlienBullet


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Создание экземпляра для хранения игровой статистики
        # и вывода счета на экран
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Передает классу Ship в качестве аргумента экземпляр класса AlienInvasion.
        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.aliens_bullets = pygame.sprite.Group()

        self._create_fleet()

        # # Создание кнопок
        self.buttons = Buttons(self)
        # # Создание кнопки для начала игры
        self.play_button = self.buttons.play_button
        # # Создание кнопки настроек
        self.options_button = self.buttons.options_button
        # # Создание кнопок выбора сложности игры и определение их позиции
        self.easy_button = self.buttons.easy_button
        self.medium_button = self.buttons.medium_button
        self.hard_button = self.buttons.hard_button

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_aliens_bullets()
                self.stats.high_score_file_write()

            self._update_screen()

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши."""
        # Отслеживание событий клавиатуры и мыши.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._difficulty_selection(mouse_pos)

    def _check_play_button(self, mouse_pos):
        # Запускает новую игру при нажатии кнопки Play
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Указатель мыши скрывается
            if self.play_button.rect.collidepoint(mouse_pos):
                self._start_game()

    def _difficulty_selection(self, mouse_pos):
        # Выбор сложности игры на старте
        # Инициализация настроек игры в зависимости от уровней сложности
        if self.easy_button.rect.collidepoint(mouse_pos):
            self.settings.game_difficulty = "easy"
            self.settings.initialize_dynamic_settings()
            self.stats.game_active = True
            pygame.mouse.set_visible(False)
        elif self.medium_button.rect.collidepoint(mouse_pos):
            self.settings.game_difficulty = "medium"
            self.settings.initialize_dynamic_settings()
            self.stats.game_active = True
            pygame.mouse.set_visible(False)
        elif self.hard_button.rect.collidepoint(mouse_pos):
            self.settings.game_difficulty = "hard"
            self.settings.initialize_dynamic_settings()
            self.stats.game_active = True
            pygame.mouse.set_visible(False)

    def _start_game(self):
        # Переход к выбору уровней сложности при нажатии кнопки Play
        # Сброс игровой статистики
        self.stats.reset_stats()
        self.stats.difficulty_selection = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Очистка списков пришельцев и снарядов
        self.aliens.empty()
        self.bullets.empty()

        # Создание нового флота и размещение корабля в центре
        self._create_fleet()
        self.ship.center_ship()

    def _check_keydown_events(self, event):
        # Реагирует на нажатие клавиш
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            if not self.stats.game_active:
                self._start_game()

    def _check_keyup_events(self, event):
        # Реагирует на отпускание клавиш
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _aliens_fire_bullet(self):
        # Создание снаряда пришельца и включение его в группу
        if len(self.aliens_bullets) < self.settings.aliens_bullets_allowed:
            new_alien_bullet = AlienBullet(self)
            self.aliens_bullets.add(new_alien_bullet)

    def _update_aliens_bullets(self):
        self.aliens_bullets.update()

        for alien_bullet in self.aliens_bullets.copy():
            if alien_bullet.rect.top >= self.screen.get_rect().bottom:
                self.aliens_bullets.remove(alien_bullet)

        self._check_bullet_ship_collision()

    def _check_bullet_ship_collision(self):
        # Проверка попадания в корабль игрока
        if pygame.sprite.spritecollideany(self.ship, self.aliens_bullets):
            self._ship_hit()

    def _fire_bullet(self):
        # Создание нового снаряда и включение его в группу bullets
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        # Обновляет позиции снарядов и уничтожает старые снаряды
        # Обновление позиций снарядов
        self.bullets.update()

        # Удаление снарядов, вышедших за предел экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # Проверка попаданий в пришельцев
        # При обнаружении попадания удалить снаряд и пришельца
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Уничтожение существующих снарядов и создание нового флота
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Увеличение уровня
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        # Создание пришельца и вычисление количества пришельцев в ряду
        # Интервал между сесодними пришельцами равен ширине пришельца
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Определяем количество рядом помещающихся на экран
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        # Создание флота вторжения
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # Создание пришельца и размещение его в ряду
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        # Обновляет позиции всех пришельцев во флоте
        self._check_fleet_edges()
        self.aliens.update()
        self._aliens_fire_bullet()

        # Проверка коллизий "пришелец - корабль"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Проверить, добрались ли пришельцы до нижнего края экрана
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        # Реагирует на достижение флотом края экрана
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        # Опускает весь флот и меняет направление
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            # Обрабатывает столкновение корабля с пришельцем
            # Уменьшение ships_left
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()
            self.aliens_bullets.empty()

            # Создание нового флото и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            # Пауза
            sleep(1.0)
        else:
            self.stats.game_active = False
            self.stats.difficulty_selection = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        # Проверяет, добрались ли пришельцы до нижнего края экрана
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Происходит то же, что при столкновении с кораблем
                self._ship_hit()
                break

    def _update_screen(self):
        """Обновляет изображение на экране и отображает новый экран."""
        # При каждом проходе цикла перерисовывается экран.
        self.screen.fill(self.settings.bd_color)
        if self.stats.game_active:
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)
            for alien_bullet in self.aliens_bullets.sprites():
                alien_bullet.draw_alien_bullet()

            # Вывод информации о счете
            self.sb.show_score()

        # Окно запуска игры отображается в том случае, если игра неактивна
        if not self.stats.game_active and not self.stats.difficulty_selection:
            self.play_button.draw_button()
            self.options_button.draw_button()

        # Окно выбора сложности игры
        if self.stats.difficulty_selection and not self.stats.game_active:
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()

        # Отображение последнего прорисованного экрана.
        pygame.display.flip()


if __name__ == "__main__":
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
