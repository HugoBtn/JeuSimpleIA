from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt


class ActionPanel(QFrame):
    """Action panel for a player (right side panel)"""

    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedWidth(280)

        # Default values
        self.nb = 1  # 1..30
        self.valeur = 1  # 1..6

        self._setup_ui()

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
        self._add_number_row(layout)

        layout.addSpacing(15)

        # Row: Value
        self._add_value_row(layout)

        layout.addStretch()

        # Bottom buttons
        self._add_buttons(layout)

        # Panel style
        self.setStyleSheet("""
            QFrame {
                border: 2px solid #95A5A6;
                border-radius: 12px;
                padding: 15px;
                background: #ECF0F1;
            }
            QPushButton {
                padding: 8px;
                font-weight: bold;
                font-size: 12px;
            }
        """)

    def _add_number_row(self, parent_layout):
        """Add the row for number"""
        row = QHBoxLayout()

        label = QLabel("Nombre :")
        label.setStyleSheet("color: #2C3E50; font-weight: bold; font-size: 14px;")

        btn_minus = QPushButton("-")
        btn_minus.setFixedWidth(40)
        btn_minus.clicked.connect(self._decrement_nb)

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
            padding: 5px;
        """)

        btn_plus = QPushButton("+")
        btn_plus.setFixedWidth(40)
        btn_plus.clicked.connect(self._increment_nb)

        row.addWidget(label)
        row.addWidget(btn_minus)
        row.addWidget(self.label_nb)
        row.addWidget(btn_plus)

        parent_layout.addLayout(row)

    def _add_value_row(self, parent_layout):
        """Add the row for value"""
        row = QHBoxLayout()

        label = QLabel("Valeur :")
        label.setStyleSheet("color: #2C3E50; font-weight: bold; font-size: 14px;")

        btn_minus = QPushButton("-")
        btn_minus.setFixedWidth(40)
        btn_minus.clicked.connect(self._decrement_valeur)

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
            padding: 5px;
        """)

        btn_plus = QPushButton("+")
        btn_plus.setFixedWidth(40)
        btn_plus.clicked.connect(self._increment_valeur)

        row.addWidget(label)
        row.addWidget(btn_minus)
        row.addWidget(self.label_valeur)
        row.addWidget(btn_plus)

        parent_layout.addLayout(row)

    def _add_buttons(self, parent_layout):
        """Add the bottom buttons"""
        row = QHBoxLayout()

        self.btn_dodo = QPushButton("DODO")
        self.btn_dodo.setStyleSheet("background-color: #E74C3C; color: white;")

        self.btn_valide = QPushButton("VALIDER")
        self.btn_valide.setStyleSheet("background-color: #27AE60; color: white;")

        row.addWidget(self.btn_dodo)
        row.addWidget(self.btn_valide)

        parent_layout.addLayout(row)

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
        """Change the title color based on player"""
        color_map = {
            "purple": "#9B59B6",
            "red": "#E74C3C",
            "blue": "#3498DB"
        }
        css_color = color_map.get(color, "#2C3E50")
        self.player_title.setStyleSheet(
            f"font-size: 20px; font-weight: bold; color: {css_color};"
        )

    def reset_values(self):
        """Reset values to 1"""
        self.nb = 1
        self.valeur = 1
        self.label_nb.setText(str(self.nb))
        self.label_valeur.setText(str(self.valeur))