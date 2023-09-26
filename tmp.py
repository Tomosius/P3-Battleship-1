def find_ship_and_coordinates(ship_data, target_coordinates):
    """
    Find the ship name and the list ID of coordinates to which the target_coordinates belong.

    Args:
        ship_data (dict): Dictionary containing ship information.
        target_coordinates (list): Coordinates to search for.

    Returns:
        tuple: A tuple containing the ship name and coordinates list ID if found, otherwise (None, None).
    """
    for ship_name, ship_info in ship_data.items():
        for list_id, coordinates_list in enumerate(ship_info['Coordinates']):
            if target_coordinates in coordinates_list:
                return ship_name, list_id

    # If coordinates are not found, return (None, None)
    return None, None

# Example usage
ship_data = {
    'AircraftCarrier': {'Size': 5, 'Quantity': 1, 'Coordinates': [[[5, 8], [6, 8], [7, 8], [8, 8], [9, 8]]]},
    'Battleship': {'Size': 4, 'Quantity': 3, 'Coordinates': [[[7, 0], [7, 1], [7, 2], [7, 3]], [[2, 3], [3, 3], [4, 3], [5, 3]], [[4, 6], [4, 7], [4, 8], [4, 9]]]},
    'Cruiser': {'Size': 3, 'Quantity': 0, 'Coordinates': []},
    'Submarine': {'Size': 3, 'Quantity': 0, 'Coordinates': []},
    'Destroyer': {'Size': 2, 'Quantity': 0, 'Coordinates': []},
    'DingyBoat': {'Size': 1, 'Quantity': 0, 'Coordinates': []}
}

target_coordinates = [4, 3]

ship_name, list_id = find_ship_and_coordinates(ship_data, target_coordinates)

if ship_name is not None and list_id is not None:
    print(f"The coordinates {target_coordinates} belong to ship '{ship_name}' in list {list_id}.")
    print(ship_data[ship_name]["Coordinates"][list_id])
else:
    print("Coordinates not found in any ship.")


# Define color dictionary
COLORS = {
    "DarkYellow": "\u001b[33m",
    "DarkBlue": "\u001b[34m",
    "DarkGreen": "\u001b[32m",
    "DarkRed": "\u001b[31m",
    "LightGray": "\u001b[37m",
    "Reset": "\u001b[0m",
}

# Define ship symbols dictionary
SHIP_SYMBOLS = {
    "Single": [COLORS["DarkYellow"] + chr(0x25C6) + COLORS["Reset"]],
    "Horizontal": [
        [COLORS["DarkBlue"] + chr(0x25C0) + COLORS["Reset"]],
        [COLORS["DarkBlue"] + chr(0x25A4) + COLORS["Reset"]]
    ],
    "Vertical": [
        [COLORS["DarkGreen"] + chr(0x25B2) + COLORS["Reset"]],
        [COLORS["DarkGreen"] + chr(0x25A5) + COLORS["Reset"]]
    ],
    "Hit": [COLORS["DarkRed"] + chr(0x25A6) + COLORS["Reset"]],
    "Miss": [COLORS["LightGray"] + chr(0x2022) + COLORS["Reset"]],
    "SingleSunk": [COLORS["DarkRed"] + chr(0x25C6) + COLORS["Reset"]],
    "HorizontalSunk": [
        [COLORS["DarkRed"] + chr(0x25C0) + COLORS["Reset"]],
        [COLORS["DarkRed"] + chr(0x25A4) + COLORS["Reset"]]
    ],
    "VerticalSunk": [
        [COLORS["DarkRed"] + chr(0x25B2) + COLORS["Reset"]],
        [COLORS["DarkRed"] + chr(0x25A5) + COLORS["Reset"]]
    ],
}

a = SHIP_SYMBOLS["Hit"]
b = SHIP_SYMBOLS["Vertical"][1]
print(a,b)
print