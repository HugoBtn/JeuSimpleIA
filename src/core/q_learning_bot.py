import random
import json
import os
from .bot_player import BotPlayer
from .bet import Bet

class QLearningBot(BotPlayer):
    """Q-learning based agent extending the base BotPlayer."""

    def __init__(self, name, color, q_table_file="brain.json", epsilon=0.0):
        # Initialize parent class (risk parameter unused but required)
        super().__init__(name, color, risk=0.5)

        self.q_table_file = q_table_file
        self.q_table = self.load_q_table()
        self.epsilon = epsilon
        self.alpha = 0.1
        self.gamma = 0.9

        self.last_state = None
        self.last_action = None

    def load_q_table(self):
        """Load Q-table from file if it exists."""
        if os.path.exists(self.q_table_file):
            try:
                with open(self.q_table_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_q_table(self):
        """Save Q-table to file."""
        with open(self.q_table_file, 'w') as f:
            json.dump(self.q_table, f)

    def _get_state(self):
        """Return a simplified representation of the current game state."""
        if not self.game:
            return "START"

        current_bet = self.game.get_current_bet()
        my_dice = self.get_goblet().get_content()
        my_values = [d.get_value() for d in my_dice]

        if current_bet is None:
            return "START"

        qty = current_bet.get_quantity()
        val = current_bet.get_value()

        if val == 1:
            matching = my_values.count(1)
        else:
            matching = my_values.count(val) + my_values.count(1)

        return f"MATCH:{matching}_QTY:{qty}_VAL:{val}"

    def get_possible_actions(self):
        """Return the list of legal actions in the current state."""
        actions = ["dodo", "tout_pile"]

        if not self.game:
            return actions

        current_bet = self.game.get_current_bet()

        if current_bet is None:
            return ["bet_1_2", "bet_1_3", "bet_1_4"]

        qty = current_bet.get_quantity()
        val = current_bet.get_value()

        total_dice = sum(
            len(p.get_goblet().get_content())
            for p in self.game.get_players()
        )

        if qty + 1 <= total_dice:
            actions.append(f"bet_{qty+1}_{val}")
        if val < 6:
            actions.append(f"bet_{qty}_{val+1}")

        return actions

    def make_bet(self, game=None):
        """
        Select and execute an action using an epsilon-greedy policy.
        """

        if game:
            self.attach_game(game)

        if not self.game:
            return

        state = self._get_state()
        actions = self.get_possible_actions()

        # Epsilon-greedy action selection
        if random.random() < self.epsilon:
            action = random.choice(actions)
        else:
            best_score = -float('inf')
            best_action = random.choice(actions)
            random.shuffle(actions)

            for a in actions:
                key = f"{state}|{a}"
                score = self.q_table.get(key, 0.0)
                if score > best_score:
                    best_score = score
                    best_action = a

            action = best_action

        self.last_state = state
        self.last_action = action

        if action == "dodo":
            self.bet = "dodo"
        elif action == "tout_pile":
            self.bet = "tout_pile"
        else:
            parts = action.split('_')
            self.bet = Bet(int(parts[1]), int(parts[2]))

    def learn(self, reward):
        """Update Q-value using a simple incremental update rule."""
        if not self.last_state or not self.last_action:
            return

        key = f"{self.last_state}|{self.last_action}"
        old_value = self.q_table.get(key, 0.0)
        new_value = old_value + self.alpha * (reward - old_value)

        self.q_table[key] = new_value