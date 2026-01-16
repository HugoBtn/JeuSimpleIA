from goblet import Goblet
from dice import Dice

def main():
    goblet = Goblet("blue", 5)
    dice1 = Dice("red")
    dice2 = Dice("green")
    
    goblet.add_dice(dice1)
    goblet.add_dice(dice2)
    
    print(goblet)

if __name__ == "__main__":
    main()