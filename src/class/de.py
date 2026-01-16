import random


class De:
    def __init__(self):
        self.__value = random.randint(1, 6)
    
    def get_value(self):
        return self.__value.copy()
    
    def lancer(self):
        self.__value = random.randint(1, 6)

    def __str__(self):
        return f"La valeur du dé est {str(self.__value)}"


if __name__ == "__main__":
    De1 = De()
    De2 = De()
    print(De1)
    print(De2)
    De1.lancer()
    print(De1)
    print(De2)
