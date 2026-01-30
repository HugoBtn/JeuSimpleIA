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
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Perudo")
        self.resize(1000, 600)

        self.players = [
            Player("Joueur 1", "purple"),
            Player("Joueur 2", "red"),
            Player("Joueur 3", "blue")
        ]
        self.active_player = 0
        self.game = Game(self.players)

        self.current_bet = None
        self.round_started = False

        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #2C3E50;")
        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout()
        central_widget.setLayout(root_layout)

        left_widget = self._create_left_panel()
        root_layout.addWidget(left_widget, stretch=3)

        right_widget = self._create_right_panel()
        root_layout.addWidget(right_widget, stretch=1)

        # Initial state
        self._refresh_turn_ui()

    def _create_left_panel(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        title = QLabel(" PERUDO ")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #ECF0F1;")
        layout.addWidget(title)

        self.player_zones = []
        for player in self.players:
            zone = PlayerZone(player)
            self.player_zones.append(zone)
            layout.addWidget(zone)

        # ---- Single button: Start round (roll all dice)
        buttons_layout = QHBoxLayout()

        btn_start_round = QPushButton(" Lancer le tour")
        btn_start_round.setStyleSheet("""
            font-size: 14px;
            padding: 10px;
            background-color: #E74C3C;
            color: #ECF0F1;
            font-weight: bold;
            border-radius: 5px;
        """)
        btn_start_round.clicked.connect(self.start_round)
        buttons_layout.addWidget(btn_start_round)

        layout.addLayout(buttons_layout)

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
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        layout.addStretch()

        self.action_panel = ActionPanel(self.players[self.active_player])

        # Now ONLY validate triggers the action
        self.action_panel.btn_valider.clicked.connect(self.on_validate_action)

        layout.addWidget(self.action_panel, alignment=Qt.AlignRight)
        layout.addStretch()

        return widget

    # ---- Round / Turn visuals
    def _hide_all_dice(self):
        for zone in self.player_zones:
            zone.hide_dice()

    def _show_active_player_dice(self):
        self._hide_all_dice()
        if self.round_started:
            self.player_zones[self.active_player].show_dice()

    def _refresh_turn_ui(self):
        current_player = self.players[self.active_player]
        self.action_panel.set_player(current_player)
        self._show_active_player_dice()

        name = current_player.get_name()
        if self.round_started:
            self.info_label.setText(f"C'est au tour de {name}")
        else:
            self.info_label.setText("Cliquez sur 'Lancer le tour' pour commencer")

    def start_round(self):
        """Roll dice for ALL players and start the round."""
        for p in self.players:
            p.play()

        self.round_started = True

        # Optional: reset current bet at new round start
        self.current_bet = None
        self.update_current_bet_display()

        self._refresh_turn_ui()

        name = self.players[self.active_player].get_name()
        self.info_label.setText(f"Tour lancé ! {name}, à toi de jouer.")

    def next_player(self):
        self.active_player = (self.active_player + 1) % len(self.players)
        self._refresh_turn_ui()

    def update_current_bet_display(self):
        if self.current_bet is None:
            self.current_bet_label.setText("Pari actuel : Aucun")
        else:
            bet = self.current_bet
            self.current_bet_label.setText(f"Pari actuel : {bet.get_quantity()} × {bet.get_value()}")

    # ---- Validate action (Valeur / Dodo / Tout pile)
    def on_validate_action(self):
        if not self.round_started:
            self.info_label.setText(" Lance d'abord le tour (Lancer le tour).")
            return

        action, payload = self.action_panel.get_selected_action()
        name = self.players[self.active_player].get_name()

        if action is None:
            self.info_label.setText(" Choisis d'abord une action : Valeur, Dodo ou Tout pile.")
            return

        if action == "bet":
            nombre, valeur = payload
            new_bet = Bet(nombre, valeur)

            palepico = self.game.is_palepico_mode()
            if new_bet.is_valid_raise(self.current_bet, palepico=palepico):
                self.current_bet = new_bet
                self.players[self.active_player].bet = new_bet

                value_text = "PACO" if valeur == 1 else f"{valeur}"
                self.info_label.setText(f" {name} parie : {nombre}× {value_text}")
                self.update_current_bet_display()

                # Reset action selection for next player
                self.action_panel.reset_action()

                # Pass turn
                self.next_player()
            else:
                self.info_label.setText(" Pari invalide.")
                return

        elif action == "dodo":
            # For now: UI only. Later you'll resolve the round in Game.
            if self.current_bet is None:
                self.info_label.setText(" Impossible : aucun pari à contester.")
                return

            self.info_label.setText(f" {name} a appelé Dodo ! (résolution à brancher)")
            self.action_panel.reset_action()
            # ici plus tard: résolution de manche, perte de dé, reset bet, choix du prochain starter…

        elif action == "tout_pile":
            if self.current_bet is None:
                self.info_label.setText(" Impossible : aucun pari en cours.")
                return

            self.info_label.setText(f" {name} a appelé Tout pile ! (résolution à brancher)")
            self.action_panel.reset_action()
            # idem: résolution à brancher


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())
