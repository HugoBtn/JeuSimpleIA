from player import Player
from bet import Bet


class Game:
    def __init__(self, players: list[Player]):
        self.__players = players
        self.__current_betting_player_index = 0
        self.__current_bet = None
        self.__dodo = False

    def is_palepico_mode(self):
        """Check if a player has only one dice left"""
        return any(p.get_goblet_length() == 1 for p in self.__players)

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

                # Gestion du "dodo"
                if bet == "dodo":
                    self.__dodo = True
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
                        # Le joueur doit refaire son pari

            # Résolution du DODO
            value = self.__current_bet.get_value()
            count = 0
            palepico = self.is_palepico_mode()

            # Compter les dés de la valeur pariée
            for p in self.__players:
                count += p.get_goblet().count_value(value)
                # Les pacos (1) comptent comme joker sauf en palepico ou si on parie sur les pacos
                if not palepico and value != 1:
                    count += p.get_goblet().count_value(1)

            print(f"\nTotal count of dice with value {value}: {count}")

            # Déterminer qui a fait le dernier pari
            dodo_caller_index = self.__current_betting_player_index
            last_bettor_index = (self.__current_betting_player_index - 1) % len(self.__players)
            last_bettor = self.__players[last_bettor_index]

            print(f"The bet was {last_bettor.bet}.\n")

            if count < last_bettor.bet.get_quantity():
                # Le parieur perd
                print(f"{last_bettor} loses the round!")
                last_bettor.lost()
                self.__current_betting_player_index = last_bettor_index
            else:
                # Celui qui a appelé DODO perd
                print(f"{self.__players[dodo_caller_index]} loses the round!")
                self.__players[dodo_caller_index].lost()

            # Réinitialiser pour le prochain tour
            self.__dodo = False
            self.__current_bet = None

            # Vérifier si des joueurs sont éliminés
            players_alive = [p for p in self.__players if p.get_goblet_length() > 0]
            if len(players_alive) == 1:
                print(f"\n {players_alive[0]} wins the game! ")
                break

            print("\n" + "=" * 50)
            print("Starting new round!")
            print("=" * 50 + "\n")


if __name__ == "__main__":
    players = [Player("Alice", "purple"), Player("Bob", "red")]
    game = Game(players)
    game.game_loop()