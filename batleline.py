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

    def __repr__(self):
        return self.color + f"{self.number:02}"


class Deck:
    COLORS = ["red", "blue", "green", "yellow", "purplue", "orange"]
    NUMBERS = [i for i in range(11)]

    def __init__(self):
        self.cards = []
        for color in self.COLORS:
            for number in self.NUMBERS:
                self.cards.append(Card(color, number))
        shuffle(self.cards)

    def draw_card(self):
        if len(self.cards) == 0:
            raise Exception("You cannot draw card. Deck is empty.")
        return self.cards.pop()


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
                "You can't add card. The number of card is limited to a maximum of 3.")
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


class Player:
    def __init__(self, name):
        self.card = None
        self.name = name
