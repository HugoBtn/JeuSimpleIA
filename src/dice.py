from random import randint


class Dice:
    def __init__(self, color="white"):
        self.__color = color
        self.__value = randint(1, 6)

    def roll(self):
        self.__value = randint(1, 6)
    
    def get_value(self):
        return self.__value

    def __str__(self):
        return f"La valeur du dé de couleur {self.__color} est {str(self.__value)}"

    def __repr__(self):
        return f"[{str(self.__value)}]"