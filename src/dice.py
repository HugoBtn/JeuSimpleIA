from random import randint

class Dice:
    """Represents a dice with a color and a value"""

    def __init__(self, color="white"):
        self.__color = color
        self.__value = randint(1, 6)

    def get_value(self):
        """Return the current value of the dice"""
        return self.__value

    def get_color(self):
        """Return the color of the dice"""
        return self.__color

    def roll(self):
        """Roll the dice and update its value"""
        self.__value = randint(1, 6)

    def __str__(self):
        return f"La valeur du dé est {str(self.__value)}"

    def __repr__(self):
        return f"Dé({self.__value})"