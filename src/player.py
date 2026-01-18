from goblet import Goblet

class Player:
    def __init__(self, name, color):
        self.__name = name
        self.__color = color
        self.__goblet = Goblet(color)
        self.bet = None
    
    def play(self):
        self.__goblet.shake()
    
    def get_goblet_length(self):
        return len(self.__goblet)
    
    def make_bet(self):
        amount = int(input(f"{self.__name}, enter your bet amount: "))
        value = int(input(f"{self.__name}, enter your bet value: "))
        self.bet = (amount, value)

    def __str__(self):
        return f'Player {self.__name}: Color={self.__color}, Goblet={self.__goblet}'
    
    def __repr__(self):
        return self.__str__()