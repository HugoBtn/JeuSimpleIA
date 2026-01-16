from goblet import Goblet

class Player:
    def __init__(self, name, color):
        self.__name = name
        self.__color = color
        self.__goblet = Goblet(color)
    
    def play(self):
        self.__goblet.shake()

    def __str__(self):
        return f'Player {self.__name}: Color={self.__color}, Goblet={self.__goblet}'
    
    def __repr__(self):
        return self.__str__()