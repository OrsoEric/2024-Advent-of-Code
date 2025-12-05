def read_rotations_from_file(filename):
    """Reads the rotations from a file and returns a list of rotations."""
    with open(filename, 'r') as file:
        rotations = [line.strip() for line in file if line.strip()]
    return rotations

def solve_password(rotations):
    """Simulates the dial's movement and returns the number of times it points to 0."""
    position = 50  # The dial starts at 50
    count = 0

    for rotation in rotations:
        direction = rotation[0]
        steps = int(rotation[1:])

        if direction == 'L':
            position -= steps
        elif direction == 'R':
            position += steps

        # Handle circular nature of the dial
        position %= 100

        # Count if the dial points to 0 after this rotation
        if position == 0:
            count += 1

    return count

def read_rotations_from_file(filename):
    """Reads the rotations from a file and returns a list of rotations."""
    with open(filename, 'r') as file:
        rotations = [line.strip() for line in file if line.strip()]
    return rotations

def count_zero_crossings(rotations):
    """
    Simulates the dial's movement and returns the number of times it points to 0,
    including during rotations.
    """
    position = 50  # The dial starts at 50
    count = 0

    for rotation in rotations:
        direction = rotation[0]
        steps = int(rotation[1:])

        if direction == 'L':
            for _ in range(steps):
                position -= 1
                position %= 100
                if position == 0:
                    count += 1
        elif direction == 'R':
            for _ in range(steps):
                position += 1
                position %= 100
                if position == 0:
                    count += 1

    return count



# Example usage:
rotations = [
    "L68", "L30", "R48", "L5", "R60", "L55", "L1", "L99", "R14", "L82"
]
print(solve_password(rotations))  # Output: 3


# Example usage:
rotations = read_rotations_from_file('input.txt')
result = solve_password(rotations)
print(result) 

# Example usage:
rotations = read_rotations_from_file('input.txt')
result = count_zero_crossings(rotations)
print(result)  # Output: 6
