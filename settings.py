class Settings():
    """Класс для хранения всех настроек игры Alien Invasion."""

    def __init__(self):
        """Инициализирует настройки игры."""
        # Параметры экрана
        self.screen_width = 1800
        self.screen_height = 1000
        self.bd_color = (230, 230, 230)

        # Настройки корабля
        self.ship_limit = 3

        # Параметры снаряда
        # Корабль игрока
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        # Пришельцы
        self.aliens_bullets_allowed = 3
        self.alien_bullet_color = (90, 90, 90)

        # Настройки пришельцев
        self.fleet_drop_speed = 10

        # Темп ускорения игры
        self.speedup_scale = 1.1
        # Множитель очков
        self.score_scale = 1.5

        # Флаг сложности игры дефолтное значение "easy"
        self.game_difficulty = "easy"

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # Инициализирует настройки, изменяющиеся в ходе игры
        if self.game_difficulty == "easy":
            self.ship_speed = 1.5
            self.bullet_speed = 3.0
            self.alien_bullet_speed = 0.5
            self.alien_speed = 1.0
        elif self.game_difficulty == "medium":
            self.ship_speed = 1.9
            self.bullet_speed = 3.9
            self.alien_bullet_speed = 0.6
            self.alien_speed = 1.3
        elif self.game_difficulty == "hard":
            self.ship_speed = 2.4
            self.bullet_speed = 4.8
            self.alien_bullet_speed = 0.8
            self.alien_speed = 1.6

        self.fleet_direction = 1

        # Подсчет очков
        self.alien_points = 50

    def increase_speed(self):
        # Увеличивает настройки скорости и стоимости
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
