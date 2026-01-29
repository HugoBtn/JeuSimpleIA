from dice import Dice

class Goblet:
    def __init__(self, color, capacity = 5):
        self.__color = color
        self.__size = capacity
        self.__content = [Dice(color) for _ in range(capacity)]

    def get_capacity(self):
        return self.__size

    def add_dice(self, dice: Dice):
        if len(self.__content) < self.__size:   
            self.__content.append(dice)
        else:
            print("Le gobelet est plein.")
    
    def remove_die(self):
        if len(self.__content) > 0:
            self.__content.pop()
        else:
            print("Le gobelet est vide.")
    
    def shake(self):
        for dice in self.__content:
            dice.roll()
    
    def count_value(self, value, palepico=False):
        if not palepico:
            if value != 1:
                return sum(1 for dice in self.__content if dice.get_value() == value or dice.get_value() == 1)
        return sum(1 for dice in self.__content if dice.get_value() == value)

    def __str__(self):
        return f"Gobelet de couleur {self.__color} avec {len(self.__content)} dés: {str(self.__content)}"
    
    def __repr__(self):
        return self.__content
    
    def __len__(self):
        return len(self.__content)
