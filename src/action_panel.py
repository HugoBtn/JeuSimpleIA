from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt


class ActionPanel(QFrame):
    """Action panel for a player (right side panel)"""

    def __init__(self, player):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedWidth(280)

        self.player = player

        # Default values
        self.nb = 1  # 1..30
        self.valeur = 1  # 1..6

        self._setup_ui()
        self.set_player(player)

    def _setup_ui(self):
        """Build the panel interface"""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Player title
        self.player_title = QLabel("Joueur 1")
        self.player_title.setAlignment(Qt.AlignCenter)
        self.player_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(self.player_title)

        layout.addSpacing(20)

        # Row: Number
        row_nb = QHBoxLayout()
        label_nb = QLabel("Nombre :")
        label_nb.setStyleSheet("color: #2C3E50; font-weight: bold; font-size: 12px;")

        btn_nb_minus = QPushButton("-")
        btn_nb_minus.setFixedWidth(40)
        btn_nb_minus.clicked.connect(self._decrement_nb)

        self.label_nb = QLabel(str(self.nb))
        self.label_nb.setAlignment(Qt.AlignCenter)
        self.label_nb.setFixedWidth(50)
        self.label_nb.setStyleSheet("""
            color: #2C3E50; 
            font-size: 18px; 
            font-weight: bold; 
            background-color: white; 
            border: 2px solid #95A5A6; 
            border-radius: 5px; 
        """)

        btn_nb_plus = QPushButton("+")
        btn_nb_plus.setFixedWidth(40)
        btn_nb_plus.clicked.connect(self._increment_nb)

        row_nb.addWidget(label_nb)
        row_nb.addWidget(btn_nb_minus)
        row_nb.addWidget(self.label_nb)
        row_nb.addWidget(btn_nb_plus)
        layout.addLayout(row_nb)

        layout.addSpacing(15)

        # Row: Value
        row_val = QHBoxLayout()
        label_val = QLabel("Valeur :")
        label_val.setStyleSheet("color: #2C3E50; font-weight: bold; font-size: 12px;")

        btn_val_minus = QPushButton("-")
        btn_val_minus.setFixedWidth(40)
        btn_val_minus.clicked.connect(self._decrement_valeur)

        self.label_valeur = QLabel(str(self.valeur))
        self.label_valeur.setAlignment(Qt.AlignCenter)
        self.label_valeur.setFixedWidth(50)
        self.label_valeur.setStyleSheet("""
            color: #2C3E50; 
            font-size: 18px; 
            font-weight: bold; 
            background-color: white; 
            border: 2px solid #95A5A6; 
            border-radius: 5px; 
        """)

        btn_val_plus = QPushButton("+")
        btn_val_plus.setFixedWidth(40)
        btn_val_plus.clicked.connect(self._increment_valeur)

        row_val.addWidget(label_val)
        row_val.addWidget(btn_val_minus)
        row_val.addWidget(self.label_valeur)
        row_val.addWidget(btn_val_plus)
        layout.addLayout(row_val)

        layout.addStretch()

        # Bottom buttons
        row_buttons = QHBoxLayout()

        self.btn_dodo = QPushButton("Dodo")

        self.btn_tout_pile = QPushButton("Tout pile")

        self.btn_valide = QPushButton("Valider")

        row_buttons.addWidget(self.btn_dodo)
        row_buttons.addWidget(self.btn_tout_pile)
        row_buttons.addWidget(self.btn_valide)
        layout.addLayout(row_buttons)

        # Panel style
        self.setStyleSheet("""
            QFrame {
                border: 2px solid #95A5A6;
                border-radius: 12px;
                background: #ECF0F1;
            }
            QPushButton {
                padding: 8px;
                font-weight: bold;
                font-size: 12px;
            }
        """)

    def set_player(self, player):
        """Set the current player and update UI"""
        self.player = player
        self.set_player_name(player.get_name())
        self.set_player_color(player.get_color())

    def _increment_nb(self):
        """Increment the number"""
        if self.nb < 30:
            self.nb += 1
            self.label_nb.setText(str(self.nb))

    def _decrement_nb(self):
        """Decrement the number"""
        if self.nb > 1:
            self.nb -= 1
            self.label_nb.setText(str(self.nb))

    def _increment_valeur(self):
        """Increment the value"""
        if self.valeur < 6:
            self.valeur += 1
            self.label_valeur.setText(str(self.valeur))

    def _decrement_valeur(self):
        """Decrement the value"""
        if self.valeur > 1:
            self.valeur -= 1
            self.label_valeur.setText(str(self.valeur))

    def get_bet(self):
        """Get the current bet (number, value)"""
        return (self.nb, self.valeur)

    def set_player_name(self, name):
        """Change the displayed player name"""
        self.player_title.setText(name)

    def set_player_color(self, color):
        """Change the panel background color based on player"""

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
            QPushButton {{
                padding: 8px;
                font-weight: bold;
                font-size: 12px;
            }}
        """)

        # Titre lisible
        self.player_title.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #2C3E50;"
        )

    def reset_values(self):
        """Reset values to 1"""
        self.nb = 1
        self.valeur = 1
        self.label_nb.setText(str(self.nb))
        self.label_valeur.setText(str(self.valeur))