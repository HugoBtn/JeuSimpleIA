from goblet import Goblet

class Player:
    def __init__(self, name, color):
        self.__name = name
        self.__color = color
        self.__goblet = Goblet(color)
        self.__palepico = False
        self.bet = None
    
    def play(self):
        self.__goblet.shake()
    
    def make_bet(self):
        while True:
            print(f"\n--- Tour de {self.__name} ---")
            entry = input("Entrez votre mise (ex: '3,4'), 'dodo' (menteur) ou 'pile' (tout pile) : ").lower().strip()
            
            if entry == "dodo":
                self.bet = "dodo"
                break
            elif entry == "pile":
                self.bet = "pile"
                break
            else:
                try:
                    # Nettoyage des parenthèses si l'utilisateur en met
                    clean_entry = entry.replace("(", "").replace(")", "")
                    amount, value = map(int, clean_entry.split(","))
                    self.bet = (amount, value)
                    break
                except ValueError:
                    print("Erreur : Format invalide. Utilisez 'quantité,valeur' (ex: 2,5).")
    
    def lost(self):
        self.__goblet.remove_die()
        # Devient Palepico s'il ne reste qu'un dé
        if not self.__palepico and len(self.__goblet) == 1:
            self.__palepico = True
            print(f"⚠️  {self.__name} n'a plus qu'un dé : passage en mode PALEPICO !")
        else:
            self.__palepico = False

    def win_die(self):
        return self.__goblet.add_dice()
    
    def palepico(self):
        return self.__palepico

    def get_goblet(self):
        return self.__goblet

    def __str__(self):
        return self.__name