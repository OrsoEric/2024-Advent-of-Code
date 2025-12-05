import logging
from typing import List
from itertools import combinations

def find_max_joltage_part2(i_bank: str) -> int:
    """
    Finds the maximum joltage possible from a bank of batteries by turning on exactly 12 batteries.

    Parameters:
    i_bank (str): A string representing a bank of batteries.

    Returns:
    int: The maximum joltage possible from the bank.
    """
    max_joltage = 0
    # Generate all possible combinations of 12 batteries
    for indices in combinations(range(len(i_bank)), 12):
        # Extract the digits at the selected indices
        selected_digits = [i_bank[i] for i in indices]
        # Sort the indices to maintain the original order
        selected_digits_sorted = [i_bank[i] for i in sorted(indices)]
        # Calculate the joltage
        current_joltage = int(''.join(selected_digits_sorted))
        if current_joltage > max_joltage:
            max_joltage = current_joltage
    return max_joltage


def find_max_joltage_part2_fast(i_bank: str) -> int:
    """
    Finds the maximum joltage possible from a bank of batteries by turning on exactly 12 batteries.

    Parameters:
    i_bank (str): A string representing a bank of batteries.

    Returns:
    int: The maximum joltage possible from the bank.
    """
    n = len(i_bank)
    k = 12
    # dp[i][j] = max number using j digits from first i digits
    dp = [[-1 for _ in range(k+1)] for __ in range(n+1)]
    dp[0][0] = 0

    for i in range(1, n+1):
        for j in range(0, k+1):
            if dp[i-1][j] != -1:
                # Option 1: skip the i-th digit
                if dp[i][j] < dp[i-1][j]:
                    dp[i][j] = dp[i-1][j]
                # Option 2: take the i-th digit
                if j < k and dp[i-1][j] != -1:
                    new_num = dp[i-1][j] * 10 + int(i_bank[i-1])
                    if new_num > dp[i][j+1]:
                        dp[i][j+1] = new_num
    return dp[n][k]


def solve_puzzle_part2(i_filename: str) -> int:
    """
    Solves the puzzle for part 2 by reading the input file and calculating the total output joltage.

    Parameters:
    i_filename (str): The name of the input file.

    Returns:
    int: The total output joltage.
    """
    with open(i_filename, 'r') as file:
        lines = file.readlines()
    total_joltage = 0
    for line in lines:
        line = line.strip()
        logging.debug(f"Processing bank: {line}")
        max_joltage = find_max_joltage_part2_fast(line)
        logging.info(f"Max joltage for bank {line}: {max_joltage}")
        total_joltage += max_joltage
    return total_joltage

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        filename="part2.log",
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s',
        filemode='w'
    )
    logging.info("Begin")

    # Example usage:
    total_joltage_part2_example = solve_puzzle_part2("input-part1-example.txt")
    logging.info(f"Example total joltage: {total_joltage_part2_example}")
    print(total_joltage_part2_example)

    # Real usage:
    total_joltage_part2 = solve_puzzle_part2("input-part1.txt")
    logging.info(f"Total joltage: {total_joltage_part2}")
    print(total_joltage_part2)
