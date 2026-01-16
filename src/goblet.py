from dice import Dice

class Goblet:
    def __init__(self, color, capacity):
        self.__color = color
        self.__size = capacity
        self.__content = []
    
    def get_color(self):
        return self.__color

    def get_capacity(self):
        return self.__size

    def get_content(self):
        return self.__content.copy()

    def add_dice(self, dice: Dice):
        if len(self.__content) < self.__size:   
            self.__content.append(dice)
        else:
            print("Le gobelet est plein.")

    def __str__(self):
        return f"Gobelet de couleur {self.__color} avec une capacité de {self.__size} dés et contenant {self.__content}."
    