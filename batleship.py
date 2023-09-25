import curses
import random
import copy
import rich
from typing import Union



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
cpu_shoot_coordinates_log = []  # List to store CPU's shot coordinates


def initialize_maps(width: int, height: int) -> list:
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
FLEET_DEFAULT = {
    "AircraftCarrier": {"Size": 5, "Quantity": 1, "Coordinates": []},
    "Battleship": {"Size": 4, "Quantity": 3, "Coordinates": []},
    "Cruiser": {"Size": 3, "Quantity": 0, "Coordinates": []},
    "Submarine": {"Size": 3, "Quantity": 0, "Coordinates": []},
    "Destroyer": {"Size": 2, "Quantity": 0, "Coordinates": []},
    "DingyBoat": {"Size": 1, "Quantity": 0, "Coordinates": []}
}

# Create copies of default fleet settings for CPU and Player
fleet_cpu = copy.deepcopy(FLEET_DEFAULT)  # Copy for CPU
fleet_player = copy.deepcopy(FLEET_DEFAULT)  # Copy for Player


def print_fleet(fleet: dict) -> None:
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
ship_symbols = {
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


def game_adjust(fleet: dict) -> bool:
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


def modify_ship(fleet: dict):
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


def add_new_ship(fleet: dict):
    """Add a new ship to the fleet.

    Args:
        fleet (dict): Dictionary containing fleet information.
    """
    ship_name = input("Enter the name of the new ship: ")
    size = int(input("Enter the size of the new ship: "))
    quantity = int(input("Enter the quantity of the new ship: "))
    fleet[ship_name] = {"Size": size, "Quantity": quantity, "Coordinates": []}


def print_map(game_map: list):
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


def check_coordinates(x: int, y: int, game_map: list) -> bool:
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


def check_ship_input(ship_info: str) -> bool:
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


def input_ship_check(x: int, y: int, align: str, game_map: list, length: int) -> bool:
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


def deploy_single_ship(game_map: list, length: int, location: list, 
                       alignment: str, ship_name: str, fleet: dict) -> list:
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



def search_map(game_map: list, width: int, height: int) -> Union[list, str]:
    """Search the map for a pattern to find suitable deployment coordinates for the CPU.
    
    Args:
        game_map (list): A 2D map to search.
        width (int): Width of the pattern to search for.
        height (int): Height of the pattern to search for.

    Returns:
        Union[list, str]: A list of suitable coordinates or 'noneFound' if none are found.
    """
    global DEFAULT_SYMBOL  # Declare global variable
    
    coordinates_list = []
    for i in range(len(game_map) - height + 1):
        for j in range(len(game_map[0]) - width + 1):
            sub_grid = [row[j:j + width] for row in game_map[i:i + height]]
            
            # Use DEFAULT_SYMBOL for comparison
            if all(cell == DEFAULT_SYMBOL for row in sub_grid for cell in row):
                coordinates_list.append((i, j))
    
    if not coordinates_list:
        return 'noneFound'
    
    return coordinates_list



def cpu_deploy_all_ships():
    """Deploy all CPU ships on the map.

    Updates:
        - Global variables fleet_cpu, fleet_default, map_cpu

    Returns:
        None
    """
    global fleet_cpu, fleet_default, map_cpu, DEFAULT_SYMBOL  # Declare global variables
    
    # Initialize map_cpu with DEFAULT_SYMBOL, if not already done
    map_cpu = initialize_maps(MAP_WIDTH, MAP_HEIGHT)

    # Make a fresh copy of the fleet, in case there were any changes
    # made for map size or fleet
    fleet_cpu = copy.deepcopy(fleet_default)

    for ship_name, ship_info in fleet_cpu.items():
        quantity = ship_info["Quantity"]
        size = ship_info["Size"]
        
        print(f"Deploying {quantity} {ship_name}(s) of size {size}")
        
        for i in range(quantity):
            symbol = random.choice(["H", "V"])  # Horizontal or vertical
            
            if symbol == "H":
                location = random.choice(search_map(map_cpu, size, 1))
            elif symbol == "V":
                location = random.choice(search_map(map_cpu, 1, size))
                
            deploy_single_ship(map_cpu, size, location, symbol, ship_name, fleet_cpu)
    
    print_map(map_cpu)


def player_deploy_all_ships():
    """Deploy all player ships on the map.

    Updates:
        - Global variables fleet_player, fleet_default, map_player

    Returns:
        list: The player's map with deployed ships.
    """
    global fleet_player, fleet_default, map_player, DEFAULT_SYMBOL  # Declare global variables
    
    # Initialize map_player with DEFAULT_SYMBOL, if not already done
    map_player = initialize_maps(MAP_WIDTH, MAP_HEIGHT)
    
    # Make a fresh copy of the fleet, in case there were any changes
    # made for map size or fleet
    fleet_player = copy.deepcopy(fleet_default)
    
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


def find_all_patterns(width, height, map, symbol):
    """
    Find all occurrences of a pattern in a map and return their coordinates.

    Args:
        width (int): Width of the pattern.
        height (int): Height of the pattern.
        map (list): The map as a nested list.
        symbol: The symbol to search for in the map.

    Returns:
        list: A list of coordinate tuples (row, col) where the pattern is found.
    """
    pattern = [[symbol] * width for _ in range(height)]  # Creating the pattern
    map_height = len(map)
    map_width = len(map[0])
    coordinates = []

    for row in range(map_height - height + 1):
        for col in range(map_width - width + 1):
            if all(
                map[row + i][col + j] == pattern[i][j]
                for i in range(height)
                for j in range(width)
            ):
                coordinates.append([row, col])

    return coordinates
