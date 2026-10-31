"""Tests for astar.py: Node, path reconstruction and the A* search.

The tests are grouped in one class per part of astar.py, plus one class
that compares both heuristics.
"""

from astar import AStar, Node
from heuristic import hamming, manhattan
from puzzle import GOAL_STATE, get_neighbors

# Test states with the number of moves of the shortest solution
ONE_MOVE_FROM_GOAL = ((1, 2, 3), (4, 5, 6), (7, 0, 8))
THREE_MOVES_FROM_GOAL = ((1, 2, 3), (0, 4, 6), (7, 5, 8))   # example from exercise slide 3
SLIDES_EXAMPLE = ((7, 2, 4), (5, 0, 6), (8, 3, 1))          # example from the lecture slides

MOVES_ONE = 1
MOVES_THREE = 3
MOVES_SLIDES_EXAMPLE = 20

# Values for the Node test
PATH_COST = 2
ESTIMATED_COST = 3
TOTAL_COST = 5

def solve(start, heuristic=manhattan):
    """Run A* and return (path, nodes_expanded, nodes_created)."""
    return AStar(start, GOAL_STATE, heuristic).astar_search()

class TestNode:
    """Tests for the Node class."""

    def test_total_cost_is_g_plus_h(self):
        node = Node(GOAL_STATE, PATH_COST, ESTIMATED_COST)
        assert node.f == TOTAL_COST

    def test_start_node_has_no_parent(self):
        node = Node(GOAL_STATE, 0, 0)
        assert node.parent is None

class TestGetPathToGoal:
    """Tests for AStar.get_path_to_goal()."""

    def test_follows_parent_links_from_start_to_goal(self):
        start_node = Node(ONE_MOVE_FROM_GOAL, 0, 1)
        goal_node = Node(GOAL_STATE, 1, 0, start_node)
        solver = AStar(ONE_MOVE_FROM_GOAL, GOAL_STATE, manhattan)
        assert solver.get_path_to_goal(goal_node) == [ONE_MOVE_FROM_GOAL, GOAL_STATE]

class TestAStarSearch:
    """Tests for AStar.astar_search()."""

    def test_start_is_goal(self):
        path, nodes_expanded, _ = solve(GOAL_STATE)
        assert path == [GOAL_STATE]
        assert nodes_expanded == 0

    def test_one_move(self):
        path, _, _ = solve(ONE_MOVE_FROM_GOAL)
        assert len(path) - 1 == MOVES_ONE

    def test_three_moves(self):
        path, _, _ = solve(THREE_MOVES_FROM_GOAL)
        assert len(path) - 1 == MOVES_THREE

    def test_slides_example(self):
        path, _, _ = solve(SLIDES_EXAMPLE)
        assert len(path) - 1 == MOVES_SLIDES_EXAMPLE

    def test_path_starts_at_start_and_ends_at_goal(self):
        path, _, _ = solve(SLIDES_EXAMPLE)
        assert path[0] == SLIDES_EXAMPLE
        assert path[-1] == GOAL_STATE

    def test_every_step_is_a_legal_move(self):
        path, _, _ = solve(SLIDES_EXAMPLE)
        for current_state, next_state in zip(path, path[1:]):
            assert next_state in get_neighbors(current_state)

    def test_more_nodes_created_than_expanded(self):
        _, nodes_expanded, nodes_created = solve(SLIDES_EXAMPLE)
        assert nodes_created > nodes_expanded

class TestCompareHeuristics:
    """Both heuristics find the shortest path, Manhattan needs fewer nodes."""

    def test_same_solution_length(self):
        path_hamming, _, _ = solve(SLIDES_EXAMPLE, hamming)
        path_manhattan, _, _ = solve(SLIDES_EXAMPLE, manhattan)
        assert len(path_hamming) == len(path_manhattan)

    def test_manhattan_expands_fewer_nodes(self):
        _, expanded_hamming, _ = solve(SLIDES_EXAMPLE, hamming)
        _, expanded_manhattan, _ = solve(SLIDES_EXAMPLE, manhattan)
        assert expanded_manhattan < expanded_hamming
