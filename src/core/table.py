class Table:
    """Manage player order and turn rotation."""

    def __init__(self, players):
        self.__players = players
        self.__current_idx = 0

    def get_current_player(self):
        """Return the player whose turn it is."""
        return self.__players[self.__current_idx]

    def next_player(self):
        """Advance to the next player in circular order."""
        self.__current_idx = (self.__current_idx + 1) % len(self.__players)
        return self.get_current_player()

    def get_previous_player(self):
        """Return the previous player in circular order."""
        return self.__players[(self.__current_idx - 1) % len(self.__players)]

    def remove_player(self, player):
        """Remove a player from the table and adjust turn index if necessary."""
        if player in self.__players:
            print(f"{player} has no dice left and is eliminated.")
            idx = self.__players.index(player)
            self.__players.remove(player)

            if idx <= self.__current_idx and self.__current_idx > 0:
                self.__current_idx -= 1

    def __len__(self):
        """Return the number of remaining players."""
        return len(self.__players)

    def __iter__(self):
        """Allow iteration over players."""
        return iter(self.__players)
