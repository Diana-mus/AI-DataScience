import heuristic

"""Tests for heuristic.py: Hamming and Manhattan distance.

The tests are grouped in one class per heuristic, plus one class that
compares both.
"""

from heuristic import GOAL_STATE, hamming, manhattan

# Test states
ONE_MOVE_FROM_GOAL = ((1, 2, 3), (4, 5, 6), (7, 0, 8))   # tile 8 one step from its place
SLIDES_EXAMPLE = ((7, 2, 4), (5, 0, 6), (8, 3, 1))       # example from the lecture slides
FAR_TILES = ((7, 2, 1), (4, 5, 6), (3, 8, 0))            # few tiles misplaced but far away

# Expected values
COST_AT_GOAL = 0
HAMMING_ONE_MOVE = 1
MANHATTAN_ONE_MOVE = 1
HAMMING_SLIDES_EXAMPLE = 6
MANHATTAN_SLIDES_EXAMPLE = 14
HAMMING_FAR_TILE = 2      # only 2 tiles are misplaced ...
MANHATTAN_FAR_TILE = 6    # ... but each is 3 steps away

# Real number of moves of the shortest solution (state, optimal moves)
OPTIMAL_SOLUTIONS = [
    (GOAL_STATE, 0),
    (ONE_MOVE_FROM_GOAL, 1),
    (SLIDES_EXAMPLE, 20),
    (FAR_TILES, 24),
]

class TestHamming:
    """Tests for Hamming"""
    def test_goal_has_zero_cost(self):
        assert hamming(GOAL_STATE) == COST_AT_GOAL

    def test_goal_one_move_from_goal(self):
        assert hamming(ONE_MOVE_FROM_GOAL) == HAMMING_ONE_MOVE

    def test_slides_example(self):
        assert hamming(SLIDES_EXAMPLE) == HAMMING_SLIDES_EXAMPLE

    def test_counts_misplaced_tiles_not_distance(self):
        assert hamming(FAR_TILES) == HAMMING_FAR_TILE

class TestManhattan:
    """Tests for Manhattan"""
    def test_goal_has_zero_cost(self):
        assert manhattan(GOAL_STATE) == COST_AT_GOAL

    def test_goal_one_move_from_goal(self):
        assert manhattan(ONE_MOVE_FROM_GOAL) == MANHATTAN_ONE_MOVE

    def test_slides_example(self):
        assert manhattan(SLIDES_EXAMPLE) == MANHATTAN_SLIDES_EXAMPLE

    def test_counts_distance_of_each_tile(self):
        assert manhattan(FAR_TILES) == MANHATTAN_FAR_TILE

class TestCompareHeuristics:
    """Manhattan is always at least as large as Hamming."""

    def test_heuristics_never_overestimate(self):
        # admissible: the estimate is never larger than the real number of moves
        for state, optimal_moves in OPTIMAL_SOLUTIONS:
            assert hamming(state) <= optimal_moves
            assert manhattan(state) <= optimal_moves

    def test_manhattan_not_smaller_than_hamming(self):
        for state in (GOAL_STATE, ONE_MOVE_FROM_GOAL, SLIDES_EXAMPLE, FAR_TILES):
            assert manhattan(state) >= hamming(state)
