from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from dice_widget import DiceWidget


class PlayerZone(QWidget):
    """Zone for a player with their dice"""

    def __init__(self, player):
        super().__init__()
        self.player = player

        # Vertical layout for this player
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Player name
        self.name_label = QLabel(f"{player.get_name()}")
        self.name_label.setStyleSheet("font-size: 14px; font-weight: bold;color: black")
        layout.addWidget(self.name_label)

        # Container for dice
        dice_container = QHBoxLayout()
        self.dice_widgets = []

        # Create dice widgets
        for dice in player.get_goblet().get_content():
            dice_widget = DiceWidget(dice.get_value(), dice.get_color())
            self.dice_widgets.append(dice_widget)
            dice_container.addWidget(dice_widget)

        layout.addLayout(dice_container)

        # Hide dice at start
        self.hide_dice()

        # Simple gray border
        self.setStyleSheet("background-color: #D3D3D3 ; padding: 10px;")

    def hide_dice(self):
        """Hide dice values"""
        for widget in self.dice_widgets:
            widget.set_value(0)

    def show_dice(self):
        """Show the real dice values"""
        dice_list = self.player.get_goblet().get_content()
        for i in range(len(dice_list)):
            self.dice_widgets[i].set_value(dice_list[i].get_value())