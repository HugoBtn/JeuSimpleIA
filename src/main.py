import sys
from PySide6.QtWidgets import QApplication

from core.bot_player import BotPlayer
from gui.game_window import GameWindow
from core.player import Player
from core.q_learning_bot import QLearningBot

def main():
    # Human player
    human = Player("Toi", "purple")

    # AI opponents
    bots = [
        QLearningBot("Super IA", "red", epsilon=0),
        BotPlayer("Bot Bleu", "blue", risk=0.60)
    ]

    app = QApplication(sys.argv)

    # Create and display the main game window
    window = GameWindow(players=[human] + bots, auto_start_rounds=True)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()