from collections import Counter
from enum import Enum


class PokerTypes(Enum):
    FIVE_OF_KIND = 7
    FOUR_OF_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

    @staticmethod
    def of(cards: str) -> 'PokerTypes':
        counter = Counter(cards)
        different_cards = len(counter.keys())
        same_cards = max(counter.values())
        if different_cards == 1:
            return PokerTypes.FIVE_OF_KIND
        if different_cards == 2:
            if same_cards == 4:
                return PokerTypes.FOUR_OF_KIND
            return PokerTypes.FULL_HOUSE
        if same_cards == 3:
            return PokerTypes.THREE_OF_KIND
        if same_cards == 2:
            cnt_of_pairs = Counter(counter.values())
            if cnt_of_pairs[2] == 2:
                return PokerTypes.TWO_PAIR
            return PokerTypes.ONE_PAIR
        return PokerTypes.HIGH_CARD

    @staticmethod
    def of_joker(cards:str) -> 'PokerTypes':
        counter = Counter(cards)
        if 'J' not in counter: return PokerTypes.of(cards)
        jokers = counter['J']
        counter['J'] = 0
        same_kind_max = max(counter.values())
        items = list(filter(lambda item: item[1] == same_kind_max, counter.items()))
        card_lbl = items[0][0]
        cards_joker_replaced = cards.replace('J', card_lbl)
        return PokerTypes.of(cards_joker_replaced)

class CardHand:
    CARD_STRENGTH = {'A': 14, 'K': 13, 'Q': 12, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2, 'J': 1}

    def __init__(self, cards: str, bid: int):
        self.cards = cards
        self.bid = bid
        self.poker_type = PokerTypes.of_joker(cards)

    def __eq__(self, other):
        return self.cards == other.cards

    def __lt__(self, other):
        if self.poker_type.value == other.poker_type.value:
            for j in range(0, len(self.cards)):
                if self.cards[j] == other.cards[j]: continue
                return CardHand.CARD_STRENGTH[self.cards[j]] < CardHand.CARD_STRENGTH[other.cards[j]]
        return self.poker_type.value < other.poker_type.value


lines = open('input/7').read().splitlines()
card_hands = list(map(lambda arr: CardHand(*arr), map(lambda l: [l.split()[0], int(l.split()[1])], lines)))
cards_total = len(card_hands)
prize = 0
for i, card_hand in enumerate(sorted(card_hands)):
    prize += card_hand.bid * (i + 1)
print(prize)
