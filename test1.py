# battleship.py test.py - this is code for testing cpu vs cpu game

# Import required libraries
import random # library to generate random
import copy # library to make copies of lists and etc, will use function deepcopy
import os # library to clear terminal
import time # importing time library for logging game actions


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
start_time = None # tamer will start with game 
game_result = None  # Store the game result (win, lose, or draw)
cpu_shot_log_tmp = []  # List to store CPU actions (coordinates) if HIT
game_actions_log = [["player or CPU", "time", "x","y", "action outcome"]]  # List to store CPU's shot coordinates


def clear_terminal():
    """Clear the terminal screen."""
    if os.name == 'posix':  # Unix/Linux/MacOS
        os.system('clear')
    elif os.name == 'nt':  # Windows
        os.system('cls')




def initialize_maps(width, height, default_symbol):
    print()
    print(" initializing function: initialize_maps")
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
    "DarkYellow": "\u001b[33m", # Single cell ship
    "DarkBlue": "\u001b[34m", # Horizontal ship
    "DarkGreen": "\u001b[32m", # Vertical ship
    "DarkRed": "\u001b[31m", # Damaged or Sunk ship
    "LightGray": "\u001b[37m", # Miss
    "Reset": "\u001b[0m", # Reset ANSI escape code in string
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
    print()
    print("initializing function map_show_ship_or_symbols")
    """Deploy a single ship on the map.

    Args:
        game_map (list): A 2D map.
        length (int): Length of the ship.
        coordinates (list): Coordinates [row, column] where the ship will be deployed.
        alignment (str): Ship alignment ("H" for horizontal, "V" for vertical).
        ship_name (str): Name of the ship.
        fleet (dict): Dictionary containing fleet information.
        SHIP_SYMBOLS (dict): Dictionary containing ship symbols.
        
    Returns:
        list: Updated map with the deployed ship.
    """
    global SHIP_SYMBOLS
    row, column = coordinates
    ship_coordinates = []
    if length == 1:
        game_map[row][column] = SHIP_SYMBOLS[alignment][0]
        ship_coordinates.append([row, column])
    else:
        if alignment == "Horizontal":
            ship_coordinates.append([row, column])
            game_map[row][column] = SHIP_SYMBOLS[alignment][0]
            for i in range(length - 1):
                game_map[row][column + i + 1] = SHIP_SYMBOLS[alignment][1]
                ship_coordinates.append([row, column + i + 1])
        elif alignment == "Vertical":
            ship_coordinates.append([row, column])
            game_map[row][column] = SHIP_SYMBOLS[alignment][0]
            for i in range(length - 1):
                game_map[row + i + 1][column] = SHIP_SYMBOLS[alignment][1]
                ship_coordinates.append([row + i + 1, column])
    fleet[ship_name]["Coordinates"].append(ship_coordinates)
    print(f"Deployed {ship_name} at Coordinates: {coordinates}")
    return game_map


def search_map_for_pattern(map, width, height):
    print()
    print("initializing function search_map_for_pattern")
    """
    Find all occurrences of a pattern in a map and return their coordinates.
    Args:
    - map_ (List[List[int]]): The map as a nested list.
    - width (int): Width of the pattern.
    - height (int): Height of the pattern.
    Returns:
    List[int, int]: A list of coordinate [row, col] where the pattern is found.
    """
    # Get the default symbol from the global constant
    global DEFAULT_SYMBOL
    # Get the dimensions of the map
    map_height = len(map)
    map_width = len(map[0])
    # Initialize an empty list to store the coordinates where the pattern matches
    coordinates = []
    # Create the pattern using list comprehension
    pattern = [[DEFAULT_SYMBOL] * width for _ in range(height)]
    # Loop through the map to search for the pattern

    for row in range(map_height - height + 1):
        for col in range(map_width - width + 1):
            pattern_matches = True
            for i in range(height):
                for j in range(width):
                    if map[row + i][col + j] != pattern[i][j]:
                        pattern_matches = False
                        break
                if not pattern_matches:
                    break
            if pattern_matches:
                # If the pattern matches, add the coordinates to the list
                coordinates.append([row, col])
    # Return "noneFound" if no matching coordinates were found
    if not coordinates:
        return "noneFound"
    print(" found coordinates: ", coordinates)
    return coordinates

def cpu_deploy_all_ships():
    print()
    print("initializing function cpu_deploy_all_ships")
    """Deploy all CPU ships on the map.
    Updates:
        - Global variables fleet_cpu, DEFAULT_FLEET, map_cpu_display
    Returns:
        None
    """
    global fleet_cpu, DEFAULT_FLEET, map_cpu_display, DEFAULT_SYMBOL, SHIP_SYMBOLS # Declare global variables
    # Initialize map_cpu_display with DEFAULT_SYMBOL, if not already done
    map_cpu_display = initialize_maps(MAP_HEIGHT, MAP_WIDTH, DEFAULT_SYMBOL)
    # Make a fresh copy of the fleet, in case there were any changes
    fleet_cpu = copy.deepcopy(DEFAULT_FLEET)
    for ship_name, ship_info in fleet_cpu.items():
        quantity = ship_info["Quantity"]
        size = ship_info["Size"]
        print(f"Deploying {quantity} {ship_name}(s) of size {size}")
        for i in range(quantity):
            if size == 1:
                alignment = "Single"
                location = random.choice(search_map_for_pattern(map_cpu_display, 1, 1))
            else:
                alignment = random.choice(["Horizontal", "Vertical"])  # Horizontal or vertical
                if alignment == "Horizontal":
                    location = random.choice(search_map_for_pattern(map_cpu_display, size, 1))
                elif alignment == "Vertical":
                    location = random.choice(search_map_for_pattern(map_cpu_display, 1, size))
            print(alignment)
            map_show_ship_or_symbols(map_cpu_display, size, location, alignment, ship_name, fleet_cpu)


def find_biggest_ship_in_fleet(fleet):
    print()
    print("initializing function find_biggest_ship_in_fleet")
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
    print("biggest_ship, biggest_ship_size", biggest_ship, biggest_ship_size)
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
    ship_name, ship_size = find_biggest_ship_in_fleet(fleet_to_search) # searching for biggest ship in fleet
    if ship_name is  None:
        print("game over print") # need to create function game over
    else:
        width = ship_size * 2 - 1
        height = ship_size * 2 - 1
        while True:
            coordinates = search_map_for_pattern(map_to_search, width, height) # getting list of possible coordinates
            if coordinates: # if there is any coordinates in list, we will choose one random
                chosen_coordinates = random.choice(coordinates) # choosing coordinates using random
                break
            else: # if there was no coordinates in list, we will reduce width or height and search map again and again
                reduce = random.choice(["width", "height"]) #choosing randomly, what to reduce for searching
                if reduce == "width":
                    width = width - 1
                    height = height
                    coordinates = search_map_for_pattern(map_to_search, width, height) # getting list of possible coordinates
                    if coordinates: # if there is any coordinates in list, we will choose one random
                        chosen_coordinates = random.choice(coordinates) # choosing coordinates using random
                        break
                    else: # if there was no coordinates found with reduced width, we will restore width and search with reduced height
                        width = width + 1
                        height = height - 1
                        coordinates = search_map_for_pattern(map_to_search, width, height) # getting list of possible coordinates
                        if coordinates: # if there is any coordinates in list, we will choose one random
                            chosen_coordinates = random.choice(coordinates) # choosing coordinates using random
                            break
                        else: #reducing width and height and try loop again
                            width = width -1 
                            height = height - 1
                elif reduce == "height":
                    width = width
                    height = height - 1
                    coordinates = search_map_for_pattern(map_to_search, width, height) # getting list of possible coordinates
                    if coordinates: # if there is any coordinates in list, we will choose one random
                        chosen_coordinates = random.choice(coordinates) # choosing coordinates using random
                        break
                    else: # if there was no coordinates found with reduced width, we will restore height and search with reduced width
                        width = width -1
                        height = height + 1
                        coordinates = search_map_for_pattern(map_to_search, width, height) # getting list of possible coordinates
                        if coordinates: # if there is any coordinates in list, we will choose one random
                            chosen_coordinates = random.choice(coordinates) # choosing coordinates using random
                            break
                        else: #reducing width and height and try loop again
                            width = width - 1 
                            height = height - 1
        # loop is over, coordinates are found
        coord_x, coord_y = chosen_coordinates # now we know coordinates last pattern was used, so based on that, we will take sweet spot - center of pattern and shoot
        coordinate_x = coord_x + width // 2 + random.choice([0,width % 2])
        coordinate_y = coord_y + height // 2 + random.choice([0,height % 2])
    print("coordinate_x, coordinate_y", coordinate_x, coordinate_y)
    return coordinate_x, coordinate_y



def action_perform_shoot(player, x, y, map_hidden, map_display, fleet):
    print()
    print("initializing function action_perform_shoot")
    print("shooting at coordinates x y:", x, y)
    """
    Perform a shooting action on the game board.
    
    Parameters:
    - player (str): The player making the shot ("CPU" or "Human").
    - x (int): The x-coordinate of the shot.
    - y (int): The y-coordinate of the shot.
    - map_hidden (list): The hidden map that tracks shots.
    - map_display (list): The displayed map that shows ships.
    - fleet (dict): Information about the fleet of ships.
    - game_actions_log (list): Log of game actions.
    - start_time (float): The game start time for logging.
    - SHIP_SYMBOLS (dict): Symbols used for different states of the ship.
    
    Returns:
    - str: The outcome of the action ("Hit" or "Miss").
    """
    global game_actions_log, start_time, SHIP_SYMBOLS
    # Find the ship and its details at the given coordinates.
    ship_name, ship_size, coordinates_list, coordinates_id = find_ship_and_coordinates(fleet, [x, y])
    # Log and display the outcome.
    try:
        if ship_name:
            print(f' {player} performed shot on coordinates {x} and {y}, {ship_name} was damaged')
            # A ship was hit; proceed to update maps and logs.
            handle_ship_hit(player, x, y, map_hidden, map_display, fleet, 
                            ship_name, ship_size, coordinates_list, 
                            coordinates_id)
        else:
            print(f' {player} performed shot on coordinates {x} and {y}, it was a MISS')
            # No ship was hit; mark as a miss.
            handle_miss(player, x, y, map_hidden, map_display)
            return "Miss"
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def handle_ship_hit(player, x, y, map_hidden, map_display, fleet, ship_name, ship_size, coordinates_list, coordinates_id):
    print()
    print("initializing function handle_ship_hit")
    global game_actions_log, start_time, SHIP_SYMBOLS, cpu_shot_log_tmp
    """
    Handle the scenario where a ship is hit.
    """
    if player == "CPU":
        cpu_shot_log_tmp.append([x, y])  # Adding hit coordinates to temporary CPU actions list
        print(player, " actions log by tomosius: ", cpu_shot_log_tmp)
    check_ship_damage(player, fleet, [x, y], map_display, map_hidden)  # Checking if ship was completely sunk
    print(player, " made a hit, now we will update log based on coordinates_list: ", coordinates_list)
    print(" coordinates list: ", coordinates_list)
    # Log the action.
    timer = time.time() - start_time
    action_outcome = f'{ship_name} was hit'
    game_actions_log.append([player, timer, x, y, action_outcome])
    # Update the displayed map.
    map_hidden[x][y] = SHIP_SYMBOLS["Hit"][0]
    # Mark the hit on display map. it will be the same symbol, just a different color
    update_display_map(ship_size, x, y, map_display, coordinates_list)
    print("game_actions_log", game_actions_log)


def handle_miss(player, x, y, map_hidden, map_display):
    print()
    print("initializing function handle_miss")
    """
    Handle the scenario where the shot is a miss.
    """
    global SHIP_SYMBOLS, start_time
    # Log the action.
    timer = time.time() - start_time
    action_outcome = f'it was a MISS'
    game_actions_log.append([player, timer, x, y, action_outcome])
    map_hidden[x][y] = SHIP_SYMBOLS["Miss"][0]
    map_display[x][y] = SHIP_SYMBOLS["Miss"][0]

def update_display_map(ship_size, x, y, map_display, coordinates_list):
    print()
    print("initializing function update_display_map")
    """
    Update the displayed map based on the hit.
    """
    global SHIP_SYMBOLS
    ship_alignment = str(detect_ship_alignment(coordinates_list)) + "Sunk"
    print(" ship alignment is now: ", ship_alignment)
    if ship_size == 1:
        map_display[x][y] = SHIP_SYMBOLS[ship_alignment][0]
    else:
        # Find the symbol to use based on the hit location.
        for coord_id, (x1, y1) in coordinates_list.items():
            if x == x1 and y == y1:
                if coord_id == 0:
                    symbol_id = 0
                else:
                    symbol_id = 1
        map_display[x][y] = SHIP_SYMBOLS[ship_alignment][symbol_id]





def find_ship_and_coordinates(fleet, target_coordinates):
    """
    Find the ship name, ship size, the list of coordinates, and the coordinate ID 
    to which the target_coordinates belong.
    
    Args:
        fleet (dict): Dictionary containing ship information.
        target_coordinates (list): Coordinates [x, y] to search for.
        
    Returns:
        tuple: A tuple containing:
        - ship_name (str): Name of the ship at the coordinates, if found.
        - ship_size (int): Size of the ship, if found.
        - ship_coordinates_list (list): List of coordinates of the ship, if found.
        - coordinates_id (int): Index of the coordinates in the list, if found.
        Returns (None, None, None, None) if no match is found.
    """
    # Iterate through each ship in the fleet to find matching coordinates
    for ship_name, ship_info in fleet.items():
        
        # Loop through each list of coordinates assigned to the current ship
        for ship_coordinates_list in ship_info['Coordinates']:
            
            # Try to find the index of the target coordinates in the list
            try:
                coordinates_id = ship_coordinates_list.index(target_coordinates)
                
                # Return the details of the ship and coordinates if a match is found
                return ship_name, ship_info['Size'], ship_coordinates_list, coordinates_id
                
            except ValueError:
                # Continue to the next iteration if no match is found
                continue

    # Return None for all fields if no matching coordinates are found
    return None, None, None, None





def check_ship_damage(player, fleet, coordinates, map_display, map_hidden):
    print()
    print("initializing function check_ship_damage")
    print("player, fleet, coordinates, map_display, map_hidden", player, fleet, coordinates)
    print(f"Type of fleet at the start of check_ship_damage: {type(fleet)}")

    """
    Check if a ship is completely damaged (sunk) and updates the game state accordingly.
    
    Args:
        player (str): The player who performed the action ("CPU" or "Human").
        fleet (dict): The current fleet information.
        ship_name (str): The name of the ship that was hit.
        ship_size (int): The size of the ship.
        alignment (str): The alignment of the ship ("Horizontal" or "Vertical").
        coordinates_list (list): The list of coordinates of the ship.
        coordinates_id (int): The ID of the ship's coordinates in the fleet.
        map_hidden (list of lists): The hidden map representing the game state.
    Returns:
        str: "Game Over" if all ships are sunk, otherwise None.
    """
    # Global variables
    global start_time, cpu_shot_log_tmp, SHIP_SYMBOLS, game_result
    # Initialize ship_damaged as False
    ship_sunk = False
    ship_name, ship_size, coordinates_list, coordinates_list_id = find_ship_and_coordinates(fleet, coordinates)
    alignment = detect_ship_alignment(coordinates_list)
    # Check if all parts of the ship are damaged
    for i in coordinates_list:
        y, x = i  # Extract the X and Y coordinates
        if map_hidden[y][x] == SHIP_SYMBOLS["Hit"][0]:
            ship_sunk = True
        else:
            ship_sunk = False  # Set to False if any part is not damaged
            break  # Exit the loop
    # If the ship is completely damaged (sunk)
    if ship_sunk:
        print(" ship ", ship_name, " was sunk")
        # Update the hidden and visible maps
        alignment = alignment + "Sunk"
        map_show_ship_or_symbols(map_hidden, ship_size, coordinates_list[0], alignment, ship_name, fleet)
        map_show_ship_or_symbols(map_display, ship_size, coordinates_list[0], alignment, ship_name, fleet)
        # Record the action
        timer = time.time() - start_time
        action_outcome = f'{ship_name} was sunk'
        game_actions_log.append([player, timer, x, y, action_outcome])
        # remove ship coordinated from CU action log TMP
        if player == "CPU":
            cpu_shot_log_tmp = update_cpu_shot_log_tmp(coordinates_list)
        # Update the fleet information
        del fleet[ship_name]["Coordinates"][coordinates_list_id]
        fleet[ship_name]["Quantity"] -= 1
        # Remove the ship from the fleet if it has no more coordinates
        if not fleet[ship_name]["Coordinates"]:
            del fleet[ship_name]
        # Check if the game is over
        if not fleet:
            timer = time.time() - start_time
            action_outcome = 'Game Over'
            game_actions_log.append([player, timer, x, y, action_outcome])
            game_result = "Game Over"

        


def update_cpu_shot_log_tmp(coordinates_list):
    print()
    print("initializing function update_cpu_shot_log_tmp", coordinates_list)
    global cpu_shot_log_tmp
    """
    Update the CPU shot log by removing coordinates that are present in
    the provided coordinates_list, implying that a ship has been sunk.
    
    Parameters:
    - coordinates_list (list): A list of coordinates that are to be removed.
    - cpu_shot_log_tmp (list): The existing CPU shot log to be updated.

    Returns:
    - list: Updated CPU shot log.
    """
    # Initialize an empty list to store the updated shot log.
    updated_log = []
    try:
        # Iterate through each coordinate in the CPU shot log.
        for coord_in_log in cpu_shot_log_tmp:
            
            # Use a flag to indicate whether the coordinate is found
            # in the coordinates_list.
            is_in_coordinates_list = False
            print(is_in_coordinates_list)
            # Iterate through each coordinate in the provided list.
            for coord_to_remove in coordinates_list:
                print(" coord to remove", coord_to_remove)
                # If a match is found, set the flag to True.
                if coord_in_log == coord_to_remove:
                    is_in_coordinates_list = True
                    break
            
            # If the coordinate is not in coordinates_list, add it to the updated log.
            if not is_in_coordinates_list:
                updated_log.append(coord_in_log)
                print(" cord in log:", coord_in_log)
                print("updated log: ", updated_log)
        
        # Replace the original CPU shot log with the updated version.
        cpu_shot_log_tmp = updated_log
        print("cpu_shot_log_tmp", cpu_shot_log_tmp)

    except Exception as e:
        print(f"An error occurred: {e}")
    
    return cpu_shot_log_tmp



def detect_ship_alignment(coordinates_list):
    print()
    print("initializing function detect_ship_alignment")
    """
    Detect the alignment of a ship based on its coordinates.
    
    Args:
        coordinates_list (list): List of coordinates to analyze. Each coordinate is a tuple (x, y).
        
    Returns:
        str: "Horizontal" if the ship is positioned horizontally, 
             "Vertical" if vertically, 
             "Single" if it has only one coordinate,
             or "Unknown" if undetermined.
    """
    # Handle the case when only one coordinate is present
    if len(coordinates_list) == 1:
        print("Single Ship Detected")
        return "Single"
    try:
        # Initialize empty lists for y-coordinates and x-coordinates
        y_values = []
        x_values = []
        # Extract y-coordinates from the list
        for coord in coordinates_list:
            y_values.append(coord[0])
        # Check for horizontal alignment: all y-values should be the same
        is_horizontal = True
        for y in y_values:
            if y != y_values[0]:
                is_horizontal = False
                break
        if is_horizontal:
            print("Horizontal Ship Detected")
            return "Horizontal"
        # Extract x-coordinates from the list
        for coord in coordinates_list:
            x_values.append(coord[1])
        # Check for vertical alignment: all x-values should be the same
        is_vertical = True
        for x in x_values:
            if x != x_values[0]:
                is_vertical = False
                break
        if is_vertical:
            print("Vertical Ship Detected")
            return "Vertical"
    except TypeError:
        # Handle the error gracefully and print a debug message
        print(f"TypeError: coordinates_list contains an unsupported data type. Received: {coordinates_list}")
        return "Unknown"
    
    # If none of the above conditions are met, the alignment is unknown
    print("Unknown Ship Alignment")
    return "Unknown"





def cpu_continue_killing_ship(map_to_search):
    print()
    print("initalizing function cpu_continue_killing_ship")
    """
    Chooses coordinates to shoot at based on ship alignment detection.
    Args:
        map_to_search (list of lists): The map to search for ship coordinates.
        DEFAULT_SYMBOL (str): The default symbol representing untargeted cells in the map.
    Returns:
        tuple: The chosen coordinates (x, y).
    """
    # Making cpu_shot_log_tmp global as it's accessed within the function
    global cpu_shot_log_tmp, DEFAULT_SYMBOL
    # Initialize variables to hold the selected coordinates
    x, y = None, None
    # Detect the alignment of the ship using the cpu_shot_log_tmp
    alignment = detect_ship_alignment(cpu_shot_log_tmp)
    # Define the map boundaries
    max_x = len(map_to_search[0]) - 1
    max_y = len(map_to_search) - 1
    # Initialize an empty list to hold adjacent coordinates
    adjacent_coordinates = []
    # Loop through the shot log to find adjacent coordinates
    for coord in cpu_shot_log_tmp:
        x, y = coord
        # Check for Horizontal alignment and append coordinates
        if alignment == "Horizontal":
            if x + 1 <= max_x and map_to_search[x + 1][y] == DEFAULT_SYMBOL:
                adjacent_coordinates.append((x + 1, y))
            if x - 1 >= 0 and map_to_search[x - 1][y] == DEFAULT_SYMBOL:
                adjacent_coordinates.append((x - 1, y))
        # Check for Vertical alignment and append coordinates
        elif alignment == "Vertical":
            if y + 1 <= max_y and map_to_search[x][y + 1] == DEFAULT_SYMBOL:
                adjacent_coordinates.append((x, y + 1))
            if y - 1 >= 0 and map_to_search[x][y - 1] == DEFAULT_SYMBOL:
                adjacent_coordinates.append((x, y - 1))
        # Check for Unknown or Single alignment and append coordinates
        else:
            if x + 1 <= max_x and map_to_search[x + 1][y] == DEFAULT_SYMBOL:
                adjacent_coordinates.append((x + 1, y))
            if x - 1 >= 0 and map_to_search[x - 1][y] == DEFAULT_SYMBOL:
                adjacent_coordinates.append((x - 1, y))
            if y + 1 <= max_y and map_to_search[x][y + 1] == DEFAULT_SYMBOL:
                adjacent_coordinates.append((x, y + 1))
            if y - 1 >= 0 and map_to_search[x][y - 1] == DEFAULT_SYMBOL:
                adjacent_coordinates.append((x, y - 1))
    # Randomly choose one of the adjacent coordinates if any are available
    if adjacent_coordinates:
        x, y = random.choice(adjacent_coordinates)
    print("x, y", x, y)
    return x, y  # Return the selected x and y coordinates






def cpu_move():
    global game_result, fleet_cpu, map_cpu_hidden, map_cpu_display , cpu_shot_log_tmp, game_actions_log, start_time, SHIP_SYMBOLS# change to player fleet and player hidden map
    # check if there is any damaged and un-sunk ships in cpu_shot_log_tmp
    player = "CPU"
    if len(cpu_shot_log_tmp) == 0:
        # there is no damaged ships
        x, y = cpu_choose_shooting_coordinates_biggest_ship(fleet_cpu, map_player_hidden) # choosing coordinates to shot
        action_perform_shoot(player, x, y, map_cpu_hidden, map_cpu_display, fleet_cpu)
        if game_result == "Game Over":
            print ("CPU HAS WON")
    else:
        x, y = cpu_continue_killing_ship(map_cpu_hidden)
        action_perform_shoot(player, x, y, map_cpu_hidden, map_cpu_display, fleet_cpu) # shooting and getting result Hit or Miss
        if game_result == "Game Over":
            print ("CPU HAS WON")






def battleship_game ():
    global start_time
    start_time = time.time() # starting timer
    clear_terminal()
    cpu_deploy_all_ships()
    print_two_maps(map_cpu_hidden, map_cpu_display,"hidden_cpu_map","cpu_map")
    print_fleet(fleet_cpu)
    for i in range(10):
        cpu_move()
        #print(game_actions_log)
        print_two_maps(map_cpu_hidden, map_cpu_display,"hidden_cpu_map","cpu_map")





battleship_game()
print(" test done")
print("all shooting actions: ", game_actions_log)






















