from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QVBoxLayout, QHBoxLayout, QLabel, QPushButton)
from PySide6.QtCore import Qt
from player_zone import PlayerZone
from player import Player
from action_panel import ActionPanel
import sys

from src.bet import Bet
from src.game import Game


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

        # Create game logic object
        self.game = Game(self.players)

        # Track current bet
        self.current_bet = None

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

        # Left part with dice
        left_widget = self._create_left_panel()
        root_layout.addWidget(left_widget, stretch=3)

        # Right part with action panel
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

        layout.addLayout(buttons_layout)

        # Current bet display
        self.current_bet_label = QLabel("Pari actuel : Aucun")
        self.current_bet_label.setAlignment(Qt.AlignCenter)
        self.current_bet_label.setStyleSheet("""
                    font-size: 16px; 
                    color: white; 
                    padding: 8px; 
                    background-color: #34495E; 
                    border-radius: 5px;
                """)
        layout.addWidget(self.current_bet_label)

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

    def _create_right_panel(self):
        """Create the right panel (action panel)"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        layout.addStretch()

        # Create action panel
        self.action_panel = ActionPanel(self.players[self.active_player])

        # Connect buttons directly
        self.action_panel.btn_valide.clicked.connect(self.on_bet_validated)
        self.action_panel.btn_dodo.clicked.connect(self.on_dodo)
        self.action_panel.btn_tout_pile.clicked.connect(self.on_tout_pile)

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
        current_player = self.players[self.active_player]
        self.action_panel.set_player(current_player)

        # Update info
        name = self.players[self.active_player].get_name()
        self.info_label.setText(f"C'est au tour de {name}")

    def update_current_bet_display(self):
        """Update the current bet display"""
        if self.current_bet is None:
            self.current_bet_label.setText("Pari actuel : Aucun")
        else:
            bet = self.current_bet
            value_text = f"{bet.get_value()}"
            self.current_bet_label.setText(f"Pari actuel : {bet.get_quantity()} × {value_text}")

    def on_bet_validated(self):
        """Callback when bet is validated"""
        nombre, valeur = self.action_panel.get_bet()
        name = self.players[self.active_player].get_name()

        # Create Bid object
        new_bet = Bet(nombre, valeur)

        # Check if in palepico mode
        palepico = self.game.is_palepico_mode()
        if new_bet.is_valid_raise(self.current_bet, palepico=palepico):
            # Save the bet
            self.current_bet = new_bet
            self.players[self.active_player].bet = new_bet

            # Update display
            value_text = "PACO" if valeur == 1 else f"valeur {valeur}"
            self.info_label.setText(f" {name} parie : {nombre}× {value_text}")
            self.update_current_bet_display()

            # Reset panel values for next player
            self.action_panel.reset_values()

            # Move to next player
            self.next_player()
        else:
            # Invalid bet
            if self.current_bet is None:
                self.info_label.setText(f" Erreur dans le pari")
            else:
                current = self.current_bet
                current_val_text = "PACO" if current.get_value() == 1 else f"val. {current.get_value()}"

                # Error messages
                if palepico:
                    self.info_label.setText(
                        f" PALEPICO! Même valeur seulement. Actuel: {current.get_quantity()}× {current_val_text}"
                    )
                elif current.get_value() == 1 or valeur == 1:
                    self.info_label.setText(
                        f" Règle PACO non respectée! Actuel: {current.get_quantity()}× {current_val_text}"
                    )
                else:
                    self.info_label.setText(
                        f" Pari trop bas! Doit être > {current.get_quantity()}× {current_val_text}"
                    )

    def on_dodo(self):
        """Callback when DODO is called"""
        name = self.players[self.active_player].get_name()
        self.info_label.setText(f" {name} a appelé Dodo!")

    def on_tout_pile(self):
        """Callback when TOUT PILE is called"""
        name = self.players[self.active_player].get_name()
        self.info_label.setText(f" {name} a appelé Tout pile!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())