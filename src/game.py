from player import Player

class Game:
    def __init__(self, players : list[Player]):
        self.__players = players
        self.__current_betting_player_index = 0
        self.__current_bet = None
    

    def is_bet_valid(self, bet):
        if self.__current_bet is None:
            return True
        palepico = any(p.get_goblet_length() == 1 for p in self.__players) # pas bon mais revoir plus tard
        current = self.__current_bet
        amount, value = bet

        if value < 1 or value > 6:
            return False
        if amount < 1 :
            return False
        
        elif current[0] != 1 and value == 1 and not palepico:
            if amount < current[0] // 2:
                return False
            else:
                return True
        
        elif current[1] == 1 and value != 1 and not palepico:
            if amount < current[0] * 2 + 1:
                return False
            else:
                return True
        
        elif palepico:
            if value != current[1]:
                return False
            if amount <= current[0]:
                return False
            else:
                return True

        elif amount <= current[0] and value > current[1]:
            return True
        
        elif amount > current[0] and value <= current[1]:
            return True
        
        else:
            return False
    
    def next_turn(self):
        print("Rolling dice for all players...")
        for player in self.__players:
            player.play()
        print("Rolling dice for all players...")
        while self.__current_betting_player_index < len(self.__players):
            player = self.__players[self.__current_betting_player_index]
            print(f"It's {player}'s turn to bet.")
            player.make_bet()
            bet = player.bet
            if self.is_bet_valid(bet):
                self.__current_bet = bet
                print(f"Bet accepted: {bet}")
                self.__current_betting_player_index = self.__current_betting_player_index + 1
        print("Betting round over.")
    

if __name__ == "__main__":
    players = [Player("Alice", "purple"), Player("Bob", "red")]
    game = Game(players)
    game.next_turn()