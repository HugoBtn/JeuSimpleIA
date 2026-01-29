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

        # =========================
        # NEW: Root layout (left game area + right action panel)
        # =========================
        root_layout = QHBoxLayout()
        central_widget.setLayout(root_layout)

        # Left area (contains your existing UI)
        left_widget = QWidget()
        root_layout.addWidget(left_widget, stretch=3)

        # Main vertical layout (UNCHANGED structure, just moved into left_widget)
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

        # =========================
        # NEW: Right-side panel (middle-right)
        # =========================
        right_container = QWidget()
        right_layout = QVBoxLayout()
        right_container.setLayout(right_layout)

        right_layout.addStretch()  # push panel to vertical middle
        right_layout.addWidget(self._build_action_panel(), alignment=Qt.AlignRight)
        right_layout.addStretch()

        root_layout.addWidget(right_container, stretch=1)

    # -------------------------
    # NEW: Build the action panel widget
    # -------------------------
    def _build_action_panel(self) -> QFrame:
        panel = QFrame()
        panel.setFrameShape(QFrame.StyledPanel)
        panel.setFixedWidth(260)

        panel_layout = QVBoxLayout()
        panel.setLayout(panel_layout)

        # Title "Joueur 1" (for now static)
        self.player_title = QLabel("Joueur 1")
        self.player_title.setAlignment(Qt.AlignCenter)
        self.player_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50;")
        panel_layout.addWidget(self.player_title)

        panel_layout.addSpacing(10)

        # Values
        self.nb = 1       # 1..30
        self.valeur = 1   # 1..6

        # Row: Nombre
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

        # Row: Valeur
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

        # Bottom buttons: dodo (left), Tout pile (center), validé (right)
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

        # Panel style
        panel.setStyleSheet("""
            QFrame {
                border: 1px solid #95A5A6;
                border-radius: 12px;
                padding: 10px;
                background: #ECF0F1;
            }
            QPushButton {
                padding: 6px;
                font-weight: bold;
            }
        """)

        return panel

    # -------------------------
    # NEW: +/- logic with bounds
    # -------------------------
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

    # -------------------------
    # NEW: action buttons handlers
    # -------------------------
    def on_dodo(self):
        self.info_label.setText("Action: dodo")

    def on_tout_pile(self):
        self.info_label.setText("Action: Tout pile")

    def on_valider(self):
        self.info_label.setText(f"Annonce validée: nombre={self.nb}, valeur={self.valeur}")

    # -------------------------
    # Existing game methods (UNCHANGED)
    # -------------------------
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
