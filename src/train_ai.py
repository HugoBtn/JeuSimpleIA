import matplotlib.pyplot as plt
import sys
import time
import json
import os

# Assure-toi d'avoir ces imports corrects
from game import Game
from q_learning_bot import QLearningBot
from bot_player import BotPlayer
from bet import Bet

def train(n_episodes=1000):
    print(f"--- Démarrage de l'entraînement ({n_episodes} parties) ---")
    
    # 1. Variables persistantes (Mémoire de l'IA)
    # On stocke le cerveau ici pour le passer au nouveau corps à chaque partie
    global_q_table = {}
    if os.path.exists("brain.json"):
        try:
            with open("brain.json", "r") as f:
                global_q_table = json.load(f)
        except:
            pass

    current_epsilon = 0.9 # On commence curieux
    history = []
    wins = 0
    
    MAX_ACTIONS_PER_GAME = 200
    
    for episode in range(n_episodes):
        # === CORRECTION ICI ===
        # On recrée les joueurs à NEUF pour qu'ils aient 5 dés chacun
        learner = QLearningBot("Learner", "purple", epsilon=current_epsilon)
        learner.q_table = global_q_table # On lui injecte la mémoire accumulée
        
        opponent = BotPlayer("Opponent", "red", risk=0.5)
        
        players = [learner, opponent]
        # ======================

        if episode % 100 == 0:
            print(f"\n=== PARTIE {episode} (Epsilon: {current_epsilon:.2f}) ===")

        game = Game(players)
        opponent.attach_game(game) # Important pour le BotPlayer
        
        game.start_new_round()
        game_over = False
        actions_count = 0
        
        while not game_over:
            actions_count += 1
            if actions_count > MAX_ACTIONS_PER_GAME:
                # print("!!! ALERTE : BOUCLE INFINIE - Arrêt forcé !!!")
                break

            current_player = players[game.get_current_player_index()]
            
            # Debug léger pour voir si ça tourne
            # print(f"[Act:{actions_count}] {current_player.get_name()}")

            if isinstance(current_player, QLearningBot):
                current_player.make_bet(game)
            else:
                current_player.make_bet()
                
            bet = current_player.bet

            # --- RÉSOLUTION ---
            if bet == "dodo":
                res = game.resolve_dodo()
                
                # Récompenses
                if res["loser"] != learner:
                    learner.learn(reward=10)
                else:
                    learner.learn(reward=-10)
                
                game_over = res["game_over"]
                if not game_over: game.start_new_round()
                    
            elif bet == "tout_pile":
                res = game.resolve_tout_pile()

                if res["winner"] == learner:
                    learner.learn(reward=20)
                elif res["loser"] == learner:
                    learner.learn(reward=-10)
                else:
                    learner.learn(reward=0)
                    
                game_over = res["game_over"]
                if not game_over: game.start_new_round()
                
            else:
                # Vérification validité
                valid = False
                try:
                    valid = bet.is_valid_raise(game.get_current_bet(), game.is_palepico_mode())
                except:
                    valid = False

                if not valid:
                    # Si invalide, on force la fin du tour pour éviter le blocage
                    if current_player == learner:
                        learner.learn(reward=-50) # Punition
                        # On force un Dodo pour débloquer la situation
                        res = game.resolve_dodo() 
                        game_over = res["game_over"]
                        if not game_over: game.start_new_round()
                    else:
                        # Si c'est l'adversaire qui bug, on force aussi
                        res = game.resolve_dodo()
                        game_over = res["game_over"]
                        if not game_over: game.start_new_round()
                else:
                    game.set_current_bet(bet)
                    game.next_betting_player()

        # Fin de partie
        if learner.get_goblet_length() > 0:
            wins += 1
            learner.learn(reward=50) # Grosse récompense de victoire
        else:
            learner.learn(reward=-20)

        # Mise à jour des variables persistantes pour le prochain tour de boucle
        global_q_table = learner.q_table
        current_epsilon = max(0.05, learner.epsilon * 0.995)
        
        history.append(wins / (episode + 1))
        
        # Sauvegarde disque de temps en temps
        if episode % 50 == 0:
            learner.save_q_table()

    # Sauvegarde finale
    learner.save_q_table()
    print("✅ Entraînement terminé !")
    
    plt.plot(history)
    plt.title("Taux de victoire du Learner")
    plt.show()

if __name__ == "__main__":
    train(10000)