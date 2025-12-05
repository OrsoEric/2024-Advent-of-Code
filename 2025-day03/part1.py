from typing import List

def find_max_joltage(i_bank: str) -> int:
    """
    Finds the maximum joltage possible from a bank of batteries.

    Parameters:
    i_bank (str): A string representing a bank of batteries.

    Returns:
    int: The maximum joltage possible from the bank.
    """
    max_joltage = 0
    for i in range(len(i_bank)):
        for j in range(i + 1, len(i_bank)):
            current_joltage = int(i_bank[i] + i_bank[j])
            if current_joltage > max_joltage:
                max_joltage = current_joltage
    return max_joltage

def solve_puzzle(i_filename: str) -> int:
    """
    Solves the puzzle by reading the input file and calculating the total output joltage.

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
        total_joltage += find_max_joltage(line)

    return total_joltage

# Example usage:
total_joltage = solve_puzzle("input-part1-example.txt")
print(total_joltage)

# Example usage:
total_joltage = solve_puzzle("input-part1.txt")
print(total_joltage)