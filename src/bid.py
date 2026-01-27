class Bid:
    def __init__(self, quantity, value):
        self.__quantity = quantity
        self.__value = value

    def get_quantity(self):
        return self.__quantity

    def get_value(self):
        return self.__value

    def is_valid_raise(self, previous_bid):
        """
        Valid = Increase quantity or same quantity but increase value
        """
        if previous_bid is None:
            return True

        previous_quantity = previous_bid.get_quantity()
        previous_value = previous_bid.get_value()

        if self.__quantity > previous_quantity:
            return True
        elif self.__quantity== previous_quantity and self.__value > previous_value:
            return True
        else:
            return False

    def __str__(self):
        return f"Bid(quantity={self.__quantity}, value={self.__value})"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    # Tests
    bid1 = Bid(3, 4)  # "3 dés de valeur 4"
    print(bid1)

    bid2 = Bid(4, 4)  # "4 dés de valeur 4" - valid raise
    print(f"{bid2} is valid raise over {bid1}? {bid2.is_valid_raise(bid1)}")

    bid3 = Bid(3, 5)  # "3 dés de valeur 5" - valid raise (same qty, higher value)
    print(f"{bid3} is valid raise over {bid1}? {bid3.is_valid_raise(bid1)}")

    bid4 = Bid(3, 3)  # "2 dés de valeur 6" - INVALID (lower quantity)
    print(f"{bid4} is valid raise over {bid1}? {bid4.is_valid_raise(bid1)}")