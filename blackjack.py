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
        
        # Adjust for aces
        while total > 21 and self.aces:
            total -= 10
            self.aces -= 1
        
        return total
    def has_blackjack(self):
        return self.calculate_value() == 21 and len(self.cards) == 2
    
class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.bet = 0

    def ask_for_bet(self):
        while True:
            try:
                self.bet = int(input("Enter your bet amount: "))
                if self.bet > 0:
                    break
                else:
                    print("Bet must be a positive number.")
            except ValueError:
                print("Please enter a valid number.")

    def initial_deal(self):
        for _ in range(2):
            self.player_hand.add_card(self.deck.deal_card())
            self.dealer_hand.add_card(self.deck.deal_card())

    def show_hands(self, show_dealer_card=False):
        print("\nYour hand:", ", ".join(map(str, self.player_hand.cards)), f"Value: {self.player_hand.calculate_value()}")
        if show_dealer_card:
            print("Dealer's hand:", ", ".join(map(str, self.dealer_hand.cards)), f"Value: {self.dealer_hand.calculate_value()}")
        else:
            print("Dealer's hand: [Hidden],", self.dealer_hand.cards[1])

    def check_blackjack(self):
        player_blackjack = self.player_hand.has_blackjack()
        dealer_showing_ten_or_ace = self.dealer_hand.cards[1].value() >= 10

        if player_blackjack:
            self.show_hands(show_dealer_card=True)
            if dealer_showing_ten_or_ace:
                print("Player has Blackjack! Dealer is showing a card valued 10 or Ace, revealing the dealer's hand...")
                self.dealer_turn()  # Reveal the dealer's hand and complete the turn
                self.determine_winner()
                return True  # End the game
            else:
                print(f"Player has Blackjack! You win ${self.bet * 2.25:.2f}")
                return True  # Player wins immediately
        return False  # No automatic win, continue the game

    def player_turn(self):
        while True:
            self.show_hands()
            move = input("\nDo you want to (h)it or (s)tand? ").lower()
            if move == 'h':
                self.player_hand.add_card(self.deck.deal_card())
                if self.player_hand.calculate_value() > 21:
                    self.show_hands()
                    print("Bust! You lose.")
                    return False
            elif move == 's':
                return True
            else:
                print("Invalid input, please enter 'h' to hit or 's' to stand.")

    def dealer_turn(self):
        while self.dealer_hand.calculate_value() < 17:
            self.dealer_hand.add_card(self.deck.deal_card())

    def determine_winner(self):
        player_total = self.player_hand.calculate_value()
        dealer_total = self.dealer_hand.calculate_value()

        if dealer_total > 21:
            print("Dealer busts! You win!")
        elif player_total > dealer_total:
            print(f"You win ${self.bet * 2.25:.2f}")
        elif player_total < dealer_total:
            print("Dealer wins! You lose.")
        else:
            print("It's a tie!")
    
    def play(self):
        self.ask_for_bet()
        self.initial_deal()

        # Check for immediate Blackjack win/loss
        if self.check_blackjack():
            return  # Player wins with a blackjack, no need to continue

        if not self.player_turn():
            return

        self.dealer_turn()
        self.show_hands(show_dealer_card=True)
        self.determine_winner()

# Running the game
if __name__ == "__main__":
    game = BlackjackGame()
    game.play()
