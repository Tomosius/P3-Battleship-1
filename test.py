# battleship.py test.py - this is code for testing cpu vs cpu game

# Import required libraries
import random  # library to generate random
import copy  # library to make copies of lists and etc, will use function deepcopy
import os  # library to clear terminal
import time  # importing time library for logging game actions

# Constants for map dimensions and default symbol
MAP_HEIGHT = 10
MAP_WIDTH = 10
DEFAULT_SYMBOL = '0'  # New global variable for the default symbol

# Create maps for CPU and Player
map_cpu_display = [[DEFAULT_SYMBOL for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
map_cpu_hidden = [[DEFAULT_SYMBOL for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
map_player_hidden = [[DEFAULT_SYMBOL for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
map_player = [[DEFAULT_SYMBOL for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

# Initialize game-related variables
start_time = time.time()  # starting timer, later it will reset with game start
game_result = None  # Store the game result (win, lose, or draw)
cpu_shot_log_tmp = []  # List to store CPU actions (coordinates) if HIT [row, column]
game_actions_log = [
    ["player or CPU", "time", "column", "row", "action outcome"]]  # List to store CPU's shot coordinates


def clear_terminal():
    """Clear the terminal screen."""
    if os.name == 'posix':  # Unix/Linux/MacOS
        os.system('clear')
    elif os.name == 'nt':  # Windows
        os.system('cls')


def initialize_maps(width, height, default_symbol):
    """Initialize a 2D map with a default symbol.

    Args:
        width (int): The width of the map.
        height (int): The height of the map.
        default_symbol (str): The default symbol to populate the map.

    Returns:
        list: A 2D list filled with the default symbol.
    """
    return [[default_symbol for _ in range(height)] for _ in range(width)]


# Default settings for the fleet
DEFAULT_FLEET = {
    "AircraftCarrier": {"Size": 5, "Quantity": 1, "Coordinates": []},
    "Battleship": {"Size": 4, "Quantity": 3, "Coordinates": []},
    "Cruiser": {"Size": 3, "Quantity": 1, "Coordinates": []},
    "Submarine": {"Size": 3, "Quantity": 2, "Coordinates": []},
    "Destroyer": {"Size": 2, "Quantity": 3, "Coordinates": []},
    "DingyBoat": {"Size": 1, "Quantity": 4, "Coordinates": []}
}


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
        coordinates = str(ship_details["Coordinates"])  # Convert the list to a string
        print("{:<20} {:<10} {:<10} {:<50}".format(
            ship, size, quantity, coordinates))


# Define color dictionary
COLORS = {
    "DarkYellow": "\u001b[33m",  # Single cell ship
    "DarkBlue": "\u001b[34m",  # Horizontal ship
    "DarkGreen": "\u001b[32m",  # Vertical ship
    "DarkRed": "\u001b[31m",  # Damaged or Sunk ship
    "LightGray": "\u001b[37m",  # Miss
    "Reset": "\u001b[0m",  # Reset ANSI escape code in string
}

# Define ship symbols dictionary
SHIP_SYMBOLS = {
    "Single": [COLORS["DarkYellow"] + chr(0x25C6) + COLORS["Reset"]],
    "Horizontal": [
        COLORS["DarkBlue"] + chr(0x25C0) + COLORS["Reset"],
        COLORS["DarkBlue"] + chr(0x25A4) + COLORS["Reset"]
    ],
    "Vertical": [
        COLORS["DarkGreen"] + chr(0x25B2) + COLORS["Reset"],
        COLORS["DarkGreen"] + chr(0x25A5) + COLORS["Reset"]
    ],
    "Hit": [COLORS["DarkRed"] + chr(0x25A6) + COLORS["Reset"]],
    "Miss": [COLORS["LightGray"] + chr(0x2022) + COLORS["Reset"]],
    "SingleSunk": [COLORS["DarkRed"] + chr(0x25C6) + COLORS["Reset"]],
    "HorizontalSunk": [
        COLORS["DarkRed"] + chr(0x25C0) + COLORS["Reset"],
        COLORS["DarkRed"] + chr(0x25A4) + COLORS["Reset"]
    ],
    "VerticalSunk": [
        COLORS["DarkRed"] + chr(0x25B2) + COLORS["Reset"],
        COLORS["DarkRed"] + chr(0x25A5) + COLORS["Reset"]
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
    num_digits_map_width = len(
        str(len(map_left[0])))  # number of symbol to represent index, like 3 - 1 symbol, 13 - 2 symbols
    num_digits_map_height = len(str(len(map_left)))
    # Create a string of blank spaces based on the gap argument
    gap_str = ' ' * gap  # this will be a gap between maps
    # maps needs to be offset to side, so they align with indexes of rows
    # when printing table, index of row from table data will be separated by " | " - 3 digits, based on that now calculating how much label has to be offset to side
    row_index_separator = " | "  # this will be separator between row column index and table
    print_map_left_offset = " " * (num_digits_map_height + len(
        row_index_separator))  # this will be an offset to side of map, based on indexes of rows (how many symbols is in index)
    # we will use same variable for left and right table, as both of them are same width
    # Labels are centered to align them with the maps
    number_char_table_total = (len(map_left[0]) * (
                num_digits_map_width + char_width + 1))  # calculating how many characters there will be in total per table width
    label_left_centered = label_left.center(number_char_table_total)  # centering left label
    label_right_centered = label_right.center(number_char_table_total)  # centering right label
    print(f"{print_map_left_offset}{label_left_centered}{gap_str}{print_map_left_offset} {label_right_centered}")
    # This step prints column indices with appropriate spacing to align them with the maps
    print(print_map_left_offset, end=" ")
    for col_index in range(len(map_left[0])):
        if col_index == len(map_left[0]) - 1:  # Check if it's the last column index
            print(f"{col_index}".rjust(num_digits_map_height + char_width),
                  end="")  # i do not want gap after last index, as it will be not aligned
        else:
            print(f"{col_index}".rjust(num_digits_map_height + char_width), end=" ")
    print(gap_str, print_map_left_offset, end=" ")
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
            print(f"{value}".rjust(num_digits_map_height + char_width - (char_width - width)), end=" ")
        # Move to the next line
        print()


def map_show_ship_or_symbols(game_map, length, coordinates, alignment, ship_name, fleet):
    """
    Deploy a single ship on the map.

    Args:
        game_map (list): The 2D map where the ship will be deployed.
        length (int): The length of the ship.
        coordinates (list): Starting coordinates [row, column] for the ship.
        alignment (str): The alignment of the ship ("Horizontal" or "Vertical").
        ship_name (str): The name of the ship.
        fleet (dict): Dictionary containing fleet information.

    Global Variables:
        SHIP_SYMBOLS (dict): Dictionary containing ship symbols.

    Returns:
        list: Updated 2D map with the deployed ship.
    """

    row, column = coordinates  # Extract row and column from coordinates
    ship_coordinates = []  # Initialize empty list to store ship coordinates

    # Case for single-cell ships
    global SHIP_SYMBOLS  # Referencing the global variable for ship symbols

    if length == 1:
        game_map[row][column] = SHIP_SYMBOLS[alignment][0]
        ship_coordinates.append([row, column])

    # Case for multi-cell ships
    else:
        # Deploy ship horizontally
        if alignment == "Horizontal":
            ship_coordinates.append([row, column])  # Append starting coordinate
            game_map[row][column] = SHIP_SYMBOLS[alignment][0]  # Set the starting cell
            for i in range(1, length):  # Loop for the remaining cells
                game_map[row][column + i] = SHIP_SYMBOLS[alignment][1]
                ship_coordinates.append([row, column + i])

        # Deploy ship vertically
        elif alignment == "Vertical":
            ship_coordinates.append([row, column])  # Append starting coordinate
            game_map[row][column] = SHIP_SYMBOLS[alignment][0]  # Set the starting cell
            for i in range(1, length):  # Loop for the remaining cells
                game_map[row + i][column] = SHIP_SYMBOLS[alignment][1]
                ship_coordinates.append([row + i, column])

    # Store the coordinates of the deployed ship in the fleet dictionary
    fleet[ship_name]["Coordinates"].append(ship_coordinates)

    return game_map


from typing import List, Tuple


def search_map_for_pattern(game_map, height, width):
    """
    Find all occurrences of a pattern of DEFAULT_SYMBOL in a map and return their coordinates.

    Args:
        game_map (List[List[str]]): The map as a nested list.
        height (int): Height of the pattern to search for.
        width (int): Width of the pattern to search for.

    Returns:
        List[Tuple[int, int]]: A list of coordinates (row, col) where the pattern is found, or an empty list if no pattern is found.
    """

    # Create a pattern of DEFAULT_SYMBOL with the given height and width
    global DEFAULT_SYMBOL
    pattern = [[DEFAULT_SYMBOL for _ in range(width)] for _ in range(height)]

    # Get the dimensions of the map
    map_height, map_width = len(game_map), len(game_map[0])

    # Initialize an empty list to store the coordinates where the pattern is found
    coordinates = []

    # Loop through the map to find occurrences of the pattern
    for row in range(map_height - height + 1):
        for col in range(map_width - width + 1):
            pattern_matches = True  # Assume the pattern matches until proven otherwise

            # Check each cell in the subgrid against the pattern
            for i in range(height):
                for j in range(width):
                    if game_map[row + i][col + j] != pattern[i][j]:
                        pattern_matches = False
                        break  # Break the inner loop if any cell doesn't match
                if not pattern_matches:
                    break  # Break the outer loop if any row doesn't match

            # If the pattern matches, add the top-left corner coordinates to the list
            if pattern_matches:
                coordinates.append([row, col])
    if len(coordinates) == 0:
        print("no coordinates found on function search_map_for_pattern")
        return "noneFound"
    else:
        print("YAY coordinates found on function search_map_for_pattern", coordinates)
        return coordinates


def cpu_deploy_all_ships():
    """
    Deploy all CPU ships on the map.

    Global Variables:
        fleet_cpu (dict): Contains the CPU's fleet information.
        DEFAULT_FLEET (dict): Default settings for the fleet.
        map_cpu_display (list): 2D map for CPU.
        DEFAULT_SYMBOL (str): Default symbol for empty cells.
        SHIP_SYMBOLS (dict): Dictionary containing ship symbols.

    Updates:
        - fleet_cpu: Updated with the ship coordinates.
        - map_cpu_display: Updated with deployed ships.

    Returns:
        None
    """

    # Declare global variables
    global fleet_cpu, DEFAULT_FLEET, map_cpu_display, DEFAULT_SYMBOL, SHIP_SYMBOLS

    # Initialize the map with default symbols if not already done
    map_cpu_display = initialize_maps(MAP_HEIGHT, MAP_WIDTH, DEFAULT_SYMBOL)

    # Make a deep copy of the default fleet to initialize fleet_cpu
    fleet_cpu = copy.deepcopy(DEFAULT_FLEET)

    # Loop through each ship type in the fleet
    for ship_name, ship_info in fleet_cpu.items():
        quantity = ship_info["Quantity"]  # Number of ships of this type
        size = ship_info["Size"]  # Size of this type of ship
        # Deploy the required number of each ship type
        location = ""
        for i in range(quantity):
            # Determine alignment and find a suitable location for the ship
            if size == 1:
                alignment = "Single"
                location = random.choice(search_map_for_pattern(map_cpu_display, 1, 1))
            else:
                alignment = random.choice(["Horizontal", "Vertical"])  # Randomly choose alignment
                if alignment == "Vertical":
                    location = random.choice(search_map_for_pattern(map_cpu_display, size, 1))
                elif alignment == "Horizontal":
                    location = random.choice(search_map_for_pattern(map_cpu_display, 1, size))
                    # Deploy the ship and update the map and fleet information
            map_show_ship_or_symbols(map_cpu_display, size, location, alignment, ship_name, fleet_cpu)


def find_biggest_ship_in_fleet(fleet):
    """
    Find the biggest ship in the fleet by its size.

    Args:
        fleet (dict): A dictionary representing the fleet of ships.
            Each key is a ship name, and each value is another dictionary
            containing 'Size' and 'Quantity'.

    Returns:
        tuple: A tuple containing the name and size of the biggest ship.
        None: If there are no ships with a quantity greater than 0.
    """

    # Filter out ships with zero quantity
    available_ships = {k: v for k, v in fleet.items() if v["Quantity"] > 0}

    # Return None if no ships are available
    if not available_ships:
        return None

    # Find the biggest ship based on size
    biggest_ship = max(available_ships, key=lambda ship: available_ships[ship]["Size"])
    biggest_ship_size = available_ships[biggest_ship]["Size"]

    print(f"Biggest ship: {biggest_ship}, Size: {biggest_ship_size}")

    return biggest_ship, biggest_ship_size


def cpu_choose_shooting_coordinates_biggest_ship(fleet_to_search, map_to_search):
    print()
    print("initializing function cpu_choose_shooting_coordinates_biggest_ship")
    """
    Choose shooting coordinates for the CPU based on the biggest ship in the fleet.
    Args:
        fleet_to_search (list): List of ships in the fleet.
        map_to_search (list): The map to search for shooting coordinates.
    Returns:
        The chosen shooting coordinates (coordinateX, coordinateY).
    """
    global cpu_shot_log_tmp, DEFAULT_SYMBOL
    coordinates = ""
    ship_name, ship_size = find_biggest_ship_in_fleet(fleet_to_search)  # searching for biggest ship in fleet
    height = ""
    width = ""
    if ship_name is None:
        print("game over print")  # need to create function game over, as no ships left in fleet
    else: # there are remaining ships in fleet
        width = ship_size * 2 - 1
        height = ship_size * 2 - 1
        coordinates = search_map_for_pattern(map_to_search, height, width)  # getting list of possible coordinates
        if coordinates == "noneFound":
            while coordinates == "noneFound":
                coordinates = search_map_for_pattern(map_to_search, height,width)  # getting list of possible coordinates
                if coordinates != "noneFound": # yay, we have found coordinates
                    print("cpu_choose_shooting_coordinates_biggest_ship found coordinates   ", coordinates)
                    break
                reduction = random.choice(["height", "width"])
                print("we have found no coordinates with height and width: ", height, width)
                if reduction == "height":
                    height, width, coordinates = map_search_reduce_height(height, width, map_to_search)
                    if coordinates != "noneFound":
                        break
                if reduction == "width":
                    height, width, coordinates = map_search_reduce_width(height, width, map_to_search)
                    if coordinates != "noneFound":
                        break
                if (height < ship_size) and (width <= 1):
                    print("we have found no coordinates with height and width: ", height, width)
                    break
                if (height <= 1) and (width < ship_size) :
                    print("we have found no coordinates with height and width: ", height, width)
                    break
                if height < 1 or width < 1:
                    print("we have found no coordinates with height and width: ", height, width)
                    break
    chosen_coordinates = random.choice(coordinates)
    if len(chosen_coordinates) != 2:
        print(f"Error: chosen_coordinates contains {len(chosen_coordinates)} values, expected 2.")
        return None, None  # or however you wish to handle this case
    # loop is over, coordinates are found
    coord_row, coord_column = chosen_coordinates  # now we k# now coordinates last pattern was used, so based on that, we will take sweet spot - center of pattern and shoot
    print("coordinates befoew selecting senter of pattern: ", coord_row, coord_column, "height and width: ", height, width)
    middle_width = (width // 2) + random.choice([1, width % 2]) - 1
    middle_height = (height // 2) + random.choice([1, height % 2]) - 1
    print("just checking for middle of width and height:", middle_height, middle_width)
    coordinate_column = coord_column + middle_width
    coordinate_row = coord_row + middle_height

    print("coordinate_x, coordinate_y", coordinate_row, coordinate_column)
    return coordinate_row, coordinate_column


def map_search_reduce_width(height, width, map_to_search):
    width -= 1  # reducing width
    coordinates = search_map_for_pattern(map_to_search, height, width)
    if coordinates == "noneFound":
        print("we have found no coordinates with height and width: ", height, width)
        width += 1  # restoring width
        height -= 1  # reducing height
        coordinates = search_map_for_pattern(map_to_search, height, width)
        if coordinates == "noneFound":
            print("we have found no coordinates with height and width: ", height, width)
            width -= 1  # reducing width, so now both height and width are deduced by 1
    return height, width, coordinates


def map_search_reduce_height(height, width, map_to_search):
    height -= 1  # reducing height
    coordinates = search_map_for_pattern(map_to_search, height, width)
    if coordinates == "noneFound":
        print("we have found no coordinates with height and width: ", height, width)
        height += 1  # restoring height
        width -= 1  # reducing width
        coordinates = search_map_for_pattern(map_to_search, height, width)
        if coordinates == "noneFound":
            print("we have found no coordinates with height and width: ", height, width)
            height -= 1  # reducing height, so now both height and width are deduced  by 1
    return height, width, coordinates


def action_perform_shoot(player, row, column, map_hidden, map_display, fleet):
    """
    Perform a shooting action on the game board.

    Args:
        player (str): The player making the shot ("CPU" or "Human").
        column (int): The column-coordinate of the shot.
        row (int): The row-coordinate of the shot.
        map_hidden (list): The hidden map that tracks shots.
        map_display (list): The displayed map that shows ships.
        fleet (dict): Information about the fleet of ships.

    Returns:
        str: The outcome of the action ("Hit" or "Miss").
    """
    # Declare global variables for game actions log, start time, and ship symbols
    global game_actions_log, start_time, SHIP_SYMBOLS

    # Find the details of the ship at the given coordinates, if any
    ship_name, ship_size, coordinates_list, coordinates_set_id, coordinates_id = find_ship_and_coordinates(fleet, [row, column])

    try:
        # If a ship was found at the coordinates
        if ship_name != None:
            print(f'{player} performed shot on coordinates {row} and {column}, {ship_name} was damaged')
            print("damaged ship cooordinates are: ", coordinates_list)

            # Handle the logic for a hit ship
            handle_ship_hit(player, row, column, map_hidden, map_display, fleet,
                            ship_name, ship_size, coordinates_list, coordinates_id)
            return "Hit"

        else:
            # If no ship was found at the coordinates, it's a miss
            print(f'{player} performed shot on coordinates {row} and {column}, it was a MISS')

            # Handle the logic for a missed shot
            handle_miss(player, row, column, map_hidden, map_display)
            return "Miss"

    except Exception as e:
        # Handle any exceptions that occur
        print(f"An error occurred: {e}")
        return None


def find_ship_and_coordinates(fleet, target_coordinates):
    """
    Find the ship name, ship size, the list of coordinates, and the coordinate ID
    to which the target_coordinates belong.

    Args:
        fleet (dict): Dictionary containing ship information.
        target_coordinates (list): Coordinates [row, column] to search for.

    Returns:
        tuple: A tuple containing:
            - ship_name (str): Name of the ship at the coordinates, if found.
            - ship_size (int): Size of the ship, if found.
            - ship_coordinates_list (list): List of coordinates of the ship, if found.
            - coordinates_set_id (int): Index of the list of coordinates for the ship, if found.
            - coordinates_id (int): Index of the coordinates in the list, if found.
        Returns (None, None, None, None, None) if no match is found.
    """

    # Iterate through each ship in the fleet to find matching coordinates
    for ship_name, ship_info in fleet.items():

        # Loop through each list of coordinates assigned to the current ship
        for coordinates_set_id, ship_coordinates_list in enumerate(ship_info['Coordinates']):

            # Try to find the index of the target coordinates in the list
            try:
                coordinates_id = ship_coordinates_list.index(target_coordinates)

                # If a match is found, return the details of the ship and coordinates
                return ship_name, ship_info['Size'], ship_coordinates_list, coordinates_set_id, coordinates_id

            except ValueError:
                # Continue to the next iteration if no match is found
                continue

    # Return None for all fields if no matching coordinates are found
    return None, None, None, None, None


def handle_ship_hit(player, row, column, map_hidden, map_display, fleet, ship_name, ship_size, coordinates_list,
                    coordinates_id):
    """
    Handle the scenario where a ship is hit.

    Args:
        player (str): The player making the shot ("CPU" or "Human").
        column (int): The column-coordinate of the shot. Width
        row (int): The row-coordinate of the shot. Height
        map_hidden (list): The hidden map that tracks shots.
        map_display (list): The displayed map that shows ships.
        fleet (dict): Information about the fleet of ships.
        ship_name (str): Name of the ship that was hit.
        ship_size (int): Size of the ship that was hit.
        coordinates_list (list): List of coordinates of the ship.
        coordinates_id (int): Index of the coordinates in the list.

    Global Variables:
        game_actions_log (list): Log of game actions.
        start_time (float): The game start time for logging.
        SHIP_SYMBOLS (dict): Symbols used for different states of the ship.
        cpu_shot_log_tmp (list): Temporary log for CPU actions.

    Returns:
        None
    """

    # Declare global variables
    global game_actions_log, start_time, SHIP_SYMBOLS, cpu_shot_log_tmp

    # Log CPU actions if the player is CPU
    if player == "CPU":
        cpu_shot_log_tmp.append([row, column])  # Adding hit coordinates to temporary CPU actions list
        print(" cpu performed hit shot tomosius ", row, column)

    # Check if the ship was completely sunk and update maps
    print("now will perform check_ship_damaga")
    check_ship_damage(player, fleet, [row, column], map_display, map_hidden)

    # Log the action with details
    print(player, " made a hit, now we will update log based on coordinates_list: ", coordinates_list)
    timer = time.time() - start_time  # Calculate the time elapsed since the game started
    action_outcome = f'{ship_name} was hit'
    game_actions_log.append([player, timer, row, column, action_outcome])


    # Update the display map, marking the hit with a different color but the same symbol
    update_display_map(ship_size, row, column, map_display, coordinates_list)

    # Output the updated game actions log
    print("game_actions_log", game_actions_log)


def handle_miss(player, row, column, map_hidden, map_display):
    """
    Handle the scenario where the shot misses any ship.

    Args:
        player (str): The player making the shot ("CPU" or "Human").
        column (int): The column-coordinate of the shot.
        row (int): The row-coordinate of the shot.
        map_hidden (list): The hidden map that tracks shots.
        map_display (list): The displayed map that shows ships.

    Global Variables:
        SHIP_SYMBOLS (dict): Symbols used for different states of the ship.
        start_time (float): The game start time for logging.
        game_actions_log (list): Log of game actions.

    Returns:
        None
    """

    # Declare global variables
    global SHIP_SYMBOLS, start_time, game_actions_log

    # Calculate the time elapsed since the game started
    timer = time.time() - start_time

    # Create the action outcome message
    action_outcome = f'it was a MISS'

    # Log the action into the game actions log
    game_actions_log.append([player, timer, row, column, action_outcome])

    # Update the hidden map to mark the miss
    map_hidden[row][column] = SHIP_SYMBOLS["Miss"][0]

    # Update the display map to mark the miss
    map_display[row][column] = SHIP_SYMBOLS["Miss"][0]


def update_display_map(ship_size, row, column, map_display, coordinates_list):
    """
    Update the displayed map based on the hit.

    Args:
        ship_size (int): The size of the ship that was hit.
        column (int): The column-coordinate of the hit.
        row (int): The row-coordinate of the hit.
        map_display (list): The displayed map that shows ships.
        coordinates_list (dict): The list of coordinates of the ship.

    Global Variables:
        SHIP_SYMBOLS (dict): Dictionary containing symbols for different ship states.

    Returns:
        None
    """

    # Declare global variables
    global SHIP_SYMBOLS

    # Detect the alignment of the ship and update it to its 'Sunk' state
    alignment, coordinates_index = find_first_ship_alignment(coordinates_list)
    ship_alignment = alignment + "Sunk"
    print(" ship alignment is now: ", ship_alignment)

    # If the ship is of size 1, update its symbol directly
    if ship_size == 1:
        map_display[row][column] = SHIP_SYMBOLS[ship_alignment][0]
    else:
        # Identify the specific symbol to use based on the hit location
        for coord_id, (row1, column1) in enumerate(coordinates_list):
            if row == row1 and column == column1:
                # Determine if the hit is at the start of the ship
                if coord_id == 0:
                    symbol_id = 0
                else:
                    # The hit is at other parts of the ship
                    symbol_id = 1

        # Update the display map with the identified symbol
        map_display[row][column] = SHIP_SYMBOLS[ship_alignment][symbol_id]


def check_ship_damage(player, fleet, coordinates, map_display, map_hidden):
    """
    Check if a ship is completely damaged (sunk) and updates the game state accordingly.

    Args:
        player (str): The player who performed the action ("CPU" or "Human").
        fleet (dict): The current fleet information.
        coordinates (list): The coordinates where the hit occurred.
        map_display (list): The displayed map that shows ships.
        map_hidden (list): The hidden map that tracks shots.

    Global Variables:
        start_time (float): Game start time.
        cpu_shot_log_tmp (list): Temporary log of CPU actions.
        SHIP_SYMBOLS (dict): Symbols for different ship states.
        game_result (str): The result of the game ("Game Over" or None).

    Returns:
        str: "Game Over" if all ships are sunk, otherwise None.
    """

    # Declare global variables
    global start_time, cpu_shot_log_tmp, SHIP_SYMBOLS, game_result

    # Initialize ship_sunk as False
    ship_sunk = False

    # Find ship details based on the coordinates where the hit occurred
    ship_name, ship_size, coordinates_list, coordinates_set_id, coordinates_list_id = find_ship_and_coordinates(fleet, coordinates)
    row, column = coordinates
    map_hidden[row][column] = SHIP_SYMBOLS["Hit"][0]
    update_display_map(ship_size, row, column, map_display, coordinates_list)

    print("find_ship_and_coordinates(fleet, coordinates)", coordinates, "tomosius")
    alignment, coordinates_index = find_first_ship_alignment(coordinates_list)
    print("found alignmeent: ", alignment)
    if ship_size == 1 and (map_hidden[row][column] == SHIP_SYMBOLS["Hit"][0]):
        map_hidden[row][column] = map_display[row][column]
        ship_sunk = True
        print(" it is single ship and status is now 888 ", ship_sunk, ship_size)
    if ship_size > 1:
        # Loop to check if all parts of the ship are damaged
        for coord in coordinates_list:
            row, column = coord  # Extract the row and column coordinates
            if map_hidden[row][column] == SHIP_SYMBOLS["Hit"][0]:
                print(f'tomosius checking map hiden if {ship_name} is damaged on coordinates {row} and {column}')
                ship_sunk = True
            else:
                ship_sunk = False  # Set to False if any part is not damaged
                break  # Exit the loop
        # If the ship is completely damaged (sunk)
    if ship_sunk == True:
        alignment += "Sunk"
        print(" tomosius ship is sunk", alignment)
        print("mmmmm id does not remove single ship?", alignment)
        # Various actions to update state and logs
        handle_ship_sunk(player, fleet, ship_name, ship_size, coordinates_list, coordinates_set_id, coordinates_list_id, map_display,
                         map_hidden, alignment)

    # Code to handle other scenarios can go here


def handle_ship_sunk(player, fleet, ship_name, ship_size, coordinates_list, coordinates_set_id, coordinates_list_id, map_display,
                     map_hidden, alignment):
    """
    Handle actions and updates for when a ship is sunk.

    Args:
        player (str): The player who sunk the ship ("CPU" or "Human").
        fleet (dict): The current fleet information.
        ship_name (str): The name of the ship that was sunk.
        ship_size (int): The size of the ship.
        coordinates_list (list): The list of coordinates of the ship.
        coordinates_list_id (int): The ID of the ship's coordinates in the fleet.
        map_display (list): The displayed map that shows ships.
        map_hidden (list): The hidden map that tracks shots.
        alignment (str): The alignment of the ship ("Horizontal" or "Vertical").

    Global Variables:
        start_time (float): Game start time.
        cpu_shot_log_tmp (list): Temporary log of CPU actions.
        SHIP_SYMBOLS (dict): Symbols for different ship states.
        game_actions_log (list): Log of game actions.
        game_result (str): The result of the game ("Game Over" or None).
    """
    # Declare global variables
    global start_time, cpu_shot_log_tmp, SHIP_SYMBOLS, game_actions_log, game_result


    print(" before updating map, i just want to see map_display, ship_size, coordinates_list[0], alignment, ship_name, fleet", ship_size, coordinates_list[0], alignment, ship_name, coordinates_list_id, coordinates_list)
    print(len(coordinates_list))
    if len(coordinates_list) == 1:
        row, column = coordinates_list[0]
        map_display[row][column] = SHIP_SYMBOLS[alignment][0]
        map_hidden[row][column] = map_display[row][column]
    else:
        row, column = coordinates_list[0]
        if alignment == "HorizontalSunk":
            map_display[row][column] = SHIP_SYMBOLS[alignment][0]  # Set the starting cell
            map_hidden[row][column] = map_display[row][column]
            for i in range(1, ship_size):  # Loop for the remaining cells
                map_display[row][column + i] = SHIP_SYMBOLS[alignment][1]
                map_hidden[row][column + i] = map_display[row][column + i]
        elif alignment == "VerticalSunk":
            map_display[row][column] = SHIP_SYMBOLS[alignment][0]  # Set the starting cell
            map_hidden[row][column] = map_display[row][column]
            for i in range(1, ship_size):  # Loop for the remaining cells
                map_hidden[row + i][column] = SHIP_SYMBOLS[alignment][1]
                map_hidden[row + i][column] = map_display[row + i][column]

    # Record the action in the log
    timer = time.time() - start_time
    action_outcome = f'{ship_name} was sunk'
    game_actions_log.append([player, timer, coordinates_list[0][0], coordinates_list[0][1], action_outcome])

    # Remove ship coordinates from CPU temporary action log if the player is the CPU
    if player == "CPU":
        print("now will update cpu shooot log")
        print(" before updating spu shot log", cpu_shot_log_tmp, "coordinate list:", coordinates_list)
        cpu_shot_log_tmp = update_cpu_shot_log(coordinates_list)
        print("after updating cpu shoot log", cpu_shot_log_tmp)
    print("now should follow coordinates removal")
    print(" jautiena remove coordinates from fleet ship name", ship_name, "coordinates set id: ", coordinates_set_id)
    remove_coordinates_from_fleet(fleet, ship_name, coordinates_set_id)
    # Check if the game is over
    if not fleet:
        timer = time.time() - start_time
        action_outcome = 'Game Over'
        game_actions_log.append([player, timer, coordinates_list[0][0], coordinates_list[0][1], action_outcome])
        game_result = "Game Over"


def remove_coordinates_from_fleet(fleet, ship_name, coordinates_list_set_id):
    """
    Removes an entire set of coordinates from a ship and updates its quantity.
    Also removes any empty coordinate sets in the list.

    Parameters:
    - fleet (dict): The fleet information
    - ship_name (str): The name of the ship to update
    - coordinates_list_set_id (int): The index of the set of coordinates to remove
    """
    print("3463rr3r   4now we will be removing fleet[ship_name][Coordinates][coordinates_list_set_id]", ship_name,
          coordinates_list_set_id)
    print_fleet(fleet)

    try:
        print()
        print_fleet(fleet)
        print("now we will be removing fleet[ship_name][Coordinates][coordinates_list_set_id]", ship_name, coordinates_list_set_id)
        # Remove the entire set of coordinates from the ship
        del fleet[ship_name]["Coordinates"][coordinates_list_set_id]

        # Remove any empty coordinate sets
        fleet[ship_name]["Coordinates"] = [coords for coords in fleet[ship_name]["Coordinates"] if coords]

        # Reduce the quantity of this type of ship by 1
        fleet[ship_name]["Quantity"] -= 1

        # If the quantity of this type of ship reaches zero, remove it from the fleet
        if fleet[ship_name]["Quantity"] <= 0:
            del fleet[ship_name]
        print_fleet(fleet)

    except KeyError:
        print(f"Failed to remove coordinates for {ship_name}.")


def update_cpu_shot_log(coordinates_list):
    """
    Update the CPU shot log by removing coordinates that are present in
    the provided coordinates_list, implying that a ship has been sunk.

    Parameters:
    - coordinates_list (list): A list of coordinates that are to be removed.

    Returns:
    - list: Updated CPU shot log.
    """

    # Declare global variable to access and modify CPU shot log
    global cpu_shot_log_tmp

    # Exception handling to gracefully manage any runtime errors
    try:
        # Loop through each coordinate pair in coordinates_list
        for coord in coordinates_list:
            # Remove the coordinate pair from cpu_shot_log_tmp
            cpu_shot_log_tmp.remove(coord)

    except ValueError as e:
        print(f"Coordinate not found in log: {e}")

    return cpu_shot_log_tmp


def find_first_ship_alignment(log):
    """
    Attempts to identify the first alignment of a ship based on its coordinates,
    by comparing each coordinate with every other coordinate. Returns the index
    of the first coordinate in that alignment.

    Parameters:
    - log (List[List[int]]): A list of [row, column] coordinates representing the ship's location.

    Returns:
    - tuple: A tuple containing:
        1. A string indicating the first observed alignment ('None', 'Single', 'Horizontal', 'Vertical').
        2. An integer representing the index of the first coordinate in that alignment, or None if not applicable.
    """

    # Check for empty list and single coordinate
    if len(log) == 0:
        return ('None', None)
    elif len(log) == 1:
        print("based on spu log find_first_ship_alignment as single")
        return ('Single', 0)

    # Use enumerate with nested loops to compare each coordinate with every other coordinate
    for i, (row1, column1) in enumerate(log):
        for j, (row2, column2) in enumerate(log[i + 1:], start=i + 1):

            # If the rows are the same, it's a horizontal alignment
            if row1 == row2:
                print(" based on cpu log find_first_ship_alignment as Vertical")
                return ('Horizontal', i)
            # If the columns are the same, it's a vertical alignment
            elif column1 == column2:
                print("based on cpu log find_first_ship_alignment as horizontal")
                return ('Vertical', i)

    # If the function hasn't returned by this point, no alignment was found
    return ('None', None)


def select_best_shot_based_on_alignment(map_to_search):
    """
    Chooses the best coordinates to shoot at based on ship alignment detection.

    Args:
        map_to_search (list of lists): The map to search for ship coordinates.
        cpu_shot_log_tmp (list of lists): Temporary log of CPU shots.
        DEFAULT_SYMBOL (str): The default symbol representing untargeted cells in the map.

    Returns:
        tuple: The chosen column and row coordinates to target next based on the identified ship alignment.
               Returns (None, None) if no suitable coordinates are found.
    """
    global cpu_shot_log_tmp, DEFAULT_SYMBOL
    # Detect the alignment of the damaged ship and the index of the last coordinate
    alignment_info = find_first_ship_alignment(cpu_shot_log_tmp)

    # Return None if no identifiable ship alignment is found
    if alignment_info is None or alignment_info[0] == 'None':
        return None, None

    alignment, last_index = alignment_info

    # Extract the last coordinate based on the last index
    last_row, last_column = cpu_shot_log_tmp[last_index]

    # Define the map boundaries
    max_column = len(map_to_search[0]) - 1
    max_row = len(map_to_search) - 1

    # Initialize an empty list to hold potential shot coordinates
    potential_shots = []

    # Define possible shifts based on the ship alignment
    if alignment == "Vertical":
        shifts = [[1, 0], [-1, 0]]
    elif alignment == "Horizontal":
        shifts = [[0, 1], [0, -1]]
    elif alignment == "Single":
        shifts = [[0, 1], [0, -1], [1, 0], [-1, 0]]

    # Loop through the shifts to find the potential shots
    for coord in cpu_shot_log_tmp:
        row, column = coord
        for drow, dcolumn in shifts:
            new_row, new_column = row + drow, column + dcolumn
            # Check if the new coordinates are within map boundaries and haven't been shot at before
            if 0 <= new_row <= max_row and 0 <= new_column <= max_column:
                # Then check if the cell hasn't been shot at before
                if map_to_search[new_row][new_column] == DEFAULT_SYMBOL:
                    potential_shots.append([new_row, new_column])
                    print("new potentail shots: ", potential_shots)

        if len(potential_shots) > 0:
            break

    if len(potential_shots) == 0:
        print("found noo coordinates on select_best_shot_based_on_alignment")
        shifts = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        for coord in cpu_shot_log_tmp:
            row, column = coord
            for drow, dcolumn in shifts:
                new_row, new_column = row + drow, column + dcolumn
                # Check if the new coordinates are within map boundaries and haven't been shot at before
                if 0 <= new_row <= max_row and 0 <= new_column <= max_column:
                    # Then check if the cell hasn't been shot at before
                    if map_to_search[new_row][new_column] == DEFAULT_SYMBOL:
                        potential_shots.append([new_row, new_column])
                        print("new potentail shots: ", potential_shots)
                if len(potential_shots) > 0:
                    break
            if len(potential_shots) > 0:
                break
    # Randomly choose one of the potential shots if any are available
    if len(potential_shots) > 0:
        selected_row, selected_column = random.choice(potential_shots)
        print("found coordinates on select_best_shot_based_on_alignment", selected_row, selected_column)
        return selected_row, selected_column
    # Return None, None if no suitable coordinates are found
    return None, None


def cpu_move():
    """
    Executes the CPU's move during the game.

    Global Variables:
    - game_result: Holds the current state of the game ("Game Over" or None).
    - fleet_cpu: Dictionary holding information about the CPU's fleet.
    - map_cpu_hidden: Hidden map for the CPU.
    - map_cpu_display: Display map for the CPU.
    - cpu_shot_log_tmp: Temporary log for the CPU's shots.
    - game_actions_log: Log for game actions.
    - start_time: Time when the game started.
    - SHIP_SYMBOLS: Dictionary holding symbols for different ship states.

    Returns:
    - None: Updates global variables as side effects.
    """

    # Declare global variables accessed within the function
    global game_result, fleet_cpu, map_cpu_hidden, map_cpu_display
    global cpu_shot_log_tmp, game_actions_log, start_time, SHIP_SYMBOLS

    # Identify the player as CPU for logging and action purposes
    player = "CPU"

    # Check if there are any damaged but unsunk ships in cpu_shot_log_tmp
    if len(cpu_shot_log_tmp) == 0:
        print("no cpu log tmp was found")
        # No damaged ships; choose coordinates based on the largest ship in the fleet
        row, column = cpu_choose_shooting_coordinates_biggest_ship(fleet_cpu, map_cpu_hidden)
        # Perform the shooting action and update game state
        action_perform_shoot(player, row, column, map_cpu_hidden, map_cpu_display, fleet_cpu)

        # Check for game over condition
        if game_result == "Game Over":
            print("CPU HAS WON")
    else:
        print(" i have found this cpu tmp log: ", cpu_shot_log_tmp)
        # There are damaged ships; focus on sinking them
        row, column = select_best_shot_based_on_alignment(map_cpu_hidden)
        # Perform the shooting action and update game state
        action_perform_shoot(player, row, column, map_cpu_hidden, map_cpu_display, fleet_cpu)

        # Check for game over condition
        if game_result == "Game Over":
            print("CPU HAS WON")


def battleship_game():
    global start_time, map_cpu_hidden, map_cpu_display, cpu_shot_log_tmp, game_actions_log, fleet_cpu
    start_time = time.time()  # starting timer
    clear_terminal()
    cpu_deploy_all_ships()
    print_two_maps(map_cpu_hidden, map_cpu_display, "hidden_cpu_map", "cpu_map")
    print_fleet(fleet_cpu)
    for i in range(100):
        print()
        print(" game turn ", i, " ******")
        cpu_move()
        print("cpu shooting actions log: ", cpu_shot_log_tmp)
        print_two_maps(map_cpu_hidden, map_cpu_display, "hidden_cpu_map", "cpu_map")
        print()
        print()
        print_fleet(fleet_cpu)
        if len(fleet_cpu) == 0:
            print("this was completed on move: ", i)
            print("GAMEE OVER")
            break


battleship_game()
print(" test done")
