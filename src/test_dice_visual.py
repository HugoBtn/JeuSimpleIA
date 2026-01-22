from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from dice_widget import DiceWidget
from dice import Dice
import sys


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dice Test")
        self.resize(300, 250)

        # Central widget
        widget = QWidget()
        self.setCentralWidget(widget)

        # Layout
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Title
        layout.addWidget(QLabel("Test the dice"))

        # Create a dice (model)
        self.dice = Dice("purple")

        # Create the visual dice (view)
        self.dice_widget = DiceWidget(self.dice.get_value(), "purple")
        layout.addWidget(self.dice_widget)

        # Button to roll
        button = QPushButton("Roll the dice")
        button.clicked.connect(self.roll)
        layout.addWidget(button)

        layout.addStretch()

    def roll(self):
        """Roll the dice and update display"""
        self.dice.roll()
        self.dice_widget.set_value(self.dice.get_value())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())