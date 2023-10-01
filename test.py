# battleship.py test.py - this is code for testing cpu vs cpu game

# Import required libraries
import random # library to generate random
import copy # library to make copies of lists and etc, will use function deepcopy
import os # library to clear terminal
import re # library to calculate string lengths when printing maps on terminal, so they are aligned


# Constants for map dimensions and default symbol
MAP_HEIGHT = 20
MAP_WIDTH = 20
DEFAULT_SYMBOL = '0'  # New global variable for the default symbol

# Create maps for CPU and Player
map_cpu = [[DEFAULT_SYMBOL for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]  
map_cpu_hidden = [[DEFAULT_SYMBOL for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]  
map_player_hidden = [[DEFAULT_SYMBOL for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]  
map_player = [[DEFAULT_SYMBOL for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]  


# Initialize game-related variables
game_result = None  # Store the game result (win, lose, or draw)
cpu_actions = []  # List to store CPU actions (shots, hit/miss, coordinates)
player_actions = []  # List to store Player actions (shots)
cpu_shoot_coordinates_log = [["x","y"]]  # List to store CPU's shot coordinates


def clear_terminal():
    """Clear the terminal screen."""
    if os.name == 'posix':  # Unix/Linux/MacOS
        os.system('clear')
    elif os.name == 'nt':  # Windows
        os.system('cls')


def initialize_maps(width, height):
    """Initialize a 2D map with zeros.
    Args:
        width (int): The width of the map.
        height (int): The height of the map.
    Returns:
        list: A 2D list filled with zeros.
    """
    global DEFAULT_SYMBOL  # Declare global variable
    return [[DEFAULT_SYMBOL for _ in range(height)] for _ in range(width)]


# Default settings for the fleet
DEFAULT_FLEET = {
    "AircraftCarrier": {"Size": 5, "Quantity": 1, "Coordinates": []},
    "Battleship": {"Size": 4, "Quantity": 3, "Coordinates": []},
    "Cruiser": {"Size": 3, "Quantity": 0, "Coordinates": []},
    "Submarine": {"Size": 3, "Quantity": 0, "Coordinates": []},
    "Destroyer": {"Size": 2, "Quantity": 0, "Coordinates": []},
    "DingyBoat": {"Size": 1, "Quantity": 4, "Coordinates": []}
}

# Create copies of default fleet settings for CPU and Player
fleet_cpu = copy.deepcopy(DEFAULT_FLEET)  # Copy for CPU
fleet_player = copy.deepcopy(DEFAULT_FLEET)  # Copy for Player


def print_fleet(fleet):
    """Print the fleet information in a formatted manner.
    Args:
        fleet (dict): Dictionary containing fleet information.
    """
    print("{:<20} {:<10} {:<10} {:<50}".format(
        "ShipType", "Size", "Quantity", "Coordinates"))
    print("=" * 40)
    for ship, ship_details in fleet.items():
        size = ship_details["Size"]
        quantity = ship_details["Quantity"]
        coordinates = ship_details["Coordinates"]
        print("{:<20} {:<10} {:<10} {:<50}".format(
            ship, size, quantity, coordinates))


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


def print_map(game_map):
    """Print the game map.
    Args:
        game_map (list): 2D list representing the game map.
    """
    print("   ", end="")
    for col_index in range(len(game_map[0])):
        print(f"{col_index}  ", end="")
    print("\n   " + "=" * (len(game_map[0]) * 3))
    for row_index, row in enumerate(game_map):
        print(f"{row_index} |", end=" ")
        for value in row:
            print(f"{value}  ", end="")
        print()




def print_two_maps(map_left, map_right, label_left, label_right, gap=10):
    """
    Print two maps side by side with labels and a customizable gap.
    Args:
        map_left (list): The first 2D list representing a map.
        map_right (list): The second 2D list representing another map.
        label_left (str): Label for the first map.
        label_right (str): Label for the second map.
        gap (int): Number of blank spaces between the two maps. Default is 10.
    """
    # Calculate the width of a single character (assuming monospaced font)
    char_width = len("X")
    # Calculate the number of digits in the dimensions for proper alignment
    num_digits_map_width = len(str(len(map_left[0]))) # number of symbol to represent index, like 3 - 1 symbol, 13 - 2 symbols
    num_digits_map_height = len(str(len(map_left)))
    print(" num_digits_map_width", num_digits_map_width)
    print("num_digits_map_height", num_digits_map_height)
    # Create a string of blank spaces based on the gap argument
    gap_str = ' ' * gap # this will be a gap between maps
    # maps needs to be offset to side, so they align with indexes of rows
    # when printing table, index of row from table data will be separated by " | " - 3 digits, based on that now calculating how much label has to be offset to side
    row_index_separator = " | " # this will be separator between row column index and table
    print_map_left_offset = " " * (num_digits_map_height + len(row_index_separator)) # this will be an offset to side of map, based on indexes of rows (how many symbols is in index)
    # we will use same variable for left and right table, as both of them are same width
    # Labels are centered to align them with the maps
    number_char_table_total = (len(map_left[0]) * (num_digits_map_width + char_width + 1)) # calculating how many characters there will be in total per table width
    label_left_centered = label_left.center(number_char_table_total) # centering left label
    label_right_centered = label_right.center(number_char_table_total) # centering right label
    print(f"{print_map_left_offset}{label_left_centered}{gap_str}{print_map_left_offset} {label_right_centered}")
    # This step prints column indices with appropriate spacing to align them with the maps
    print(print_map_left_offset,end=" ")
    for col_index in range(len(map_left[0])):
        if col_index == len(map_left[0]) - 1:  # Check if it's the last column index
            print(f"{col_index}".rjust(num_digits_map_height + char_width), end="") # i do not want gap after last index, as it will be not aligned
        else:
            print(f"{col_index}".rjust(num_digits_map_height + char_width), end=" ")
    print(gap_str, print_map_left_offset,end=" ")
    for col_index in range(len(map_right[0])):
        # Right-justify the column index with proper spacing
        print(f"{col_index}".rjust(num_digits_map_height + char_width), end=" ")
    print()
    # Print the horizontal separator line
    # This step prints a separator line to visually separate the maps
    separator_length_left = len(map_left[0]) * (num_digits_map_width + char_width + 1)
    separator_length_right = len(map_right[0]) * (num_digits_map_width + char_width + 1)
    print(print_map_left_offset + "=" * separator_length_left, end=gap_str)
    print(" " + print_map_left_offset + "=" * separator_length_right)
    # Loop through each row and print the map values
    for row_index, (row_left, row_right) in enumerate(zip(map_left, map_right)):
        # Print row for the left map
        print(f"{row_index}".rjust(num_digits_map_width + 1), end=row_index_separator)
        for value in row_left:
            width = len(str(value))
            # Right-justify the map value with proper spacing
            print(f"{value}".rjust(num_digits_map_height + char_width - (char_width - width)), end=" ")
        # Insert the gap between the two maps
        print(gap_str, end="")
        
        # Print row for the right map
        print(f"{row_index}".rjust(num_digits_map_width + 1), end=row_index_separator)
        for value in row_right:
            width = len(str(value))
            # Right-justify the map value with proper spacing
            print(f"{value}".rjust(num_digits_map_height  + char_width - (char_width - width)), end=" ")
        
        # Move to the next line
        print()












def map_show_ship_or_symbols(game_map, length, coordinates, alignment, ship_name, fleet):
    """Deploy a single ship on the map. This function will be used when deploying player ships, CPU. Also when revealing sunken ship for both players
    Args:
        game_map (list): A 2D map.
        length (int): Length of the ship.
        location (list): Coordinates [row, column] where the ship will be deployed.
        alignment (str): Ship alignment ("H" for horizontal, "V" for vertical).
        ship_name (str): Name of the ship.
        fleet (dict): Dictionary containing fleet information.
    Returns:
        list: Updated map with the deployed ship.
    """
    global SHIP_SYMBOLS
    row, column = coordinates
    ship_coordinates = []
    if length == 1:
        game_map[row][column] = SHIP_SYMBOLS[alignment][0]
        ship_coordinates.append([row, column])
        return game_map
    else:
        if alignment == "Horizontal":
            ship_coordinates.append([row, column])
            game_map[row][column] = SHIP_SYMBOLS[alignment][0][0]
            for i in range(length - 1):
                game_map[row][column + i + 1] = SHIP_SYMBOLS[alignment][1][0]
                ship_coordinates.append([row, column + i + 1])
        elif alignment == "Vertical":
            ship_coordinates.append([row, column])
            game_map[row][column] = SHIP_SYMBOLS[alignment][0][0]
            for i in range(length - 1):
                game_map[row + i + 1][column ] = SHIP_SYMBOLS[alignment][1][0]
                ship_coordinates.append([row + i + 1, column])
    fleet[ship_name]["Coordinates"].append(ship_coordinates)
    print_map(game_map)
    print(f"Deployed {ship_name} at Coordinates: {coordinates}")
    return game_map



def search_map_for_pattern(map, width, height):
    """
    Find all occurrences of a pattern in a map and return their coordinates.
    Args:
    - map_ (List[List[int]]): The map as a nested list.
    - width (int): Width of the pattern.
    - height (int): Height of the pattern.
    Returns:
    List[Tuple[int, int]]: A list of coordinate tuples (row, col) where the pattern is found.
    """
    # Get the default symbol from the global constant
    symbol = DEFAULT_SYMBOL
    # Get the dimensions of the map
    MAP_WIDTH, MAP_HEIGHT = len(map), len(map[0])
    # Initialize an empty list to store the coordinates where the pattern matches
    coordinates = []
    # Create the pattern using list comprehension
    pattern = [[symbol] * width for _ in range(height)]
    # Loop through the map to search for the pattern
    for row in range(MAP_WIDTH - height + 1):
        for col in range(MAP_HEIGHT - width + 1):
            # Check if the pattern matches at the current coordinates
            if all(
                map[row + i][col + j] == pattern[i][j]
                for i in range(height)
                for j in range(width)
            ):
                # If the pattern matches, add the coordinates to the list
                coordinates.append([row, col])
    # Return "noneFound" if no matching coordinates were found
    if not coordinates:
        return "noneFound"
    return coordinates



def cpu_deploy_all_ships():
    """Deploy all CPU ships on the map.
    Updates:
        - Global variables fleet_cpu, DEFAULT_FLEET, map_cpu
    Returns:
        None
    """
    global fleet_cpu, DEFAULT_FLEET, map_cpu, DEFAULT_SYMBOL  # Declare global variables
    # Initialize map_cpu with DEFAULT_SYMBOL, if not already done
    map_cpu = initialize_maps(MAP_HEIGHT, MAP_WIDTH)
    # Make a fresh copy of the fleet, in case there were any changes
    # made for map size or fleet
    fleet_cpu = copy.deepcopy(DEFAULT_FLEET)
    for ship_name, ship_info in fleet_cpu.items():
        quantity = ship_info["Quantity"]
        size = ship_info["Size"]
        print(f"Deploying {quantity} {ship_name}(s) of size {size}")
        for i in range(quantity):
            if size == 1:
                alignment = "Single"
            else:
                alignment = random.choice(["Horizontal", "Vertical"])  # Horizontal or vertical
            if alignment == "Horizontal":
                location = random.choice(search_map_for_pattern(map_cpu, size, 1))
            elif alignment == "Vertical":
                location = random.choice(search_map_for_pattern(map_cpu, 1, size))
            print(alignment)
            map_show_ship_or_symbols(map_cpu, size, location, alignment, ship_name, fleet_cpu)


def find_biggest_ship_in_fleet(fleet):
    """
    Find the biggest ship in the fleet by size.
    Args:
        fleet (Dict[str, Dict[str, int]]): A dictionary representing the fleet of ships.
    Returns:
        name and size of the biggest ship,
        or None if there are no ships with quantity > 0.
    """
    available_ships = {k: v for k, v in fleet.items() if v["Quantity"] > 0}
    if not available_ships:
        return None  # No ships with quantity > 0
    biggest_ship = max(available_ships, key=lambda ship: available_ships[ship]["Size"])
    biggest_ship_size = available_ships[biggest_ship]["Size"]
    return biggest_ship, biggest_ship_size


def remove_coordinates_from_list(A, B):
    """
    Remove coordinates from list A if they are also present in list B.
    This function will be used to check, if there was previously made shot to those coordinates. will be needed for CPU and Player
    Args:
        A (List[List[int]]): The first nested list of coordinates.
        B (List[List[int]]): The second nested list of coordinates.
    Returns:
        List[List[int]]: List A with coordinates removed if they are present in list B.
    """
    # Create a set of coordinates from list B for faster lookup
    coordinates_set_B = set(tuple(coord) for coord in B)
    # Filter list A to keep only coordinates not present in list B
    filtered_A = [coord for coord in A if tuple(coord) not in coordinates_set_B]
    return filtered_A


def cpu_choose_shooting_coordinates_biggest_ship(fleet_to_search, map_to_search):
    """
    Choose shooting coordinates for the CPU based on the biggest ship in the fleet.
    Args:
        fleet_to_search (list): List of ships in the fleet.
        map_to_search (list): The map to search for shooting coordinates.
    Returns:
        The chosen shooting coordinates (coordinateX, coordinateY).
    """
    global cpu_actions, cpu_shoot_coordinates_log, DEFAULT_SYMBOL
    ship_name, ship_size = find_biggest_ship_in_fleet(fleet_to_search) # searching for biggest ship in fleet
    if ship_name is  None:
        print("game over print") # need to create function game over
    else:
        width = ship_size * 2 - 1
        height = ship_size * 2 - 1
        while True:
            coordinates = search_map_for_pattern(map_to_search, width, height) # getting list of possible coordinates
            checked_coordinates = remove_coordinates_from_list(coordinates, cpu_shoot_coordinates_log) # removing any coordinates from coordinates list, if they were previously used
            if checked_coordinates: # if there is any coordinates in list, we will choose one random
                chosen_coordinates = random.choice(checked_coordinates) # choosing coordinates using random
                break
            else: # if there was no coordinates in list, we will reduce width or height and search map again and again
                reduce = random.choice(["width", "height"]) #choosing randomly, what to reduce for searching
                if reduce == "width":
                    width = width - 1
                    height = height
                    coordinates = search_map_for_pattern(map_to_search, width, height) # getting list of possible coordinates
                    checked_coordinates = remove_coordinates_from_list(coordinates, cpu_shoot_coordinates_log) # removing any coordinates from coordinates list, if they were previously used
                    if checked_coordinates: # if there is any coordinates in list, we will choose one random
                        chosen_coordinates = random.choice(checked_coordinates) # choosing coordinates using random
                        break
                    else: # if there was no coordinates found with reduced width, we will restore width and search with reduced height
                        width = width + 1
                        height = height - 1
                        coordinates = search_map_for_pattern(map_to_search, width, height) # getting list of possible coordinates
                        checked_coordinates = remove_coordinates_from_list(coordinates, cpu_shoot_coordinates_log) # removing any coordinates from coordinates list, if they were previously used
                        if checked_coordinates: # if there is any coordinates in list, we will choose one random
                            chosen_coordinates = random.choice(checked_coordinates) # choosing coordinates using random
                            break
                        else: #reducing width and height and try loop again
                            width = width -1 
                            height = height - 1
                elif reduce == "height":
                    width = width
                    height = height - 1
                    coordinates = search_map_for_pattern(map_to_search, width, height) # getting list of possible coordinates
                    checked_coordinates = remove_coordinates_from_list(coordinates, cpu_shoot_coordinates_log) # removing any coordinates from coordinates list, if they were previously used
                    if checked_coordinates: # if there is any coordinates in list, we will choose one random
                        chosen_coordinates = random.choice(checked_coordinates) # choosing coordinates using random
                        break
                    else: # if there was no coordinates found with reduced width, we will restore height and search with reduced width
                        width = width -1
                        height = height + 1
                        coordinates = search_map_for_pattern(map_to_search, width, height) # getting list of possible coordinates
                        checked_coordinates = remove_coordinates_from_list(coordinates, cpu_shoot_coordinates_log) # removing any coordinates from coordinates list, if they were previously used
                        if checked_coordinates: # if there is any coordinates in list, we will choose one random
                            chosen_coordinates = random.choice(checked_coordinates) # choosing coordinates using random
                            break
                        else: #reducing width and height and try loop again
                            width = width - 1 
                            height = height - 1
        # loop is over, coordinates are found
        coord_x, coord_y = chosen_coordinates # now we know coordinates last pattern was used, so based on that, we will take sweet spot - center of pattern and shoot
        coordinate_x = coord_x + width // 2 + random.choice([0,width % 2])
        coordinate_y = coord_y + height // 2 + random.choice([0,height % 2])
    return coordinate_x, coordinate_y


def find_ship_and_coordinates(fleet, coordinates):
    """
    Find the ship name, ship size, and the list ID of coordinates to which the target_coordinates belong.
    Args:
        fleet (dict): Dictionary containing ship information.
        coordinates (list): Coordinates to search for.
    Returns:
        A tuple containing the ship name, ship size, and coordinates list ID if found, otherwise (None, None, None).
    """
    for ship_name, ship_info in fleet.items():
        for list_id, coordinates_list in enumerate(ship_info['Coordinates']):
            if coordinates in coordinates_list:
                return ship_name, ship_info['Size'], list_id
    # If coordinates are not found, return (None, None, None)
    return None, None, None


def detect_ship_orientation(coordinates_list):
    """
    Detect the orientation of a ship based on its coordinates.

    Args:
        coordinates (list): List of coordinates to analyze.

    Returns:
        "horizontal" if the ship is positioned horizontally, "vertical" if vertically, or "unknown" if undetermined.
    """
    # Check if all y-coordinates are the same (horizontal)
    y_values = [coord[1] for coord in coordinates_list]
    if all(y == y_values[0] for y in y_values):
        return "horizontal"

    # Check if all x-coordinates are the same (vertical)
    x_values = [coord[0] for coord in coordinates_list]
    if all(x == x_values[0] for x in x_values):
        return "vertical"

    # If neither condition is met, it's undetermined
    return "unknown"




clear_terminal()
cpu_deploy_all_ships()
print_two_maps(map_cpu_hidden, map_cpu,"hidfdwfwefwdden","actuawefweewfl")
#print_two_maps(map_cpu, map_cpu_hidden,"hidden","actual")

print("learning")
def test():
    global fleet_cpu, map_cpu_hidden
    ship_name, ship_size = find_biggest_ship_in_fleet(fleet_cpu) # searching for biggest ship in fleet
    coordinates = search_map_for_pattern(map_cpu_hidden, ship_size, ship_size) # getting list of possible coordinates
    tomasx, tomasy = cpu_choose_shooting_coordinates_biggest_ship(fleet_cpu, map_cpu_hidden)
    print(ship_name, ship_size)
    print (tomasx, tomasy)

#test()
print("finished")
print(fleet_cpu)







