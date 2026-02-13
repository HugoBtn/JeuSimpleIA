import random
from typing import Optional, Tuple, Union
from .player import Player
from .bet import Bet as BetObject

Bet = Union[str, Tuple[int, int]]


class BotPlayer(Player):
    """Rule-based AI player with adjustable risk behavior."""

    def __init__(self, name: str, color: str, risk: float = 0.55):
        super().__init__(name, color)
        self.game = None

        # Risk parameter controls aggressiveness (0 = cautious, 1 = aggressive)
        self.risk = max(0.0, min(1.0, risk))

    def attach_game(self, game):
        """Attach the bot to the current game instance."""
        self.game = game

    def _get_current_bet(self):
        """Return the current bet on the table."""
        return self.game.get_current_bet() if self.game else None

    def _get_my_dice_values(self):
        """Return the dice values currently held by the bot."""
        return [d.get_value() for d in self.get_goblet().get_content()]

    def _estimate_total(self, value: int) -> float:
        """
        Estimate the expected total number of dice matching a value.
        A small random variation is added to avoid deterministic behavior.
        """
        total_dice = sum(p.get_goblet_length() for p in self.game.get_players())
        my_dice = self._get_my_dice_values()

        is_joker_active = not self.palepico()

        if is_joker_active and value != 1:
            my_count = sum(1 for v in my_dice if v == value or v == 1)
            prob = 1 / 3
        else:
            my_count = sum(1 for v in my_dice if v == value)
            prob = 1 / 6

        unknown_dice = total_dice - len(my_dice)
        expected = my_count + (unknown_dice * prob)

        # Add slight randomness to simulate imperfect reasoning
        return expected + random.uniform(-0.75, 0.75)

    def make_bet(self):
        """Main decision method executed during the bot's turn."""
        if not self.game:
            return

        curr_bet = self._get_current_bet()

        # First bet of the round
        if curr_bet is None:
            my_vals = self._get_my_dice_values()
            best_val = max(set(my_vals), key=my_vals.count)
            self.bet = BetObject(1, best_val)
            return

        target_amt = curr_bet.get_quantity()
        target_val = curr_bet.get_value()

        expected = self._estimate_total(target_val)

        # Threshold adjusted by risk parameter
        limit = -0.15 + (0.35 * (1.0 - self.risk))

        if (expected - target_amt) < limit:
            self.bet = "dodo"
        else:
            self.bet = self._find_best_raise()

    def _find_best_raise(self):
        """Select a valid raise among the most promising options."""
        all_bets = []

        total_dice = sum(p.get_goblet_length() for p in self.game.get_players())
        current_bet = self._get_current_bet()
        palepico = self.game.is_palepico_mode() if self.game else False

        for amt in range(1, total_dice + 1):
            for val in range(1, 7):
                candidate = BetObject(amt, val)
                if candidate.is_valid_raise(current_bet, palepico=palepico):
                    score = self._estimate_total(val) - amt
                    all_bets.append((score, candidate))

        all_bets.sort(key=lambda x: x[0], reverse=True)

        if not all_bets:
            return "dodo"

        # Select among top candidates to avoid deterministic play
        top_k = min(10, len(all_bets))
        return random.choice(all_bets[:top_k])[1]