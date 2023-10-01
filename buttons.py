from button import Button

class Buttons(Button):

    def __init__(self, ai_game):
        # Создание кнопок
        # Создание кнопкидля начала игры
        self.play_button = Button(ai_game, "Play")
        self.play_button.rect.y = self.play_button.rect.y - self.play_button.rect.height
        self.play_button._prep_msg(self.play_button.msg)

        # Создание кнопок выбора сложности игры и определение их позиции
        self.easy_button = Button(ai_game, "Easy")
        self.easy_button.rect.x = self.easy_button.rect.x - (1.1 * self.easy_button.width)
        self.easy_button._prep_msg(self.easy_button.msg)

        self.medium_button = Button(ai_game, "Medium")
        self.medium_button.button_color = (255, 255, 0)
        self.medium_button._prep_msg(self.medium_button.msg)

        self.hard_button = Button(ai_game, "Hard")
        self.hard_button.button_color = (255, 0, 0)
        self.hard_button.rect.x = self.hard_button.rect.x + (1.1 * self.hard_button.width)
        self.hard_button._prep_msg(self.hard_button.msg)

        # Создание кнопок меню
        self.options_button = Button(ai_game, "Options")
        self.options_button.rect.y = self.options_button.rect.y - (2.1 * self.options_button.rect.height)
        self.options_button._prep_msg(self.options_button.msg)
