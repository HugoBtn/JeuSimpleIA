class Table:
    def __init__(self, players):
        self.__players = players
        self.__current_idx = 0
    
    def get_current_player(self):
        return self.__players[self.__current_idx]
    
    def next_player(self):
        self.__current_idx = (self.__current_idx + 1) % len(self.__players)
        return self.get_current_player()
    
    def get_previous_player(self):
        return self.__players[(self.__current_idx - 1) % len(self.__players)]

    def remove_player(self, player):
        if player in self.__players:
            print(f"💀 {player} n'a plus de dés et est éliminé !")
            idx = self.__players.index(player)
            self.__players.remove(player)
            if idx <= self.__current_idx and self.__current_idx > 0:
                self.__current_idx -= 1

    def __len__(self):
        return len(self.__players)

    def __iter__(self):
        return iter(self.__players)