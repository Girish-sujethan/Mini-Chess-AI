import random  
from typing import Optional  
  
import a2_game_tree  
import a2_minichess  
  
  
class ExploringPlayer(a2_minichess.Player):  
    """A Minichess player that plays greedily some of the time, and randomly some of the time. 
 
    See assignment handout for details. 
    """  
    # Private Instance Attributes:  
    #   - _game_tree:  
    #       The GameTree that this player uses to make its moves. If None, then this  
    #       player just makes random moves.  
    _game_tree: Optional[a2_game_tree.GameTree]  
    _exploration_probability: float  
  
    def __init__(self, game_tree: a2_game_tree.GameTree, exploration_probability: float) -> None:  
        """Initialize this player."""  
        self._game_tree = game_tree  
        self._exploration_probability = exploration_probability  
  
    def make_move(self, game: a2_minichess.MinichessGame, previous_move: Optional[str]) -> str:  
        """Make a move given the current game. 
 
        previous_move is the opponent player's most recent move, or None if no moves 
        have been made. 
 
        Preconditions: 
            - There is at least one valid move for the given game 
        """  
  
        ran_num = random.uniform(0.0, 1.0)  
  
        if self._game_tree is not None and previous_move is not None:  
            self._game_tree = self._game_tree.find_subtree_by_move(previous_move)  
  
        if self._game_tree is None or self._game_tree.get_subtrees() == []:  
            return random.choice(game.get_valid_moves())  
  
        if ran_num < self._exploration_probability:  
            self._game_tree = None  
            return random.choice(game.get_valid_moves())  
  
        else:  
            if game.is_white_move():  
                temp_subtree = self._game_tree.get_subtrees()[0]  
                for subtree in self._game_tree.get_subtrees():  
                    if subtree.white_win_probability > temp_subtree.white_win_probability:  
                        temp_subtree = subtree  
                self._game_tree = temp_subtree  
                return temp_subtree.move  
  
            else:  
                temp_subtree = self._game_tree.get_subtrees()[0]  
                for subtree in self._game_tree.get_subtrees():  
                    if subtree.white_win_probability < temp_subtree.white_win_probability:  
                        temp_subtree = subtree  
                self._game_tree = temp_subtree  
  
                return temp_subtree.move  
  
  
def run_learning_algorithm(exploration_probabilities: list[float],  
                           show_stats: bool = True) -> a2_game_tree.GameTree:  
    """Play a sequence of Minichess games using an ExploringPlayer as the White player. 
 
    This algorithm first initializes an empty GameTree. All ExploringPlayers will use this 
    SAME GameTree object, which will be mutated over the course of the algorithm! 
    Return this object. 
 
    There are len(exploration_probabilities) games played, where at game i (starting at 0): 
        - White is an ExploringPlayer (using the game tree) whose exploration probability 
            is equal to exploration_probabilities[i] 
        - Black is a RandomPlayer 
        - AFTER the game, the move sequence from the game is inserted into the game tree, 
          with a white win probability of 1.0 if White won the game, and 0.0 otherwise. 
 
    Implementation note: 
        - A NEW ExploringPlayer instance should be created for each loop iteration. 
          However, each one should use the SAME GameTree object. 
        - You should call run_game, NOT run_games, from a2_minichess. This is because you 
          need more control over what happens after each game runs, which you can get by 
          writing your own loop that calls run_game. However, you can base your loop on 
          the implementation of run_games. 
        - Note that run_game from a2_minichess returns both the winner and the move sequence 
          after the game ends. 
        - You may call print in this function to report progress made in each game. 
        - Note that this function returns the final GameTree object. You can inspect the 
          white_win_probability of its nodes, calculate its size, or and use it in a 
          RandomTreePlayer or GreedyTreePlayer to see how they do with it. 
    """  
    # Start with a GameTree in the initial state  
    game_tree = a2_game_tree.GameTree()  
  
    # Play games using the GreedyRandomPlayer and update the GameTree after each one  
    results_so_far = []  
  
    # Write your loop here, according to the description above.  
    for i in exploration_probabilities:  
        # make a copy of game_tree  
        temp_game_tree = a2_game_tree.GameTree()  
        for subtree in game_tree.get_subtrees():  
            temp_game_tree.add_subtree(subtree)  
  
        white_player = ExploringPlayer(temp_game_tree, i)  
        black_player = a2_minichess.RandomPlayer()  
        results = a2_minichess.run_game(white_player, black_player)  
  
        if results[0] == 'White':  
            game_tree.insert_move_sequence(results[1], 1.0)  
            results_so_far.append(results[0])  
  
        else:  
            game_tree.insert_move_sequence(results[1], 0.0)  
            results_so_far.append(results[0])  
  
    if show_stats:  
        a2_minichess.plot_game_statistics(results_so_far)  
  
    return game_tree  
  
  
def part3_runner() -> a2_game_tree.GameTree:  
    """Run example for Part 3. 
 
    Please note that unlike part1_runner and part2_runner, this function is NOT graded. 
    We encourage you to experiment with different exploration probability sequences 
    to see how quickly you can develop a "winning" GameTree! 
    """  
    probabilities = [0.5] * 900  
  
    return run_learning_algorithm(probabilities)  
  
  
if __name__ == '__main__':  
    import python_ta  
    python_ta.check_all(config={  
        'max-line-length': 100,  
        'max-nested-blocks': 4,  
        'disable': ['E1136'],  
        'extra-imports': ['random', 'a2_minichess', 'a2_game_tree'],  
        'allowed-io': ['run_learning_algorithm']  
    })  
  
    # part3_runner() 
