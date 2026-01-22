from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QBrush
from PySide6.QtCore import Qt


class DiceWidget(QWidget):
    """Widget that draws a dice"""

    def __init__(self, dice_value=1, color="white"):
        super().__init__()
        self.dice_value = dice_value
        self.dice_color = color
        self.setFixedSize(60, 60)  # Fixed size for the dice

    def set_value(self, value):
        """Change the dice value and redraw"""
        self.dice_value = value
        self.update() # Qt will call paintEvent

    def paintEvent(self, event):
        """Draws the dice"""
        painter = QPainter(self)

        # Draw the square
        painter.setPen(QPen(Qt.black, 2))

        # Background color
        colors = {
            "white": QColor(255, 255, 255),
            "purple": QColor(147, 112, 219),
            "red": QColor(220, 100, 100),
            "blue": QColor(100, 150, 220),
        }
        painter.setBrush(QBrush(colors.get(self.dice_color, QColor(255, 255, 255))))
        painter.drawRoundedRect(5, 5, 50, 50, 5, 5)

        # Draw dots
        painter.setBrush(QBrush(Qt.black))
        self.draw_dots(painter)

    def draw_dots(self, painter):
        """Draw dots based on dice value"""
        size = 8

        # Dot positions
        tl = (15, 15)  # top left
        tr = (45, 15)  # top right
        ml = (15, 30)  # middle left
        c = (30, 30)  # center
        mr = (45, 30)  # middle right
        bl = (15, 45)  # bottom left
        br = (45, 45)  # bottom right

        # Function to draw a dot
        def dot(pos):
            painter.drawEllipse(pos[0] - size // 2, pos[1] - size // 2, size, size)

        if self.dice_value == 1:
            dot(c)
        elif self.dice_value == 2:
            dot(tl)
            dot(br)
        elif self.dice_value == 3:
            dot(tl)
            dot(c)
            dot(br)
        elif self.dice_value == 4:
            dot(tl)
            dot(tr)
            dot(bl)
            dot(br)
        elif self.dice_value == 5:
            dot(tl)
            dot(tr)
            dot(c)
            dot(bl)
            dot(br)
        elif self.dice_value == 6:
            dot(tl)
            dot(tr)
            dot(ml)
            dot(mr)
            dot(bl)
            dot(br)