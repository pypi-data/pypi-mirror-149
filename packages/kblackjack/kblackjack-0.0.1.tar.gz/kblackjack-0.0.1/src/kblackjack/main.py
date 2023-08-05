from kblackjack.card import Card, Suit
from kblackjack.players import Player, FakePlayer, RealPlayer
import random

def createDeck() -> list[Card]:
    deck = []
    for _, suit in Suit.__members__.items():
        # for ranks 2 through 10 + J, Q, K, A
        for rank in [str(x) for x in range(2, 11)] + list('JQKA'):
            deck.append(Card(rank, suit))
    random.shuffle(deck)
    return deck

def dealCards(deck: list[Card], num: int, players: list[Player]) -> None:
    """
    Deal the given number of cards to each player
    """
    for p in players:
        for _ in range(num):
            if not deck:
                print('\n\nDeck is empty! Ending game.')
                exit(2)
            p.cards.append(deck.pop())

def discardHands(discardList: list[Card], players: list[Player]) -> None:
    """
    Move all cards from all players' hands to the discard pile
    """
    for p in players:
        discardList.extend(p.cards)
        p.cards = []

def checkForBlackjack(players: list[Player]) -> list[Player]:
    result = []
    for p in players:
        if p.handTotal() == 21:
            result.append(p)
    return result

def doRound(players: list[Player], deck: list[Card], discarded: list[Card]) -> None:
    allPlayersStand = False

    # If any players got blackjack, print the winners and end the round
    winners = checkForBlackjack(players)
    if winners:
        print(f'Round over! {len(winners)} players got blackjack!')
        print('Winners:')
        for winner in winners:
            winner.roundsWon += 1
            print('\t' + winner.reprWithCards())
        return

    while not allPlayersStand:
        for player in players:
            print(player)

        # Allow each player to play their round
        allPlayersStand = True
        for player in players:
            # Dealer doesn't hit until the end
            if isinstance(player, FakePlayer) and player.isDealer:
                continue

            if player.willHit():
                allPlayersStand = False
                dealCards(deck, 1, [player])
                if isinstance(player, RealPlayer):
                    print(f'You received: {player.cards[-1]}')
                    print(f'You now have: {player.cards}')

        print('\n\n\n')

    # Locate dealer in players list
    dealer = next(filter(lambda p: isinstance(p, FakePlayer) and p.isDealer, players))
    while dealer.willHit():
        dealCards(deck, 1, [dealer])

    # At this point, all players have stood or busted, including the dealer

    # Find the winner(s)
    bestScore = 0
    winners = []
    for player in players:
        score = player.handTotal()
        if score == bestScore:
            winners.append(player)
        elif score > bestScore and score <= 21:
            bestScore = score
            winners = [player]

    print(f'Round over! Best score: {bestScore}')
    print('Winners:')
    for winner in winners:
        print('\t' + winner.reprWithCards())

def main():
    deck = createDeck()
    discarded = []
    players = []

    # Dealer is added first so they're printed first during rounds
    players.append(FakePlayer(isDealer=True))

    try:
        numPlayers = int(input('How many fake players would you like? '))
    except ValueError:
        print('Invalid number of players')
        exit(1)
    for i in range(numPlayers):
        players.append(FakePlayer())

    # Real player gets added last so they get printed at the bottom during
    # rounds
    players.append(RealPlayer())

    try:
        rounds = int(input('How many rounds would you like to play? '))
    except ValueError:
        print('Invalid number of players')
        exit(1)

    for i in range(rounds):
        dealCards(deck, 2, players)
        print(f'======= ROUND {i + 1} =======\n')
        doRound(players, deck, discarded)
        discardHands(discarded, players)
        if i + 1 < rounds:
            print('\n\n\n\n')
