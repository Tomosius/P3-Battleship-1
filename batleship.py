import curses
import random
import copy
import rich



# Constants for map dimensions and default symbol
MAP_WIDTH = 10
MAP_HEIGHT = 10
DEFAULT_SYMBOL = '0'  # New global variable for the default symbol

# Create maps for CPU and Player
map_cpu = [[DEFAULT_SYMBOL for _ in range(MAP_HEIGHT)] for _ in range(MAP_WIDTH)]  
map_cpu_hidden = [[DEFAULT_SYMBOL for _ in range(MAP_HEIGHT)] for _ in range(MAP_WIDTH)]  
map_player_hidden = [[DEFAULT_SYMBOL for _ in range(MAP_HEIGHT)] for _ in range(MAP_WIDTH)]  
map_player = [[DEFAULT_SYMBOL for _ in range(MAP_HEIGHT)] for _ in range(MAP_WIDTH)]  

# ... Remaining code ...


# Initialize game-related variables
game_result = None  # Store the game result (win, lose, or draw)
cpu_actions = []  # List to store CPU actions (shots, hit/miss, coordinates)
player_actions = []  # List to store Player actions (shots)
cpu_shoot_coordinates_log = [["x","y"]]  # List to store CPU's shot coordinates


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
    "DingyBoat": {"Size": 1, "Quantity": 0, "Coordinates": []}
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


def game_adjust(fleet):
    """Adjust game settings, including the map and Battle Ships Fleet.

    Args:
        fleet (dict): A dictionary containing fleet information.

    Returns:
        bool: True if the game adjustment was interrupted, False otherwise.
    """
    while True:
        try:
            changes = input(
                "Would you like to adjust game settings? (Y/N): ").capitalize()
            if changes in ["Y", "YES"]:
                print("Using default game settings; the map is 10x10.")
                print_fleet(fleet)
                choice = input("1. Modify Game Map\n2. Modify Ship\n3. Add New Ship\n4. Finish\nEnter choice: ")
                if choice.isdigit():
                    choice = int(choice)
                    if choice == 1:
                        map_size_select()
                    elif choice == 2:
                        modify_ship(fleet)
                    elif choice == 3:
                        add_new_ship(fleet)
                    elif choice == 4:
                        return False
                    else:
                        print("Invalid choice.")
                else:
                    print("Please enter a valid choice (1/2/3/4).")
            elif changes in ["N", "NO", ""]:
                return False
        except KeyboardInterrupt:
            print("Game adjustment interrupted.")
            return True


def map_size_select():
    """Select the size of the game map (Width and Height).
    
    Updates:
        - Global variables for map dimensions and maps.
    """
    global MAP_WIDTH, MAP_HEIGHT, map_cpu, map_player
    while True:
        try:
            map_size = input("Enter map size (Width,Height). Example: 10,10: ")
            MAP_WIDTH, MAP_HEIGHT = map(int, map_size.split(","))
            print(f"The game map is {MAP_WIDTH}x{MAP_HEIGHT}.")
            map_cpu = initialize_maps(MAP_WIDTH, MAP_HEIGHT)
            map_player = initialize_maps(MAP_WIDTH, MAP_HEIGHT)
            break
        except ValueError:
            print("Invalid input. Enter two numbers separated by a comma.")


def modify_ship(fleet):
    """Modify an existing ship in the fleet.

    Args:
        fleet (dict): Dictionary containing fleet information.
    """
    print_fleet(fleet)
    ship_choice = input("Enter the ship name or index to modify: ")
    if ship_choice.isdigit():
        ship_index = int(ship_choice) - 1
        ship_names = list(fleet.keys())
        if 0 <= ship_index < len(ship_names):
            ship_name = ship_names[ship_index]
        else:
            print("Invalid index.")
            return
    else:
        ship_name = ship_choice

    if ship_name not in fleet:
        print(f"The ship '{ship_name}' does not exist.")
        return

    size = int(input(f"Enter new size for '{ship_name}': "))
    quantity = int(input(f"Enter new quantity for '{ship_name}': "))
    fleet[ship_name]["Size"] = size
    fleet[ship_name]["Quantity"] = quantity
    fleet[ship_name]["Coordinates"] = []


def add_new_ship(fleet):
    """Add a new ship to the fleet.

    Args:
        fleet (dict): Dictionary containing fleet information.
    """
    ship_name = input("Enter the name of the new ship: ")
    size = int(input("Enter the size of the new ship: "))
    quantity = int(input("Enter the quantity of the new ship: "))
    fleet[ship_name] = {"Size": size, "Quantity": quantity, "Coordinates": []}


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


def check_coordinates(x, y, game_map):
    """Check if the coordinates are within map boundaries.

    Args:
        x (int): X-coordinate.
        y (int): Y-coordinate.
        game_map (list): 2D map.

    Returns:
        bool: True if coordinates are valid, False otherwise.
    """
    if x >= len(game_map) or y >= len(game_map[0]) or x < 0 or y < 0:
        print(f"Coordinates ({x}, {y}) are out of the map. Enter correct values.")
        return False
    return True


def check_ship_input(ship_info):
    """Check if ship deployment info is valid.

    Args:
        ship_info (str): Ship deployment information (x, y, and alignment).

    Returns:
        bool: True if input is valid, False otherwise.
    """
    try:
        parts = [part.strip() for part in ship_info.split(',')]
        if len(parts) == 3:
            x, y, align = parts
            if x.isdigit() and y.isdigit() and align.lower() in ["v", "h"]:
                return True
            else:
                print("Check entered values and information.")
                return False
        else:
            print("Enter coordinates, alignment, and ship size separated by commas.")
            return False
    except ValueError:
        print("Enter coordinates, alignment, and ship size separated by commas.")
        return False


def input_ship_check(x, y, align, game_map, length):
    """Check if ship deployment input is valid.

    Args:
        x (int): X-coordinate.
        y (int): Y-coordinate.
        align (str): Ship alignment ("H" for horizontal, "V" for vertical).
        game_map (list): 2D map.
        length (int): Length of the ship.

    Returns:
        bool: True if input is valid, False otherwise.
    """
    if not check_coordinates(x, y, game_map):
        return False
    if align == "H":
        if all(game_map[x][y + i] == 0 for i in range(length)):
            return True
        else:
            print(f"Cannot place the ship horizontally at coordinates ({x}, {y}).")
            return False
    elif align == "V":
        if all(game_map[x + i][y] == 0 for i in range(length)):
            return True
        else:
            print(f"Cannot place the ship vertically at coordinates ({x}, {y}).")
            return False
    else:
        print("Invalid alignment.")
        return False


def deploy_single_ship(game_map, length, location, alignment, ship_name, fleet):
    """Deploy a single ship on the map.

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
    row, column = location
    ship_coordinates = []
    if length == 1:
        game_map[row][column] = SHIP_SYMBOLS["Single"][0]
        ship_coordinates.append([row, column])
        return game_map
    else:
        if alignment == "H":
            ship_coordinates.append([row, column])
            game_map[row][column] = SHIP_SYMBOLS["Horizontal"][0][0]
            for i in range(length - 1):
                game_map[row][column + i + 1] = SHIP_SYMBOLS["Horizontal"][1][0]
                ship_coordinates.append([row, column + i + 1])
        elif alignment == "V":
            ship_coordinates.append([row, column])
            game_map[row][column] = SHIP_SYMBOLS["Vertical"][0][0]
            for i in range(length - 1):
                game_map[row + i + 1][column] = SHIP_SYMBOLS["Vertical"][1][0]
                ship_coordinates.append([row + i + 1, column])
    fleet[ship_name]["Coordinates"].append(ship_coordinates)
    print_map(game_map)
    print(f"Deployed {ship_name} at Coordinates: {location}")
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
    map_height, map_width = len(map), len(map[0])
    
    # Initialize an empty list to store the coordinates where the pattern matches
    coordinates = []
    
    # Create the pattern using list comprehension
    pattern = [[symbol] * width for _ in range(height)]
    
    # Loop through the map to search for the pattern
    for row in range(map_height - height + 1):
        for col in range(map_width - width + 1):
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
    map_cpu = initialize_maps(MAP_WIDTH, MAP_HEIGHT)

    # Make a fresh copy of the fleet, in case there were any changes
    # made for map size or fleet
    fleet_cpu = copy.deepcopy(DEFAULT_FLEET)

    for ship_name, ship_info in fleet_cpu.items():
        quantity = ship_info["Quantity"]
        size = ship_info["Size"]
        
        print(f"Deploying {quantity} {ship_name}(s) of size {size}")
        
        for i in range(quantity):
            symbol = random.choice(["H", "V"])  # Horizontal or vertical
            
            if symbol == "H":
                location = random.choice(search_map_for_pattern(map_cpu, size, 1))
            elif symbol == "V":
                location = random.choice(search_map_for_pattern(map_cpu, 1, size))
                
            deploy_single_ship(map_cpu, size, location, symbol, ship_name, fleet_cpu)


def player_deploy_all_ships():
    """Deploy all player ships on the map.

    Updates:
        - Global variables fleet_player, DEFAULT_FLEET, map_player

    Returns:
        list: The player's map with deployed ships.
    """
    global fleet_player, DEFAULT_FLEET, map_player, DEFAULT_SYMBOL  # Declare global variables
    
    # Initialize map_player with DEFAULT_SYMBOL, if not already done
    map_player = initialize_maps(MAP_WIDTH, MAP_HEIGHT)
    
    # Make a fresh copy of the fleet, in case there were any changes
    # made for map size or fleet
    fleet_player = copy.deepcopy(DEFAULT_FLEET)
    
    for ship_name, ship_info in fleet_player.items():
        quantity = ship_info["Quantity"]
        size = ship_info["Size"]
        
        for i in range(quantity):
            print_map(map_player)
            print(f"Now you will be deploying ship {ship_name} NO: {i + 1} of a total {quantity} of this type of ships.")
            
            while True:  # Loop to keep asking the user to input correct information to deploy a ship
                random_x = random.randint(0, len(map_player) - 1)
                random_y = random.randint(0, len(map_player[0]) - 1)
                random_alignment = random.choice(['H', 'V'])
                
                user_ship_input = input(
                    f"Please choose coordinates where you would like to deploy your ship, also the ship alignment and its size. (Column, Row, alignment) Example: {random_x},{random_y},{random_alignment}: ")
                
                if not check_ship_input(user_ship_input):
                    continue
                
                x, y, align = user_ship_input.split(',')
                x = int(x)  # Convert to integer
                y = int(y)  # Convert to integer
                alignment = align[0].upper()  # Taking just the first letter and in uppercase
                
                if not check_coordinates(x, y, map_player):
                    continue
                elif not input_ship_check(x, y, alignment, map_player, size):
                    continue
                
                location = [x, y]
                deploy_single_ship(map_player, size, location, alignment, ship_name, fleet_player)
                break  # Successfully deployed the ship, so exit the loop
    return map_player


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
    Find the ship name and the list ID of coordinates to which the target_coordinates belong.

    Args:
        fleet (dict): Dictionary containing ship information.
        coordinates (list): Coordinates to search for.

    Returns:
        A tuple containing the ship name and coordinates list ID if found, otherwise (None, None).
    """
    for ship_name, ship_info in fleet.items():
        for list_id, coordinates_list in enumerate(ship_info['Coordinates']):
            if coordinates in coordinates_list:
                return ship_name, list_id

    # If coordinates are not found, return (None, None)
    return None, None


def check_ship_status(fleet, map, hidden_map, coordinates):
    """
    Check the status of a ship at given coordinates on the map.

    Args:
        fleet (dict): Dictionary containing ship information.
        map (list of lists): 2D map representing the game board.
        hidden_map (list of lists): 2D map representing hidden ship positions.
        coordinates (list): Coordinates to check.

    Returns:
        "sunk" if the ship is entirely sunk, "incomplte" if part of the ship is damaged, or "not found" if no ship is at the coordinates.
    """
    global DEFAULT_SYMBOL

    # Find the ship and its list ID based on coordinates
    ship_name, list_id = find_ship_and_coordinates(fleet, coordinates)

    if ship_name is None:
        return "not found"  # No ship found at the coordinates
    
    full_ship_coordinates = fleet[ship_name]["Coordinates"][list_id]

    # Initialize variables to track ship status
    all_hit = True
    some_hit = False

    # Check the status of each coordinate of the ship
    for coord in full_ship_coordinates:
        x, y = coord
        if hidden_map[x][y] == DEFAULT_SYMBOL["Hit"]:
            all_hit = True  # At least one coordinate is "Hit"
        else:
            all_hit = False


    # Determine the ship status based on the checks
    if all_hit:
        # All coordinates are "Hit," remove the ship from the fleet and decrement quantity
        fleet[ship_name]["Coordinates"].pop(list_id)
        fleet[ship_name]["Quantity"] -= 1
        return "sunk"  # The ship is entirely sunk
    else:
        # No coordinates are "Hit" or "Miss," indicating incomplete information
        return "incomplete"  # The status is incomplete due to missing information


def mark_ship_on_map_sunk(map, hidden_map, coordinates_list):
    global SHIP_SYMBOLS
    for coord in coordinates_list:
        x, y = coord
        for symbol_name, symbol_list in SHIP_SYMBOLS.items():
            if map[x][y] in symbol_list:
                symbol_id = symbol_name
        break









cpu_deploy_all_ships()
print_map(map_cpu)
print("mokomes")
def test():
    global fleet_cpu, map_cpu_hidden
    ship_name, ship_size = find_biggest_ship_in_fleet(fleet_cpu) # searching for biggest ship in fleet
    coordinates = search_map_for_pattern(map_cpu_hidden, ship_size, ship_size) # getting list of possible coordinates
    tomasx, tomasy = cpu_choose_shooting_coordinates_biggest_ship(fleet_cpu, map_cpu_hidden)
    print(ship_name, ship_size)
    print (tomasx, tomasy)

test()
print("baigta")
print(fleet_cpu)