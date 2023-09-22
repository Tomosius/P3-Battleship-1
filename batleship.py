"""
Section for Global Variables
"""
mapX = 10           # default map size X - horizontal
mapY = 10          # default map size Y - vertical


"""
default Battleship fleet - i use as dictionary, so in case if player changes map size or ships quantities, it will be easier to play
"""
battleshipFleet = {
    "Aircraft Carrier": {
        "Size": 5,
        "Quantity": 1,
        "Coordinates": []
    },
    "Battleship": {
        "Size": 4,
        "Quantity": 0,
        "Coordinates": []
    },
    "Cruiser": {
        "Size": 3,
        "Quantity": 0,
        "Coordinates": []
    },
    "Submarine": {
        "Size": 3,
        "Quantity": 0,
        "Coordinates": []
    },
    "Destroyer": {
        "Size": 2,
        "Quantity": 0,
        "Coordinates": []
    },
    "Dingy Boat": {
        "Size": 1,
        "Quantity": 0,
        "Coordinates": []
    }
}


"""
function to print out all fleet as a table
"""
def printFleet(fleet):
    print("{:<20} {:<10} {:<10} {:<50}".format("Ship Type", "Size", "Quantity", "Coordinates"))
    print("="*40)
    for ship, details in fleet.items():
        size = details["Size"]
        quantity = details["Quantity"]
        coordinates = details["Coordinates"]
        coordinates_str = str(coordinates)  # Convert the list to a string
        print("{:<20} {:<10} {:<10} {:<50}".format(ship, size, quantity, coordinates_str))

"""
will create list of colors, so i can use them on map.
"""

colors = {
    "DARK_YELLOW": "\033[33m",   # Dark Yellow - single cell ship
    "LIGHT_GRAY": "\033[37m",    # Light Gray - empty space on map,. n o need to shoot
    "DARK_BLUE": "\033[34m",     # Dark Blue - horizontal ships
    "DARK_GREEN": "\033[32m",    # Dark Green - vertical ships
    "DARK_RED": "\033[31m",      # Dark Red - damaged ship
    "RESET": "\033[0m"           # Reset color to default
}
"""
section for imports of libraries
"""
import curses # want to implement mouse activity for game, not just terminal, but this for future, depends how project will go
import random # i believe this import is self explaining
import copy # will use it to copy default fleet to CPU and player, where coordinates and etc can be stored for future use
fleetCPU = copy.deepcopy(battleshipFleet) # making copy of fleet for CPU
fleetPlayer = copy.deepcopy(battleshipFleet) # making copy of fleet for Player
"""
Function for player to change map size
"""
def mapSizeSelect(): #function for user to input map size
    global mapX, mapY
    while True:
        # user will be requested to input map size
        mapSize = input("Please select MAP size You would like to play. First number - Width, second number - Height. Example: 10,10 \n")
        try: #testing if user used correct pattern to input map size
            mapX,mapY = mapSize.split(',') # splitting user input into 2 separate parts 
            if mapX.isdigit() and mapY.isdigit(): # checking if both inputs parts are numbers
                mapSize = [int(mapX), int(mapY)] #if both inputs are valid, assigning them to mapSize
                break #now function can stop as all is correct
            else:  #if any part of inout is not numeric, printing out message
                print("Invalid input. Please enter two numbers separated by a comma.")
        except ValueError: #if user input can not be split in 2 parts will raise an issue:
            print("Invalid input. Please enter two numbers separated by a comma.")
    return mapX,mapY

"""
creating an array that will be representing map based on X and Y
"""
mapCPU = [[0 for c in range(mapY)] for r in range(mapX)]
mapPlayer = [[0 for j in range(mapY)] for i in range(mapX)]


"""
Print the CPU MAP array to the console - will create function, later will be easier to print the map
"""
def printMap(table):
    print("   ", end="")
    for col_index in range(len(table[0])):
        print(f"{col_index}  ", end="")
    print("\n" + "   " + "=" * (len(table[0]) * 3))

    # Iterate through the table and print row coordinates on the left side
    for row_index, row in enumerate(table):
        print(f"{row_index} |", end=" ")
        for value in row:
            print(f"{value}  ", end="")
        print() 

"""
function to create ship or pattern by given width and length, will be hande searching map
"""
def createPattern(width, height):
    return [[0] * width for _ in range(height)]

"""
function to search map by givven pattern
"""
def searchMap(map, width, height):
    coordinatesList = []
    for i in range(len(map) - height + 1):
        for j in range(len(map[0]) - width + 1):
            subgrid = [row[j:j + width] for row in map[i:i + height]]
            if all(cell == 0 for row in subgrid for cell in row):
                coordinatesList.append((i, j))
    return coordinatesList


"""
function to deploy single ship on specified map
"""
def deploySingleShip(map,length,location,alignment,ship,fleet):
    row, column = location  # getting row and column numbers
    print(location)
    fleet[ship]["Coordinates"].append(location)
    if length == 1: # if ship ius made just of one cell, then we will show only:
        color = colors["DARK_YELLOW"]
        map[row][column] = color +  chr(0x25C6) + colors["RESET"]# ship will be displayed as ◆
    else: #if ship is or longer then 2 cells:
        if alignment == "H":
            color = colors["DARK_BLUE"]
            map[row][column] = color + chr(0x25C0) + colors["RESET"]# if ship is horizontal, first cell will be ◂
            for i in range(length - 1):
                map[row][column + i + 1] = color + chr(0x25A0)  + colors["RESET"]# deploying ship all remaining cells as ■
        else:
            color = colors["DARK_GREEN"]
            map[row][column] = color + chr(0x25B2) + colors["RESET"]# if ship is horizontal, first cell will be ▲
            for i in range(length - 1):
                map[row + i + 1][column] = color + chr(0x25A0)  + colors["RESET"]# deploying ship all remaining cells as ■
    return map


"""
function to deploy CPU ships
"""
def cpuDeployAllShips():
    global fleetCPU, battleshipFleet, mapCPU
    fleetCPU = copy.deepcopy(battleshipFleet) # making fresh copy, in case there were any changes made for map size or fleet
    for shipName, shipInfo in fleetCPU.items():
        quantity = shipInfo["Quantity"]
        size = shipInfo["Size"]
        print(f"Deploying {quantity} {shipName}(s) of size {size}")
        for i in range(quantity):
            symbol = random.choice(["H", "V"]) # horizontal or vertical
            if symbol == "H":
                location = random.choice(searchMap(mapCPU, size, 1))
            elif symbol == "V":
                location = random.choice(searchMap(mapCPU, 1, size))
            deploySingleShip(mapCPU, size, location, symbol, shipName, fleetCPU)
    return mapCPU



"""
function to deploy player single
"""
def playerSingleShipDeploy():
    while True:
        location = input("Please choose coordinates where you would like to deploy your ship, also ship alignment and its size. Example: 3,1,h -  this will mean: 3 column, 1 row, horizontal")
        try:
            c, r, align = [part.strip() for part in location.replace(',', ' ').replace('.', ' ').replace('x', ' ').split()]
            if c.isdigit() and r.isdigit() and align in ["v", "h", "V", "H", "vertical", "horizontal", "Vertical", "Horizontal"]: # eliminating errors if player passes just letter of full word of alignment
                align = align[0].capitalize()
                return int(c), int(r), align
            else:
                print("Invalid input, please check you have entered values and information correctly")
        except ValueError:
            print("Invalid input. Please enter coordinates, alignment, and ship size. All information MUST be separated by commas.")

"""
function to deploy all layer ships
"""
def playerDeployAllShips():
    global fleetPlayer, battleshipFleet, mapPlayer
    fleetPlayer = copy.deepcopy(battleshipFleet)
    for shipName, shipInfo in fleetPlayer.items():
        quantity = shipInfo["Quantity"]
        size = shipInfo["Size"]
        for i in range(quantity):
            print(f"Deploying {i+1} {shipName}(s) out of {quantity} of size {size}")
            mapX, mapY, alignment = playerSingleShipDeploy()
            location = (mapX, mapY)
            deploySingleShip(mapPlayer, size, location, alignment, shipName, fleetPlayer)
    return mapPlayer



cpuDeployAllShips()
printMap(mapCPU)
printFleet(fleetCPU)
print()
playerDeployAllShips()
printMap(mapPlayer)

