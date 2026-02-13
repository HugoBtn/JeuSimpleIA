import matplotlib.pyplot as plt
import sys
import time
import json
import os
import numpy as np # Si pas installé : pip install numpy

# Imports du projet
from core.game import Game
from core.q_learning_bot import QLearningBot
from core.bot_player import BotPlayer
from core.bet import Bet

def train(n_episodes=1000):
    print(f"--- 📊 Démarrage de l'entraînement analytique ({n_episodes} parties) ---")
    
    # --- MÉMOIRE PERSISTANTE ---
    global_q_table = {}
    if os.path.exists("brain.json"):
        try:
            with open("brain.json", "r") as f:
                global_q_table = json.load(f)
            print(f"   🧠 Cerveau chargé ({len(global_q_table)} états connus)")
        except:
            pass

    # --- STATISTIQUES ---
    history_win = []           # 1 si victoire, 0 si défaite
    history_illegal = []       # Nombre de coups illégaux par partie
    history_actions = {"dodo": [], "tout_pile": [], "bet": []} # % d'utilisation par partie
    
    current_epsilon = 0.9 
    
    for episode in range(n_episodes):
        # 1. Reset des joueurs
        learner = QLearningBot("Learner", "purple", epsilon=current_epsilon)
        learner.q_table = global_q_table 
        opponent = BotPlayer("Opponent", "red", risk=0.5)
        players = [learner, opponent]

        game = Game(players)
        opponent.attach_game(game)
        
        game.start_new_round()
        game_over = False
        
        # Stats de la partie en cours
        illegal_moves_count = 0
        actions_count = {"dodo": 0, "tout_pile": 0, "bet": 0}
        total_actions = 0
        
        while not game_over:
            # Sécurité boucle infinie
            if total_actions > 200: break

            current_player = players[game.get_current_player_index()]
            
            # Action
            if isinstance(current_player, QLearningBot):
                current_player.make_bet(game)
            else:
                current_player.make_bet()
                
            bet = current_player.bet

            # Suivi des stats d'action (seulement pour le Learner)
            if current_player == learner:
                total_actions += 1
                if bet == "dodo": actions_count["dodo"] += 1
                elif bet == "tout_pile": actions_count["tout_pile"] += 1
                else: actions_count["bet"] += 1

            # Résolution
            if bet == "dodo":
                res = game.resolve_dodo()
                if res["loser"] != learner: learner.learn(reward=10)
                else: learner.learn(reward=-10)
                game_over = res["game_over"]
                if not game_over: game.start_new_round()
                    
            elif bet == "tout_pile":
                res = game.resolve_tout_pile()
                if res["winner"] == learner: learner.learn(reward=20)
                elif res["loser"] == learner: learner.learn(reward=-10)
                else: learner.learn(reward=-1)
                game_over = res["game_over"]
                if not game_over: game.start_new_round()
                
            else:
                # Vérification validité
                valid = False
                try:
                    valid = bet.is_valid_raise(game.get_current_bet(), game.is_palepico_mode())
                except: valid = False

                if not valid:
                    # C'est un coup illégal !
                    if current_player == learner:
                        illegal_moves_count += 1
                        learner.learn(reward=-50) # Grosse punition
                        # On force un dodo pour avancer
                        res = game.resolve_dodo()
                        game_over = res["game_over"]
                        if not game_over: game.start_new_round()
                    else:
                        # L'adversaire bug ? On passe.
                        res = game.resolve_dodo()
                        game_over = res["game_over"]
                        if not game_over: game.start_new_round()
                else:
                    game.set_current_bet(bet)
                    game.next_betting_player()

        # --- FIN DE PARTIE ---
        
        # 1. Victoire ou Défaite
        if learner.get_goblet_length() > 0:
            learner.learn(reward=50)
            history_win.append(1)
        else:
            learner.learn(reward=-20)
            history_win.append(0)
            
        # 2. Stats Illégales
        history_illegal.append(illegal_moves_count)
        
        # 3. Stats Actions (en pourcentage)
        if total_actions > 0:
            history_actions["dodo"].append(actions_count["dodo"] / total_actions)
            history_actions["tout_pile"].append(actions_count["tout_pile"] / total_actions)
            history_actions["bet"].append(actions_count["bet"] / total_actions)
        else:
            history_actions["dodo"].append(0)
            history_actions["tout_pile"].append(0)
            history_actions["bet"].append(0)

        # Maintenance IA
        global_q_table = learner.q_table
        current_epsilon = max(0.05, learner.epsilon * 0.995)

        if episode % 100 == 0:
            win_rate_100 = sum(history_win[-100:]) if len(history_win) >= 100 else 0
            print(f"Partie {episode} | WinRate(100): {win_rate_100}% | Illégal: {illegal_moves_count} | Eps: {current_epsilon:.2f}")

    # Sauvegarde
    learner.save_q_table()
    print("✅ Entraînement terminé !")
    
    # --- AFFICHAGE GRAPHIQUE ---
    plot_statistics(history_win, history_illegal, history_actions, n_episodes)

def plot_statistics(wins, illegals, actions, n_episodes):
    """Génère un tableau de bord complet avec Matplotlib"""
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    
    # Fenêtre glissante pour lisser les courbes (Moyenne sur 50 parties)
    window_size = 50
    def moving_average(data):
        return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

    x_axis = range(window_size - 1, len(wins))

    # Graphique 1 : Taux de Victoire (Rolling Average)
    ax1.plot(x_axis, moving_average(wins) * 100, color='green', label='Taux de victoire')
    ax1.set_ylabel('Victoires (%)')
    ax1.set_title(f'Performance de l\'IA (Moyenne glissante {window_size} parties)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # Graphique 2 : Coups Illégaux
    ax2.plot(x_axis, moving_average(illegals), color='red', label='Coups Illégaux / Partie')
    ax2.set_ylabel('Nombre d\'erreurs')
    ax2.set_title('Apprentissage des règles (Erreurs)')
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    # Graphique 3 : Style de Jeu (Distribution des actions)
    ax3.stackplot(x_axis, 
                  moving_average(actions["bet"]), 
                  moving_average(actions["dodo"]), 
                  moving_average(actions["tout_pile"]),
                  labels=['Parier', 'Dodo', 'Tout Pile'],
                  colors=['#3498db', '#e74c3c', '#f1c40f'], alpha=0.7)
    ax3.set_ylabel('Distribution des Actions')
    ax3.set_xlabel('Nombre de parties')
    ax3.set_title('Évolution du Style de Jeu')
    ax3.legend(loc='upper left')
    ax3.margins(0, 0)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    train(5000)