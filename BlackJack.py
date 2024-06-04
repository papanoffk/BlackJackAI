from Deck import Deck


class Hand():
    def __init__(self):
        self.cards = []
        self.ace = 0
        self.points = 0

    def add_card(self, card: str):
        self.cards.append(card)
        point = 0

        match card[0:2]:
            case '2-':
                point = 2
            case '3-':
                point = 3
            case '4-':
                point = 4
            case '5-':
                point = 5
            case '6-':
                point = 6
            case '7-':
                point = 7
            case '8-':
                point = 8
            case '9-':
                point = 9
            case '10':
                point = 10
            case 'j-':
                point = 10
            case 'q-':
                point = 10
            case 'k-':
                point = 10
            case 'a-':
                point = 11
                self.ace += 1

        self.points += point

    def my_points(self):
        if self.points <= 21:
            return self.points
        elif self.points == 22 and len(self.cards) == 2:
            return 21
        else:
            return self.points - 10 * self.ace

class BlackJack:
    def __init__(self, money):
        self.money = money
        self.deck = Deck()
        self.games = []

        self.dealer = Hand()
        self.players_hands = []

    def start(self, count_hand: int, bets):
        self.games.clear()
        self.players_hands.clear()
        self.deck.reload()
        self.deck.shaffle()

        def get_hand():
            hand = Hand()
            hand.add_card(self.deck.get_card())
            hand.add_card(self.deck.get_card())
            return hand

        self.dealer = get_hand()

        for i in range(count_hand):
            self.players_hands.append(get_hand())
            self.games.append(True)

        print(self.dealer.cards[0])
        for player in self.players_hands:
            print(player.cards[0], player.cards[1], player.my_points())

    def winner(self, index: int):
        player = self.players_hands[index].my_points()
        dealer = self.dealer.my_points()

        if player > dealer:
            return -1
        if player == dealer:
            return 0
        return 1


    def draw_turn(self, index: int):
        print('Draw!')
        if self.games[index]:
            self.players_hands[index].add_card(self.deck.get_card())

            if self.players_hands[index].my_points() >= 21:
                self.games[index] = False

            print('Your hand: ', self.players_hands[index].cards)
            print('Your points: ', self.players_hands[index].my_points())

    def pass_turn(self, index: int):
        self.games[index] = False

    def dealer_turn(self):
        if True in self.games:
            return False

        while (self.dealer.my_points() < 17):
            self.dealer.add_card(self.deck.get_card())

        print('Dealer hand:')
        print(self.dealer.cards, self.dealer.my_points())

        return True


    def end_game(self):
        result = [0 for i in range(len(self.players_hands))]

        for i in range(len(self.players_hands)):
            result[i] = self.winner(i)

        return result


if __name__ == '__main__':
    game = BlackJack(10)
    players = 1
    game.start(players, 10)
    while not game.dealer_turn():
        print('Выберете действие: ')
        print('1) Draw; 2) Pass.')
        menu = int(input())
        match menu:
            case 1:
                game.draw_turn(0)
            case 2:
                game.pass_turn(0)

    print(game.end_game())