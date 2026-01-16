import random


class Dice:
    def __init__(self, color="white"):
        self.__color = color
        self.__value = random.randint(1, 6)
    
    def get_value(self):
        return self.__value.copy()

    def get_color(self):
        return self.__color

    def throw(self):
        self.__value = random.randint(1, 6)

    def __str__(self):
        return f"La valeur du dé est {str(self.__value)}"


if __name__ == "__main__":
    Dice1 = Dice()
    Dice2 = Dice()
    print(Dice1)
    print(Dice2)
    Dice1.throw()
    print(Dice1)
    print(Dice2)