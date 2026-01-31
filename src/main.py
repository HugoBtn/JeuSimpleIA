from player import Player

def main():
    player = Player("Alice", "purple")

    print("Before playing:")
    print(player)

    # Player plays (shakes the goblet)
    player.play()

    print("After playing:")
    print(player)

if __name__ == "__main__":
    main()