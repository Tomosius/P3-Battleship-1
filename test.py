# Define the map size
map_size = 15
map = [[0 for _ in range(map_size)] for _ in range(map_size)]

# Define the pattern size
size = 5
width = size * 2 - 1
height = size * 2 - 1

# Create the pattern with zeros
pattern = [[0 for _ in range(width)] for _ in range(height)]

# Function to check if a pattern exists at a given position
def pattern_exists(map, pattern, x, y):
    for i in range(len(pattern)):
        for j in range(len(pattern[0])):
            if pattern[i][j] != map[y + i][x + j]:
                return False
    return True

# Search for the pattern within the map
coordinates = []
for y in range(map_size - height + 1):
    for x in range(map_size - width + 1):
        if pattern_exists(map, pattern, x, y):
            coordinates.append((x, y))

# Print the coordinates where the pattern was found
if coordinates:
    print("Pattern found at the following coordinates:")
    for coord in coordinates:
        print(f"Coordinates: ({coord[0]}, {coord[1]})")
else:
    print("Pattern not found in the map.")
