"""Tests for puzzle.py: board operations, solvability and random puzzles."""

from puzzle import (GOAL_STATE, find_blank, generate_random_puzzle,
                    get_neighbors, is_goal, is_solvable)

# Test states
ONE_MOVE_FROM_GOAL = ((1, 2, 3), (4, 5, 6), (7, 0, 8))  # blank on bottom edge
CENTER_BLANK = ((1, 2, 3), (4, 0, 5), (6, 7, 8))  # blank in the center
CENTER_BLANK_MOVED_UP = ((1, 0, 3), (4, 2, 5), (6, 7, 8))  # center blank after moving up
UNSOLVABLE_STATE = ((1, 2, 3), (4, 5, 6), (8, 7, 0))  # tiles 7 and 8 swapped

# Expected values
GOAL_BLANK_POSITION = (2, 2)  # bottom right corner
MOVES_FROM_CORNER = 2
MOVES_FROM_EDGE = 3
MOVES_FROM_CENTER = 4

# Number of random puzzles to check
NUMBER_OF_RANDOM_PUZZLES = 50

class TestIsGoal:
    """Tests for is_goal()."""

    def test_goal_is_detected(self):
        assert is_goal(GOAL_STATE)

    def test_other_state_is_not_goal(self):
        assert not is_goal(ONE_MOVE_FROM_GOAL)


class TestFindBlank:
    """Tests for find_blank()."""

    def test_blank_in_goal_is_bottom_right(self):
        assert find_blank(GOAL_STATE) == GOAL_BLANK_POSITION


class TestGetNeighbors:
    """Tests for get_neighbors()."""

    def test_corner_has_two_neighbors(self):
        assert len(get_neighbors(GOAL_STATE)) == MOVES_FROM_CORNER

    def test_edge_has_three_neighbors(self):
        assert len(get_neighbors(ONE_MOVE_FROM_GOAL)) == MOVES_FROM_EDGE

    def test_center_has_four_neighbors(self):
        assert len(get_neighbors(CENTER_BLANK)) == MOVES_FROM_CENTER

    def test_contains_expected_move(self):
        assert CENTER_BLANK_MOVED_UP in get_neighbors(CENTER_BLANK)

    def test_original_state_is_unchanged(self):
        state = CENTER_BLANK
        get_neighbors(state)
        assert state == ((1, 2, 3), (4, 0, 5), (6, 7, 8))


class TestIsSolvable:
    """Tests for is_solvable()."""

    def test_solvable_state(self):
        assert is_solvable(ONE_MOVE_FROM_GOAL)

    def test_unsolvable_state(self):
        assert not is_solvable(UNSOLVABLE_STATE)


class TestGenerateRandomPuzzle:
    """Tests for generate_random_puzzle()."""

    def test_random_puzzles_are_solvable(self):
        for _ in range(NUMBER_OF_RANDOM_PUZZLES):
            assert is_solvable(generate_random_puzzle())
