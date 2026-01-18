from dice import Dice

class Goblet:
    def __init__(self, color, capacity = 5):
        self.__color = color
        self.__size = capacity
        self.__content = [Dice(color) for _ in range(capacity)]
    
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
    
    def shake(self):
        for dice in self.__content:
            dice.roll()

    def __str__(self):
        return f"{self.__content}"
    
    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        return len(self.__content)
