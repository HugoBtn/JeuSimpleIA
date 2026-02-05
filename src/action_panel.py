from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
from PySide6.QtCore import Qt


class ActionPanel(QFrame):
    """Action panel for a player (right side panel)"""

# Constructor
    def __init__(self, player):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedWidth(280)

        self.player = player

        # Default bet inputs
        self.quantity = 1
        self.value = 1

        # Selected action: "bet", "dodo", "tout_pile", or None
        self._selected_action = None

        self._setup_ui()
        self.set_player(player)

    def _setup_ui(self):
        """Build the user interface for the action panel"""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Player title label at the top
        self.player_title = QLabel("Joueur")
        self.player_title.setAlignment(Qt.AlignCenter)
        self.player_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(self.player_title)

        layout.addSpacing(12)

        # Action buttons row (Valeur / Dodo / Tout pile)
        self.btn_value = QPushButton("Valeur")
        self.btn_dodo = QPushButton("Dodo")
        self.btn_tout_pile = QPushButton("Tout pile")

        # Make action buttons checkable
        for b in (self.btn_value, self.btn_dodo, self.btn_tout_pile):
            b.setCheckable(True)

        # Connect buttons to action their methods
        self.btn_value.clicked.connect(self.select_bet)
        self.btn_dodo.clicked.connect(self.select_dodo)
        self.btn_tout_pile.clicked.connect(self.select_tout_pile)

        row_actions = QHBoxLayout()
        row_actions.addWidget(self.btn_value)
        row_actions.addWidget(self.btn_dodo)
        row_actions.addWidget(self.btn_tout_pile)
        layout.addLayout(row_actions)
        layout.addSpacing(12)

        # Bet inputs widget (shown only if Valeur is selected)
        self.bet_widget = QWidget()
        bet_layout = QVBoxLayout()
        bet_layout.setContentsMargins(0, 0, 0, 0)
        bet_layout.setSpacing(10)
        self.bet_widget.setLayout(bet_layout)
        self.bet_widget.setStyleSheet("background: transparent;")

        # Row: Number
        row_nb = QHBoxLayout()
        label_nb = QLabel("Nombre :")
        label_nb.setStyleSheet("color: #2C3E50; font-weight: bold; font-size: 12px;")

        self.btn_nb_minus = QPushButton("-")
        self.btn_nb_minus.setFixedWidth(40)
        self.btn_nb_minus.clicked.connect(self._decrement_nb)

        self.label_nb = QLabel(str(self.quantity))
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

        # Row: Value
        row_val = QHBoxLayout()
        label_val = QLabel("Valeur :")
        label_val.setStyleSheet("color: #2C3E50; font-weight: bold; font-size: 12px;")

        self.btn_val_minus = QPushButton("-")
        self.btn_val_minus.setFixedWidth(40)
        self.btn_val_minus.clicked.connect(self._decrement_value)

        self.label_valeur = QLabel(str(self.value))
        self.label_valeur.setAlignment(Qt.AlignCenter)
        self.label_valeur.setFixedWidth(50)
        self.label_valeur.setObjectName("ValueBox")

        self.btn_val_plus = QPushButton("+")
        self.btn_val_plus.setFixedWidth(40)
        self.btn_val_plus.clicked.connect(self._increment_value)

        row_val.addWidget(label_val)
        row_val.addWidget(self.btn_val_minus)
        row_val.addWidget(self.label_valeur)
        row_val.addWidget(self.btn_val_plus)
        bet_layout.addLayout(row_val)

        # Add bet widget to main layout
        layout.addWidget(self.bet_widget)
        layout.addStretch()

        # Validate button at the bottom
        self.btn_valider = QPushButton("Valider")
        layout.addWidget(self.btn_valider)
        self.btn_valide = self.btn_valider
        self.bet_widget.setVisible(False)

        # Step button style (dark blue) for +/- controls
        step_style = """
            QPushButton {
                background-color: #2C3E50;
                color: #ECF0F1;
                border: none;
                border-radius: 6px;
                padding: 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #1F2E3A; }
            QPushButton:pressed { background-color: #16222B; }
        """
        self.btn_nb_minus.setStyleSheet(step_style)
        self.btn_nb_plus.setStyleSheet(step_style)
        self.btn_val_minus.setStyleSheet(step_style)
        self.btn_val_plus.setStyleSheet(step_style)

        # General panel and button styles
        self.setStyleSheet("""
            QFrame {
                border: 2px solid #95A5A6;
                border-radius: 12px;
                background: #ECF0F1;
                padding: 10px;
            }
            QLabel#ValueBox {
                color: #2C3E50;
                font-size: 18px;
                font-weight: bold;
                background-color: white;
                border: 2px solid #95A5A6;
                border-radius: 5px;
                padding: 6px;
            }
            QPushButton {
                padding: 8px;
                font-weight: bold;
                font-size: 12px;
                background-color: #ECF0F1;
                color: #2C3E50;
                border: 2px solid #95A5A6;
                border-radius: 6px;
            }
            QPushButton:hover { background-color: #D0D3D4; }
            QPushButton:pressed { background-color: #B3B6B7; }
            QPushButton:checked { border: 2px solid #2C3E50; }

            QPushButton[text="Valider"] {
                background-color: #34495E;
                color: #ECF0F1;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
            }
            QPushButton[text="Valider"]:hover { background-color: #2C3E50; }
        """)

# Action selection
    def _uncheck_actions(self):
        """Deselect all action buttons"""
        for b in (self.btn_value, self.btn_dodo, self.btn_tout_pile):
            b.blockSignals(True)
            b.setChecked(False)
            b.blockSignals(False)

    def select_bet(self):
        """Select 'bet' action and show bet input"""
        self._selected_action = "bet"
        self._uncheck_actions()
        self.btn_value.setChecked(True)
        self.bet_widget.setVisible(True)

    def select_dodo(self):
        """Select 'dodo' action and hide bet input"""
        self._selected_action = "dodo"
        self._uncheck_actions()
        self.btn_dodo.setChecked(True)
        self.bet_widget.setVisible(False)

    def select_tout_pile(self):
        """Select 'tout_pile' action and hide bet input"""
        self._selected_action = "tout_pile"
        self._uncheck_actions()
        self.btn_tout_pile.setChecked(True)
        self.bet_widget.setVisible(False)

    def get_selected_action(self):
        """Return the currently selected action and the bet values"""
        if self._selected_action == "bet":
            return "bet", (self.quantity, self.value)
        if self._selected_action in ("dodo", "tout_pile"):
            return self._selected_action, None
        return None, None

# Player updates
    def set_player(self, player):
        """Update the panel to the current active player"""
        self.player = player
        self.set_player_name(player.get_name())
        self.set_player_color(player.get_color())
        self.reset_action()

    def reset_action(self):
        """Reset action selection and hide bet input"""
        self._selected_action = None
        self._uncheck_actions()
        self.bet_widget.setVisible(False)
        self.reset_values()

    def set_player_name(self, name):
        """Update the player title label"""
        self.player_title.setText(name)

    def set_player_color(self, color):
        """Update the panel background color to match the player"""
        color_map = {
            "red": "rgb(220, 100, 100)",
            "blue": "rgb(100, 150, 220)",
            "purple": "rgb(147, 112, 219)"
        }
        bg_color = color_map.get(color, "#ECF0F1")

        # Add the new style of the background
        self.setStyleSheet(self.styleSheet() + f"""
            QFrame {{
                background: {bg_color};
                border: 2px solid #D3D3D3;
                border-radius: 12px;
                padding: 10px;
            }}
        """)

        self.player_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2C3E50;")

# +/- controls
    def _increment_nb(self):
        """Increase the number input, maximum 30"""
        if self.quantity < 30:
            self.quantity += 1
            self.label_nb.setText(str(self.quantity))

    def _decrement_nb(self):
        """Decrease the number input, minimum 1"""
        if self.quantity > 1:
            self.quantity -= 1
            self.label_nb.setText(str(self.quantity))

    def _increment_value(self):
        """Increase the value input, maximum 6"""
        if self.value < 6:
            self.value += 1
            self.label_valeur.setText(str(self.value))

    def _decrement_value(self):
        """Decrease the value input, minimum 1"""
        if self.value > 1:
            self.value -= 1
            self.label_valeur.setText(str(self.value))

    def reset_values(self):
        """Reset both number and value inputs to defaults"""
        self.quantity = 1
        self.value = 1
        self.label_nb.setText(str(self.quantity))
        self.label_valeur.setText(str(self.value))
