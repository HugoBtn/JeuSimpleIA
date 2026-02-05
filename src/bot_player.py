import random
from typing import Optional, Tuple, Union
from player import Player
from bet import Bet as BetObject

Bet = Union[str, Tuple[int, int]]

class BotPlayer(Player):

    def __init__(self, name: str, color: str, risk: float = 0.55):
        super().__init__(name, color)
        self.game = None
        # Le risque définit le tempérament (prudent vs hardi)
        self.risk = max(0.0, min(1.0, risk))

    def attach_game(self, game):
        """ Connects the bot to the current game instance"""
        self.game = game

    def _get_current_bet(self):
        """Access the current bet"""
        return self.game.get_current_bet() if self.game else None

    def _get_my_dice_values(self):
        """Return the actual values of the dice in the bot's cup"""
        return [d.get_value() for d in self.get_goblet().get_content()]

    def _estimate_total(self, value: int) -> float:
        """
        Calculates the expected value (probable mean).
        Adds a slight blur to humanize the decisions
        """
        total_dice = sum(p.get_goblet_length() for p in self.game.get_players())
        my_dice = self._get_my_dice_values()
        
        # Joker management (Paco)
        is_joker_active = not self.palepico()
        
        if is_joker_active and value != 1:
            my_count = sum(1 for v in my_dice if v == value or v == 1)
            prob = 1/3 # Value + Joker
        else:
            my_count = sum(1 for v in my_dice if v == value)
            prob = 1/6

        unknown_dice = total_dice - len(my_dice)
        exact_expected = my_count + (unknown_dice * prob)

        # We add a small error in judgment (-0.75 to +0.75 dice)
        error_margin = random.uniform(-0.75, 0.75)
        return exact_expected + error_margin

    def make_bet(self):
        """Primary decision method (AI)"""
        if not self.game: return

        curr_bet = self._get_current_bet()
        
        # Case 1: The bot starts the turn
        if curr_bet is None:
            # Betting on the best value
            my_vals = self._get_my_dice_values()
            best_val = max(set(my_vals), key=my_vals.count)
            self.bet = BetObject(1, best_val)
            return

        # Case 2: Analyzing the opponent's bid
        target_amt, target_val = curr_bet.get_quantity(), curr_bet.get_value()
        expected = self._estimate_total(target_val)
        
        # Calculating the reporting threshold based on risk
        limit = -0.15 + (0.35 * (1.0 - self.risk))

        if (expected - target_amt) < limit:
            self.bet = "dodo"
        else:
            # Trying to outbid each other
            self.bet = self._find_best_raise()

    def _find_best_raise(self):
        """Look for a higher bid among the best likely options"""
        all_bets = []
        total_dice = sum(p.get_goblet_length() for p in self.game.get_players())
        current_bet = self._get_current_bet()
        palepico = self.game.is_palepico_mode() if self.game else False
        
        for amt in range(1, total_dice + 1):
            for val in range(1, 7):
                candidate = BetObject(amt, val)
                if candidate.is_valid_raise(current_bet, palepico=palepico):
                    # The bid is noted: the more the estimate exceeds the bid, the better the score
                    score = self._estimate_total(val) - amt
                    all_bets.append((score, candidate))

        # Sorting of auctions from safest to riskiest
        all_bets.sort(key=lambda x: x[0], reverse=True)
        
        # We choose from the Top 10 so as not to be too perfect
        top_k = min(10, len(all_bets))
        if top_k <= 0:
            return "dodo"
        chosen = random.choice(all_bets[:top_k])
        return chosen[1]