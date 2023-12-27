import random
from constants import *


class Deck: 
    #Default ctor to create a deck object
    def __init__(self):
        self.cards = []
        self.build()

    #Create the full 52 card deck
    def build(self):
        for value in RANKS:
            for suit in SUITS:
                self.cards.append((value, suit))

    #Use the random package to shuffle the deck
    def shuffle(self):
        random.shuffle(self.cards)

    #Deal one card
    #return the last element in the deck
    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop()
        

#Hand class that inherits from the Deck class
class Hand(Deck):
    #Default ctor for the player and dealer hands
    def __init__(self):
        self.cards = []
        self.card_img = []
        self.value = 0

    #Add card to the hand
    def add_card(self, card):
        self.cards.append(card)

    #Calculate the value of the hand
    def calc_hand(self):
        self.value = 0
        first_card_rank = [card[0] for card in self.cards]
        non_aces = [card for card in first_card_rank if card != 'A']
        aces = [card for card in first_card_rank if card == 'A']

        for card in non_aces:
            if card in 'JQK':
                self.value += 10
            else:
                self.value += int(card)

        for card in aces:
            if self.value <= 10:
                self.value += 11
            else:
                self.value += 1

    #Display cards in the hand
    def display_cards(self):
        for card in self.cards:
            cards = "".join((card[0], card[1]))
            if cards not in self.card_img:
                self.card_img.append(cards)
