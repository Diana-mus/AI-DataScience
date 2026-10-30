"""8-puzzle board operations for Lab 01.

A state is a 3x3 tuple of tuples. The number 0 represents the blank tile.
"""

import random

GOAL_STATE = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0),
)


def is_goal(state, goal=GOAL_STATE):
    """Return True when state matches the goal; O(9) time."""
    return state == goal


def find_blank(state):
    """Return the (row, column) of tile 0; O(9) time."""
    for row in range(3):
        for col in range(3):
            if state[row][col] == 0:
                return row, col
    raise ValueError("The puzzle must contain an empty tile (0).")


def get_neighbors(state):
    """Return every state reachable by one legal blank-tile move.

    Input: a 3x3 tuple of tuples.
    Output: list of 2 to 4 new states; the original state stays unchanged.
    Time and space: O(1) for a fixed-size 8-puzzle.
    """
    blank_row, blank_col = find_blank(state)
    neighbors = []
    for row_change, col_change in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_row = blank_row + row_change
        new_col = blank_col + col_change
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            board = [list(row) for row in state]
            board[blank_row][blank_col], board[new_row][new_col] = (
                board[new_row][new_col], board[blank_row][blank_col]
            )
            neighbors.append(tuple(tuple(row) for row in board))
    return neighbors


def create_new_states(state):
    """Alias for get_neighbors(), useful when integrating with A*."""
    return get_neighbors(state)


def inversion_count(state):
    """Count out-of-order tile pairs, excluding 0; O(8^2) time."""
    tiles = [tile for row in state for tile in row if tile != 0]
    return sum(tiles[i] > tiles[j]
               for i in range(len(tiles))
               for j in range(i + 1, len(tiles)))


def is_solvable(state, goal=GOAL_STATE):
    """Check solvability for a 3x3 puzzle by inversion parity.

    For odd-width boards, state and goal are mutually reachable exactly
    when they have the same even/odd number of inversions.
    """
    tiles = [tile for row in state for tile in row]
    goal_tiles = [tile for row in goal for tile in row]
    if len(tiles) != 9 or sorted(tiles) != list(range(9)):
        raise ValueError("State must contain each tile from 0 to 8 exactly once.")
    if len(goal_tiles) != 9 or sorted(goal_tiles) != list(range(9)):
        raise ValueError("Goal must contain each tile from 0 to 8 exactly once.")
    return inversion_count(state) % 2 == inversion_count(goal) % 2


def generate_random_puzzle(moves=30, goal=GOAL_STATE):
    """Generate a solvable puzzle by making legal moves from the goal.

    Input: number of random moves (nonnegative integer).
    Output: a solvable 3x3 state. The optimal solution may be shorter
    than the number of random moves.
    """
    if not isinstance(moves, int) or moves < 0:
        raise ValueError("moves must be a nonnegative integer")
    state = goal
    previous = None
    for _ in range(moves):
        options = get_neighbors(state)
        if previous is not None:
            options = [option for option in options if option != previous]
        next_state = random.choice(options)
        previous, state = state, next_state
    return state


if __name__ == "__main__":
    easy = ((1, 2, 3), (4, 5, 6), (7, 0, 8))
    impossible = ((1, 2, 3), (4, 5, 6), (8, 7, 0))
    print("Goal detected:", is_goal(GOAL_STATE))
    print("Easy puzzle solvable:", is_solvable(easy))
    print("Impossible puzzle solvable:", is_solvable(impossible))
    print("Moves from easy puzzle:", len(get_neighbors(easy)))
    print("Random puzzle solvable:", is_solvable(generate_random_puzzle()))