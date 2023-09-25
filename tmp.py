

# Example usage:
map_data = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
]

pattern_to_find = [
    [1, 1],
    [1, 1],
]

found_coordinates = find_all_patterns(map_data, pattern_to_find)
print("Pattern found at coordinates:", found_coordinates)
