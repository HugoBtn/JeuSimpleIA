import sys

from PySide6.QtWidgets import QApplication

from bot_player import BotPlayer
from game_window import GameWindow
from player import Player


def main():
    human = Player("Toi", "purple")
    bots = [
        BotPlayer("Bot Rouge", "red", risk=0.55),
        BotPlayer("Bot Bleu", "blue", risk=0.60),
    ]

    app = QApplication(sys.argv)
    window = GameWindow(players=[human] + bots, auto_start_rounds=True)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()