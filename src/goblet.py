from dice import Dice

class Goblet:
    """Represents a goblet with a set of dice"""

    def __init__(self, color, initial_dice = 5):
        self.__color = color
        self.__size = 6
        self.__content = [Dice(color) for _ in range(initial_dice)]

    def get_color(self):
        """Return the goblet color"""
        return self.__color

    def get_capacity(self):
        """Return the maximum number of dice"""
        return self.__size

    def get_content(self):
        """Return a copy of the dice list"""
        return self.__content.copy()

    def add_dice(self, dice: Dice):
        """Add a dice to the goblet if there is space"""
        if len(self.__content) < self.__size:   
            self.__content.append(dice)
        else:
            print("The goblet is full.")
    
    def remove_dice(self):
        """Remove a dice from the goblet"""
        if len(self.__content) > 0:
            self.__content.pop()
        else:
            print("The goblet is empty.")
    
    def shake(self):
        """Roll all dice in the goblet"""
        for dice in self.__content:
            dice.roll()
    
    def count_value(self, value):
        """Count how many dice have a specific value"""
        return sum(1 for dice in self.__content if dice.get_value() == value)

    def __str__(self):
        return f"Goblet of color {self.__color} with {len(self.__content)} dice: {str(self.__content)}"
    
    def __repr__(self):
        return self.__content
    
    def __len__(self):
        return len(self.__content)