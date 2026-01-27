from goblet import Goblet
from bid import Bid

class Player:
    def __init__(self, name, color):
        self.__name = name
        self.__color = color
        self.__goblet = Goblet(color)
        self.bet = None
        self.__palepico = False
    
    def play(self):
        self.__goblet.shake()
    
    def get_goblet_length(self):
        return len(self.__goblet)
    
    def get_goblet(self):
        return self.__goblet
    
    def make_bet(self):
        bet = input(f"{self.__name}, enter your bet (dodo or (amount, value)): ")
        if "dodo" in bet.lower():
            self.bet = "dodo"
        else:
            amount, value = map(int, bet.strip("()").split(","))
            self.bet = Bid(amount,value)
    
    def lost(self):
        if len(self.__goblet) > 0:
            self.__goblet.remove_die()
        if not self.__palepico and len(self.__goblet) == 1:
            self.__palepico = True
    
    def palepico(self):
        return self.__palepico

    def __str__(self):
        return f'Player {self.__name}: Goblet={str(self.__goblet)}'
    
    def __repr__(self):
        return self.__str__()