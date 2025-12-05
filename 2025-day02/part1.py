from typing import List, Tuple

def load_puzzle_input(i_filename: str) -> List[Tuple[int, int]]:
    """
    Loads the puzzle input from a file and returns a list of ranges as tuples.

    Parameters:
    i_filename (str): The name of the file containing the ranges.

    Returns:
    List[Tuple[int, int]]: A list of tuples, each representing a range.
    """
    with open(i_filename, 'r') as f_file:
        s_input = f_file.read().strip()
    ln_ranges = []
    for s_range in s_input.split(','):
        s_start, s_end = s_range.split('-')
        ln_ranges.append((int(s_start), int(s_end)))
    return ln_ranges

def is_invalid_id(i_id: int) -> bool:
    """
    Checks if an ID is invalid (i.e., made of a sequence of digits repeated exactly twice).

    Parameters:
    i_id (int): The ID to check.

    Returns:
    bool: True if the ID is invalid, False otherwise.
    """
    s_id = str(i_id)
    n_length = len(s_id)
    if n_length % 2 != 0:
        return False
    n_half = n_length // 2
    return s_id[:n_half] == s_id[n_half:]


def solve(i_ranges: List[Tuple[int, int]]) -> int:
    """
    Solves the problem by iterating through the ranges and summing invalid IDs.

    Parameters:
    i_ranges (List[Tuple[int, int]]): The list of ranges to check.

    Returns:
    int: The sum of all invalid IDs.
    """
    n_sum = 0
    for tn_range in i_ranges:
        n_start, n_end = tn_range
        for n_id in range(n_start, n_end + 1):
            if is_invalid_id(n_id):
                n_sum += n_id
    return n_sum

# Example usage
s_example_filename = "input-part1-example.txt"
s_problem_filename = "input-part1.txt"

# Solve the example
ln_example_ranges = load_puzzle_input(s_example_filename)
n_example_result = solve(ln_example_ranges)
print(f"The sum of invalid IDs in the example is: {n_example_result}")

# Solve the problem
ln_problem_ranges = load_puzzle_input(s_problem_filename)
n_problem_result = solve(ln_problem_ranges)
print(f"The sum of invalid IDs in the problem is: {n_problem_result}")
