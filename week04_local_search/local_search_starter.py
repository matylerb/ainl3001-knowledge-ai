"""
AINL3001 — Knowledge-Driven AI
Week 4 — Local Search and Optimisation
BSP 2026

This week introduces local search.

In previous weeks, search algorithms explored paths through
a state space in order to reach a goal.

Local search takes a different approach:

    1. Start with a state.
    2. Evaluate how good that state is.
    3. Generate neighbouring states.
    4. Move to a better neighbour.
    5. Repeat.

We will explore this using the N-Queens problem.

Tasks
-----

1. Understand the problem representation.
2. Implement conflict counting.
3. Explore neighbouring states.
4. Implement Hill Climbing.
5. Implement Simulated Annealing.
"""

import math
import random

from queens_problem import QueensProblem

N = 8


# --------------------------------------------------
# TASK 0 — UNDERSTANDING THE STATE
# --------------------------------------------------

example_board = [0, 1, 2, 3]

print("Manual Exploration Board:")
print(example_board)

print(
    "\nEach list position represents a column."
)

print(
    "Each value represents the row containing the queen."
)

print(
    "\nQuestion: How many conflicts exist on this board?"
)


# --------------------------------------------------
# TASK 1 — EVALUATE A STATE
# --------------------------------------------------

def count_conflicts(board):
    """
    Return the number of pairs of queens
    that attack each other.

    Lower values are better.

    A solution has:

        conflict count = 0
    """

    # TODO:
    # Compare each queen with every queen
    # that comes after it.
    #
    # Queens conflict when they are:
    #
    #   1. in the same row
    #   2. on the same diagonal

    conflicts = 0  # start with zero conflicts

    for i in range(len(board)):  # loop over every column
        for j in range(i + 1, len(board)):  # compare with every column after i (avoids checking pairs twice)
            if board[i] == board[j]:  # same row = conflict
                conflicts += 1
            if abs(board[i] - board[j]) == abs(i - j):  # same diagonal = conflict
                conflicts += 1

    return conflicts  # total number of attacking pairs


# --------------------------------------------------
# TASK 2 — EXPLORE THE PROBLEM
# --------------------------------------------------

def generate_neighbours(problem, board):
    """
    Generate all neighbouring boards.

    Use the Problem interface introduced this week:

        problem.actions(state)
        problem.result(state, action)
    """

    neighbours = []  # list to collect all neighbouring boards

    actions = problem.actions(board)  # get every possible move from the current board

    for action in actions:  # loop over each possible move
        neighbours.append(problem.result(board, action))  # apply the move and add the resulting board

    return neighbours  # return all neighbouring boards


# --------------------------------------------------
# TASK 3 — HILL CLIMBING
# --------------------------------------------------

def hill_climbing(problem, start_board):
    """
    Use Hill Climbing to reduce the number
    of conflicts.

    Algorithm:

        current = start state

        repeat:

            generate neighbours

            find the neighbour with the
            lowest conflict count

            if the neighbour is not better:
                stop

            otherwise:
                move to the neighbour

        return current
    """

    current = start_board  # start from the given board

    # TODO

    while True:  # keep going until we manually break out
        neighbours = generate_neighbours(problem, current)  # get all boards reachable in one move
        best = min(neighbours, key=count_conflicts)  # find the neighbour with the fewest conflicts

        if count_conflicts(best) < count_conflicts(current):  # if best neighbour is better than current
            current = best  # move to it
        else:
            break  # no improvement possible, stop

    return current  # return the best board found


# --------------------------------------------------
# TASK 4 — SIMULATED ANNEALING
# --------------------------------------------------

def simulated_annealing(problem, start_board):
    """
    Use Simulated Annealing to search for
    a solution.

    Unlike Hill Climbing, Simulated Annealing
    can sometimes accept a worse state.

    This can help escape local minima.
    """

    current = start_board  # start from the given board

    temperature = 10.0  # start hot — willing to accept bad moves
    cooling_rate = 0.95  # multiply temperature by this each iteration to cool down

    # TODO

    while temperature > 0.1:  # keep going until temperature is too cold
        neighbours = generate_neighbours(problem, current)  # get all boards reachable in one move
        next_board = random.choice(neighbours)  # pick a random neighbour (not necessarily the best)

        delta = count_conflicts(next_board) - count_conflicts(current)  # positive = worse, negative = better

        if delta < 0:  # next_board has fewer conflicts — always move to it
            current = next_board
        elif random.random() < math.exp(-delta / temperature):  # next_board is worse — maybe move anyway
            current = next_board  # high temperature makes this more likely

        temperature *= cooling_rate  # cool down by 5% each iteration

    return current  # return the best board found


# --------------------------------------------------
# TESTING AREA
# --------------------------------------------------

if __name__ == "__main__":

    board = [
        random.randint(0, N - 1)
        for _ in range(N)
    ]

    problem = QueensProblem(board)

    print("\nRandom Board")
    print(board)

    print("\nConflicts")
    print(
        count_conflicts(board)
    )

    print("\nPossible Actions")

    actions = problem.actions(board)

    print(
        f"{len(actions)} actions available"
    )

    print("\nNeighbours")

    neighbours = generate_neighbours(
        problem,
        board
    )

    print(
        f"{len(neighbours)} neighbours generated"
    )

    print("\n--- Hill Climbing ---")
    print("Start board:", board)
    print("Start cost:", count_conflicts(board))
    hc_result = hill_climbing(problem, board)
    print("End board:", hc_result)
    print("Final cost:", count_conflicts(hc_result))

    print("\n--- Simulated Annealing ---")
    print("Start board:", board)
    print("Start cost:", count_conflicts(board))
    sa_result = simulated_annealing(problem, board)
    print("End board:", sa_result)
    print("Final cost:", count_conflicts(sa_result))


# --------------------------------------------------
# EXTENSION 1 — VISUALISE THE BOARD
# --------------------------------------------------

def visualise_board(board):
    n = len(board)
    for row in range(n):
        line = ""
        for col in range(n):
            if board[col] == row:
                line += "Q "
            else:
                line += ". "
        print(line.strip())


# --------------------------------------------------
# EXTENSION 2 — RANDOM RESTART HILL CLIMBING
# --------------------------------------------------

def random_restart_hill_climbing(problem, n, max_restarts=100):
    for attempt in range(max_restarts):
        board = [random.randint(0, n - 1) for _ in range(n)]
        problem = QueensProblem(board)
        result = hill_climbing(problem, board)
        if count_conflicts(result) == 0:
            print(f"Solution found after {attempt + 1} restart(s)")
            return result
    print(f"No solution found after {max_restarts} restarts")
    return result


# --------------------------------------------------
# EXTENSION 3 — LARGER BOARDS
# --------------------------------------------------

def test_larger_boards():
    import time
    for n in [8, 20, 50]:
        board = [random.randint(0, n - 1) for _ in range(n)]
        problem = QueensProblem(board)

        start = time.time()
        hc_result = hill_climbing(problem, board)
        hc_time = time.time() - start

        start = time.time()
        sa_result = simulated_annealing(problem, board)
        sa_time = time.time() - start

        neighbours = generate_neighbours(problem, board)

        print(f"\nN={n}")
        print(f"  Neighbours:           {len(neighbours)}")
        print(f"  Hill Climbing cost:   {count_conflicts(hc_result)}  ({hc_time:.3f}s)")
        print(f"  Simulated Annealing:  {count_conflicts(sa_result)}  ({sa_time:.3f}s)")