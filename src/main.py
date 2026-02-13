import sys
from PySide6.QtWidgets import QApplication

from bot_player import BotPlayer
from game_window import GameWindow
from player import Player
# Assure-toi que le fichier q_learning_bot.py existe bien dans src/
from q_learning_bot import QLearningBot 

def main():
    # Toi (L'humain)
    human = Player("Toi", "purple")
    
    bots = [
        # --- L'IA ENTRAÎNÉE ---
        # epsilon=0 signifie : "Ne joue aucun coup au hasard, utilise uniquement ton cerveau (brain.json)"
        QLearningBot("Super IA", "red", epsilon=0),
        
        # --- Un Bot Classique (pour comparer) ---
        BotPlayer("Bot Bleu", "blue", risk=0.60),
    ]

    app = QApplication(sys.argv)
    
    # On lance la fenêtre de jeu
    window = GameWindow(players=[human] + bots, auto_start_rounds=True)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()