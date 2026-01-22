from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
import sys

class FirstWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Title of the window
        self.setWindowTitle("Perudo")

        # Size of the window
        self.resize(400,300)

        # Create a central widget
        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        # Create a layout
        layout = QVBoxLayout()
        widget_central.setLayout(layout)

        # Add a text
        texte = QLabel("Welcome to Perudo")
        layout.addWidget(texte)

        # Add a button
        bouton = QPushButton("Click me")
        bouton.clicked.connect(self.when_we_click) # we connect the button to a method
        layout.addWidget(bouton)

    def when_we_click(self):
        "Function that is executed when the button is clicked"
        print("You clicked")


# Entry point of the program
if __name__ == "__main__":
    # Create the application
    app = QApplication(sys.argv)

    #  Create the window
    fenetre = FirstWindow()

    # Show the window
    fenetre.show()

    # Launch the application (infinite loop until closed)
    sys.exit(app.exec())