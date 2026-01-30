class Bet:
    def __init__(self, quantity, value):
        self.__quantity = quantity
        self.__value = value


    def get_quantity(self):
        return self.__quantity

    def get_value(self):
        return self.__value

    def is_valid_raise(self, previous_bet, palepico=False):
        """Valid = Increase quantity or same quantity but increase value"""
        # Check the value
        if self.__value < 1 or self.__value > 6:
            return False
        if self.__quantity < 1:
            return False

        # First bet
        if previous_bet is None:
            return True

        previous_quantity = previous_bet.get_quantity()
        previous_value = previous_bet.get_value()

        # PALEPICO MODE: Strict Rules
        # Only increase the quantity, not change the value
        if palepico:
            if self.__value != previous_value:
                return False
            if self.__quantity <= previous_quantity:
                return False
            return True

        # SPECIAL RULE: From normal to PACO
        # PACOs count as half
        if previous_value != 1 and self.__value == 1:
            # At least ceil(previous_quantity / 2)
            import math
            min_quantity = math.ceil(previous_quantity / 2.0)
            if self.__quantity >= min_quantity:
                return True
            else:
                return False

        # SPECIAL RULE: From PACO to normal
        # At least (quantity_pacos * 2) + 1
        if previous_value == 1 and self.__value != 1:
            min_quantity = previous_quantity * 2 + 1
            if self.__quantity >= min_quantity:
                return True
            else:
                return False

        # NORMAL RULES
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
    bid1 = Bet(3, 4)  # "3 dés de valeur 4"
    print(bid1)

    bid2 = Bet(4, 4)  # "4 dés de valeur 4" - valid raise
    print(f"{bid2} is valid raise over {bid1}? {bid2.is_valid_raise(bid1)}")

    bid3 = Bet(3, 5)  # "3 dés de valeur 5" - valid raise (same qty, higher value)
    print(f"{bid3} is valid raise over {bid1}? {bid3.is_valid_raise(bid1)}")

    bid4 = Bet(3, 3)  # "2 dés de valeur 6" - INVALID (lower quantity)
    print(f"{bid4} is valid raise over {bid1}? {bid4.is_valid_raise(bid1)}")