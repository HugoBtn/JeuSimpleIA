from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
import sys

class PremiereFenetre(QMainWindow):
    def __init__(self):
        super().__init__()

        # Titre de la fenêtre
        self.setWindowTitle("Perudo")

        # Taille de la fenêtre
        self.resize(400,300)

        # Crée un widget central
        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        # Crée un layout
        layout = QVBoxLayout()
        widget_central.setLayout(layout)

        # Ajoute un texte
        texte = QLabel("Bienvenue dans Perudo")
        layout.addWidget(texte)

        # Ajoute un bouton
        bouton = QPushButton("Cliquez-moi")
        bouton.clicked.connect(self.quand_on_clique) # on connecte le bouton à une méthode
        layout.addWidget(bouton)

    def quand_on_clique(self):
        "Fonction qui s'exécute quand on clique le bouton"
        print("Vous avez cliqué")


# Point d'entrée dy programme
if __name__ == "__main__":
    # Créer l'application
    app = QApplication(sys.argv)

    # Créer la fenêtre
    fenetre = PremiereFenetre()

    # Afficher la fenêtre
    fenetre.show()

    # Lancer l'application (boucle infinie jusqu'à fermeture)
    sys.exit(app.exec())