"""CSC111 Winter 2021 Assignment 2: Trees, Chess, and Artificial Intelligence (Part 0)

Module Description
===============================

This Python module contains a sample GameTree that matches an example from the assignment
handout. Please feel free to modify this file to experiment with the code found in
a2_game_tree.py and a2_minichess.py. You won't be submitting this file for grading (nor
will this file affect other parts of this assignment).

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 David Liu and Isaac Waller.
"""
from a2_game_tree import GameTree, GAME_START_MOVE


def build_sample_game_tree() -> GameTree:
    """Create an example game tree."""
    game_tree = GameTree(GAME_START_MOVE, True)

    game_tree.add_subtree(GameTree('a2b3', False, 0.2))
    game_tree.add_subtree(GameTree('b2c3', False, 0.3))
    game_tree.add_subtree(GameTree('b2a3', False, 0.1))

    sub1 = GameTree('c2d3', False, 0.5)
    sub2 = GameTree('d4d3', True, 0.12)
    sub2.add_subtree(GameTree('d2c3', False, 0.69))
    sub2.add_subtree(GameTree('b1d3', False, 0.12))
    sub1.add_subtree(sub2)
    game_tree.add_subtree(sub1)

    game_tree.add_subtree(GameTree('c2b3', False,0.5))
    game_tree.add_subtree(GameTree('d2c3', False, 0.2))

    return game_tree
