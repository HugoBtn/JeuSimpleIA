# Perudo - Jeu de Dés

Implémentation du jeu de dés Perudo avec interface graphique PySide6 et joueurs IA.

## Description

Ce projet est une version numérique du jeu Perudo, incluant:
- Interface graphique développée avec PySide6
- Joueurs IA avec différents niveaux de difficulté
- Gestion complète des règles (Dodo, Tout Pile, mode Palepico)
- Système de paris avec validation automatique

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

Vérifier votre version de Python:
```bash
python --version
```

## Installation

### 1. Télécharger le projet

Téléchargez et extrayez le projet dans un dossier de votre choix.

### 2. Installer les dépendances

Ouvrez un terminal dans le dossier du projet et exécutez:

```bash
pip install -r requirements.txt
```

## Lancement du jeu

Dans le dossier du projet, exécutez:

```bash
python src/main.py
```

Le jeu s'ouvrira dans une fenêtre graphique.

## Règles du jeu

### Objectif
Être le dernier joueur avec des dés en main en réalisant des paris astucieux et en détectant les bluffs.

### Déroulement d'un Tour

1. **Lancer les dés** : Tous les joueurs lancent leurs dés secrètement
2. **Parier** : À tour de rôle, chaque joueur fait un pari sur le nombre total de dés d'une certaine valeur présents sur la table
3. **Surenchérir ou Contester** :
   - **Surenchérir** : Augmenter la quantité ou la valeur du pari
   - **Dodo** : Contester le pari précédent (dire que c'est faux)
   - **Tout Pile** : Parier que le pari précédent est exactement juste

### Règles Spéciales

#### Les Pacos (1)
- Les **1** sont des jokers et comptent pour toutes les valeurs (sauf en mode Palepico)

**Passer d'un pari normal vers un pari sur les Pacos :**
- Il faut au minimum la moitié (arrondie au supérieur) de la quantité précédente
- Exemple : après "5 × 4", on peut parier "3 × Paco" (car 5÷2 = 2.5, arrondi à 3)

**Passer d'un pari sur les Pacos vers un pari normal :**
- Il faut au minimum le double de Pacos + 1
- Exemple : après "3 × Paco", on peut parier "7 × 4" (car 3×2+1 = 7)

#### Mode Palepico
- S'active automatiquement quand un joueur n'a plus qu'**un seul dé**
- Les Pacos ne sont **plus des jokers**
- On ne peut parier que sur la **même valeur** en augmentant la quantité

#### Résolution des Contestations

<u>Dodo</u> :
- Si le nombre de dés est **inférieur** au pari → Le parieur **perd un dé**
- Si le nombre de dés est **égal ou supérieur** au pari → Le contestataire **perd un dé**

<u>Tout Pile</u>:
- Si le nombre de dés est **exactement** le pari → Le contestataire **gagne un dé** (max 6)
- Sinon → Le contestataire **perd un dé**

### Fin de Partie
Le dernier joueur ayant encore des dés remporte la partie !

## Structure du projet

```
src/
├── main.py                 # Point d'entrée du programme
|
├── bet.py                  # Gestion des paris
├── bot_player.py           # Classe joueur IA
├── dice.py                 # Classe dé
├── game.py                 # Logique principale du jeu
├── goblet.py               # Classe gobelet
├── player.py               # Classe joueur humain
|
├── game_window.py          # Interface graphique
├── action_panel.py         # Panneau d'actions (interface)
├── dice_widget.py          # Widget graphique pour les dés
├── player_zone.py          # Zone d'affichage des joueurs
|
└── graph.py                # Génération de graphiques statistiques
```

## Configuration

Vous pouvez modifier les joueurs dans le fichier `main.py`:

```python
def main():
    human = Player("Toi", "purple")
    bots = [
        BotPlayer("Bot Rouge", "red", risk=0.55),
        BotPlayer("Bot Bleu", "blue", risk=0.60),
    ]
    
    app = QApplication(sys.argv)
    window = GameWindow(players=[human] + bots, auto_start_rounds=False)
    window.show()
    sys.exit(app.exec())
```

Le paramètre `risk` des bots (entre 0.0 et 1.0) contrôle leur agressivité:
- 0.0-0.3: Bot prudent
- 0.4-0.6: Bot équilibré
- 0.7-1.0: Bot agressif

Couleurs disponibles: `"purple"`, `"red"`, `"blue"`, `"white"`

## Utilisation

1. Cliquez sur "Lancer le tour" pour commencer
2. Pour faire un pari:
   - Sélectionnez "Valeur"
   - Ajustez le Nombre et la Valeur avec les boutons +/-
   - Cliquez sur "Valider"
3. Pour contester:
   - "Dodo": le pari est trop haut
   - "Tout pile": le pari est exactement juste
4. Les dés se révèlent après chaque contestation