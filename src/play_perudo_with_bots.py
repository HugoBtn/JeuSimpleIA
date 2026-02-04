import sys

from bot_player import BotPlayer
from game import Game
from player import Player


def main():
    # 1 humain + 4 bots
    human = Player("Toi", "Blanc")
    # Création d'une liste de 4 bots
    noms = ["Bleu", "Rouge", "Vert", "Jaune"]
    bots = [BotPlayer(f"Bot {n}", c, risk=0.5 + (i*0.05)) for i, (n, c) in enumerate(zip(noms, noms))]
    
    # Création du jeu avec l'humain et tous les bots
    game = Game([human] + bots)
    
    for b in bots:
        b.attach_game(game)

    game.game_loop()


if __name__ == "__main__":
    main()
