"""A* search for the 8-puzzle.

A state is a 3x3 tuple of tuples. The number 0 represents the blank tile.
Puzzle rules come from puzzle.py, heuristics from heuristic.py.
"""

from puzzle import get_neighbors


class Node:
    """One node in the A* search tree.

    Stores a puzzle state together with its costs and the node it was
    generated from, so the solution path can be rebuilt at the end.
    """

    def __init__(self, state, g, h, parent=None):
        """Create a node with g, h, f = g + h and its parent; O(1) time."""
        self.state = state
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent


def find_lowest_cost_node(nodes_to_explore):
    """Remove and return the node with the lowest f from the open list.

    Input: non-empty list of nodes.
    Output: the node with the lowest f; it is removed from the list.
    Time: O(n) for n nodes in the list (linear scan plus removal).
    """
    lowest_cost_node = nodes_to_explore[0]
    for node in nodes_to_explore:
        if node.f < lowest_cost_node.f:
            lowest_cost_node = node
    nodes_to_explore.remove(lowest_cost_node)
    return lowest_cost_node


class AStar:
    """A* search that solves one 8-puzzle with a given heuristic."""

    def __init__(self, start_state, goal_state, heuristic):
        """Store start, goal and the heuristic, called as heuristic(state, goal)."""
        self.start = start_state
        self.goal = goal_state
        self.heuristic = heuristic

    def get_path_to_goal(self, node):
        """Rebuild the solution by following the parent links.

        Input: the goal node.
        Output: list of states from the start to the goal.
        Time and space: O(d) for a solution with d moves.
        """
        path = []
        while node is not None:
            path.append(node.state)
            node = node.parent
        path.reverse()
        return path

    def astar_search(self):
        """Find the shortest solution with A* (f = g + h).

        Always expands the open-list node with the lowest f. States that
        were already expanded are kept in a closed set and skipped.
        Output: (path, nodes_expanded, nodes_created); path is None if no
        solution exists.
        Time: up to O(b^d) nodes (b = about 2.67 moves per state,
        d = solution length). Picking the lowest f from a plain list
        takes O(n), so the whole search is O(N^2) for N created nodes.
        Space: O(N) for the open list and the closed set.
        """
        start_node = Node(self.start, 0, self.heuristic(self.start, self.goal))
        open_list = [start_node]
        closed_list = set()
        nodes_expanded = 0
        nodes_created = 1

        while open_list:
            current = find_lowest_cost_node(open_list)

            if current.state == self.goal:
                return self.get_path_to_goal(current), nodes_expanded, nodes_created

            if current.state in closed_list:
                continue
            closed_list.add(current.state)
            nodes_expanded += 1

            for new_state in get_neighbors(current.state):
                if new_state not in closed_list:
                    g = current.g + 1
                    h = self.heuristic(new_state, self.goal)
                    open_list.append(Node(new_state, g, h, current))
                    nodes_created += 1

        return None, nodes_expanded, nodes_created


def print_puzzle(state):
    """Print a state as a 3x3 grid with the blank shown as "_"; O(9) time."""
    for row in range(3):
        for col in range(3):
            if state[row][col] == 0:
                print("_", end=" ")
            else:
                print(state[row][col], end=" ")
        print()


if __name__ == "__main__":
    from heuristic import hamming, manhattan
    from puzzle import GOAL_STATE

    test_easy = ((1, 2, 3), (4, 5, 6), (7, 0, 8))      # 1 move
    test_medium = ((1, 2, 3), (0, 4, 6), (7, 5, 8))    # 3 moves
    test_hard = ((7, 2, 4), (5, 0, 6), (8, 3, 1))      # 20 moves

    for heuristic in (hamming, manhattan):
        print(heuristic.__name__)
        for name, start in [("easy", test_easy), ("medium", test_medium), ("hard", test_hard)]:
            solver = AStar(start, GOAL_STATE, heuristic)
            path, nodes_expanded, nodes_created = solver.astar_search()
            print(" ", name, "->", len(path) - 1, "moves,",
                  nodes_expanded, "expanded,", nodes_created, "created")
        print()
