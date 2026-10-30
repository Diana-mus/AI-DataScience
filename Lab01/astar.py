# Prints a puzzle state as a 3x3 grid, blank shown as "_"
def print_puzzle(state):
    for row in range(3):
        for col in range(3):
            if state[row][col] == 0:
                print("_", end=" ")
            else:
                print(state[row][col], end=" ")
        print()


# Finds the position (row, col) of the blank tile
def find_blank(state):
    for row in range(3):
        for col in range(3):
            if state[row][col] == 0:
                return row, col


# Returns the positions of all tiles the blank can swap with
def find_blank_neighbors(state):
    row, col = find_blank(state)
    neighbors = []

    if row > 0:
        neighbors.append((row - 1, col))
    if row < 2:
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col < 2:
        neighbors.append((row, col + 1))
    return neighbors


# Returns all states reachable with one move
def create_new_states(state):
    blank_row, blank_col = find_blank(state)
    new_states = []

    for neighbor_row, neighbor_col in find_blank_neighbors(state):
        copy = [list(row) for row in state]
        copy[blank_row][blank_col], copy[neighbor_row][neighbor_col] = (
            copy[neighbor_row][neighbor_col],
            copy[blank_row][blank_col],
        )
        new_states.append(tuple(tuple(row) for row in copy))

    return new_states


class Node:
    def __init__(self, state, g, h, parent=None):
        self.state = state      # the puzzle state
        self.g = g              # g(n): moves from start to this node
        self.h = h              # h(n): estimated moves to the goal
        self.f = g + h          # f(n) = g(n) + h(n)
        self.parent = parent    # parent node: the node this one was generated from


# Returns the node with the lowest total cost (f) and removes it from the list
def find_lowest_cost_node(nodes_to_explore):
    lowest_cost_node = nodes_to_explore[0]
    for node in nodes_to_explore:
        if node.f < lowest_cost_node.f:
            lowest_cost_node = node
    nodes_to_explore.remove(lowest_cost_node)
    return lowest_cost_node


class AStar:
    def __init__(self, start_state, goal_state, heuristic):
        self.start = start_state    # start state of the puzzle
        self.goal = goal_state      # goal state of the puzzle
        self.heuristic = heuristic  # which heuristic to use

    # Follows the parent links from the goal node back to the start
    # Returns every state from start to goal
    def get_path_to_goal(self, node):
        path = []
        while node is not None:
            path.append(node.state)
            node = node.parent
        path.reverse()
        return path

    # Runs the A* search
    # Returns (path, nodes_expanded, nodes_created), path is None if no solution exists
    def astar_search(self):
        start_node = Node(self.start, 0, self.heuristic(self.start, self.goal))
        open_list = [start_node]    # nodes waiting to be explored
        closed_list = set()         # states already explored
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

            for new_state in create_new_states(current.state):
                if new_state not in closed_list:
                    g = current.g + 1
                    h = self.heuristic(new_state, self.goal)
                    open_list.append(Node(new_state, g, h, current))
                    nodes_created += 1

        return None, nodes_expanded, nodes_created


if __name__ == "__main__":
    # TEMPORARY: only for testing, real heuristics come from heuristic.py
    def hamming(state, goal):
        count = 0
        for row in range(3):
            for col in range(3):
                if state[row][col] != 0 and state[row][col] != goal[row][col]:
                    count += 1
        return count

    goal_state = ((1, 2, 3),
                  (4, 5, 6),
                  (7, 8, 0))

    test_easy = ((1, 2, 3), (4, 5, 6), (7, 0, 8))      # 1 move
    test_medium = ((1, 2, 3), (0, 4, 6), (7, 5, 8))    # 3 moves
    test_hard = ((7, 2, 4), (5, 0, 6), (8, 3, 1))      # 20 moves

    for name, start in [("easy", test_easy), ("medium", test_medium), ("hard", test_hard)]:
        solver = AStar(start, goal_state, hamming)
        path, nodes_expanded, nodes_created = solver.astar_search()
        print(name, "->", len(path) - 1, "moves,", nodes_expanded, "expanded,", nodes_created, "created")

    print()
    print("Solution for medium:")
    path, _, _ = AStar(test_medium, goal_state, hamming).astar_search()
    for step, state in enumerate(path):
        print("Step", step)
        print_puzzle(state)
        print()
