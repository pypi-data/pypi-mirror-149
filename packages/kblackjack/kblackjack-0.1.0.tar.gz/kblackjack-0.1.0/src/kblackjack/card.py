from dataclasses import dataclass, field
from enum import Enum, unique

@unique
class Suit(Enum):
    SPADE = '\N{BLACK SPADE SUIT}'
    CLUB = '\N{BLACK CLUB SUIT}'
    HEART = '\N{BLACK HEART SUIT}'
    DIAMOND = '\N{BLACK DIAMOND SUIT}'

@dataclass(frozen=True, order=True)
class Card:
    rank: str
    suit: Suit = field(default=Suit.SPADE, compare=False)

    def __repr__(self):
        return f'{self.rank} {self.suit.value}'

    @property
    def value(self):
        if self.rank.isnumeric():
            return int(self.rank)
        elif self.rank == 'A':
            return 11
        return 10
