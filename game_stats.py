class GameStats():
    """Отслеживание статистики для игры ALien Invasion"""

    def __init__(self, ai_game):
        # Инициализирует статистику
        self.settings = ai_game.settings
        self.reset_stats()
        self.file = "high_score.txt"

        # Флаги для смены окон игры
        self.game_active = False
        self.difficulty_selection = False

        # Рекорд не должен сбрасываться
        self.high_score_file_read()

    def reset_stats(self):
        # Инициализирует ститистику, изщменяющуюся в ходе игры
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def high_score_file_read(self):
        # Загружает данные рекорда из файла "high_score.txt"
        with open(self.file, "r+") as f:
            self.high_score = int(f.read())

    def high_score_file_write(self):
        # Перезаписывает рекорд в файле "high_score.txt"
        with open(self.file, "r+") as f:
            f.write(str(self.high_score))
