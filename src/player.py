from goblet import Goblet

class Player:
    def __init__(self, name, color):
        self.__name = name
        self.__color = color
        self.__goblet = Goblet(color)

    def get_name(self):
        return self.__name

    def get_color(self):
        return self.__color

    def get_goblet(self):
        return self.__goblet
    
    def play(self):
        self.__goblet.shake()

    def __str__(self):
        return f'Player {self.__name}: Color={self.__color}, Goblet={self.__goblet}'
    
    def __repr__(self):
        return self.__str__()