"""CSC111 Winter 2021 Assignment 2: Trees, Chess, and Artificial Intelligence (Minichess Library)

Module Description
==================

This module contains a collection of Python classes and functions that you'll use on
this assignment to represent games of Minichess. You are responsible for reading the
*docstrings* of this file to understand how to use these classes and functions,
but should not modify anything in this file. It will not be submitted, and we will
supply our own copy for grading purposes.

Note: as is standard for CSC111, we use a leading underscore to indicate private
functions, methods, and instance attributes. You don't have to worry about any of these,
and in fact shouldn't use them in this assignment!

Disclaimer: we didn't have time to make this file fully PythonTA-compliant!

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

import copy
import random
import time
from typing import Optional

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import chessboard.display as display


################################################################################
# Representing Minichess
################################################################################
_FILE_TO_INDEX = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
_INDEX_TO_FILE = {i: f for f, i in _FILE_TO_INDEX.items()}
_RANK_TO_INDEX = {'1': 0, '2': 1, '3': 2, '4': 3}
_INDEX_TO_RANK = {i: r for r, i in _RANK_TO_INDEX.items()}


_MAX_MOVES = 50


class MinichessGame:
    """A class representing a state of a game of Minichess.

    >>> game = MinichessGame()
    >>> # Get all valid moves for white at the start of the game.
    >>> game.get_valid_moves()
    ['a2b3', 'b2c3', 'b2a3', 'c2d3', 'c2b3', 'd2c3']
    >>> # Make a move. This method mutates the state of the game.
    >>> game.make_move('a2b3')
    >>> game.get_valid_moves()  # Now, black only has one valid move
    ['b4b3']
    >>> # If you try to make an invalid move, a ValueError is raised.
    >>> game.make_move('a4d1')
    Traceback (most recent call last):
    ValueError: Move "a4d1" is not valid
    >>> # This move is okay.
    >>> game.make_move('b4b3')
    >>> game.get_url()
    'https://lichess.org/analysis/standard/8/8/8/8/r1kr4/pqpp4/1PPP4/RQKR4'
    """
    # Private Instance Attributes:
    #   - _board: a two-dimensional representation of a Minichess board
    #   - _valid_moves: a list of the valid moves of the current player
    #   - _is_white_active: a boolean representing whether white is the current player
    #   - _move_count: the number of moves that have been made in the current game
    _board: list[list[Optional[_Piece]]]
    _valid_moves: list[str]
    _is_white_active: bool
    _move_count: int

    def __init__(self, board: list[list[Optional[_Piece]]] = None,
                 white_active: bool = True, move_count: int = 0) -> None:

        if board is not None:
            self._board = board
        else:
            self._board = [
                [_Piece('r', True), _Piece('q', True), _Piece('k', True), _Piece('r', True)],
                [_Piece('p', True), _Piece('p', True), _Piece('p', True), _Piece('p', True)],
                [_Piece('p', False), _Piece('p', False), _Piece('p', False), _Piece('p', False)],
                [_Piece('r', False), _Piece('q', False), _Piece('k', False), _Piece('r', False)]
            ]

        self._is_white_active = white_active
        self._move_count = move_count
        self._valid_moves = []

        self._recalculate_valid_moves()

    def get_valid_moves(self) -> list[str]:
        """Return a list of the valid moves for the active player."""
        return self._valid_moves

    def make_move(self, move: str) -> None:
        """Make the given chess move. This instance of Minichess will be mutated, and will
        afterwards represent the game state after move is made.

        If move is not a currently valid move, raise a ValueError.
        """
        if move not in self._valid_moves:
            raise ValueError(f'Move "{move}" is not valid')

        self._board = self._board_after_move(move)

        self._is_white_active = not self._is_white_active
        self._move_count += 1

        self._recalculate_valid_moves()

    def copy_and_make_move(self, move: str) -> MinichessGame:
        """Make the given chess move in a copy of this MinichessGame, and return that copy.

        If move is not a currently valid move, raise a ValueError.
        """
        return MinichessGame(board=self._board_after_move(move),
                             white_active=not self._is_white_active,
                             move_count=self._move_count + 1)

    def is_white_move(self) -> bool:
        """Return whether the white player is to move next."""
        return self._is_white_active

    def get_winner(self) -> Optional[str]:
        """Return the winner of the game (black or white) or 'draw' if the game ended in a draw.

        Return None if the game is not over.
        """
        if self._move_count >= _MAX_MOVES:
            return 'Draw'
        elif len(self._valid_moves) == 0:
            return 'Black' if self._is_white_active else 'White'
        else:
            return None

    def _calculate_moves_for_board(self, board: list[list[Optional[_Piece]]],
                                   is_white_active: bool) -> tuple:
        """Return all possible moves on a given board with a given active player."""
        moves = []
        # Used to calculate whether the other players' king is in check
        # (i.e. the black king if is_white_active, otherwise the white king)
        check = []

        for pos in [(y, x) for y in range(0, 4) for x in range(0, 4)]:
            piece = board[pos[0]][pos[1]]
            if piece is None or piece.is_white != is_white_active:
                continue

            kind, is_white = piece.kind, piece.is_white

            if kind == 'p':
                # Pawns can only move towards the opponent's end of the board.
                direction = 1 if is_white else -1

                check += self._find_moves_in_direction(board, moves, pos, is_white, (direction, 0),
                                                       limit=1, capture=False)
                check += self._find_moves_in_direction(board, moves, pos, is_white, (direction, 1),
                                                       limit=1, capture=True)
                check += self._find_moves_in_direction(board, moves, pos, is_white, (direction, -1),
                                                       limit=1, capture=True)

            if kind == 'r' or kind == 'q':
                check += self._find_moves_in_direction(board, moves, pos, is_white, (0, 1))
                check += self._find_moves_in_direction(board, moves, pos, is_white, (1, 0))
                check += self._find_moves_in_direction(board, moves, pos, is_white, (0, -1))
                check += self._find_moves_in_direction(board, moves, pos, is_white, (-1, 0))

            if kind == 'q':
                for y, x in [(y, x) for y in [-1, 1] for x in [-1, 1]]:
                    check += self._find_moves_in_direction(board, moves, pos, is_white, (y, x))

            if kind == 'k':
                for y, x in [(y, x) for y in [-1, 0, 1] for x in [-1, 0, 1]]:
                    check += self._find_moves_in_direction(board, moves, pos, is_white, (y, x),
                                                           limit=1)

        return moves, check

    def _find_moves_in_direction(self, board, moves, pos, is_white, direction, limit=None,
                                 capture=None):
        """Find valid moves moving in a given direction from a certain position.

        capture: True if must capture, False if must not capture, None otherwise.
        """

        move_start = _index_to_algebraic(pos)
        stop = False
        i = 1
        check = []
        while not stop:
            y, x = pos[0] + direction[0] * i, pos[1] + direction[1] * i

            if x < 0 or y < 0 or x > 3 or y > 3:
                break  # Out of bounds

            contents = board[y][x]
            move = move_start + _index_to_algebraic((y, x))

            if contents is not None:
                # Square contains piece
                stop = True

                if contents.is_white != is_white and contents.kind == 'k' \
                        and capture is not False:
                    # Cannot capture king, but they are in check
                    check.append(move)
                elif contents.is_white != is_white and capture is not False:
                    # Capture
                    moves.append(move)
            else:
                # Empty square
                if capture is not True:
                    moves.append(move)

            i += 1

            if limit is not None and i > limit:
                stop = True

        return check

    def _board_after_move(self, move: str) -> list[list[Optional[_Piece]]]:
        """Return a copy of self._board representing the state of the board after making move.
        """
        board_copy = copy.deepcopy(self._board)

        start_pos = _algebraic_to_index(move[0:2])
        end_pos = _algebraic_to_index(move[2:])

        board_copy[end_pos[0]][end_pos[1]] = board_copy[start_pos[0]][start_pos[1]]
        board_copy[start_pos[0]][start_pos[1]] = None

        return board_copy

    def _recalculate_valid_moves(self) -> None:
        """Update the valid moves for this game board."""

        moves, check = self._calculate_moves_for_board(self._board, self._is_white_active)

        assert len(check) == 0, \
            "The other player's king can never be in check at the start of your turn."

        # Filter moves that would leave the current player's king in check
        valid_moves = []
        for move in moves:
            board_copy = self._board_after_move(move)
            _, check = self._calculate_moves_for_board(board_copy, not self._is_white_active)
            if len(check) == 0:
                valid_moves.append(move)

        self._valid_moves = valid_moves

    def get_fen(self) -> str:
        """Return a string description of the current game state in Forsyth-Edwards Notation.

        Reference: https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation.

        This method is used to visualize the game board using Pygame---you won't need to call it
        directly.
        """
        rows = [''.join([(p.fen() if p is not None else '1') for p in row]) + '4' for row in
                self._board]
        return '/'.join(reversed(rows))

    def get_url(self) -> str:
        """Return a URL to a web page where you can examine the current state of the board."""
        return "https://lichess.org/analysis/standard/8/8/8/8/" + self.get_fen()


def _algebraic_to_index(move: str) -> tuple[int, int]:
    """Convert coordinates in algebraic format ex. 'a2' to array indices (y, x)."""
    return (_RANK_TO_INDEX[move[1]], _FILE_TO_INDEX[move[0]])


def _index_to_algebraic(pos: tuple[int, int]) -> str:
    """Convert coordinates in array indices (y, x) to algebraic format."""
    return _INDEX_TO_FILE[pos[1]] + _INDEX_TO_RANK[pos[0]]


class _Piece:
    """Represents a single piece in Minichess.

    Instance Attributes:
        - kind: the type of piece
        - is_white: whether the piece belongs to the white player
    """
    kind: str  # One of 'rqkp' (rook, queen, king, pawn)
    is_white: bool

    def __init__(self, kind: str, is_white: bool) -> None:
        """Initialize a new piece."""
        self.kind = kind
        self.is_white = is_white

    def fen(self) -> str:
        """Return the string representing this piece in FEN."""
        if self.is_white:
            return self.kind.upper()
        else:
            return self.kind

    def __str__(self) -> str:
        return self.fen()


################################################################################
# Chess player classes
################################################################################
class Player:
    """An abstract class representing a Minichess AI.

    This class can be subclassed to implement different strategies for playing chess.
    """

    def make_move(self, game: MinichessGame, previous_move: Optional[str]) -> str:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        raise NotImplementedError


class RandomPlayer(Player):
    """A Minichess AI whose strategy is always picking a random move."""

    def make_move(self, game: MinichessGame, previous_move: Optional[str]) -> str:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        possible_moves = game.get_valid_moves()
        return random.choice(possible_moves)


################################################################################
# Functions for running games
################################################################################
DEFAULT_FPS = 6  # Default number of moves per second to display in the visualization


def run_games(n: int, white: Player, black: Player,
              visualize: bool = False, fps: int = DEFAULT_FPS,
              show_stats: bool = False) -> None:
    """Run n games using the given Players.

    Optional arguments:
        - visualize: whether to use Pygame to visualize the games
        - fps: the number of moves per second to display (only relevant if visualize is True)
        - show_stats: whether to use Plotly to display statistics for the game runs

    Preconditions:
        - n >= 1
        - fps >= 1
    """
    if visualize:
        _initialize_display()

    stats = {'White': 0, 'Black': 0, 'Draw': 0}
    results = []
    for i in range(0, n):
        white_copy = copy.deepcopy(white)
        black_copy = copy.deepcopy(black)

        winner, _ = run_game(white_copy, black_copy, visualize, fps)
        stats[winner] += 1
        results.append(winner)

        print(f'Game {i} winner: {winner}')

    for outcome in stats:
        print(f'{outcome}: {stats[outcome]}/{n} ({100.0 * stats[outcome] / n:.2f}%)')

    if visualize:
        _terminate_display()

    if show_stats:
        plot_game_statistics(results)


def run_game(white: Player, black: Player,
             visualize: bool = False, fps: int = DEFAULT_FPS) -> tuple[str, list[str]]:
    """Run a Minichess game between the two given players.

    Return the winner and list of moves made in the game.
    """
    game = MinichessGame()

    move_sequence = []
    previous_move = None
    current_player = white
    while game.get_winner() is None:

        previous_move = current_player.make_move(game, previous_move)
        game.make_move(previous_move)
        move_sequence.append(previous_move)

        if visualize:
            display.update(game.get_fen(), game.get_winner())
            time.sleep(1 / fps)

        if current_player is white:
            current_player = black
        else:
            current_player = white

    if visualize:
        # Give slightly more time to the victory visualization
        time.sleep(4 / fps)

    return game.get_winner(), move_sequence


def _initialize_display() -> None:
    """Initialize the Minichess visualization pygame window."""
    display.start('8/8/8/8', size=4)


def _terminate_display() -> None:
    """Close the Minichess visualization pygame window."""
    display.terminate()


def plot_game_statistics(results: list[str]) -> None:
    """Plot the outcomes and win probabilities for a given list of Minichess game results.

    Preconditions:
        - all(r in {'White', 'Black', 'Draw'} for r in results)
    """
    outcomes = [1 if result == 'White' else 0 for result in results]

    cumulative_win_probability = [sum(outcomes[0:i]) / i for i in range(1, len(outcomes) + 1)]
    rolling_win_probability = \
        [sum(outcomes[max(i - 50, 0):i]) / min(50, i) for i in range(1, len(outcomes) + 1)]

    fig = make_subplots(rows=2, cols=1)
    fig.add_trace(go.Scatter(y=outcomes, mode='markers',
                             name='Outcome (1 = White win, 0 = Draw/Black win)'),
                  row=1, col=1)
    fig.add_trace(go.Scatter(y=cumulative_win_probability, mode='lines',
                             name='White win percentage (cumulative)'),
                  row=2, col=1)
    fig.add_trace(go.Scatter(y=rolling_win_probability, mode='lines',
                             name='White win percentage (most recent 50 games)'),
                  row=2, col=1)
    fig.update_yaxes(range=[0.0, 1.0], row=2, col=1)

    fig.update_layout(title='Minichess Game Results', xaxis_title='Game')
    fig.show()


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Demo running Minichess games being played between two random players
    # run_games(100, RandomPlayer(), RandomPlayer(), show_stats=True)

    # Try running this to visualize games (takes longer)
    # run_games(20, RandomPlayer(), RandomPlayer(), visualize=True, fps=10, show_stats=True)
