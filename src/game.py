from player import Player
from bet import Bet


class Game:
    def __init__(self, players: list[Player]):
        self.__players = players
        self.__current_betting_player_index = 0
        self.__current_bet = None
        self.__round_active = False

        self.__current_betting_player_index = self.__find_next_alive_index(self.__current_betting_player_index)

    def __find_next_alive_index(self, start_index: int) -> int:
        if not self.__players:
            return 0
        for i in range(len(self.__players)):
            idx = (start_index + i) % len(self.__players)
            if self.__players[idx].get_goblet_length() > 0:
                return idx
        return start_index

    def __normalize_current_player_index(self):
        self.__current_betting_player_index = self.__find_next_alive_index(self.__current_betting_player_index)

    def is_palepico_mode(self):
        """Check if a player has only one dice left"""
        return any(p.get_goblet_length() == 1 for p in self.__players)

    def get_current_player_index(self):
        """Get the index of the current betting player"""
        self.__normalize_current_player_index()
        return self.__current_betting_player_index

    def get_current_bet(self):
        """Get the current bet"""
        return self.__current_bet

    def set_current_bet(self, bet):
        """Set the current bet"""
        self.__current_bet = bet

    def start_new_round(self):
        """Start a new round - roll dice for all players"""
        self.__current_bet = None
        self.__round_active = True
        for player in self.__players:
            if player.get_goblet_length() > 0:
                player.play()
        self.__normalize_current_player_index()

    def is_round_active(self):
        """Check if a round is currently active"""
        return self.__round_active

    def next_betting_player(self):
        """Move to the next betting player"""
        if not self.__players:
            return
        self.__current_betting_player_index = (self.__current_betting_player_index + 1) % len(self.__players)
        self.__normalize_current_player_index()

    def count_dice_for_bet(self, value):
        count = 0
        palepico = self.is_palepico_mode()

        for p in self.__players:
            count += p.get_goblet().count_value(value)
            if not palepico and value != 1:
                count += p.get_goblet().count_value(1)

        return count

    def end_round(self):
        self.__current_bet = None
        self.__round_active = False

        players_alive = [p for p in self.__players if p.get_goblet_length() > 0]
        game_over = len(players_alive) == 1
        winner = players_alive[0] if game_over else None

        if not game_over:
            self.__normalize_current_player_index()

        return game_over, winner

    def no_active_bet_result(self):
        return {
            "loser": None,
            "count": 0,
            "expected": 0,
            "message": "Aucun pari actif!",
            "game_over": False,
            "winner": None
        }

    def resolve_dodo(self):
        """Resolve a Dodo call"""
        if self.__current_bet is None:
            return self.no_active_bet_result()

        value = self.__current_bet.get_value()
        expected_count = self.__current_bet.get_quantity()
        count = self.count_dice_for_bet(value)

        dodo_caller_index = self.__current_betting_player_index
        last_bettor_index = (dodo_caller_index - 1) % len(self.__players)

        dodo_caller = self.__players[dodo_caller_index]
        last_bettor = self.__players[last_bettor_index]

        if count < expected_count:
            loser = last_bettor
            loser.lost()
            self.__current_betting_player_index = last_bettor_index
            self.__normalize_current_player_index()
            message = f"{loser.get_name()} perd! Il y avait {count} dé(s) au lieu de {expected_count}"
        else:
            loser = dodo_caller
            loser.lost()
            self.__normalize_current_player_index()
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
        """Resolve a Tout pile call"""
        if self.__current_bet is None:
            return self.no_active_bet_result()

        value = self.__current_bet.get_value()
        expected_count = self.__current_bet.get_quantity()
        count = self.count_dice_for_bet(value)

        tout_pile_caller_index = self.__current_betting_player_index
        last_bettor_index = (tout_pile_caller_index - 1) % len(self.__players)

        tout_pile_caller = self.__players[tout_pile_caller_index]
        last_bettor = self.__players[last_bettor_index]

        # Exact match required
        if count == expected_count:
            loser = last_bettor
            loser.lost()
            self.__current_betting_player_index = last_bettor_index
            self.__normalize_current_player_index()
            message = (f"TOUT PILE réussi ! Exactement {count} dé(s). {last_bettor.get_name()} perd !")
        else:
            loser = tout_pile_caller
            loser.lost()
            self.__normalize_current_player_index()
            message = (f"TOUT PILE raté ! Il y avait {count} dé(s) au lieu de {expected_count}. {tout_pile_caller.get_name()} perd !")

        game_over, winner = self.end_round()

        return {
            "loser": loser,
            "count": count,
            "expected": expected_count,
            "message": message,
            "game_over": game_over,
            "winner": winner
        }

    def get_all_dice_values(self):
        """
        Get all dice values from all players (for showing after DODO/TOUT PILE)
        Returns a dict: {player_name: [dice_values]}
        """
        result = {}
        for player in self.__players:
            dice_list = player.get_goblet().get_content()
            result[player.get_name()] = [dice.get_value() for dice in dice_list]
        return result

    def get_players(self):
        """Get all players"""
        return self.__players

    # Original game_loop for console version (kept for compatibility)
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

                # Gestion du "dodo"
                if bet == "dodo":
                    dodo = True
                    print(f"{player} has called dodo!")
                else:
                    # Vérifier si le pari est valide avec is_valid_raise
                    palepico = self.is_palepico_mode()

                    if bet.is_valid_raise(self.__current_bet, palepico=palepico):
                        self.__current_bet = bet
                        print(f"Bet accepted: {bet}")
                        self.__current_betting_player_index = (self.__current_betting_player_index + 1) % len(
                            self.__players)
                    else:
                        print(f"Invalid bet! Please try again.")

            # Résolution du DODO
            result = self.resolve_dodo()
            print(result["message"])

            if result["game_over"]:
                print(f"\n {result['winner'].get_name()} wins the game! ")
                break

            print("\n" + "=" * 50)
            print("Starting new round!")
            print("=" * 50 + "\n")


if __name__ == "__main__":
    players = [Player("Alice", "purple"), Player("Bob", "red")]
    game = Game(players)
    game.game_loop()