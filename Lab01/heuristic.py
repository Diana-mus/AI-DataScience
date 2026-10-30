"""Two admissible heuristics for A* search on the 8-puzzle."""

GOAL_STATE = ((1, 2, 3), (4, 5, 6), (7, 8, 0))


def hamming(state, goal=GOAL_STATE):
    """Count misplaced numbered tiles (not the blank 0).

    Input: state and goal as 3x3 tuples of tuples.
    Output: nonnegative integer h(n).
    Time: O(9) for a fixed 3x3 board.
    """
    misplaced = 0
    for row in range(3):
        for col in range(3):
            tile = state[row][col]
            if tile != 0 and tile != goal[row][col]:
                misplaced += 1
    return misplaced


def manhattan(state, goal=GOAL_STATE):
    """Sum horizontal + vertical distances of all numbered tiles.

    The blank tile is excluded. This heuristic does not overestimate
    the number of moves needed to reach the goal.
    Input: state and goal as 3x3 tuples of tuples.
    Output: nonnegative integer h(n).
    Time: O(9) for a fixed 3x3 board.
    """
    goal_positions = {}
    for row in range(3):
        for col in range(3):
            goal_positions[goal[row][col]] = (row, col)

    total_distance = 0
    for row in range(3):
        for col in range(3):
            tile = state[row][col]
            if tile != 0:
                target_row, target_col = goal_positions[tile]
                total_distance += abs(row - target_row) + abs(col - target_col)
    return total_distance


if __name__ == "__main__":
    easy = ((1, 2, 3), (4, 5, 6), (7, 0, 8))
    example_from_slides = ((7, 2, 4), (5, 0, 6), (8, 3, 1))
    print("Easy: Hamming =", hamming(easy), "Manhattan =", manhattan(easy))
    print("Slides: Hamming =", hamming(example_from_slides),
          "Manhattan =", manhattan(example_from_slides))