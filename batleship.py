"""
Section for Global Variables
"""
X = 10           # default map size X - horizontal
Y = 10          # default map size Y - vertical
mapSize = [X,Y]   # first number - horizontal lines, second - vertical, by default it will be 10 x 10

"""
default Battleship fleet - i use as dictionary, so in case if player changes map size or ships quantities, it will be easier to play
"""
battleshipFleet = {
    "Aircraft Carrier": {
        "Size": 5,
        "Quantity": 3
    },
    "Battleship": {
        "Size": 4,
        "Quantity": 2
    },
    "Cruiser": {
        "Size": 3,
        "Quantity": 3
    },
    "Submarine": {
        "Size": 3,
        "Quantity": 2
    },
    "Destroyer": {
        "Size": 2,
        "Quantity": 3
    },
    "tomas": {
        "Size": 1,
        "Quantity": 3
    }
}

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


"""
Function for player to change map size
"""
def mapSizeSelect(): #function for user to input map size
    while True:
        # user will be requested to input map size
        mapSize = input("Please select MAP size You would like to play. First number - Width, second number - Height. Example: 10,10 \n")
        try: #testing if user used correct pattern to input map size
            X,Y = mapSize.split(',') # splitting user input into 2 separate parts 
            if X.isdigit() and Y.isdigit(): # checking if both inputs parts are numbers
                mapSize = [int(X), int(Y)] #if both inputs are valid, assigning them to mapSize
                break #now function can stop as all is correct
            else:  #if any part of inout is not numeric, printing out message
                print("Invalid input. Please enter two numbers separated by a comma.")
        except ValueError: #if user input can not be split in 2 parts will raise an issue:
            print("Invalid input. Please enter two numbers separated by a comma.")
    print(mapSize)


"""
function to start new Game
"""
def newGame(): #function to start new game
    mapSizeSelect() #asking user to input new map size


"""
creating an array that will be representing map based on X and Y
"""
mapCPU = [[0 for c in range(Y)] for r in range(X)]
mapPlayer = [[0 for j in range(Y)] for i in range(X)]


"""
Print the CPU MAP array to the console - will create function, later will be easier to print the map
"""
def printMap(printMap):
    for row in printMap:
        for item in row:
            print(item, end="")
        print()  


"""
will rotate map, so colmns becomes rows, rows into columns. This will help to use same function to search on map, but now it would be searching in columns, after such search, map will need to be fliped again back to notmal state
"""
def mapFlip(mapRotate):
    return [[mapRotate[j][i] for j in range(len(mapRotate))] for i in range(len(mapRotate[0]))]



"""
creating loop for all battleships, starting name and then going to sublevel - QTY of each of them
"""
def deployAllShips():
    global mapCPU  # Add this line
    global battleshipFleet
    for shipName, shipInfo in battleshipFleet.items():
        quantity = shipInfo["Quantity"]
        size = shipInfo["Size"]
        print(f"Deploying {quantity} {shipName}(s) of size {size}")
        for i in range(quantity):
            align = random.choice(["horizontal", "vertical"])
            symbol = 'V' if align == 'vertical' else 'H'
            mapSearch = mapFlip(mapCPU) if align == 'vertical' else mapCPU
            location = findShipLocation(mapSearch, size, 0)
            if location is not None:
                shipDeploy(mapSearch, size, location, symbol)
                mapCPU = mapFlip(mapSearch) if align == 'vertical' else mapSearch
            else:
                print(f"Error: Cannot deploy {shipName}. No valid location found.")
            mapCPU = mapFlip(mapSearch) if align == 'vertical' else mapSearch


"""
function to find given ship on map (search by rows), if needed to search by columns, searchMap columns should be converted to rows and rows to columns, use function mapConvertRowsToColumns(map)
"""
def findShipLocation(searchMap, shipLength, cellValue):
    validLocations = []  # List to store valid ship deployment locations
    mapSizeX = len(searchMap[0])
    mapSizeY = len(searchMap)
    for c in range(mapSizeY):  # Loop through all columns
        for r in range(mapSizeX - shipLength + 1):  # Loop through row cells
            if all(cell == cellValue for cell in searchMap[c][r:r + shipLength]):
                # Check if the ship can fit in the row
                validLocations.append((c, r))  # Store valid location as (row, column)
    if validLocations:
        return random.choice(validLocations)  # Choose a random valid location
    else:
        return None  # No valid location found for the ship


"""
function to deploy ship to map by given location, and ships will be displayed as symbols not letters, so it is easier to see where is what ship, is it vertical or horizontal and etc.
"""
def shipDeploy(map, shipLength, location, symbol):
    row, column = location  # getting row and column numbers
    
    if shipLength == 1: # if ship ius made just of one cell, then we will show only:
        color = colors["DARK_YELLOW"]
        map[row][column] = color +  chr(0x25C6) + colors["RESET"]# ship will be displayed as ◆
    else:
        if symbol == "H": 
            color = colors["DARK_BLUE"]
            map[row][column] = color + chr(0x25C0) + colors["RESET"]# if ship is horizontal, first cell will be ◂
        else:
            color = colors["DARK_GREEN"]
            map[row][column] = color + chr(0x25B2) + colors["RESET"]# if ship is vertical, first cell will be ▲
        column = column + 1
        for i in range(shipLength - 1):  # looping through given location
            map[row][column + i] = color + chr(0x25A0)  + colors["RESET"]# deploying ship all remaining cells as ■

deployAllShips()
printMap(mapCPU)