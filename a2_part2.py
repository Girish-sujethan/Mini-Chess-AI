"""CSC111 Winter 2021 Assignment 2: Trees, Chess, and Artificial Intelligence (Part 2)

Instructions (READ THIS FIRST!)
===============================

This Python module contains the start of functions and/or classes you'll define
for Part 2 of this assignment. Please note that in addition to this file, you will
also need to modify a2_game_tree.py by following the instructions on the assignment
handout. You should NOT make any changes to a2_minichess.py.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 David Liu and Isaac Waller.
"""
import random
from typing import Optional

import a2_game_tree
import a2_minichess


def generate_complete_game_tree(root_move: str, game_state: a2_minichess.MinichessGame,
                                d: int) -> a2_game_tree.GameTree:
    """Generate a complete game tree of depth d for all valid moves from the current game_state.

    For the returned GameTree:
        - Its root move is root_move.
        - Its `is_white_move` attribute is set using the current game_state.
        - It contains all possible move sequences of length <= d from game_state.
          For each node in the tree, its subtrees appear in the same order that their
          moves were returned by game_state.get_valid_moves(),
        - If d == 0, a size-one GameTree is returned.

    Note that some paths down the tree may have length < d, because they result in an end state
    (win or draw) from game_state in fewer than d moves.

    Preconditions:
        - d >= 0
        - root_move == GAME_START_MOVE or root_move is a valid chess move

    Implementation hints:
        - This function must be implemented recursively.
        - In the recursive step, use the MinichessGame.copy_and_make_move method to create
          a copy of the game state with one new move made.
        - You'll need to review the public interface of the MinichessGame class to see what
          methods are available to help implement this function.

    WARNING: we recommend not calling this function with depth greater than 6, as this will
    likely take a very long time on your computer.
    """
    # game_tree = a2_game_tree.GameTree()
    # game_tree.move = root_move
    #
    # # game_tree.is_white_move = game_state.is_white_move()
    #
    # if d == 0:
    #     game_tree.is_white_move = game_state.is_white_move()
    #     return game_tree
    # elif d == 1:
    #
    #     valid_moves = game_state.get_valid_moves()
    #     for x in valid_moves:
    #         # sub_tree = a2_game_tree.GameTree()
    #         # sub_tree.move = x
    #         # sub_tree.is_white_move = not game_tree.is_white_move
    #         # game_tree.add_subtree(sub_tree)
    #         boolean = game_state.is_white_move()
    #
    #         if game_state.get_winner() == 'White':
    #             game_tree.white_win_probability = 1.0
    #
    #         game_tree.add_subtree(a2_game_tree.GameTree(x, boolean))
    #         game_tree.is_white_move = boolean
    #     return game_tree
    # else:
    #     valid_moves1 = game_state.get_valid_moves()
    #     for y in valid_moves1:
    #         temp_game_state1 = game_state.copy_and_make_move(y)
    #         temp_game_tree = generate_complete_game_tree(y, temp_game_state1, d - 1)
    #         temp_game_tree.is_white_move = not game_state.is_white_move()
    #         if game_state.get_winner() == 'White':
    #             game_tree.white_win_probability = 1.0
    #         game_tree.add_subtree(temp_game_tree)
    #
    # game_tree.is_white_move = game_state.is_white_move()
    # if root_move == "*":
    #     game_tree.is_white_move = True
    # if game_state.get_winner() == 'White':
    #     game_tree.white_win_probability = 1.0
    # return game_tree

    game_tree = a2_game_tree.GameTree(root_move, game_state.is_white_move())
    if d == 0:
        if game_state.get_winner() == 'White':
            game_tree.white_win_probability = 1.0
        return game_tree
    elif game_state.get_valid_moves() == []:  # end of game
        if game_state.get_winner() == 'White':
            game_tree.white_win_probability = 1.0
        return game_tree
    else:
        for move in game_state.get_valid_moves():
            this_game_state = game_state.copy_and_make_move(move)
            game_tree.add_subtree(generate_complete_game_tree(move, this_game_state, d - 1))
            if game_state.get_winner() == 'White':
                game_tree.white_win_probability = 1.0
        return game_tree

    if game_state.get_winner() == 'White':
        game_tree.white_win_probability = 1.0

    game_tree = a2_game_tree.GameTree(root_move, game_state.is_white_move())
    if d == 0:

        return game_tree
    elif game_state.get_valid_moves() == []:  # end of game
        return game_tree
    else:
        for move in game_state.get_valid_moves():
            this_game_state = game_state.copy_and_make_move(move)
            game_tree.add_subtree(generate_complete_game_tree(move, this_game_state, d - 1))
        return game_tree


class GreedyTreePlayer(a2_minichess.Player):
    """A Minichess player that plays greedily based on a given GameTree.

    See assignment handout for description of its strategy.
    """
    # Private Instance Attributes:
    #   - _game_tree:
    #       The GameTree that this player uses to make its moves. If None, then this
    #       player just makes random moves.
    _game_tree: Optional[a2_game_tree.GameTree]

    def __init__(self, game_tree: a2_game_tree.GameTree) -> None:
        """Initialize this player.

        Preconditions:
            - game_tree represents a game tree at the initial state (root is '*')
        """
        self._game_tree = game_tree

    def make_move(self, game: a2_minichess.MinichessGame, previous_move: Optional[str]) -> str:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        if previous_move is None:
            #White chooses best opening move
            temp_subtree = self._game_tree.get_subtrees()[0]
            for subtree in self._game_tree.get_subtrees():
                if subtree.white_win_probability > temp_subtree.white_win_probability:
                    temp_subtree = subtree
            self._game_tree = temp_subtree
            return temp_subtree.move
        else:
            for subtree in self._game_tree.get_subtrees():
                if previous_move == subtree.move:
                    self._game_tree = subtree
                    break
            if self._game_tree is not None and self._game_tree.get_subtrees() != [] and game.is_white_move:
            if self._game_tree is not None and self._game_tree.get_subtrees() != []:
                if game.is_white_move():
                    #white turn
                    temp_subtree = self._game_tree.get_subtrees()[0]
                    for subtree in self._game_tree.get_subtrees():
                        if subtree.white_win_probability > temp_subtree.white_win_probability:
                            temp_subtree = subtree
                    self._game_tree = temp_subtree
                    return temp_subtree.move
                else:
                    #black turn
                    temp_subtree = self._game_tree.get_subtrees()[0]
                    for subtree in self._game_tree.get_subtrees():
                        if subtree.white_win_probability < temp_subtree.white_win_probability:
                            temp_subtree = subtree
                    self._game_tree = temp_subtree

                    return temp_subtree.move
            else:
                #random player ai
                return random.choice(game.get_valid_moves())




        # if self._game_tree.move == "*":
        #     temp_subtree = self._game_tree.get_subtrees()[0]
        #     for subtree in self._game_tree.get_subtrees():
        #         if subtree.white_win_probability > temp_subtree.white_win_probability:
        #             temp_subtree = subtree
        #     self._game_tree = temp_subtree
        #     print(temp_subtree.white_win_probability)
        #     return temp_subtree.move
        #     # previous_move is not None and self._game_tree is not None:
        # else:
        #     for subtree in self._game_tree.get_subtrees():
        #         if previous_move == subtree.move:
        #             self._game_tree = subtree
        #             break
        #
        # if self._game_tree is None or self._game_tree.get_subtrees() == []:
        #     possible_moves = game.get_valid_moves()
        #     print("bruheee")
        #     return random.choice(possible_moves)
        # else:
        #     print("nigger")
        #     if game.is_white_move():
        #         #black turn
        #         temp_subtree = self._game_tree.get_subtrees()[0]
        #         for subtree in self._game_tree.get_subtrees():
        #             if subtree.white_win_probability < temp_subtree.white_win_probability:
        #                 temp_subtree = subtree
        #         self._game_tree = temp_subtree
        #         return temp_subtree.move
        #     else:
        #         #white turn
        #         temp_subtree = self._game_tree.get_subtrees()[0]
        #         for subtree in self._game_tree.get_subtrees():
        #             if subtree.white_win_probability > temp_subtree.white_win_probability:
        #                 temp_subtree = subtree
        #         self._game_tree = temp_subtree
        #         print(temp_subtree.white_win_probability)
        #         return temp_subtree.move



def part2_runner(d: int, n: int, white_greedy: bool) -> None:
    """Create a complete game tree with the given depth, and run n games where
    one player is a GreedyTreePlayer and the other is a RandomPlayer.

    The GreedyTreePlayer uses the complete game tree with the given depth.
    If white_greedy is True, the White player is the GreedyTreePlayer and Black is a RandomPlayer.
    This is switched when white_greedy is False.

    Precondtions:
        - d >= 0
        - n >= 1

    Implementation notes:
        - Your implementation MUST correctly call a2_minichess.run_games. You may choose
          the values for the optional arguments passed to the function.
    """
    game = a2_minichess.MinichessGame()
    if white_greedy:
        white_player = GreedyTreePlayer(generate_complete_game_tree('*', game, d))
        black_player = a2_minichess.RandomPlayer()
    else:
        black_player = GreedyTreePlayer(generate_complete_game_tree('*', game, d))
        white_player = a2_minichess.RandomPlayer()

    a2_minichess.run_games(n, white_player, black_player, True, 2)


# if __name__ == '__main__':
#     import python_ta
#     python_ta.check_all(config={
#         'max-line-length': 100,
#         'max-nested-blocks': 4,
#         'disable': ['E1136'],
#         'extra-imports': ['random', 'a2_minichess', 'a2_game_tree']
#     })

    # Sample call to part2_runner (you can change this, just keep it in the main block!)
    # part2_runner(5, 50, False)
