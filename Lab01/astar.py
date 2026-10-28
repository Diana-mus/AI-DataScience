class Node:
    def __init__(self, state,  path_cost = 0, estimated_cost = 0, parent = None):
        # the puzzle state
        self.state = state

        # g(n): cost from start to the current node
        self.path_cost = path_cost

        # h(n): estimated cost of the goal
        self.estimated_cost = estimated_cost

        # f(n) = g(n) + h(n)
        self.total_cost = path_cost + estimated_cost

        # parent node: the node this one was generated from
        self.parent = parent

# Returns the node with the lowest total cost (f) and removes it from the list
def find_lowest_cost_node(nodes_to_explore):
        lowest_cost_node = nodes_to_explore[0]
        for node in nodes_to_explore:
            if node.total_cost < lowest_cost_node.total_cost:
                lowest_cost_node = node
        nodes_to_explore.remove(lowest_cost_node)
        return lowest_cost_node

class AStar:
    def __init__(self, start_state, goal_state, heuristic):
        # start state of the puzzle
        self.start = start_state

        # end state of the puzzle
        self.goal = goal_state

        # which heuristic to use
        self.heuristic = heuristic



# Finds a specific tile in the given puzzle state
def find_tile_by_number(state, tile_to_find):
    if tile_to_find < 0 or tile_to_find > 8:
        return -1, -1

    for row in range(3):
        for col in range(3):
            if state[row][col] == tile_to_find:
                return row, col
    return -1, -1

def find_tiles_by_row_and_col(state, row, col):
    if row < 0 or row > 2 or col < 0 or col > 2:
        return None
    return state[row][col]

def find_blank_tile_neighbors(state):
    blank_row, blank_col = find_tile_by_number(state, 0)
    neighbors = {}

    if blank_col > 0:
        left_neighbor = find_tiles_by_row_and_col(state, blank_row, blank_col - 1)
        neighbors[left_neighbor] = (blank_row, blank_col - 1)

    if blank_col < 2:
        right_neighbor = find_tiles_by_row_and_col(state, blank_row, blank_col + 1)
        neighbors[right_neighbor] = (blank_row, blank_col + 1)

    if blank_row > 0:
        top_neighbor = find_tiles_by_row_and_col(state, blank_row - 1, blank_col)
        neighbors[top_neighbor] = (blank_row - 1, blank_col)

    if blank_row < 2:
        bottom_neighbor = find_tiles_by_row_and_col(state, blank_row + 1, blank_col)
        neighbors[bottom_neighbor] = (blank_row + 1, blank_col)

    return neighbors


def create_new_states(state):
    neighbors = find_blank_tile_neighbors(state)
    blank_row, blank_col = find_tile_by_number(state, 0)
    generated_states = []
    for neighbor_row, neighbor_col in neighbors.values():
        grid = []
        for row in state:
            grid.append(list(row))
        grid[blank_row][blank_col] = grid[neighbor_row][neighbor_col]
        grid[neighbor_row][neighbor_col] = 0
        generated_states.append(tuple(tuple(row) for row in grid))
    return generated_states



goal = ((1, 2, 3),
        (4, 5, 6),
        (7, 8, 0))

test_medium =  ((1, 2, 3),
               (4, 0, 6),
               (7, 5, 8))

test_easy = ((1, 2, 3),
             (4, 5, 6),
             (7, 0, 8))

test_hard = ((7, 2, 4),
             (5, 0, 6),
             (8, 3, 1))


#next_states = create_new_states(test_medium)
#print(next_states)