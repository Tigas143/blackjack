import random


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def value(self):
        """ Return the blackjack value of the card. """
        if self.rank in ['Jack', 'Queen', 'King']:
            return 10
        elif self.rank == 'Ace':
            return 11  # or 1 depending on the hand's context
        else:
            return int(self.rank)

class Deck:
    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        self.cards = [Card(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(self.cards)

    def deal_card(self):
        """ Deal a card from the deck """
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.aces = 0  # To handle the Ace's special case

    def add_card(self, card):
        self.cards.append(card)
        if card.rank == 'Ace':
            self.aces += 1

    def calculate_value(self):
        total = sum(card.value() for card in self.cards)
        aces = self.aces
        # Adjust for aces
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total
    def has_blackjack(self):
        return self.calculate_value() == 21 and len(self.cards) == 2
    def can_split(self):
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank
    
class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hands = []
        self.dealer_hand = Hand()
        self.bets = []  # To keep track of bets for each hand

    def ask_for_bet(self, hand):
        while True:
            try:
                bet = int(input("Enter your bet amount for Hand "+ str(hand) +":"))
                if bet > 0:
                    return bet
                else:
                    print("Bet must be a positive number.")
            except ValueError:
                print("Please enter a valid number.")

    def player_deal(self):
        hand = 1
        while True:
            num_hands = input("How many hands do you want to play? ")
            if num_hands.isdigit() and int(num_hands) > 0:
                num_hands = int(num_hands)
                break
            else:
                print("Please enter a valid positive number.")
        for _ in range(num_hands):
            self.player_hands.append(Hand())
            self.bets.append(self.ask_for_bet(hand))  # Ask for a bet for each hand
            hand +=1
        for player_hand in self.player_hands:
            player_hand.add_card(self.deck.deal_card())
        for player_hand in self.player_hands:
            player_hand.add_card(self.deck.deal_card())

    def dealer_deal(self):
        self.dealer_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())

    def show_hands(self, show_dealer_card=False):
        hand = 1
        for player_hand in self.player_hands:
            print(f"\nHand {hand}: {', '.join(map(str, player_hand.cards))}, Value: {player_hand.calculate_value()}, Bet: ${self.bets[hand-1]}")
            hand += 1
        if show_dealer_card:
            print("Dealer's hand:", ", ".join(map(str, self.dealer_hand.cards)), f"Value: {self.dealer_hand.calculate_value()}")
        else:
            print("Dealer's hand: [Hidden],", self.dealer_hand.cards[1])

    def check_blackjack(self):
        hand = 1
        for player_hand in self.player_hands:
            player_blackjack = player_hand.has_blackjack()
            dealer_showing_ten_or_ace = self.dealer_hand.cards[1].value() >= 10

            if player_blackjack:
                self.show_hands(show_dealer_card=True)
                if dealer_showing_ten_or_ace:
                    print(f"Hand {hand}: Player has Blackjack! Dealer is showing a card valued 10 or Ace")
                else:
                    print(f"Hand {hand}: Player has Blackjack! You win ${self.bets[hand-1] * 2.25:.2f}")
                    self.player_hands.pop(hand - 1)
                    self.bets.pop(hand - 1)
            hand += 1

    def split_hand(self, hand_index):
        # Split the hand into two hands
        card_to_split = self.player_hands[hand_index].cards.pop()
        new_hand = Hand()
        new_hand.add_card(card_to_split)
        self.player_hands[hand_index].add_card(self.deck.deal_card())
        new_hand.add_card(self.deck.deal_card())
        self.player_hands.append(new_hand)
        self.bets.append(self.bets[hand_index])  # The bet for the new hand is the same as the original hand

    def player_turn(self):
        hand = 1
        for i, player_hand in enumerate(self.player_hands):
            turn = True
            while turn:
                player_total = player_hand.calculate_value()
                self.show_hands()
                # Offer options for hit, stand, double down, or split if possible
                if player_hand.can_split():
                    move = input(f"\nHand {hand}: Do you want to (h)it, (s)tand, (d)ouble down, or (p)split? ").lower()
                elif player_total in [9, 10, 11]:
                    move = input(f"\nHand {hand}: Do you want to (h)it, (s)tand, or (d)ouble down? ").lower()
                else:
                    move = input(f"\nHand {hand}: Do you want to (h)it or (s)tand? ").lower()

                if move == 'h':
                    player_hand.add_card(self.deck.deal_card())
                    if player_hand.calculate_value() >= 21:
                        turn = False
                elif move == 's':
                    turn = False
                elif move == 'd' and player_total in [9, 10, 11]:
                    self.bets[i] *= 2
                    print(f"Hand {hand}: Your bet is now doubled to ${self.bets[i]}.")
                    player_hand.add_card(self.deck.deal_card())
                    turn = False
                elif move == 'p' and player_hand.can_split():
                    self.split_hand(i)
                    turn = True
                else:
                    print("Invalid input, please enter 'h' to hit, 's' to stand, 'd' to double down, or 'p' to split.")
            hand += 1

    def dealer_turn(self):
        while self.dealer_hand.calculate_value() < 17:
            self.dealer_hand.add_card(self.deck.deal_card())

    def determine_winner(self):
        hand = 1
        print("\n")
        for i, player_hand in enumerate(self.player_hands):
            player_total = player_hand.calculate_value()
            dealer_total = self.dealer_hand.calculate_value()
            if player_hand.has_blackjack() and not self.dealer_hand.has_blackjack:
                print(f"Hand {hand}: Player has Blackjack! You win ${self.bets[i] * 2.25:.2f}")
            elif player_total > 21:
                print(f"Hand {hand}: Bust! You lose.")
            elif dealer_total > 21:
                print(f"Hand {hand}: Dealer busts! You win ${self.bets[i] * 2:.2f}")
            elif player_total > dealer_total:
                print(f"Hand {hand}: You win ${self.bets[i] * 2:.2f}")
            elif player_total < dealer_total:
                print(f"Hand {hand}: Dealer wins! You lose.")
            else:
                print(f"Hand {hand}: It's a tie!")
            hand += 1

    def play(self):
        self.player_deal()
        self.dealer_deal()

        # Check for immediate Blackjack win/loss
        self.check_blackjack()

        self.player_turn()
        self.dealer_turn()
        self.show_hands(show_dealer_card=True)
        self.determine_winner()

# Running the game
if __name__ == "__main__":
    game = BlackjackGame()
    game.play()
