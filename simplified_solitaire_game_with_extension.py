"""
October 2023.
Simplified version of solitaire (extended).
Author: Leo Duncan.
"""

import time
import random


#default cards
default_cards = [1,2,3,4,5] #feel free to change this to your own cards
random.shuffle(default_cards)

# A function that makes it much easier to perform the aesthetic
# character-by-character printing.
def print_slowly(text, the_end='\n'):
    for char in text[:-1]:
        print(char, end='')
        time.sleep(0.03)
    print(text[-1], end=the_end)
    # similar to "end" in the print() function.

# A function that makes it easier to print in any desired colour.
def colours(a_colour, text):
    return(f"\033[38;5;{a_colour}m{text}")
    # Applies the new colour using an ANSI escape code


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
            print_slowly(str(self.items[0]) + ' *'*(self.size()-1))
        else:
            print_slowly(str(self.items).replace(',', '')[1:-1])


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
            print_slowly(f"{i}: ", the_end='')
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
        print_slowly(colours(199, "Hiya!"))
        print_slowly(colours(74, "Welcome to ") + \
                     colours(199, "Fun-itaire! ") + \
                     colours(74, "A simplified version of the classic Solitaire."))

        print_slowly(colours(74, "**********************") + \
                     colours(199, " NEW GAME ") + \
                     colours(74, "*****************************"))

        move_number = 1
        while move_number <= self.max_num_moves and not self.is_complete():
            self.display()
            print_slowly(colours(74, "Round ") + \
                         colours(199, str(move_number)) + \
                         colours(74, " out of ") + \
                         colours(199, str(self.max_num_moves)) + \
                         colours(74, ": Move from pile no.:"), the_end='')

            pile1 = int(input(" "))
            print_slowly(colours(74, "Round ") + \
                         colours(199, str(move_number)) + \
                         colours(74, " out of ") + \
                         colours(199, str(self.max_num_moves)) + \
                         colours(74, ": Move to pile no.:"), the_end='')

            pile2 = int(input(" "))
            if pile1 >= 0 and pile2 >= 0 and pile1 < self.num_piles and \
                pile2 < self.num_piles:
                # If both selections are in-between pile 0 and the
                # maximum pile number, then a potentially valid move
                # can take place
                self.move(pile1, pile2)
            move_number += 1

        # Winning/losing message once the game has ended
        if self.is_complete():
            print_slowly(colours(199, \
                                 f"You Win in {move_number - 1} steps!\n"))
        else:
            print_slowly(colours(199, "You Lose!\n"))


game = Solitaire(default_cards)
game.play()
