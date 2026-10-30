"""Experiments: compare the Hamming and Manhattan heuristics for A*.

Solves the same random start states (from puzzle.py) with both heuristics and
reports mean, variance and standard deviation of the measured values.
"""

import random
import statistics
import time

import heuristic
from astar import AStar
from puzzle import GOAL_STATE, generate_random_puzzle

# Number of random start states, solved once with each heuristic
NUMBER_OF_START_STATES = 100

# Fixed random seed (any constant number works): every run creates
# the same start states, so the results can be reproduced
RANDOM_SEED = 100


def run_experiment(states, heuristic_function):
    """Solve every state with A* and measure the search.

    Input: list of start states and a heuristic function.
    Output: list with one dictionary of results per state.
    """
    results = []
    for state in states:
        solver = AStar(state, GOAL_STATE, heuristic_function)

        start_time = time.perf_counter()
        path, nodes_expanded, nodes_created = solver.astar_search()
        runtime = time.perf_counter() - start_time

        results.append({
            "moves": len(path) - 1,
            "nodes_expanded": nodes_expanded,
            "nodes_created": nodes_created,
            "runtime": runtime,
        })
    return results

def summarize(results, key):
    """Return (mean, variance, standard deviation) of one measured value."""
    values = [result[key] for result in results]
    return statistics.mean(values), statistics.variance(values), statistics.stdev(values)

def print_results(name, results):
    """Print mean, variance and standard deviation of every measured value."""
    print(name)
    for key in ["moves", "nodes_expanded", "nodes_created", "runtime"]:
        mean, variance, std_dev = summarize(results, key)
        print(f"  {key:15} mean {mean:12.4f}   variance {variance:16.4f}   std dev {std_dev:12.4f}")


if __name__ == "__main__":
    random.seed(RANDOM_SEED)
    states = [generate_random_puzzle() for _ in range(NUMBER_OF_START_STATES)]

    # same start states for both heuristics
    hamming_results = run_experiment(states, heuristic.hamming)
    manhattan_results = run_experiment(states, heuristic.manhattan)

    print_results("Hamming", hamming_results)
    print()
    print_results("Manhattan", manhattan_results)