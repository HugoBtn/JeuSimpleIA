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

# Constructor
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Perudo")
        self.resize(1000, 600)

        # Initialize players
        self.players = [
            Player("Joueur 1", "purple"),
            Player("Joueur 2", "red"),
            Player("Joueur 3", "blue")
        ]

        # Index of the player playing
        self.active_player = 0

        # Create game logic
        self.game = Game(self.players)

        # Round state
        self.round_started = False

        # User Interface
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

        # Left panel : player zones and round
        left_widget = self._create_left_panel()
        root_layout.addWidget(left_widget, stretch=3)

        # Right panel : action panel of the player
        right_widget = self._create_right_panel()
        root_layout.addWidget(right_widget, stretch=1)

    def _create_left_panel(self):
        """Create the left panel including player zones and round controls"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Title label
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

        # Button to start round
        buttons_layout = QHBoxLayout()
        self.btn_start_round = QPushButton(" Lancer le tour")
        self.btn_start_round.setStyleSheet("""
                    font-size: 14px; 
                    padding: 10px; 
                    background-color: #E74C3C; 
                    color: #ECF0F1; 
                    font-weight: bold; 
                    border-radius: 5px;
                """)
        self.btn_start_round.clicked.connect(self.start_round)
        buttons_layout.addWidget(self.btn_start_round)
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
        self.info_label = QLabel("Cliquez sur 'Lancer le tour' pour commencer")
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
        """Create the right panel containing the action panel"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        layout.addStretch()

        # Action panel for the current player
        self.action_panel = ActionPanel(self.players[self.active_player])

        # Connect only the validate button
        self.action_panel.btn_valider.clicked.connect(self.on_validate_action)

        layout.addWidget(self.action_panel, alignment=Qt.AlignRight)
        layout.addStretch()
        return widget

# Dice
    def _hide_all_dice(self):
        """Hide dice for all players"""
        for zone in self.player_zones:
            zone.hide_dice()

    def _show_active_player_dice(self):
        """Show dice only for the active player"""
        self._hide_all_dice()
        if self.round_started:
            self.player_zones[self.active_player].show_dice()

    def _show_all_dice(self):
        """Reveal all dice at the end of a round"""
        for zone in self.player_zones:
            zone.show_dice()
# Round
    def start_round(self):
        """Start a new round: roll dice and update UI"""
        self.game.start_new_round()
        self.round_started = True

        # Update dice and bet
        self._show_active_player_dice()
        self.update_current_bet_display()

        name = self.players[self.active_player].get_name()
        self.info_label.setText(f"Tour lancé ! {name}, à toi de jouer.")

    def next_player(self):
        """Move to next player and update action panel and UI"""
        self.active_player = (self.active_player + 1) % len(self.players)
        current_player = self.players[self.active_player]
        self.action_panel.set_player(current_player)
        self._show_active_player_dice()

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
            palepico_warning = "  [PALEPICO MODE]" if self.game.is_palepico_mode() else ""
            self.current_bet_label.setText(f"Pari actuel : {current_bet.get_quantity()} × {value_text}{palepico_warning}")

# Actions
    def on_validate_action(self):
        """Handle validation of the selected action from the action panel"""
        if not self.round_started:
            self.info_label.setText(" Lance d'abord le tour (Lancer le tour).")
            return

        action, bet_values = self.action_panel.get_selected_action()
        name = self.players[self.active_player].get_name()

        if action is None:
            self.info_label.setText(" Choisis d'abord une action : Valeur, Dodo ou Tout pile.")
            return

        # Action types
        if action == "bet":
            self._handle_bet(bet_values, name)
        elif action == "dodo":
            self._handle_dodo(name)
        elif action == "tout_pile":
            self._handle_tout_pile(name)

    def _handle_bet(self, bet_values, name):
        """Process a bet action, validate it, update game state and UI."""
        nombre, valeur = bet_values
        new_bet = Bet(nombre, valeur)
        palepico = self.game.is_palepico_mode()
        current_bet = self.game.get_current_bet()

        if new_bet.is_valid_raise(current_bet, palepico=palepico):
            # Save and display thr bet
            self.game.set_current_bet(new_bet)
            self.players[self.active_player].bet = new_bet
            value_text = "PACO" if valeur == 1 else f"valeur {valeur}"
            self.info_label.setText(f" {name} parie : {nombre} × {value_text}")
            self.update_current_bet_display()

            # Prepare for the next player
            self.action_panel.reset_action()
            self.game.next_betting_player() # Update game's betting player index
            self.next_player() # Move to next player in UI
        else:
            # Invalid bet : error message
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

    def _handle_action(self, name, call_name, resolve_function):
        """Handler for Dodo and Tout pile to avoid code duplication"""
        if self.game.get_current_bet() is None:
            self.info_label.setText(f"Aucun pari actif!")
            return

        # Reveal dice and resolve action
        self._show_all_dice()
        result = resolve_function()

        # Display result and update UI
        self.info_label.setText(f" {name} a appelé {call_name.upper()}! {result['message']}")
        self.update_current_bet_display()
        self._update_player_zones()
        self.action_panel.reset_action()

        # End game
        if result["game_over"]:
            winner_name = result["winner"].get_name()
            QMessageBox.information(self,"Partie terminée",f" {winner_name} remporte la partie!")
            self.action_panel.setEnabled(False)
            self.btn_start_round.setEnabled(False)
            return

        # Prepare next round
        self.active_player = self.game.get_current_player_index()
        self.action_panel.set_player(self.players[self.active_player])
        self.round_started = False
        self._hide_all_dice()

    def _handle_dodo(self, name):
        """Handle 'Dodo' action"""
        self._handle_action(name=name, call_name="dodo", resolve_function=self.game.resolve_dodo)

    def _handle_tout_pile(self, name):
        """Handle 'Tout pile' action"""
        self._handle_action(name=name,call_name="tout pile",resolve_function=self.game.resolve_tout_pile)

    def _update_player_zones(self):
        """Update all player zones with their current dice"""
        for zone in self.player_zones:
            zone.update_dice_count()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())