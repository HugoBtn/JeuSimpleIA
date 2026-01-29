from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSizePolicy)
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
        central_widget.setStyleSheet("background-color: #2C3E50;")
        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout()
        central_widget.setLayout(root_layout)

        left_widget = QWidget()
        root_layout.addWidget(left_widget, stretch=3)

        main_layout = QVBoxLayout()
        left_widget.setLayout(main_layout)

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

        # Right-side panel
        right_container = QWidget()
        right_layout = QVBoxLayout()
        right_container.setLayout(right_layout)

        right_layout.addStretch()
        right_layout.addWidget(self._build_action_panel(), alignment=Qt.AlignRight)
        right_layout.addStretch()

        root_layout.addWidget(right_container, stretch=1)

        self._refresh_action_panel()

    def _build_action_panel(self) -> QFrame:
        panel = QFrame()
        panel.setFrameShape(QFrame.StyledPanel)
        panel.setFixedWidth(260)

        panel_layout = QVBoxLayout()
        panel.setLayout(panel_layout)

        self.player_title = QLabel("Joueur 1")
        self.player_title.setAlignment(Qt.AlignCenter)
        self.player_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50;")
        panel_layout.addWidget(self.player_title)

        panel_layout.addSpacing(10)

        self.nb = 1
        self.valeur = 1

        row_nb = QHBoxLayout()
        label_nb = QLabel("Nombre :")
        label_nb.setStyleSheet("color: #2C3E50; font-weight: bold;")
        label_nb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        btn_nb_minus = QPushButton("-")
        btn_nb_minus.setFixedWidth(35)
        btn_nb_minus.clicked.connect(self.decrement_nb)

        self.label_nb_value = QLabel(str(self.nb))
        self.label_nb_value.setAlignment(Qt.AlignCenter)
        self.label_nb_value.setFixedWidth(40)
        self.label_nb_value.setStyleSheet("color: #2C3E50; font-size: 14px; font-weight: bold;")

        btn_nb_plus = QPushButton("+")
        btn_nb_plus.setFixedWidth(35)
        btn_nb_plus.clicked.connect(self.increment_nb)

        row_nb.addWidget(label_nb)
        row_nb.addWidget(btn_nb_minus)
        row_nb.addWidget(self.label_nb_value)
        row_nb.addWidget(btn_nb_plus)
        panel_layout.addLayout(row_nb)

        panel_layout.addSpacing(8)

        row_val = QHBoxLayout()
        label_val = QLabel("Valeur :")
        label_val.setStyleSheet("color: #2C3E50; font-weight: bold;")
        label_val.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        btn_val_minus = QPushButton("-")
        btn_val_minus.setFixedWidth(35)
        btn_val_minus.clicked.connect(self.decrement_valeur)

        self.label_val_value = QLabel(str(self.valeur))
        self.label_val_value.setAlignment(Qt.AlignCenter)
        self.label_val_value.setFixedWidth(40)
        self.label_val_value.setStyleSheet("color: #2C3E50; font-size: 14px; font-weight: bold;")

        btn_val_plus = QPushButton("+")
        btn_val_plus.setFixedWidth(35)
        btn_val_plus.clicked.connect(self.increment_valeur)

        row_val.addWidget(label_val)
        row_val.addWidget(btn_val_minus)
        row_val.addWidget(self.label_val_value)
        row_val.addWidget(btn_val_plus)
        panel_layout.addLayout(row_val)

        panel_layout.addStretch()

        bottom_row = QHBoxLayout()

        btn_dodo = QPushButton("dodo")
        btn_dodo.clicked.connect(self.on_dodo)

        btn_tout_pile = QPushButton("Tout pile")
        btn_tout_pile.clicked.connect(self.on_tout_pile)

        btn_valide = QPushButton("validé")
        btn_valide.clicked.connect(self.on_valider)

        bottom_row.addWidget(btn_dodo)
        bottom_row.addStretch()
        bottom_row.addWidget(btn_tout_pile)
        bottom_row.addStretch()
        bottom_row.addWidget(btn_valide)

        panel_layout.addLayout(bottom_row)

        self.action_panel = panel
        self.panel_base_style = """
            QFrame {
                border: 2px solid rgba(0,0,0,0.25);
                border-radius: 12px;
                padding: 10px;
            }
            QPushButton {
                padding: 6px;
                font-weight: bold;
            }
        """

        return panel

    def _get_player_color(self, player) -> str:
        if hasattr(player, "get_color"):
            c = player.get_color()
        elif hasattr(player, "color"):
            c = player.color
        else:
            c = "#ECF0F1"

        if not isinstance(c, str):
            return "#ECF0F1"

        c_low = c.strip().lower()

        palette = {
            "red": "#E74C3C",
            "blue": "#3498DB",
            "purple": "#9B59B6",
        }

        return palette.get(c_low, c)

    def _get_player_name(self, player) -> str:
        if hasattr(player, "get_name"):
            return player.get_name()
        if hasattr(player, "name"):
            return player.name
        return "Joueur"

    def _refresh_action_panel(self):
        player = self.players[self.active_player]
        name = self._get_player_name(player)
        color = self._get_player_color(player)

        self.player_title.setText(name)

        self.action_panel.setStyleSheet(self.panel_base_style + f"""
            QFrame {{
                background: {color};
            }}
        """)

    def _update_panel_labels(self):
        self.label_nb_value.setText(str(self.nb))
        self.label_val_value.setText(str(self.valeur))

    def increment_nb(self):
        if self.nb < 30:
            self.nb += 1
            self._update_panel_labels()

    def decrement_nb(self):
        if self.nb > 1:
            self.nb -= 1
            self._update_panel_labels()

    def increment_valeur(self):
        if self.valeur < 6:
            self.valeur += 1
            self._update_panel_labels()

    def decrement_valeur(self):
        if self.valeur > 1:
            self.valeur -= 1
            self._update_panel_labels()

    def on_dodo(self):
        self.info_label.setText("Action: dodo")

    def on_tout_pile(self):
        self.info_label.setText("Action: Tout pile")

    def on_valider(self):
        self.info_label.setText(f"Annonce validée: nombre={self.nb}, valeur={self.valeur}")

    def roll_dice(self):
        self.players[self.active_player].play()
        self.player_zones[self.active_player].show_dice()

        name = self.players[self.active_player].get_name()
        self.info_label.setText(f"{name} rolled the dice!")

        self._refresh_action_panel()

    def next_player(self):
        self.player_zones[self.active_player].hide_dice()
        self.active_player = (self.active_player + 1) % len(self.players)

        name = self.players[self.active_player].get_name()
        self.info_label.setText(f"It's {name}'s turn")

        self._refresh_action_panel()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())
