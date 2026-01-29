from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QVBoxLayout, QHBoxLayout, QLabel, QPushButton)
from PySide6.QtCore import Qt
from player_zone import PlayerZone
from player import Player
import sys


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Perudo - Dice Game")
        self.resize(800, 500)

        # Create players
        self.players = [
            Player("Player 1", "purple"),
            Player("Player 2", "red"),
            Player("Player 3", "blue")
        ]
        self.active_player = 0

        # Central widget
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: white;")
        self.setCentralWidget(central_widget)

        # Main vertical layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Title
        title = QLabel("PERUDO")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title)

        # Player zones
        self.player_zones = []

        for player in self.players:
            zone = PlayerZone(player)
            self.player_zones.append(zone)
            main_layout.addWidget(zone)

        # Buttons
        buttons_layout = QHBoxLayout()

        btn_roll = QPushButton("Roll dice")
        btn_roll.setStyleSheet("font-size: 14px; padding: 8px; background-color: #E74C3C; color: #ECF0F1;font-weight: bold;")
        btn_roll.clicked.connect(self.roll_dice)
        buttons_layout.addWidget(btn_roll)

        btn_next = QPushButton("Next player")
        btn_next.setStyleSheet("font-size: 14px; padding: 8px; background-color: #3498DB; color: #ECF0F1;font-weight: bold;")
        btn_next.clicked.connect(self.next_player)
        buttons_layout.addWidget(btn_next)

        main_layout.addLayout(buttons_layout)

        # Info zone
        self.info_label = QLabel("Click 'Roll dice' to start")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("font-size: 14px; color: #ECF0F1; margin: 10px;")
        main_layout.addWidget(self.info_label)

    def roll_dice(self):
        """Roll dice for the active player """

        # Roll dice for active player
        self.players[self.active_player].play()

        # Update display for active player
        self.player_zones[self.active_player].show_dice()

        name = self.players[self.active_player].get_name()
        self.info_label.setText(f"{name} rolled the dice!")

    def next_player(self):
        """Move to next player"""

        # Hide current player's dice
        self.player_zones[self.active_player].hide_dice()

        # Move to next
        self.active_player = (self.active_player + 1) % len(self.players)

        name = self.players[self.active_player].get_name()
        self.info_label.setText(f"It's {name}'s turn")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())