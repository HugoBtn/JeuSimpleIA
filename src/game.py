from player import Player
from table import Table

class Game:
    def __init__(self, players):
        self.__table = Table(players)
        self.__current_bet = None
        self.__action = None 

    def is_bet_valid(self, bet):
        if bet in ["dodo", "pile"]:
            return self.__current_bet is not None # Impossible au premier tour
        
        amount, value = bet
        if not (1 <= value <= 6) or amount < 1:
            return False
            
        if self.__current_bet is None:
            return True

        curr_amt, curr_val = self.__current_bet
        palepico = self.__table.get_current_player().palepico()

        if palepico:
            # En Palepico, la valeur ne change pas, seule la quantité augmente
            return value == curr_val and amount > curr_amt

        # Passage aux As (1)
        if curr_val != 1 and value == 1:
            return amount >= (curr_amt + 1) // 2
        # Sortie des As
        elif curr_val == 1 and value != 1:
            return amount >= (curr_amt * 2) + 1
        # Enchère classique
        else:
            if value == curr_val:
                return amount > curr_amt
            return (value > curr_val and amount >= curr_amt) or amount > curr_amt

    def game_loop(self):
        while len(self.__table) > 1:
            self.__current_bet = None
            self.__action = None
            
            print("\n" + "═"*40)
            print(" DÉBUT DE MANCHE - Les joueurs secouent leurs gobelets")
            print("═"*40)
            
            for p in self.__table:
                p.play()
                # Aide visuelle pour le test (affiche les dés de chaque joueur)
                print(f"(Secret) {p}: {p.get_goblet()}")

            while self.__action not in ["dodo", "pile"]:
                player = self.__table.get_current_player()
                if self.__current_bet:
                    print(f"\n📢 Enchère à battre : {self.__current_bet[0]} dés de face {self.__current_bet[1]}")
                else:
                    print("\n🆕 Première enchère de la manche.")

                player.make_bet()
                
                if self.is_bet_valid(player.bet):
                    if player.bet in ["dodo", "pile"]:
                        self.__action = player.bet
                    else:
                        self.__current_bet = player.bet
                        print(f"✅ Mise acceptée : {self.__current_bet}")
                        self.__table.next_player()
                else:
                    print("❌ Mise invalide ! (Rappel : on ne peut pas baisser l'enchère)")

            # Résolution de l'action (Dodo ou Pile)
            caller = self.__table.get_current_player()
            bidder = self.__table.get_previous_player()
            target_amt, target_val = self.__current_bet
            
            # On utilise le mode Palepico si celui qui a misé (le bidder) est Palepico
            is_palepico = bidder.palepico()
            count = sum(p.get_goblet().count_value(target_val, is_palepico) for p in self.__table)
            
            print("\n" + "🔍 RÉVÉLATION " + "🔍")
            print(f"L'enchère était : {target_amt} dés de {target_val}")
            print(f"Résultat du comptage : {count} dés au total (Jokers inclus : {'Non' if is_palepico else 'Oui'})")

            if self.__action == "pile":
                if count == target_amt:
                    print(f"✨ TOUT PILE ! {caller} avait raison et récupère un dé !")
                    caller.win_die()
                else:
                    print(f"❌ RATÉ ! Il n'y en avait pas pile {target_amt}. {caller} perd un dé.")
                    caller.lost()
            else: # Action "Dodo" (Menteur)
                if count < target_amt:
                    print(f"🎯 BIEN JOUÉ ! {bidder} a menti. {bidder} perd un dé.")
                    bidder.lost()
                else:
                    print(f"🚫 PERDU ! L'enchère était bonne. {caller} perd un dé.")
                    caller.lost()

            # Nettoyage des joueurs éliminés
            for p in list(self.__table):
                if len(p.get_goblet()) == 0:
                    self.__table.remove_player(p)

        print("\n" + "🏆" * 15)
        print(f" LA PARTIE EST FINIE ! VICTOIRE DE {self.__table.get_current_player()}")
        print("🏆" * 15)

if __name__ == "__main__":
    game = Game([Player("Alice", "Rouge"), Player("Bob", "Bleu"), Player("Charlie", "Vert")])
    game.game_loop()