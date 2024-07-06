"""
October 2023.
Simplified version of solitaire.
Author: Leo Duncan.
"""

# Class of a pile of cards
class CardPile:
    def __init__(self):
        self.items = []

    def add_top(self, item):
        self.items.insert(0, item)

    def add_bottom(self, item):
        self.items.append(item)

    def remove_top(self):
        temp = self.items[0]
        self.items.remove(temp)
        return temp

    def remove_bottom(self):
        temp = self.items[-1]
        self.items.remove(temp)
        return temp

    def size(self):
        return len(self.items)

    def peek_top(self):
        if self.size() == 0:
            return -1
        return self.items[0]

    def peek_bottom(self):
        if self.size() == 0:
            return -1
        return self.items[-1]

    def print_all(self, index): # Displays the card pile
        if self.size() == 0:
            print('')
        elif index == 0:
            print(str(self.items[0]) + ' *'*(self.size()-1))
            # Hides the turned down cards with '*' symbol
        else:
            print(str(self.items).replace(',', '')[1:-1])


# Class of the main game, Solitaire
class Solitaire:
    def __init__(self, cards):
        self.piles = []
        self.num_cards = len(cards)
        self.num_piles = (self.num_cards // 8) + 3
        self.max_num_moves = self.num_cards * 2
        for i in range(self.num_piles):
            self.piles.append(CardPile())
        for i in range(self.num_cards):
            self.piles[0].add_bottom(cards[i])

    def get_pile(self, i):
        return self.piles[i]

    def display(self):
        for i in range(self.num_piles):
            print(f"{i}: ", end='')
            self.piles[i].print_all(i)

    def move(self, p1, p2):
        if p1 == p2 == 0 and self.piles[p1].size() != 0:
            self.piles[p1].add_bottom(self.piles[p1].remove_top())

        elif p1 == 0 and p2 > 0:
            if (self.piles[p1].size() != 0 and \
                (self.piles[p2].peek_bottom() - 1 == \
                 self.piles[p1].peek_top() or \
                 self.piles[p2].size() == 0)):
                # If pile p1 is non-empty and pile p2 is empty or it's
                # bottom card is 1 less than pile p2's top card, then
                # this is a valid move.
                self.piles[p2].add_bottom(self.piles[p1].remove_top())

        elif p1 > 0 and p2 > 0:
            if (self.piles[p1].size() != 0 and \
                self.piles[p2].size() != 0 and \
                self.piles[p2].peek_bottom() - 1 == \
                self.piles[p1].peek_top()):
                # If piles p1 and p2 are non-empty and pile p2's bottom
                # card is 1 less than pile p2's top card, then this is
                # a valid move.
                for i in range(self.piles[p1].size()):
                    self.piles[p2].add_bottom(self.piles[p1].remove_top())

    def is_complete(self):
        if self.piles[0].size() == 0 and True in \
            [self.piles[i].size() == self.num_cards \
             for i in range(self.num_piles)]:
            # If there are no cards on the first pile, and all the
            # cards are in exactly one other pile, then the game has
            # finished and the player has won.
            return True
        return False

    # Starts the game
    def play(self):
        print("********************** NEW GAME *****************************")
        move_number = 1
        while move_number <= self.max_num_moves and not self.is_complete():
            self.display()
            print("Round", move_number, "out of", \
                  self.max_num_moves, end=": ")
            pile1 = int(input("Move from pile no.: "))
            print("Round", move_number, "out of", \
                  self.max_num_moves, end=": ")
            pile2 = int(input("Move to pile no.: "))
            if pile1 >= 0 and pile2 >= 0 and \
                pile1 < self.num_piles and pile2 < self.num_piles:
                # If both selections are in-between pile 0 and the
                # maximum pile number, then a potentially valid move
                # can take place
                self.move(pile1, pile2)
            move_number += 1
        if self.is_complete(): # Finishing message once the game has ended
            print("You Win in", move_number - 1, "steps!\n")
        else:
            print("You Lose!\n")

