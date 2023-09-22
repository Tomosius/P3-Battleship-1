# Define ship symbols
shipSymbols = {
    "Hit": ["X"],
    "Miss": ["."],
}

# Initialize the game map
map_size = 10  # Adjust the size as needed
map = [[shipSymbols["Miss"][0] for _ in range(map_size)] for _ in range(map_size)]

# Initialize CPU shoot history
cpuSHOOT = []

# Define the battleship fleet
battleshipFleet = {
    "Aircraft Carrier": {
        "Size": 5,
        "Quantity": 1,
        "Coordinates": [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]]
    },
    "Battleship": {
        "Size": 4,
        "Quantity": 1,
        "Coordinates": [[2, 3], [2, 4], [2, 5], [2, 6]]
    },
    "Submarine": {
        "Size": 3,
        "Quantity": 2,
        "Coordinates": [
            [[4, 8], [4, 9], [4, 10]],
            [[6, 2], [6, 3], [6, 4]]
        ]
    },
    # ... other ship types ...
}
target_coordinates = [6, 2]
ship_index = None

for ship_name, ship_data in battleshipFleet.items():
    for index, coordinates in enumerate(ship_data["Coordinates"]):
        if target_coordinates in coordinates:
            ship_index = index
            break  # Exit the loop if the coordinates are found in a ship
            

if ship_index is not None:
    print(f"The coordinates {target_coordinates} belong to the ship with index {ship_index}.")
else:
    print(f"The coordinates {target_coordinates} are not part of any ship.")
