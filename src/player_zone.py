from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from dice_widget import DiceWidget


class PlayerZone(QWidget):
    """Zone for a player with their dice"""

# Constructor
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.dice_widgets = []

        self._setup_ui()
        self.setStyleSheet("background-color: #D3D3D3; padding: 10px;")

    def _setup_ui(self):
        """Build the player zone UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Player name
        self.name_label = QLabel(f"{self.player.get_name()}")
        self.name_label.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: white; "
            "background-color: #212F3C; padding: 5px;"
        )
        layout.addWidget(self.name_label)

        # Container for dice
        self.dice_container = QHBoxLayout()
        layout.addLayout(self.dice_container)

        # Create initial dice widgets
        self._create_dice_widgets()

        # Hide dice at start
        self.hide_dice()

# Dice management
    def _create_dice_widgets(self):
        """Create dice widgets based on current player goblet"""
        # Clear existing widgets
        for widget in self.dice_widgets:
            widget.deleteLater()
        self.dice_widgets.clear()

        # Create new widgets
        for dice in self.player.get_goblet().get_content():
            dice_widget = DiceWidget(dice.get_value(), dice.get_color())
            self.dice_widgets.append(dice_widget)
            self.dice_container.addWidget(dice_widget)

    def update_dice_count(self):
        """Update dice widgets when player loses dice"""
        current_dice = self.player.get_goblet().get_content()

        # If dice count changed, recreate widgets
        if len(current_dice) != len(self.dice_widgets):
            self._create_dice_widgets()

        # Update values
        self.show_dice()

# Visibility
    def hide_dice(self):
        """Hide dice values (show as blank)"""
        for widget in self.dice_widgets:
            widget.set_value(0)

    def show_dice(self):
        """Show the real dice values"""
        dice_list = self.player.get_goblet().get_content()
        for i, dice in enumerate(dice_list):
            if i < len(self.dice_widgets):
                self.dice_widgets[i].set_value(dice.get_value())
