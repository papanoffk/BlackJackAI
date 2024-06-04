from random import shuffle

class Deck:
    def __init__(self):
        self.__deck = []

        self.reload()
        self.shaffle()

    def get_card(self):
        return self.__deck.pop()

    def shaffle(self):
        shuffle(self.__deck)

    def reload(self):
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a']  # ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a']
        suits = ['crosses', 'hearts', 'diamonds', 'spades']

        for value in values:
            for suit in suits:
                self.__deck.append(value + '-' + suit)



if __name__ == '__main__':
    deck = Deck()
    print(deck.get_card())