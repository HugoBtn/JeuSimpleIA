from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
from PySide6.QtCore import Qt


class ActionPanel(QFrame):
    """Action panel for a player (right side panel)"""

    def __init__(self, player):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedWidth(280)

        self.player = player
        self.nb = 1
        self.valeur = 1

        # Selected action: "bet", "dodo", "tout_pile", or None
        self._selected_action = None

        self._setup_ui()
        self.set_player(player)

    def _setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Player title
        self.player_title = QLabel("Joueur")
        self.player_title.setAlignment(Qt.AlignCenter)
        self.player_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(self.player_title)

        layout.addSpacing(12)

        # --- Action buttons row (Valeur / Dodo / Tout pile)
        row_actions = QHBoxLayout()

        self.btn_valeur = QPushButton("Valeur")
        self.btn_dodo = QPushButton("Dodo")
        self.btn_tout_pile = QPushButton("Tout pile")

        # (option) action buttons selectable => subtle "selected" border
        for b in (self.btn_valeur, self.btn_dodo, self.btn_tout_pile):
            b.setCheckable(True)

        self.btn_valeur.clicked.connect(self.select_bet)
        self.btn_dodo.clicked.connect(self.select_dodo)
        self.btn_tout_pile.clicked.connect(self.select_tout_pile)

        row_actions.addWidget(self.btn_valeur)
        row_actions.addWidget(self.btn_dodo)
        row_actions.addWidget(self.btn_tout_pile)
        layout.addLayout(row_actions)

        layout.addSpacing(12)

        # --- Bet inputs container (hidden unless "Valeur" selected)
        self.bet_widget = QWidget()
        bet_layout = QVBoxLayout()
        bet_layout.setContentsMargins(0, 0, 0, 0)
        self.bet_widget.setLayout(bet_layout)
        self.bet_widget.setStyleSheet("background: transparent;")

        # Row: Number
        row_nb = QHBoxLayout()
        label_nb = QLabel("Nombre :")
        label_nb.setStyleSheet("color: #2C3E50; font-weight: bold; font-size: 12px;")

        self.btn_nb_minus = QPushButton("-")
        self.btn_nb_minus.setFixedWidth(40)
        self.btn_nb_minus.clicked.connect(self._decrement_nb)

        self.label_nb = QLabel(str(self.nb))
        self.label_nb.setAlignment(Qt.AlignCenter)
        self.label_nb.setFixedWidth(50)
        self.label_nb.setObjectName("ValueBox")

        self.btn_nb_plus = QPushButton("+")
        self.btn_nb_plus.setFixedWidth(40)
        self.btn_nb_plus.clicked.connect(self._increment_nb)

        row_nb.addWidget(label_nb)
        row_nb.addWidget(self.btn_nb_minus)
        row_nb.addWidget(self.label_nb)
        row_nb.addWidget(self.btn_nb_plus)
        bet_layout.addLayout(row_nb)

        bet_layout.addSpacing(10)

        # Row: Value
        row_val = QHBoxLayout()
        label_val = QLabel("Valeur :")
        label_val.setStyleSheet("color: #2C3E50; font-weight: bold; font-size: 12px;")

        self.btn_val_minus = QPushButton("-")
        self.btn_val_minus.setFixedWidth(40)
        self.btn_val_minus.clicked.connect(self._decrement_valeur)

        self.label_valeur = QLabel(str(self.valeur))
        self.label_valeur.setAlignment(Qt.AlignCenter)
        self.label_valeur.setFixedWidth(50)
        self.label_valeur.setObjectName("ValueBox")

        self.btn_val_plus = QPushButton("+")
        self.btn_val_plus.setFixedWidth(40)
        self.btn_val_plus.clicked.connect(self._increment_valeur)

        row_val.addWidget(label_val)
        row_val.addWidget(self.btn_val_minus)
        row_val.addWidget(self.label_valeur)
        row_val.addWidget(self.btn_val_plus)
        bet_layout.addLayout(row_val)

        layout.addWidget(self.bet_widget)
        layout.addStretch()

        # --- Validate button (global validation)
        self.btn_valider = QPushButton("Valider")
        layout.addWidget(self.btn_valider)

        # Compat si ailleurs ton code utilise encore btn_valide
        self.btn_valide = self.btn_valider

        # Base style (neutral, then recolored in set_player_color)
        self.setStyleSheet("""
            QFrame {
                border: 2px solid #95A5A6;
                border-radius: 12px;
                background: #ECF0F1;
                padding: 10px;
            }
            QPushButton {
                padding: 8px;
                font-weight: bold;
                font-size: 12px;
            }
        """)

        # Hide bet inputs by default
        self.bet_widget.setVisible(False)

    # ---- Action selection
    def _uncheck_actions(self):
        for b in (self.btn_valeur, self.btn_dodo, self.btn_tout_pile):
            b.blockSignals(True)
            b.setChecked(False)
            b.blockSignals(False)

    def select_bet(self):
        self._selected_action = "bet"
        self._uncheck_actions()
        self.btn_valeur.setChecked(True)
        self.bet_widget.setVisible(True)

    def select_dodo(self):
        self._selected_action = "dodo"
        self._uncheck_actions()
        self.btn_dodo.setChecked(True)
        self.bet_widget.setVisible(False)

    def select_tout_pile(self):
        self._selected_action = "tout_pile"
        self._uncheck_actions()
        self.btn_tout_pile.setChecked(True)
        self.bet_widget.setVisible(False)

    def get_selected_action(self):
        if self._selected_action == "bet":
            return "bet", (self.nb, self.valeur)
        if self._selected_action in ("dodo", "tout_pile"):
            return self._selected_action, None
        return None, None

    # ---- Player updates
    def set_player(self, player):
        self.player = player
        self.set_player_name(player.get_name())
        self.set_player_color(player.get_color())
        self.reset_action()

    def reset_action(self):
        self._selected_action = None
        self._uncheck_actions()
        self.bet_widget.setVisible(False)
        self.reset_values()

    def set_player_name(self, name):
        self.player_title.setText(name)

    def set_player_color(self, color):
        """Explicit button styling to avoid OS dark-blue buttons."""
        color_map = {
            "red": "rgb(220, 100, 100)",
            "blue": "rgb(100, 150, 220)",
            "purple": "rgb(147, 112, 219)"
        }
        bg_color = color_map.get(color, "#ECF0F1")

        self.setStyleSheet(f"""
            QFrame {{
                border: 2px solid #D3D3D3;
                border-radius: 12px;
                padding: 10px;
                background: {bg_color};
            }}

            QLabel {{
                color: #2C3E50;
                font-weight: bold;
                font-size: 12px;
            }}

            QLabel#ValueBox {{
                color: #2C3E50;
                font-size: 18px;
                font-weight: bold;
                background-color: white;
                border: 2px solid #95A5A6;
                border-radius: 5px;
                padding: 6px;
            }}

            QPushButton {{
                padding: 8px;
                font-weight: bold;
                font-size: 12px;
                background-color: #ECF0F1;
                color: #2C3E50;
                border: 2px solid #95A5A6;
                border-radius: 6px;
            }}

            QPushButton:hover {{
                background-color: #D0D3D4;
            }}

            QPushButton:pressed {{
                background-color: #B3B6B7;
            }}

            QPushButton:checked {{
                border: 2px solid #2C3E50;
            }}

            QPushButton[text="Valider"] {{
                background-color: #34495E;
                color: #ECF0F1;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
            }}

            QPushButton[text="Valider"]:hover {{
                background-color: #2C3E50;
            }}
        """)

        self.player_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2C3E50;")

    # ---- +/- controls
    def _increment_nb(self):
        if self.nb < 30:
            self.nb += 1
            self.label_nb.setText(str(self.nb))

    def _decrement_nb(self):
        if self.nb > 1:
            self.nb -= 1
            self.label_nb.setText(str(self.nb))

    def _increment_valeur(self):
        if self.valeur < 6:
            self.valeur += 1
            self.label_valeur.setText(str(self.valeur))

    def _decrement_valeur(self):
        if self.valeur > 1:
            self.valeur -= 1
            self.label_valeur.setText(str(self.valeur))

    def reset_values(self):
        self.nb = 1
        self.valeur = 1
        self.label_nb.setText(str(self.nb))
        self.label_valeur.setText(str(self.valeur))
