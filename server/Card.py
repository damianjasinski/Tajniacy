from shared.CardColor import CardColor


class Card():
    def __init__(self, text):
        self.text = text
        self.color = CardColor.NEUTRAL
        self.shown = False

    def set_color(self, color):
        self.color = color
