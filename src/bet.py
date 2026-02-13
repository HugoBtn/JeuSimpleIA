class Bet:
    """Represents a bet in the Perudo game"""

#Constructor
    def __init__(self, quantity, value):
        self.__quantity = quantity
        self.__value = value

# Getters
    def get_quantity(self):
        """Return the number of dice in the bet"""
        return self.__quantity

    def get_value(self):
        """Return the dice value of the bet"""
        return self.__value

# Validation
    def is_valid_raise(self, previous_bet, palepico=False):
        """Check if this bet is valid compared to the previous one"""

        # Number validation
        if self.__value < 1 or self.__value > 6:
            return False
        if self.__quantity < 1:
            return False

        # First bet of the round
        if previous_bet is None:
            return True

        previous_quantity = previous_bet.get_quantity()
        previous_value = previous_bet.get_value()

        # Palepico mode : same value, higher quantity
        if palepico:
            if self.__value != previous_value:
                return False
            if self.__quantity <= previous_quantity:
                return False
            return True

        # Normal -> Paco
        if previous_value != 1 and self.__value == 1:
            # At least ceil(previous_quantity / 2)
            import math
            min_quantity = math.ceil(previous_quantity / 2.0)
            if self.__quantity >= min_quantity:
                return True
            else:
                return False

        # Paco -> Normal
        if previous_value == 1 and self.__value != 1:
            # At least (quantity_pacos * 2) + 1
            min_quantity = previous_quantity * 2 + 1
            if self.__quantity >= min_quantity:
                return True
            else:
                return False

        # Standard Rules
            # Increase the quantity
        if self.__quantity > previous_quantity:
            return True

            # Same quantity but increase the value
        if self.__quantity == previous_quantity and self.__value > previous_value:
            return True

            # Invalid bet
        return False

    def __str__(self):
        return f"Bid({self.__quantity}, {self.__value})"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    # Tests
    bid1 = Bet(3, 4)  # "3 dice of value 4"
    print(bid1)

    bid2 = Bet(4, 4)  # "4 dice of value 4" - valid raise
    print(f"{bid2} is valid raise over {bid1}? {bid2.is_valid_raise(bid1)}")

    bid3 = Bet(3, 5)  # "3 dice of value 5" - valid raise (same qty, higher value)
    print(f"{bid3} is valid raise over {bid1}? {bid3.is_valid_raise(bid1)}")

    bid4 = Bet(3, 3)  # "2 dice of value 6" - INVALID (lower quantity)
    print(f"{bid4} is valid raise over {bid1}? {bid4.is_valid_raise(bid1)}")