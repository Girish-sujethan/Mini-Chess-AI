import csv  
import random  
from typing import Optional  
  
import a2_game_tree  
import a2_minichess  
  
  
################################################################################  
# Loading Minichess datasets  
################################################################################  
def load_game_tree(games_file: str) -> a2_game_tree.GameTree:  
    """Create a game tree based on games_file. 
 
    Preconditions: 
        - games_file refers to a csv file in the format described on the assignment handout 
 
    Implementation hints: 
        - You can review Tutorial 4 for how we read CSV files in Python. 
    """  
    list_of_all_moves = []  
    game_tree = a2_game_tree.GameTree('*', True)  
    with open(games_file) as csv_file:  
        csv_reader = csv.reader(csv_file)  
        for row in csv_reader:  
            list_of_all_moves.append(row)  
  
    # iterate over all move sequences given and return the complete game tree  
    for sequence in list_of_all_moves:  
        game_tree.insert_move_sequence(sequence)  
  
    return game_tree  
  
  
################################################################################  
# Minichess AI that uses a GameTree  
################################################################################  
class RandomTreePlayer(a2_minichess.Player):  
    """A Minichess player that plays randomly based on a given GameTree. 
 
    This player uses a game tree to make moves, descending into the tree as the game is played. 
    On its turn: 
 
        1. First it updates its game tree to its subtree corresponding to the move made by 
           its opponent. If no subtree is found, its game tree is set to None. 
        2. Then, if its game tree is not None, it picks its next move randomly from among 
           the subtrees of its game tree, and then reassigns its game tree to that subtree. 
           But if its game tree is None or has no subtrees, the player picks its next move randomly, 
           and then sets its game tree to None. 
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
        if previous_move is not None and self._game_tree is not None:  
            existing_move = False  
  
            for subtree in self._game_tree.get_subtrees():  
                if previous_move == subtree.move:  
                    self._game_tree = subtree  
                    existing_move = True  
                    break  
            if not existing_move:  
                self._game_tree = None  
  
        if self._game_tree is None or self._game_tree.get_subtrees() == []:  
            possible_moves = game.get_valid_moves()  
            return random.choice(possible_moves)  
  
        else:  
            new_tree = random.choice(self._game_tree.get_subtrees())  
            self._game_tree = new_tree  
            return new_tree.move  
  
  
def part1_runner(games_file: str, n: int, black_random: bool) -> None:  
    """Create a game tree from the given file, and run n games where White is a RandomTreePlayer. 
 
    The White player is a RandomTreePlayer whose game tree is the one generated from games_file. 
    The Black player is a RandomPlayer if black_random is True, otherwise it is a RandomTreePlayer 
    using the SAME game tree as White. 
 
    Precondtions: 
        - n >= 1 
        - games_file refers to a csv file in the format described on the assignment handout 
 
    Implementation notes: 
        - Your implementation MUST correctly call a2_minichess.run_games. You may choose 
          the values for the optional arguments passed to the function. 
    """  
    white_player = RandomTreePlayer(load_game_tree(games_file))  
  
    if black_random:  
        black_player = a2_minichess.RandomPlayer()  
  
    else:  
        black_player = RandomTreePlayer(load_game_tree(games_file))  
  
    a2_minichess.run_games(n, white_player, black_player)  
  
  
if __name__ == '__main__':  
    import python_ta  
    python_ta.check_all(config={  
        'max-line-length': 100,  
        'disable': ['E1136'],  
        'extra-imports': ['a2_minichess', 'a2_game_tree', 'random', 'csv'],  
        'allowed-io': ['load_game_tree']  
    })  
  
    # Sample call to part1_runner (you can change this, just keep it in the main block!)  
    # part1_runner('data/white_wins.csv', 50, True)  
