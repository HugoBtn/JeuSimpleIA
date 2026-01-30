from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox)
from PySide6.QtCore import Qt
from player_zone import PlayerZone
from player import Player
from action_panel import ActionPanel
from bet import Bet
from game import Game
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

        # Create game logic object
        self.game = Game(self.players)

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
        """Roll dice for all players (start new round)"""
        # Start new round
        self.game.start_new_round()

        # Show all dice temporarily to verify they rolled
        for zone in self.player_zones:
            zone.show_dice()

        # Update current bet display
        self.update_current_bet_display()

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
        current_bet = self.game.get_current_bet()

        if current_bet is None:
            self.current_bet_label.setText("Pari actuel : Aucun")
        else:
            value = current_bet.get_value()
            value_text = "PACO" if value == 1 else f"{value}"

            # Add palepico warning if in palepico mode
            palepico_warning = "  PALEPICO MODE" if self.game.is_palepico_mode() else ""

            self.current_bet_label.setText(
                f"Pari actuel : {current_bet.get_quantity()} × {value_text}{palepico_warning}"
            )

    def on_bet_validated(self):
        """Callback when bet is validated"""
        nombre, valeur = self.action_panel.get_bet()
        name = self.players[self.active_player].get_name()

        # Create Bet object
        new_bet = Bet(nombre, valeur)

        # Check if in palepico mode
        palepico = self.game.is_palepico_mode()
        current_bet = self.game.get_current_bet()

        # Validate the bet using Bet's is_valid_raise method
        if new_bet.is_valid_raise(current_bet, palepico=palepico):
            # Save the bet in game
            self.game.set_current_bet(new_bet)
            self.players[self.active_player].bet = new_bet

            # Update display
            value_text = "PACO" if valeur == 1 else f"valeur {valeur}"
            self.info_label.setText(f" {name} parie : {nombre} × {value_text}")
            self.update_current_bet_display()

            # Reset panel values for next player
            self.action_panel.reset_values()

            # Update game's betting player index
            self.game.next_betting_player()

            # Move to next player in UI
            self.next_player()
        else:
            # Invalid bet - generate error message
            if current_bet is None:
                self.info_label.setText(" Erreur dans le pari")
            else:
                current_val_text = "PACO" if current_bet.get_value() == 1 else f"val. {current_bet.get_value()}"

                if palepico:
                    error_msg = f" PALEPICO! Même valeur seulement. Actuel: {current_bet.get_quantity()}× {current_val_text}"
                elif current_bet.get_value() == 1 or valeur == 1:
                    error_msg = f" Règle PACO non respectée! Actuel: {current_bet.get_quantity()}× {current_val_text}"
                else:
                    error_msg = f" Pari trop bas! Doit être > {current_bet.get_quantity()}× {current_val_text}"

                self.info_label.setText(error_msg)

    def show_all_dice(self):
        """Show all players' dice"""
        for zone in self.player_zones:
            zone.show_dice()

    def on_dodo(self):
        """Callback when DODO is called"""
        name = self.players[self.active_player].get_name()

        # Check if there's a bet to challenge
        if self.game.get_current_bet() is None:
            self.info_label.setText(" Impossible d'appeler DODO : aucun pari actif!")
            return

        # Show all dice before resolution
        self.show_all_dice()

        # Resolve DODO
        result = self.game.resolve_dodo()

        # Show result in info label
        self.info_label.setText(f" {name} a appelé DODO! {result['message']}")

        # Update current bet display
        self.update_current_bet_display()

        # Update player zones to reflect lost dice
        self._update_player_zones()

        # If game is over, disable controls
        if result['game_over']:
            self.action_panel.setEnabled(False)
        else:
            # Move to the player who should start next round
            self.active_player = self.game.get_current_player_index()
            self.action_panel.set_player(self.players[self.active_player])
            self.action_panel.reset_values()

    def on_tout_pile(self):
        """Callback when TOUT PILE is called"""
        name = self.players[self.active_player].get_name()

        # Check if there's a bet to challenge
        if self.game.get_current_bet() is None:
            self.info_label.setText(" Impossible d'appeler TOUT PILE : aucun pari actif!")
            return

        # Show all dice before resolution
        self.show_all_dice()

        # Resolve TOUT PILE
        result = self.game.resolve_tout_pile()

        # Show result in info label
        self.info_label.setText(f" {name} a appelé TOUT PILE! {result['message']}")

        # Update current bet display
        self.update_current_bet_display()

        # Update player zones to reflect lost dice
        self._update_player_zones()

        # If game is over, disable controls
        if result['game_over']:
            self.action_panel.setEnabled(False)
        else:
            # Move to the player who should start next round
            self.active_player = self.game.get_current_player_index()
            self.action_panel.set_player(self.players[self.active_player])
            self.action_panel.reset_values()

    def _update_player_zones(self):
        """Update all player zones to reflect current dice counts"""
        for zone in self.player_zones:
            zone.update_dice_count()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())