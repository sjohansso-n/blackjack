from random import randrange
import time

"""
A simplified version of Black Jack allowing up to 
ten players.
"""

class Deck():
    
    def __init__(self):
        self.cards = ([i for i in range(1,11)]+[10]*3)*4
    
    def draw(self):
        index = randrange(0,len(self.cards))
        return self.cards.pop(index)

class Player():
    
    def __init__(self,name,hand,markers):
        self.name = name
        self.hand = hand
        self.markers = markers
        self.bet_amount = 0
        
    def bet(self):
        while self.bet_amount not in range(1, self.markers+1):
            self.bet_amount = int(input("How much do you want to bet? "))
    
    def draw(self,deck):
        card = deck.draw()
        self.hand.append(card)
        return card

    def value_of_ace(self):
        if 1 in self.hand or 11 in self.hand:
            aces = self.hand.count(1) + self.hand.count(11)
            indexes = [i for i, x in enumerate(self.hand) if x == 1 or x == 11]
            print(f"Your hand contains {aces} aces.")
            print("The default value of ace is 1.")
            print(self.hand)
            for ind in indexes:
                self.hand[ind] = 1
                while True:
                    change = input("Do you want to change the value of this ace to 11? [y/n] ").lower()
                    if change == 'y':
                        self.hand[ind] = 11
                        print(f"The value of your hand is now {sum(self.hand)}.")
                        print(self.hand)
                        break
                    elif change == 'n':
                        break
    
    def win(self,amount):
        self.markers += amount
        return self.markers
        
    def defeat(self,amount):
        if amount <= self.markers:
            self.markers -= amount
        else:
            self.markers = 0
        return self.markers

class Dealer():
    
    def __init__(self,hand):
        self.hand = hand
        
    def draw(self,deck):
        card = deck.draw()
        self.hand.append(card)
        return card

def black_jack(player_count=1,markers=10):
    
    deck = Deck()
    players = []
    for player in range(0,player_count):
        name = input("Enter name of player: ")
        player_hand = [deck.draw(),deck.draw()]
        player = Player(name,player_hand, markers)
        players.append((True,player))    
        
    while True:
        deck = Deck()
        dealer_hand = [deck.draw(),deck.draw()]
        dealer = Dealer(dealer_hand)
        for in_game,player in players:
            if player.markers == 0:
                print(f"\n{player.name}, you are out of markers.")
                time.sleep(2)
                print("You're no longer in the game.")
                time.sleep(2)
                players.remove((in_game,player))
        for in_game,player in players:
            player.hand = [deck.draw(),deck.draw()]
            players[players.index((in_game,player))] = (True,player)

            print(f"\n{player.name}'s turn")
            print(f"Your current value of hand is {sum(player.hand)}.")
            print(f"Dealer hand is ({dealer.hand[0]}, X).")
            print(f"You got {player.markers} markers.")

            player.value_of_ace()
            player.bet_amount = 0
            player.bet()
            player_turn = True

            while player_turn:
                play = input("\nDo you want to draw a card? [y/n] ").lower()
                if play != 'y':
                    player_turn = False
                else:
                    card = player.draw(deck)
                    print(f'\nDrew card: {card}')
                    time.sleep(1)
                    player.value_of_ace()
                    time.sleep(2)
                    print(f'Current value of hand: {sum(player.hand)}')
                    time.sleep(2)

                    if sum(player.hand) > 21:
                        players[players.index((in_game,player))] = (False,player)
                        print(f"\nThe sum of your hand is above 21. {player.name}, you are out of the game.")
                        time.sleep(2)
                        player_turn = False

        while True:
            card = dealer.draw(deck)
            print(f"\nDealer drew card: {card}")
            time.sleep(2)
            print(f"Current value of dealer's hand: {sum(dealer.hand)}")
            time.sleep(2)

            if sum(dealer.hand) > 21:
                print(f"\nThe sum of the dealer's hand is above 21.")
                time.sleep(2)
                check_winner(players)
                break
            for in_game,player in players:
                if in_game == True:
                    if sum(dealer.hand) < sum(player.hand):
                        break
            else:
                print(f"\nThe dealer's hand is {sum(dealer.hand)} and better than all players hands. The dealer won.")
                time.sleep(2)
                all_players_defeated(players)
                break

        time.sleep(2)
        play_again = input("Do you want to play another turn? [y/n] ")

        if play_again != 'y':
            break
        
def check_winner(players):
    all_bets = 0
    l = [0]
    for in_game,player in players:
        all_bets += player.bet_amount
        if in_game == True and sum(player.hand) <= 21 and sum(player.hand) > l[0]:
            l[0] = sum(player.hand)
            winner = player
    for in_game,player in players:
        if player != winner:
            markers = player.defeat(player.bet_amount)
            print(f"\n{player.name}, your hand is {sum(player.hand)}. You were defeated. You now got {markers} markers left.")
            time.sleep(2)
    markers = winner.win(all_bets)
    print(f"\nCongratulations {winner.name}! You won! Your hand is {sum(winner.hand)}. You now got {markers} markers.")
    
def all_players_defeated(players):
    for in_game,player in players:
        markers = player.defeat(player.bet_amount)
        print(f"\n{player.name}, your loosing hand was {sum(player.hand)}. You now got {markers} markers left.")
        time.sleep(2)

if __name__ == "__main__":
    num = ''
    while num not in range(1,11):
        num = int(input('Enter number of players: '))
    black_jack(num)



