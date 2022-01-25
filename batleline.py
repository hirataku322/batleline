import numpy as np
from random import shuffle


class Card:
    def __init__(self, color, number):
        self.color = color
        self.number = number

    def __lt__(self, c2):
        return self.number < c2.number

    def __gt__(self, c2):
        return self.number > c2.number

    def __str__(self):
        return self.color + f"{self.number:02}"


class Deck:
    COLORS = ['B', 'G', 'O', 'P', 'R', 'Y']
    NUMBERS = [i for i in range(1, 11)]

    def __init__(self):
        self.cards = []
        for color in self.COLORS:
            for number in self.NUMBERS:
                self.cards.append(Card(color, number))
        shuffle(self.cards)

    def draw_card(self):
        if len(self.cards) == 0:
            raise Exception("Deck is empty.")
        return self.cards.pop()

    def draw_cards(self, n):
        if n > len(self.cards):
            raise Exception(
                "You can draw less than the number of cards in the deck.")
        return [self.draw_card() for _ in range(n)]


class Line:
    def __init__(self):
        self.formations = (Formation(), Formation())
        self.flag = None

    def add(self, turn, card):
        f = self.formations[turn % 2]
        f.add(card)

    def attempt(self, turn):
        f1 = self.formations[turn % 2]
        f2 = self.formations[(turn + 1) % 2]
        return f1 > f2

    def draw(self):
        pass

    def __str__(self):
        f1, f2 = self.formations[:]
        return str(f1) + " F " + str(f2)


class Formation:
    FORMATION_POWER = {"Wedge": 4, "Batalion": 3,
                       "Phalanx": 2, "Scarmisher": 1, "Host": 0}

    def __init__(self):
        self.cards = []
        self.colors = []
        self.numbers = []
        self.formation = ""
        self.sum_num = 0

    def add(self, card):
        if len(self.cards) == 3:
            raise Exception(
                "The number of card is limited to a maximum of 3.")
        else:
            self.cards.append(card)
            self.colors.append(card.color)
            self.numbers.append(card.number)
            self.numbers.sort()
            if len(self.cards) == 3:
                self.formation = self.__eval_formation()
                self.sum_num = sum(self.numbers)

    def __is_same_color(self):
        return (len(set(self.colors)) == 1)

    def __is_same_number(self):
        return (len(set(self.numbers)) == 1)

    def __is_serial_number(self):
        return (set(np.diff(self.numbers, 1)) == 1)

    def __eval_formation(self):
        is_same_color = self.__is_same_color()
        is_same_number = self.__is_same_number()
        is_serial_number = self.__is_serial_number()

        if is_same_color:
            return "Wedge" if is_serial_number else "Batalion"
        elif is_same_number:
            return "Phalanx"
        elif is_serial_number:
            return "Scarmisher"
        else:
            return "Host"

    def __lt__(self, f2):
        if self.formation == f2.formation:
            return self.sum_num < f2.sum_num
        else:
            return self.FORMATION_POWER[self.formation] < f2.FORMATION_POWER[f2.formation]

    def __gt__(self, f2):
        if self.formation == f2.formation:
            return self.sum_num > f2.sum_num
        else:
            return self.FORMATION_POWER[self.formation] > f2.FORMATION_POWER[f2.formation]

    def __str__(self):
        return " ".join([str(card) for card in self.cards])


class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)
        self.cards.sort(key=lambda card: card.number)

    def add_cards(self, cards):
        for card in cards:
            self.add_card(card)

    def play_card(self, card_str):
        for i, card in enumerate(self.cards):
            if str(card) == card_str:
                return self.cards.pop(i)
        raise Exception(f"Not found {card_str}. {self.__str__()}")

    def __str__(self):
        return f"name: {self.name}\n" + "cards: " + " ".join([str(card) for card in self.cards])


class Game:
    def __init__(self):
        name1 = input("p1 name: ")
        name2 = input("p2 name: ")
        self.deck = Deck()
        self.line = Line()
        self.players = [Player(name1), Player(name2)]

    def wins(self, winner):
        print(f"{winner.name} wins the round!")

    def draw(self):
        print("draw")

    def play_game(self):
        for p in self.players:
            initial_cards = self.deck.draw_cards(7)
            p.add_cards(initial_cards)

        turn = 0
        while(1):
            p = self.players[turn % 2]
            o = self.players[(turn + 1) % 2]

            # print Line
            print(self.line)

            # print players cards
            print(p)

            # submit a card
            card_str = input("choise -> ")
            # TODO: 誤ったカードを選択した際にもう一度選択させる
            card = p.play_card(card_str)
            self.line.add(turn, card)

            # draw a card
            p.add_card(self.deck.draw_card())

            # end game
            if turn == 5:
                winner = p if self.line.attempt(turn) else o
                self.wins(winner)
                break

            # update
            turn += 1
            print()


if __name__ == "__main__":
    game = Game()
    game.play_game()
