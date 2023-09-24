import curses
import random
import copy

# Constants for map dimensions
MAP_WIDTH = 10
MAP_HEIGHT = 10

# Initialize the game result, CPU actions, and player actions
gameResult = None  # Stores the result of the game (win, lose, or draw)
cpuActions = []  # List to store CPU actions (shots)
playerActions = []  # List to store Player actions (shots)
cpuShootCoordinates = []  # List to store CPU's shot coordinates


def initializeMaps(width: int, height: int) -> list:
    """
    Initialize a 2D map with given dimensions.

    Args:
        width (int): The width of the map.
        height (int): The height of the map.

    Returns:
        list: A 2D map filled with zeros.
    """
    return [[0 for _ in range(height)] for _ in range(width)]


# Create maps for CPU and Player
mapCpu = initializeMaps(MAP_WIDTH, MAP_HEIGHT)  # CPU's visible map
mapCpuHidden = initializeMaps(MAP_WIDTH, MAP_HEIGHT)  # CPU's hidden map
mapPlayerHidden = initializeMaps(MAP_WIDTH, MAP_HEIGHT)  # Player's hidden map
mapPlayer = initializeMaps(MAP_WIDTH, MAP_HEIGHT)  # Player's visible map

# Default settings for the fleet
FLEET_DEFAULT = {
    "AircraftCarrier": {"Size": 5, "Quantity": 1, "Coordinates": []},
    "Battleship": {"Size": 4, "Quantity": 3, "Coordinates": []},
    "Cruiser": {"Size": 3, "Quantity": 0, "Coordinates": []},
    "Submarine": {"Size": 3, "Quantity": 0, "Coordinates": []},
    "Destroyer": {"Size": 2, "Quantity": 0, "Coordinates": []},
    "DingyBoat": {"Size": 1, "Quantity": 0, "Coordinates": []}
}

# Create a copy of default fleet settings for CPU and Player
fleetCpu = copy.deepcopy(FLEET_DEFAULT)  # Copy of default fleet settings for CPU
fleetPlayer = copy.deepcopy(FLEET_DEFAULT)  # Copy of default fleet settings for Player


def printFleet(fleet: dict) -> None:
    """
    Print the fleet information in a formatted manner.

    Args:
        fleet (dict): A dictionary containing fleet information.

    Returns:
        None
    """
    # Print the header for the fleet information
    print("{:<20} {:<10} {:<10} {:<50}".format("ShipType", "Size", "Quantity", "Coordinates"))
    print("=" * 40)

    # Loop through each ship in the fleet and print its details
    for ship, shipDetails in fleet.items():
        size = shipDetails["Size"]
        quantity = shipDetails["Quantity"]
        coordinates = shipDetails["Coordinates"]
        # Print the ship's details in a formatted manner
        print("{:<20} {:<10} {:<10} {:<50}".format(ship, size, quantity, coordinates))


# Colors used for rendering the game elements
COLORS = {
    "DarkYellow": "\033[33m",
    "LightGray": "\033[37m",
    "DarkBlue": "\033[34m",
    "DarkGreen": "\033[32m",
    "DarkRed": "\033[31m",
    "Reset": "\033[0m"
}

# Ship symbols remain the same as per your request
shipSymbols = {
    "Single": [COLORS["DarkYellow"] + chr(0x25C6) + COLORS["Reset"]],
    "Horizontal": [[COLORS["DarkBlue"] + chr(0x25C0) + COLORS["Reset"]],
                   [COLORS["DarkBlue"] + chr(0x25A4) + COLORS["Reset"]]],
    "Vertical": [[COLORS["DarkGreen"] + chr(0x25B2) + COLORS["Reset"]],
                 [COLORS["DarkGreen"] + chr(0x25A5) + COLORS["Reset"]]],
    "Hit": [COLORS["DarkRed"] + chr(0x25A6) + COLORS["Reset"]],
    "miss": [COLORS["LightGray"] + chr(0x2022) + COLORS["Reset"]],
    "singleSunk": [COLORS["DarkRed"] + chr(0x25C6) + COLORS["Reset"]],
    "horizontalSunk": [[COLORS["DarkRed"] + chr(0x25C0) + COLORS["Reset"]],
                       [COLORS["DarkRed"] + chr(0x25A4) + COLORS["Reset"]]],
    "verticalSunk": [[COLORS["DarkRed"] + chr(0x25B2) + COLORS["Reset"]],
                     [COLORS["DarkRed"] + chr(0x25A5) + COLORS["Reset"]]],
}


def gameAdjust(fleet : dict):
    """
    Adjust game settings, including the map and Battle Ships Fleet.

    Args:
        fleet (dict): A dictionary containing fleet information.

    Returns:
        bool: True if the game adjustment was interrupted, False otherwise.
    """
    while True:
        changes = input(
            "If you would like to adjust game settings, like map or Battle Ships Fleet, please enter Y (or enter or N to skip changing game settings and continue to deploying ships): \n")
        changes = changes.capitalize()
        try:
            if changes == "Y" or changes == "YES":
                print("Using default game settings; the map is 10 by 10.\n")
                print("Current game fleet is:")
                printFleet(fleet)
                print("\nOptions:")
                print("1. Modify Game Map")
                print("2. Modify existing ship")
                print("3. Add a new ship")
                print("4. Finish")
                choice = input("Enter your choice (1/2/3/4): ")
                if choice.isdigit():
                    choice = int(choice)
                    if choice == 1:
                        mapSizeSelect()
                    elif choice == 2:
                        modifyShip(fleet)
                    elif choice == 3:
                        addNewShip(fleet)
                    elif choice == 4:
                        return False
                    else:
                        print("Invalid choice. Please select a valid option.")
                else:
                    print("Invalid input. Please enter a valid choice (1/2/3/4).")
            elif changes == "N" or changes == "NO" or changes == "":
                return False
        except KeyboardInterrupt:
            print("Game adjustment interrupted.")
    return False


def mapSizeSelect():
    """
    Select the size of the game map (Width and Height).

    Updates:
        - global mapWidth
        - global mapHeight
        - global mapCpu
        - global mapPlayer

    Returns:
        None
    """
    global mapWidth, mapHeight, mapCpu, mapPlayer
    while True:
        mapSize = input(
            "Please select the map size you would like to play. Enter the first number for Width and the second number for Height. Example: 10,10\n")
        try:
            mapWidth, mapHeight = mapSize.split(',')
            if mapWidth.isdigit() and mapHeight.isdigit():
                mapWidth, mapHeight = int(mapWidth), int(mapHeight)
                print(f"The game you will play will be {mapWidth} wide and {mapHeight} high.")
                break
            else:
                print("Invalid input. Please enter two numbers separated by a comma.")
        except ValueError:
            print("Invalid input. Please enter two numbers separated by a comma.")
    mapCpu = [[0 for _ in range(mapHeight)] for _ in range(mapWidth)]
    mapPlayer = [[0 for _ in range(mapHeight)] for _ in range(mapWidth)]


def modifyShip(fleet :dict):
    """
    Modify an existing ship in the fleet.

    Args:
        fleet (dict): A dictionary containing fleet information.

    Returns:
        None
    """
    # Sort the fleet by ship size for easier navigation
    fleetSorted = dict(sorted(fleet.items(), key=lambda item: item[1]["Size"]))
    printFleet(fleetSorted)
    shipChoice = input("Enter the ship name or index to modify: ")
    if shipChoice.isdigit():
        shipIndex = int(shipChoice)
        if 1 <= shipIndex <= len(fleetSorted):
            shipName = list(fleetSorted.keys())[shipIndex - 1]
            if shipName in fleet:
                while True:
                    sizeInput = input(f"Enter the new size of the '{shipName}' ship: ")
                    if sizeInput.isdigit():
                        size = int(sizeInput)
                        break
                    else:
                        print("Invalid input. Please enter a valid size as a positive integer.")
                while True:
                    quantityInput = input(f"Enter the new quantity of the '{shipName}' ship: ")
                    if quantityInput.isdigit():
                        quantity = int(quantityInput)
                        break
                    else:
                        print("Invalid input. Please enter a valid quantity as a non-negative integer.")
                fleet[shipName]["Size"] = size
                fleet[shipName]["Quantity"] = quantity
                fleet[shipName]["Coordinates"] = []
                fleet = dict(sorted(fleet.items(), key=lambda item: item[1]["Size"]))
            else:
                print(f"The ship '{shipName}' does not exist in the fleet.")
        else:
            print("Invalid index. Please enter a valid index.")
    else:
        shipName = shipChoice
        if shipName in fleet:
            while True:
                sizeInput = input(f"Enter the new size of the '{shipName}' ship: ")
                if sizeInput.isdigit():
                    size = int(sizeInput)
                    break
                else:
                    print("Invalid input. Please enter a valid size as a positive integer.")
            while True:
                quantityInput = input(f"Enter the new quantity of the '{shipName}' ship: ")
                if quantityInput.isdigit():
                    quantity = int(quantityInput)
                    break
                else:
                    print("Invalid input. Please enter a valid quantity as a non-negative integer.")
            fleet[shipName]["Size"] = size
            fleet[shipName]["Quantity"] = quantity
            fleet[shipName]["Coordinates"] = []
            fleet = dict(sorted(fleet.items(), key=lambda item: item[1]["Size"]))
        else:
            print(f"The ship '{shipName}' does not exist in the fleet.")


def addNewShip(fleet: dict):
    """
    Add a new ship to the fleet.

    Args:
        fleet (dict): A dictionary containing fleet information.

    Returns:
        None
    """
    shipName = input("Enter the name of the new ship: ")
    while True:
        sizeInput = input("Enter the size of the new ship: ")
        if sizeInput.isdigit():
            size = int(sizeInput)
            break
        else:
            print("Invalid input. Please enter a valid size as a positive integer.")
    while True:
        quantityInput = input("Enter the quantity of the new ship: ")
        if quantityInput.isdigit():
            quantity = int(quantityInput)
            break
        else:
            print("Invalid input. Please enter a valid quantity as a non-negative integer.")
    coordinates = []
    for i in range(size):
        coord = input(f"Enter coordinates for part {i + 1} of the ship (e.g., 'A3'): ").strip().upper()
        coordinates.append([ord(coord[0]) - ord('A'), int(coord[1:]) - 1])
    fleet[shipName] = {
        "Size": size,
        "Quantity": quantity,
        "Coordinates": coordinates
    }
    fleet = dict(sorted(fleet.items(), key=lambda item: item[1]["Size"]))


def printMap(map :list):
    """
    Print the game map.

    Args:
        map (list): A 2D map to be printed.

    Returns:
        None
    """
    print("   ", end="")
    for colIndex in range(len(map[0])):
        print(f"{colIndex}  ", end="")
    print("\n" + "   " + "=" * (len(map[0]) * 3))

    for rowIndex, row in enumerate(map):
        print(f"{rowIndex} |", end=" ")
        for value in row:
            print(f"{value}  ", end="")
        print()


def checkCoordinates(x :int, y : int, map :list):
    """
    Check if input coordinates are within map boundaries.

    Args:
        x (int): X-coordinate.
        y (int): Y-coordinate.
        map (list): A 2D map.

    Returns:
        bool: True if coordinates are valid, False otherwise.
    """
    if x >= len(map) or y >= len(map[0]) or x < 0 or y < 0:
        print(f"Your entered coordinates ({x}, {y}) are out of the map. Please enter correct values.")
        return False
    return True


def checkShipInput(info):
    """
    Check if ship deployment information is valid.

    Args:
        info (str): A string containing ship deployment information (x, y, and alignment).

    Returns:
        bool: True if input is valid, False otherwise.
    """
    try:
        parts = [part.strip() for part in info.split(',')]
        if len(parts) == 3:
            mapX, mapY, align = parts
            if mapX.isdigit() and mapY.isdigit() and align.lower() in ["v", "h", "Vertical", "Horizontal"]:
                return True
            else:
                print("Please check that you have entered values and information correctly.")
                return False
        else:
            print(
                "Please enter coordinates, alignment, and ship size separated by commas. Provided information is insufficient.")
            return False
    except ValueError:
        print("Please enter coordinates, alignment, and ship size separated by commas.")
        return False


def inputShipCheck(x :int, y :int, align :str, map :list, length : str):
    """
    Check if ship deployment input is valid.

    Args:
        x (int): X-coordinate.
        y (int): Y-coordinate.
        align (str): Ship alignment ("H" for horizontal, "V" for vertical).
        map (list): A 2D map.
        length (int): Length of the ship.

    Returns:
        bool: True if the input is valid for ship placement, False otherwise.
    """
    if 0 <= x < len(map) and 0 <= y < len(map[0]):
        if x + length > len(map) or y + length > len(map[0]):
            print(
                f"Coordinates you have given are within the map, but the ship cannot be placed as part of its body will be out of the map. Please choose different coordinates.")
            return False
        elif align == "H":
            if all(map[x][y + i] == 0 for i in range(length)):
                print("The ship will fit.")
                return True
            else:
                print(
                    f"Sorry, but the ship cannot be placed on the map horizontally at coordinates {x} and {y} as there is another ship there. Please choose different coordinates.")
                return False
        elif align == "V":
            if all(map[x + i][y] == 0 for i in range(length)):
                print("The ship will fit.")
                return True
            else:
                print(
                    f"Sorry, but the ship cannot be placed on the map vertically at coordinates {x} and {y} as there is another ship there. Please choose different coordinates.")
                return False
    else:
        print("Sorry, but the given coordinates are out of the map's size. Please choose valid ones.")
        return False


def playerDeployAllShips():
    """
    Deploy all player ships.

    Updates:
        - global fleetPlayer
        - global FLEET_DEFAULT
        - global mapPlayer

    Returns:
        list: The player's map with deployed ships.
    """
    global fleetPlayer, FLEET_DEFAULT, mapPlayer
    fleetPlayer = copy.deepcopy(FLEET_DEFAULT)
    for shipName, shipInfo in fleetPlayer.items():
        quantity = shipInfo["Quantity"]
        size = shipInfo["Size"]
        for i in range(quantity):
            printMap(mapPlayer)
            print(f"Now you will be deploying ship {shipName} NO: {i + 1} of a total {quantity} of this type of ships")
            while True:  # Loop to keep asking the user to input correct information to deploy a ship
                randomX = random.randint(0, len(mapPlayer) - 1)
                randomY = random.randint(0, len(mapPlayer[0]) - 1)
                randomAlignment = random.choice(['H', 'V'])
                userShipInput = input(
                    f"Please choose coordinates where you would like to deploy your ship, also the ship alignment and its size. (Column, Row, alignment) Example: {randomX},{randomY},{randomAlignment}: ")
                if not checkShipInput(userShipInput):
                    continue
                x, y, align = userShipInput.split(',')
                x = int(x)  # Convert to integer
                y = int(y)  # Convert to integer
                alignment = align[0].upper()  # Taking just the first letter and in uppercase
                if not checkCoordinates(x, y, mapPlayer):
                    continue
                elif not inputShipCheck(x, y, alignment, mapPlayer, size):
                    continue
                location = [x, y]
                deploySingleShip(mapPlayer, size, location, alignment, shipName, fleetPlayer)
                break  # Successfully deployed the ship, so exit the loop
    return mapPlayer


def deploySingleShip(map :list, length :str, location :list, alignment :str, shipName :str, fleet :dict):
    """
    Deploy a single ship on the map.

    Args:
        map (list): A 2D map.
        length (int): Length of the ship.
        location (list): Coordinates [row, column] where the ship will be deployed.
        alignment (str): Ship alignment ("H" for horizontal, "V" for vertical).
        shipName (str): Name of the ship.
        fleet (dict): A dictionary containing fleet information.

    Returns:
        list: The updated map with the deployed ship.
    """
    global shipSymbols
    row, column = location
    print(location)
    shipCoordinates = []
    if length == 1:
        map[row][column] = shipSymbols["Single"][0]
        shipCoordinates.append([row, column])
        return map
    else:
        if alignment == "H":
            shipCoordinates.append([row, column])
            map[row][column] = shipSymbols["Horizontal"][0][0]
            for i in range(length - 1):
                map[row][column + i + 1] = shipSymbols["Horizontal"][1][0]
                shipCoordinates.append([row, column + i + 1])
        elif alignment == "V":
            shipCoordinates.append([row, column])
            map[row][column] = shipSymbols["Vertical"][0][0]
            for i in range(length - 1):
                map[row + i + 1][column] = shipSymbols["Vertical"][1][0]
                shipCoordinates.append([row + i + 1, column])
    fleet[shipName]["Coordinates"].append(shipCoordinates)
    printMap(map)
    print(f"You have deployed {shipName} in Coordinates: {location}")
    return map


def searchMap(map :list, width :int, height :int):
    """
    Search the map for a pattern to find suitable deployment coordinates for the CPU.

    Args:
        map (list): A 2D map to search.
        width (int): Width of the pattern to search for.
        height (int): Height of the pattern to search for.

    Returns:
        Union[list, str]: A list of suitable coordinates or 'noneFound' if none are found.
    """
    coordinatesList = []
    for i in range(len(map) - height + 1):
        for j in range(len(map[0]) - width + 1):
            subgrid = [row[j:j + width] for row in map[i:i + height]]
            if all(cell == 0 for row in subgrid for cell in row):
                coordinatesList.append((i, j))
    if not coordinatesList:
        return 'noneFound'
    return coordinatesList


def cpuDeployAllShips():
    """
    Deploy all CPU ships on the map.

    Updates:
        - global fleetCpu
        - global FLEET_DEFAULT
        - global mapCpu

    Returns:
        None
    """
    global fleetCpu, FLEET_DEFAULT, mapCpu
    fleetCpu = copy.deepcopy(
        FLEET_DEFAULT)  # Make a fresh copy, in case there were any changes made for map size or fleet
    for shipName, shipInfo in fleetCpu.items():
        quantity = shipInfo["Quantity"]
        size = shipInfo["Size"]
        print(f"Deploying {quantity} {shipName}(s) of size {size}")
        for i in range(quantity):
            symbol = random.choice(["H", "V"])  # Horizontal or vertical
            if symbol == "H":
                location = random.choice(searchMap(mapCpu, size, 1))
            elif symbol == "V":
                location = random.choice(searchMap(mapCpu, 1, size))
            deploySingleShip(mapCpu, size, location, symbol, shipName, fleetCpu)
    printMap(mapCpu)


def findBiggestShipInPlayerFleet(fleet :dict):
    """
    Find the biggest ship in the player's fleet.

    Args:
        fleet (dict): A dictionary containing fleet information.

    Returns:
        int: The size of the biggest ship in the fleet.
    """
    biggestShipName = None
    biggestShipSize = 0
    # Loop through each ship and its details in the fleet
    for shipName, shipDetails in fleet.items():
        size = shipDetails.get("Size", 0)  # Get the size of the ship, default to 0 if "Size" key is not found
        if size > biggestShipSize:
            biggestShipSize = size
            biggestShipName = shipName
    print(f" def findBiggestShipInPlayerFleet(fleet :dict): I have found the biggest ship {biggestShipName} in the fleet with size {biggestShipSize}")
    return biggestShipSize


def searchMapForBiggestShip(map :list, shipSize :int, cpuShootCoordinates :list):
    """
    Search the map for a suitable location to shoot the biggest unsunk ship in the fleet.

    Args:
        map (list): A 2D map to search.
        shipSize (int): The size of the biggest unsunk ship.
        cpuShootCoordinates (list): List of CPU's previous shot coordinates.

    Returns:
        Tuple[int, int]: The coordinates (X, Y) to shoot at.
    """
    width = shipSize * 2 - 1
    height = shipSize * 2 - 1
    coordinates = "noneFound"  # Initialize the coordinates

    while True:  # An outer loop to keep generating new coordinates until unique ones are found
        while coordinates == "noneFound":  # Keep searching until a pattern is found
            coordinates = searchMap(map, width, height)  # Search for a pattern
            if coordinates == "noneFound":  # If no pattern is found
                orientation = random.choice(["width", "height"])  # Choose an orientation to reduce
                if orientation == "width":
                    width -= 1  # Reduce the width
                elif orientation == "height":
                    height -= 1  # Reduce the height

                # If reducing either width or height did not work, try reducing both
                if coordinates == "noneFound":
                    width -= 1
                    height -= 1

        shootingCoordinates = random.choice(coordinates)  # Choose a random coordinate
        coordinatesX, coordinatesY = shootingCoordinates  # Extract X and Y coordinates

        # Calculate the middle of the X and Y coordinates
        coordinatesX = coordinatesX // 2 + 1 - (random.choice([0, 1]) if coordinatesX % 2 == 1 else 0)
        coordinatesY = coordinatesY // 2 + 1 - (random.choice([0, 1]) if coordinatesY % 2 == 1 else 0)

        # Check if these coordinates already exist in cpuShootCoordinates
        if [coordinatesX, coordinatesY] not in cpuShootCoordinates:
            print(
                f'I have found the biggest ship still available of size {shipSize} and will select coordinates {coordinatesX} and {coordinatesY}')
            return coordinatesX, coordinatesY  # Return the coordinates to shoot
        else:
            coordinates = "noneFound"  # Reset and search again for a unique set of coordinates


def shootCheck(coordX, coordY, map, fleet, actionsLog):
    """
    Check if a shooting was successful (hit) or a miss.

    Args:
        coordX (int): The X coordinate of the shot.
        coordY (int): The Y coordinate of the shot.
        map (list): The map where the shooting takes place.
        fleet (dict): A dictionary containing fleet information.
        actionsLog (list): A list to log shooting actions.

    Returns:
        list: The updated actions log.
    """
    global shipSymbols  # Declare global variables
    checkCoordinates = [coordX, coordY]  # Create a list for the coordinates
    shootHit = None  # Initialize a variable to store the ship name if hit
    # Initialize a list to store the whole coordinates of the hit ship
    wholeShipCoordinates = []

    # Loop through all ships in the fleet to get coordinates of all ships
    for shipName, shipData in fleet.items():
        # Loop through all coordinates of all ships
        for coordinatesAllShips in shipData["Coordinates"]:
            # Check if the shot coordinates match any ship coordinates
            if checkCoordinates in coordinatesAllShips:
                map[coordX][coordY] = shipSymbols["Hit"][0]  # Mark the hit on the map
                shootHit = shipName  # Store the name of the ship if it is there, otherwise it is None
                wholeShipCoordinates = coordinatesAllShips  # Store all coordinates of the hit ship

    # If a ship was hit
    if shootHit:
        actionsLog.append(["Hit", coordX, coordY])  # Log the hit in logActions
        # Check if the whole ship is sunk
        for singleCoordinate in wholeShipCoordinates:
            if map[singleCoordinate[0]][singleCoordinate[1]] != shipSymbols["Hit"][0]:
                print(f" have hit ship fully on coordinated {coordX}, {coordY}")
                break  # The ship is not fully sunk yet
        else:
            actionsLog.clear()  # Clear the actions log for the sunk ship
            # I assume you have a function to remove the ship from the fleet.
            shipInfo = fleetRemoveShip(shipName, wholeShipCoordinates, fleet)
            print(f" {shipInfo} +  was sunk on coordinates {singleCoordinate}")

            fleetRemoveShip(shipName,singleCoordinate,fleet)

    # If the shot was a miss
    if not shootHit:
        map[coordX][coordY] = shipSymbols["miss"][0]  # Mark the miss on the map
        actionsLog.append(["Miss", coordX, coordY])  # Log the miss in logActions
        print(f" have missed shot on coordinated {coordX}, {coordY}")


def fleetRemoveShip(shipName, coordinates, fleet):
    """
    Remove a given ship from the fleet.

    Args:
        shipName (str): The name of the ship to be removed.
        coordinates (list): The coordinates of the ship to be removed.
        fleet (dict): A dictionary containing fleet information.

    Returns:
        dict or None: Information about the removed ship or None if the ship was not found.
    """
    # Initialize the variable to store the removed ship's information
    removedShipInfo = None

    # Check if the ship exists in the fleet
    if shipName in fleet:
        # Retrieve the ship's data from the fleet
        shipData = fleet[shipName]

        # Check if the ship has more than one instance in the fleet
        if shipData["Quantity"] > 1:
            # Loop through the coordinates of each instance of the ship
            for index, coordinatesFleet in enumerate(shipData["Coordinates"]):
                # If the given coordinates match
                if coordinates in coordinatesFleet:
                    # Remove the coordinates from the ship's data
                    removedCoordinates = shipData["Coordinates"].pop(index)
                    # Decrease the quantity of this type of ship in the fleet
                    shipData["Quantity"] -= 1

                    # Store the removed ship's information
                    removedShipInfo = {
                        "shipName": shipName,
                        "removedCoordinates": removedCoordinates
                    }

                    # If there are no more instances of this type of ship, remove it from the fleet
                    if shipData["Quantity"] == 0:
                        del fleet[shipName]

                    break  # Exit the loop after removing the coordinates
        else:
            # If there is only one instance of the ship, remove it entirely from the fleet
            del fleet[shipName]

            # Store the removed ship's information
            removedShipInfo = {
                "shipName": shipName,
                "removedCoordinates": shipData["Coordinates"]
            }

    # Return the information of the removed ship
    return removedShipInfo


def cpuMove(fleet, map):
    """
    Perform the CPU's move in the game.

    Args:
        fleet (dict): A dictionary containing fleet information.
        map (list): The game map.

    Returns:
        None
    """
    global cpuActions, cpuShootCoordinates, gameResult

    if cpuActions == []:
        print(f'debug no cpu actions found, seraching for biggest ship')
        # If there is no stored information about hit ships that are not sunk:
        biggestShipSize = findBiggestShipInPlayerFleet(fleet)
        coordX, coordY = searchMapForBiggestShip(map, biggestShipSize, cpuShootCoordinates)
        cpuShootCoordinates.append([coordX, coordY])
        cpuActions = shootCheck(coordX, coordY, map, fleet, cpuActions)
        print(f"CPU's move: Shot at coordinates ({coordX}, {coordY})")
    else:
        print(f'have found cpu action log')
        # If there is stored information about hit ships that are not yet sunk:
        coordinates = findBestShot(cpuActions)
        if coordinates:
            coordX, coordY = coordinates
            cpuShootCoordinates.append([coordX, coordY])
            cpuActions = shootCheck(coordX, coordY, map, fleet, cpuActions)
            print(f"CPU's move: Shot at coordinates ({coordX}, {coordY})")


def fleetCheck(fleet):
    """
    Check if there are any remaining ships in the fleet.

    Args:
        fleet (dict): A dictionary containing fleet information.

    Returns:
        str: The game result, either "gameOver" if there are no remaining ships or None if the game continues.
    """
    global gameResult

    # Initialize a list to store the names of ships with a quantity of 0
    shipsToRemove = []

    # Loop through the fleet to find ships with a quantity of 0
    for shipName, shipData in fleet.items():
        if shipData["Quantity"] == 0:
            shipsToRemove.append(shipName)

    # Loop through the list and remove ships with a quantity of 0 from the fleet
    for shipName in shipsToRemove:
        del fleet[shipName]

    # Check if there are no remaining ships in the fleet
    if not fleet:
        print("Game over")  # Indicate that the game is over if there are no remaining ships
        return "gameOver"


def determineOrientation(hitActions):
    """
    Determine the orientation of a hit ship based on hit actions.

    Args:
        hitActions (list): A list of hit actions containing coordinates.

    Returns:
        str: The orientation of the hit ship ("Vertical", "Horizontal", or "Unknown").
    """
    # If only one hit, orientation is unknown
    if len(hitActions) == 1:
        return "Unknown"

    # If multiple hits, determine orientation
    x_coords = [action[1] for action in hitActions]
    y_coords = [action[2] for action in hitActions]

    if len(set(x_coords)) == 1:
        return "Vertical"
    elif len(set(y_coords)) == 1:
        return "Horizontal"
    else:
        return "Unknown"


def findBestShot(cpuActions):
    """
    Find the best shot based on CPU actions.

    Args:
        cpuActions (list): A list of CPU actions, each containing information about hits or misses.

    Returns:
        tuple: A tuple representing the best shot coordinates (x, y) or None if no suitable shot is found.
    """
    # Step 1: Filter out all "Hit" actions
    hitActions = [action for action in cpuActions if action[0] == "Hit"]

    if not hitActions:
        return None  # No hits to analyze

    # Step 2: Determine the orientation of the hit ship
    orientation = determineOrientation(hitActions)

    # Step 3: Calculate probabilities (for now, we'll just find immediate neighbors)
    candidates = []

    if orientation == "Vertical":
        min_y = min(action[2] for action in hitActions)
        max_y = max(action[2] for action in hitActions)
        x = hitActions[0][1]  # All x-coordinates are the same for a vertical hit
        candidates.append((x, min_y - 1))  # Add the cell above the first hit
        candidates.append((x, max_y + 1))  # Add the cell below the last hit
    elif orientation == "Horizontal":
        min_x = min(action[1] for action in hitActions)
        max_x = max(action[1] for action in hitActions)
        y = hitActions[0][2]  # All y-coordinates are the same for a horizontal hit
        candidates.append((min_x - 1, y))  # Add the cell to the left of the first hit
        candidates.append((max_x + 1, y))  # Add the cell to the right of the last hit
    else:  # Orientation is "Unknown"
        for x, y in hitActions:
            candidates.extend([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)])  # Add all surrounding cells

    # Step 4: Choose the best shot (for now, we'll just take the first candidate)
    bestShot = candidates[0]
    return bestShot


def newGame():
    global mapCpu, mapCpuHidden, mapPlayer, mapPlayerHidden, FLEET_DEFAULT, fleetCpu, fleetPlayer

    # Uncomment the following lines to allow player adjustments and deployment
    # while gameAdjust(fleetPlayer):
    #     pass
    # playerDeployAllShips()

    # Deploy CPU ships
    cpuDeployAllShips()
    printMap(mapCpu)

    result = None
    while result is None:
        cpuMove(fleetCpu, mapCpuHidden)  # Start CPU actions

        # Add a condition to end the game when it's over
        result = fleetCheck(fleetCpu)
        if result == "gameOver":
            print("Game over! CPU wins!")  # You can customize the end message
            break


# Start a new game
newGame()

