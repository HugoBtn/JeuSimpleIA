from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QVBoxLayout, QHBoxLayout, QLabel, QPushButton)
from PySide6.QtCore import Qt
from player_zone import PlayerZone
from player import Player
from action_panel import ActionPanel
import sys


class GameWindow(QMainWindow):
    """Main window for Perudo game"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Perudo")
        self.resize(1000, 600)

        # Create players
        self.players = [
            Player("Joueur 1", "purple"),
            Player("Joueur 2", "red"),
            Player("Joueur 3", "blue")
        ]
        self.active_player = 0

        self._setup_ui()

    def _setup_ui(self):
        """Build the interface"""
        # Central widget
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #2C3E50;")
        self.setCentralWidget(central_widget)

        # Main layout (left + right)
        root_layout = QHBoxLayout()
        central_widget.setLayout(root_layout)

        # Left part
        left_widget = self._create_left_panel()
        root_layout.addWidget(left_widget, stretch=3)

        # Right part
        right_widget = self._create_right_panel()
        root_layout.addWidget(right_widget, stretch=1)

    def _create_left_panel(self):
        """Create the left panel (player zones)"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Title
        title = QLabel(" PERUDO ")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #ECF0F1;")
        layout.addWidget(title)

        # Player zones
        self.player_zones = []
        for player in self.players:
            zone = PlayerZone(player)
            self.player_zones.append(zone)
            layout.addWidget(zone)

        # Buttons
        self._add_control_buttons(layout)

        # Info label
        self.info_label = QLabel("Cliquez sur 'Lancer les dés' pour commencer")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("""
            font-size: 14px; 
            color: #ECF0F1; 
            padding: 10px; 
            background-color: #34495E; 
            border-radius: 5px;
        """)
        layout.addWidget(self.info_label)

        return widget

    def _add_control_buttons(self, parent_layout):
        """Add control buttons"""
        buttons_layout = QHBoxLayout()

        btn_roll = QPushButton(" Lancer les dés")
        btn_roll.setStyleSheet("""
            font-size: 14px; 
            padding: 10px; 
            background-color: #E74C3C; 
            color: #ECF0F1; 
            font-weight: bold; 
            border-radius: 5px;
        """)
        btn_roll.clicked.connect(self.roll_dice)
        buttons_layout.addWidget(btn_roll)

        btn_next = QPushButton(" Joueur suivant")
        btn_next.setStyleSheet("""
            font-size: 14px; 
            padding: 10px; 
            background-color: #3498DB; 
            color: #ECF0F1; 
            font-weight: bold; 
            border-radius: 5px;
        """)
        btn_next.clicked.connect(self.next_player)
        buttons_layout.addWidget(btn_next)

        parent_layout.addLayout(buttons_layout)

    def _create_right_panel(self):
        """Create the right panel (action panel)"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        layout.addStretch()

        # Create action panel
        self.action_panel = ActionPanel(self.players[self.active_player])

        # Connect buttons directly (no signals)
        self.action_panel.btn_valide.clicked.connect(self.on_bet_validated)
        self.action_panel.btn_dodo.clicked.connect(self.on_dodo)

        layout.addWidget(self.action_panel, alignment=Qt.AlignRight)
        layout.addStretch()

        return widget

    def roll_dice(self):
        """Roll dice for the active player"""
        # Roll the dice
        self.players[self.active_player].play()

        # Show the dice
        self.player_zones[self.active_player].show_dice()

        # Update info
        name = self.players[self.active_player].get_name()
        self.info_label.setText(f"{name} a lancé les dés!")

    def next_player(self):
        """Move to next player"""
        # Hide current player's dice
        self.player_zones[self.active_player].hide_dice()

        # Move to next player
        self.active_player = (self.active_player + 1) % len(self.players)

        # Update the action panel
        self.update_action_panel()

        # Update info
        name = self.players[self.active_player].get_name()
        self.info_label.setText(f"C'est au tour de {name}")

    def update_action_panel(self):
        """Update the action panel for the active player"""
        current_player = self.players[self.active_player]
        self.action_panel.set_player(current_player)

    def on_bet_validated(self):
        """Callback when bet is validated"""
        nombre, valeur = self.action_panel.get_bet()
        name = self.players[self.active_player].get_name()
        self.info_label.setText(f"✓ {name} a validé: {nombre}x {valeur}")

    def on_dodo(self):
        """Callback when DODO is called"""
        name = self.players[self.active_player].get_name()
        self.info_label.setText(f" {name} a appelé DODO!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())