import itertools
from kblackjack.card import Card

class Player:
    _idCounter = itertools.count()

    id: int
    cards: list[Card]
    roundsWon: int

    def __init__(self, cards: list[Card] = None):
        if cards is None:
            cards = []
        self.cards = cards
        self.id = next(Player._idCounter)
        self.roundsWon = 0

    def __repr__(self) -> str:
        bust = ''
        if self.handTotal() > 21:
            bust = ' (BUST)'
        return f'Player {self.id}{bust}: {len(self.cards)} cards'

    def reprWithCards(self) -> str:
        bust = ''
        if self.handTotal() > 21:
            bust = ' (BUST)'
        return f'Player {self.id}{bust}: {self.cards}'

    def handTotal(self) -> int:
        """
        Return the highest sum of the given cards that doesn't exceed 21. If
        staying below 21 isn't possible, return the smallest possible sum.
        """
        aceCount = self.cards.count(Card('A'))
        sumWithoutAces = 0
        for c in self.cards:
            if c.rank != 'A':
                sumWithoutAces += c.value
        gap = 21 - sumWithoutAces
        if gap >= 11 + aceCount - 1:
            return sumWithoutAces + 11 + aceCount - 1
        else:
            return sumWithoutAces + aceCount

class FakePlayer(Player):
    def __init__(self, isDealer: bool = False):
        super().__init__()
        self.isDealer = isDealer

    def __repr__(self) -> str:
        bust = ''
        if self.handTotal() > 21:
            bust = ' (BUST)'
        if self.isDealer:
            return f'Dealer{bust}: {len(self.cards)} cards\n\tVisible card: {self.cards[1]}'
        else:
            return 'Fake ' + super().__repr__()

    def reprWithCards(self) -> str:
        if self.isDealer:
            name = 'Dealer'
        else:
            name = f'Fake Player {self.id}'
        return f'{name}: {self.cards}'

    def willHit(self) -> bool:
        """
        Simulates the player taking a turn. Currently will hit on 16 or below
        and stand on 17 and above.
        """
        return self.handTotal() < 16

class RealPlayer(Player):
    def __repr__(self) -> str:
        bust = ''
        if self.handTotal() > 21:
            bust = ' (BUST)'
        return f'You{bust}: {self.cards}'

    reprWithCards = __repr__

    def willHit(self) -> bool:
        if self.handTotal() > 21:
            return False

        choice = input('\nHit? (Y/n) ').lower()
        if choice[0] == 'n':
            return False
        elif not choice or choice[0] == 'y':
            return True
        else: # if not 'y*', 'n*', or empty, ask again
            return self.willHit()
