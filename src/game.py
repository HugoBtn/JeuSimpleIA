from player import Player
from bet import Bet


class Game:
    """Core game logic for Perudo."""

# Constructor
    def __init__(self, players: list[Player]):
        self.__players = players
        self.__current_betting_player_index = 0
        self.__current_bet = None
        self.__round_active = False

# Getters
    def get_current_player_index(self):
        """Return the index of the current betting player"""
        return self.__current_betting_player_index

    def get_current_bet(self):
        """Return the current bet"""
        return self.__current_bet

    def get_all_dice_values(self):
        """Return a dictionnary with all dice values"""
        result = {}
        for player in self.__players:
            dice_list = player.get_goblet().get_content()
            result[player.get_name()] = [dice.get_value() for dice in dice_list]
        return result

# Game state
    def is_palepico_mode(self):
        """Check if the fame is in Palepico mode"""
        return any(p.palepico() for p in self.__players)

# Round
    def start_new_round(self):
        """Start a new round by rolling dice for all players"""
        self.__round_active = True
        for player in self.__players:
            player.play()

    def end_round(self):
        """End the current round, reset bet, check for game over and return if there is a winner"""
        self.__current_bet = None
        self.__round_active = False

        players_alive = [p for p in self.__players if p.get_goblet_length() > 0]
        game_over = len(players_alive) == 1
        winner = players_alive[0] if game_over else None

        return game_over, winner

# Betting logic
    def set_current_bet(self, bet):
        """Set the current bet"""
        self.__current_bet = bet

    def next_betting_player(self):
        """Move to the next betting player"""
        self.__current_betting_player_index = (self.__current_betting_player_index + 1) % len(self.__players)

    def _count_dice_for_bet(self, value):
        """Count total dice of the value in all players

        Rules :
        - In normal mode, PACO (1) counts as a wildcard for all values
        - In Palepico mode, PACO is not a wildcard"""
        count = 0
        palepico = self.is_palepico_mode()

        for p in self.__players:
            count += p.get_goblet().count_value(value)

            if not palepico and value != 1:
                count += p.get_goblet().count_value(1)

        return count

# Resolution
    def _no_active_bet_result(self):
        """Return dictionnary when no bet is active"""
        return {
            "loser": None,
            "count": 0,
            "expected": 0,
            "message": "Aucun pari actif!",
            "game_over": False,
            "winner": None
        }

    def resolve_dodo(self):
        """Resolve a Dodo call

        Rules :
        - If the dice count is lower than the bet, the last bettor loses
        - If not, the Dodo caller loses"""
        if self.__current_bet is None:
            return self._no_active_bet_result()

        value = self.__current_bet.get_value()
        expected_count = self.__current_bet.get_quantity()
        count = self._count_dice_for_bet(value)

        dodo_caller_index = self.__current_betting_player_index
        last_bettor_index = (dodo_caller_index - 1) % len(self.__players)

        dodo_caller = self.__players[dodo_caller_index]
        last_bettor = self.__players[last_bettor_index]

        if count < expected_count:
            loser = last_bettor
            loser.lost()
            self.__current_betting_player_index = last_bettor_index
            message = f"{loser.get_name()} perd! Il y avait {count} dé(s) au lieu de {expected_count}"
        else:
            loser = dodo_caller
            loser.lost()
            message = f"{loser.get_name()} perd! Il y avait {count} dé(s), le pari était juste!"

        game_over, winner = self.end_round()

        return {
            "loser": loser,
            "count": count,
            "expected": expected_count,
            "message": message,
            "game_over": game_over,
            "winner": winner
        }

    def resolve_tout_pile(self):
        """Resolve a Tout pile call

        Rules :
        -If the count matches exactly, the caller wins a dice
        - If not, the caller loses a dice"""
        if self.__current_bet is None:
            return self._no_active_bet_result()

        value = self.__current_bet.get_value()
        expected_count = self.__current_bet.get_quantity()
        count = self._count_dice_for_bet(value)

        tout_pile_caller_index = self.__current_betting_player_index
        tout_pile_caller = self.__players[tout_pile_caller_index]

        if count == expected_count:
            tout_pile_caller.won()
            self.__current_betting_player_index = tout_pile_caller_index
            message = (f"Tout pile réussi ! Exactement {count} dé(s). {tout_pile_caller.get_name()} gagne un dé !")
            loser = None
        else:
            loser = tout_pile_caller
            loser.lost()
            message = (f"Tout pile raté ! Il y avait {count} dé(s) au lieu de {expected_count}. {tout_pile_caller.get_name()} perd !")

        game_over, winner = self.end_round()

        return {
            "loser": loser,
            "count": count,
            "expected": expected_count,
            "message": message,
            "game_over": game_over,
            "winner": winner
        }

# Game loop
    def game_loop(self):
        while True:
            print("Rolling dice for all players...")
            for player in self.__players:
                player.play()

            dodo = False
            while not dodo:
                player = self.__players[self.__current_betting_player_index]
                print(f"It's {player}'s turn to bet.")
                player.make_bet()
                bet = player.bet

                if bet == "dodo":
                    dodo = True
                    print(f"{player} has called dodo!")
                else:
                    palepico = self.is_palepico_mode()
                    if bet.is_valid_raise(self.__current_bet, palepico=palepico):
                        self.__current_bet = bet
                        print(f"Bet accepted: {bet}")
                        self.__current_betting_player_index = (self.__current_betting_player_index + 1) % len(
                            self.__players)
                    else:
                        print(f"Invalid bet! Please try again.")

            # Resolve Dodo
            result = self.resolve_dodo()
            print(result["message"])

            if result["game_over"]:
                print(f"\n {result['winner'].get_name()} wins the game! ")
                break

            print("\n" + "=" * 50)
            print("Starting new round!")
            print("=" * 50 + "\n")


if __name__ == "__main__":
    # Example usage with two players
    players = [Player("Alice", "purple"), Player("Bob", "red")]
    game = Game(players)
    game.game_loop()