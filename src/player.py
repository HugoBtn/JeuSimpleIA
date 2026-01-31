from goblet import Goblet
from bet import Bet

class Player:
    """Represents a player in the Perudo game"""

# Constructor
    def __init__(self, name, color):
        self.__name = name
        self.__color = color
        self.__goblet = Goblet(color)
        self.bet = None
        self.__palepico = False

# Getters
    def get_name(self):
        """Return the player's name"""
        return self.__name

    def get_color(self):
        """Return the player's color"""
        return self.__color

    def get_goblet(self):
        """Return the player's goblet"""
        return self.__goblet

    def get_goblet_length(self):
        """Get number of dice remaining"""
        return len(self.__goblet.get_content())

# Game actions
    def play(self):
        """Roll all dice in the goblet"""
        self.__goblet.shake()

    def lost(self):
        """Player loses a die"""
        if len(self.__goblet.get_content()) > 0:
            self.__goblet.remove_dice()
        if not self.__palepico and len(self.__goblet.get_content()) == 1:
            self.__palepico = True

# Game state
    def palepico(self):
        """Check if player is in palepico mode (1 die left)"""
        return self.__palepico

# Console version
    def make_bet(self):
        """Ask a player to make a bet, used in the console version"""
        bet = input(f"{self.__name}, enter your bet (dodo or (amount, value)): ")

        if "dodo" in bet.lower():
            self.bet = "dodo"
        else:
            amount, value = map(int, bet.strip("()").split(","))
            self.bet = Bet(amount,value)

    def __str__(self):
        return f'Player {self.__name}: Color={self.__color}, Goblet={self.__goblet}'

    def __repr__(self):
        return self.__str__()
