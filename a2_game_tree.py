"""CSC111 Winter 2021 Assignment 2: Trees, Chess, and Artificial Intelligence (Game Tree)

Instructions (READ THIS FIRST!)
===============================

This Python module contains the start of a GameTree class that you'll be working with
and modifying in this assignment. You WILL be submitting this file!

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 David Liu and Isaac Waller.
"""
from __future__ import annotations
from typing import Optional

GAME_START_MOVE = '*'


class GameTree:
    """A decision tree for Minichess moves.

    Each node in the tree stores a Minichess move and a boolean representing whether
    the current player (who will make the next move) is White or Black.

    Instance Attributes:
      - move: the current chess move (expressed in chess notation), or '*' if this tree
              represents the start of a game
      - is_white_move: True if White is to make the next move after this, False otherwise
      -  white_win_probability: a float between 0 and 1, which represents the probability of white
               winning the minichess game

    Representation Invariants:
        - self.move == GAME_START_MOVE or self.move is a valid Minichess move
        - self.move != GAME_START_MOVE or self.is_white_move == True
        - 0.0 <= self.white_win_probability <= 1.0
    """
    move: str
    is_white_move: bool
    white_win_probability: float

    # Private Instance Attributes:
    #  - _subtrees:
    #      the subtrees of this tree, which represent the game trees after a possible
    #      move by the current player
    _subtrees: list[GameTree]

    def __init__(self, move: str = GAME_START_MOVE,
                 is_white_move: bool = True, white_win_probability: float = 0.0) -> None:
        """Initialize a new game tree.

        Note that this initializer uses optional arguments, as illustrated below.

        >>> game = GameTree()
        >>> game.move == GAME_START_MOVE
        True
        >>> game.is_white_move
        True
        """
        self.move = move
        self.is_white_move = is_white_move
        self._subtrees = []
        self.white_win_probability = white_win_probability

    def get_subtrees(self) -> list[GameTree]:
        """Return the subtrees of this game tree."""
        return self._subtrees

    def find_subtree_by_move(self, move: str) -> Optional[GameTree]:
        """Return the subtree corresponding to the given move.

        Return None if no subtree corresponds to that move.
        """
        for subtree in self._subtrees:
            if subtree.move == move:
                return subtree

        return None

    def add_subtree(self, subtree: GameTree) -> None:
        """Add a subtree to this game tree."""

        self._subtrees.append(subtree)
        self._update_white_win_probability()


    def __str__(self) -> str:
        """Return a string representation of this tree.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        white_win = str(self.white_win_probability)
        if self.is_white_move:
            turn_desc = "White's move"
        else:
            turn_desc = "Black's move"
        move_desc = f'{self.move} -> {turn_desc + " " + white_win}\n'
        s = '  ' * depth + move_desc
        if self._subtrees == []:
            return s
        else:
            for subtree in self._subtrees:
                s += subtree._str_indented(depth + 1)
            return s

    ############################################################################
    # Part 1: Loading and "Replaying" Minichess games
    ############################################################################
    def insert_move_sequence(self, moves: list[str], white_win_probability=0.0) -> None:
        """Insert the given sequence of moves into this tree.

        The inserted moves form a chain of descendants, where:
            - moves[0] is a child of this tree's root
            - moves[1] is a child of moves[0]
            - moves[2] is a child of moves[1]
            - etc.

        Do not create duplicate moves that share the same parent; for example, if moves[0] is
        already a child of this tree's root, you should recurse into that existing subtree rather
        than create a new subtree with moves[0].
        But if moves[0] is not a child of this tree's root, create a new subtree for it
        and append it to the existing list of subtrees.

        Implementation Notes:
            - Your implementation must use recursion, and NOT use any loops to "go down" the tree.
            - Your implementation must have a worst-case running time of Theta(m + n) time,
              where m is the length of moves and n is the size of this tree.
              This means you shouldn't use list slicing to access the "rest" of the list of moves,
              like in Tutorial 4. Instead, you can use one of the following approaches:

              i) Use a recursive helper method that takes an extra "current index" argument to
                 keep track of the next move in the list.
              ii) First reverse the list, and then use a recursive helper method that calls
                 `list.pop` on the list of moves. Just make sure the original list isn't changed
                 when the function ends!
        """
        reversed_moves = list(moves)

        # This will only every happen once, to reverse the list
        if self.move == '*':
            reversed_moves.reverse()

        # Very Base Case. If this is met, moves is empty and recursion terminates
        elif moves == []:
            return

        # Find set first move and set that it is not in subtree
        curr_move = reversed_moves.pop()
        in_subtree = False

        for subtree in self._subtrees:
            # If the move is in the subtree, just recurse into it and alter nothing
            if subtree.move == curr_move:
                subtree.insert_move_sequence(reversed_moves, white_win_probability)
                in_subtree = True

        # If the move is not in the subtree, add subtree and recurse
        if not in_subtree:
            if self.is_white_move:
                new_tree = GameTree(curr_move,False, white_win_probability)
                self.add_subtree(new_tree)

                new_tree.insert_move_sequence(reversed_moves, white_win_probability)

            else:
                new_tree = GameTree(curr_move,True, white_win_probability)
                self.add_subtree(new_tree)
                new_tree.insert_move_sequence(reversed_moves, white_win_probability)

    ############################################################################
    # Part 2: Complete Game Trees and Win Probabilities
    ############################################################################

    def _update_white_win_probability(self) -> None:
        """Recalculate the white win probability of this tree.

        Note: like the "_length" Tree attribute from tutorial, you should only need
        to update self here, not any of its subtrees. (You should *assume* that each
        subtree has the correct white win probability already.)

        Use the following definition for the white win probability of self:
            - if self is a leaf, don't change the white win probability
              (leave the current value alone)
            - if self is not a leaf and self.is_white_move is True, the white win probability
              is equal to the MAXIMUM of the white win probabilities of its subtrees
            - if self is not a leaf and self.is_white_move is False, the white win probability
              is equal to the AVERAGE of the white win probabilities of its subtrees
        """
        if self._subtrees == []:
            pass
        elif self.is_white_move:
            maxi = self.find_max()

            self.white_win_probability = maxi
        else:
            average = self.avg_helper()
            self.white_win_probability = average[0] / average[1]

    def find_max(self: GameTree, maxi: float = 0.0) -> float:
        """Helper function for _update_white_win_probability. Finds the max value of
        white win probability in our subtrees"""

    # Base case
        max_list = []
        if self._subtrees == []:
            if self.white_win_probability > maxi:
                return self.white_win_probability
            else:
                return maxi
        else:
            for subtree in self._subtrees:
                max_list += [subtree.find_max(maxi)]
                maxi = max(max_list)
            return maxi

    def avg_helper(self: GameTree, total=0, amount=0) -> tuple[float, int]:
        """Helper function for _update_white_win_probability. Finds the average value of
        white win probability in our subtrees"""
        # if self._subtrees != []:
        #     total += self.white_win_probability
        #     amount += 1
        #     for subtree in self._subtrees:
        #         subtree.avg_helper(total, amount)
        #
        # return (total, amount)
        for subtree in self._subtrees:
            amount+=1
            total += self.white_win_probability
            amount += subtree.avg_helper()[1]
            total += subtree.avg_helper()[0]
        return (total, amount)



    # def find_max_v2(self: GameTree, move: str, maxi: float = 0.0) -> tuple[str, float]:
    #     """Helper function for GreedyTreePlayer in a2_part2.py. Finds the max value of
    #     white win probability in our subtrees"""
    #
    #     # Base case
    #     max_list = []
    #     if self._subtrees == []:
    #         if maxi < self.white_win_probability:
    #             return (self.move, self.white_win_probability)
    #         else:
    #             return (move, maxi)
    #     else:
    #         for subtree in self._subtrees:
    #             max_list += [subtree.find_max_v2(subtree.move)]
    #         max_list2 = [max_list[1] for x in max_list]
    #         max_index = max_list.index(max(max_list2))
    #         return (max_list2[max_index][0], max_list2[max_index][1])
    #
    #
    # def find_min(self: GameTree, move: str, mini: float = 0.0) -> tuple[str, float]:
    #     """Helper function for GreedyTreePlayer in a2_part2.py. Finds the max value of
    #     white win probability in our subtrees"""
    #
    #     # Base case
    #     min_list = []
    #     if self._subtrees == []:
    #         if mini > self.white_win_probability:
    #             return (self.move, self.white_win_probability)
    #         else:
    #             return (move, mini)
    #     else:
    #         for subtree in self._subtrees:
    #             min_list += [subtree.find_min(subtree.move)]
    #         min_list2 = [min_list[x][1] for x in range(0, len(min_list))]
    #         print(min_list)
    #         min_index = min_list2.index(min(min_list2))
    #
    #         print(min_list2)
    #         print(min_index)
    #
    #         return (min_list[min_index][0], min_list[min_index][1])


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
    })
