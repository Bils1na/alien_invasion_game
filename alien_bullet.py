import pygame
from random import randint
from pygame.sprite import Sprite


class AlienBullet(Sprite):
    """Класс для управления снарядами выпущенными кораблем"""

    def __init__(self, ai_game):
        # Создает объект снарядов в текущей позиции корабля
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.alien_bullet_color

        # Создание снаряда в позиции (0, 0) и назначение правильной позиции
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midbottom = ai_game.aliens.sprites()[randint(0, len(ai_game.aliens.sprites())) - 1].rect.midbottom

        # Позиция снаряда хранится в вещественном формате.
        self.y = float(self.rect.y)

    def update(self):
        # Перемещает снаряд вверх по экрану
        # Обновление позиции снаряда в вещественном формате
        self.y += 0.5
        # Обновление позиции прямоугольника
        self.rect.y = self.y

    def draw_alien_bullet(self):
        # Вывод снаряда на экран
        pygame.draw.rect(self.screen, self.color, self.rect)
