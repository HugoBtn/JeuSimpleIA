from player import Player
from bid import Bid

class Game:
    def __init__(self, players : list[Player]):
        self.__players = players
        self.__current_betting_player_index = 0
        self.__current_bet = None
        self.__dodo = False
    

    def is_bet_valid(self, bet):
        if self.__current_bet is None:
            return True
        palepico = any(p.get_goblet_length() == 1 for p in self.__players) # pas bon mais revoir plus tard
        current = self.__current_bet
        if bet == "dodo":
            return True
        amount = bet.get_quantity()
        value = bet.get_value()

        if value < 1 or value > 6:
            return False
        if amount < 1 :
            return False

        current_amount = current.get_quantity()
        current_value = current.get_value()

        if current_value != 1 and value == 1 and not palepico:
            if amount < current_amount // 2:
                return False
            else:
                return True
        
        elif current_value == 1 and value != 1 and not palepico:
            if amount < current_amount * 2 + 1:
                return False
            else:
                return True
        
        elif palepico:
            if value != current_value:
                return False
            if amount <= current_amount:
                return False
            else:
                return True

        elif amount <= current_amount and value > current_value:
            return True
        
        elif amount > current_amount and value <= current_value:
            return True
        
        else:
            return False

    def game_loop(self):
        while True:
            print("Rolling dice for all players...")
            for player in self.__players:
                player.play()
            while not self.__dodo:
                player = self.__players[self.__current_betting_player_index]
                print(f"It's {player}'s turn to bet.")
                player.make_bet()
                bet = player.bet
                if self.is_bet_valid(bet):
                    if bet == "dodo":
                        self.__dodo = True
                        print(f"{player} has called dodo!")
                    else:
                        self.__current_bet = bet
                        print(f"Bet accepted: {bet}")
                        self.__current_betting_player_index = (self.__current_betting_player_index + 1) % len(self.__players)
            value = self.__current_bet.get_value()
            count = 0
            for p in self.__players:
                count += p.get_goblet().count_value(value)

            print(f"\nTotal count of dice with value {value}: {count}")
            dodo = self.__players[self.__current_betting_player_index - 1 if self.__current_betting_player_index - 1 >= 0 else len(self.__players) - 1]
            print(f"The bet was {dodo.bet}.\n")

            if count < dodo.bet.get_quantity():
                print(f"{dodo} loses the round!")
                dodo.lost()
                self.__current_betting_player_index = self.__current_betting_player_index - 1 if self.__current_betting_player_index - 1 >= 0 else len(self.__players) - 1
                self.__dodo = False
            else:
                print(f"{self.__players[self.__current_betting_player_index]} loses the round!")
                self.__players[self.__current_betting_player_index].lost()
                self.__dodo = False
    

if __name__ == "__main__":
    players = [Player("Alice", "purple"), Player("Bob", "red")]
    game = Game(players)
    game.game_loop()