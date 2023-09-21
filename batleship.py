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
        "Quantity": 1
    },
    "Battleship": {
        "Size": 4,
        "Quantity": 0
    },
    "Cruiser": {
        "Size": 3,
        "Quantity": 0
    },
    "Submarine": {
        "Size": 3,
        "Quantity": 0
    },
    "Destroyer": {
        "Size": 2,
        "Quantity": 0
    },
    "Dingy Boat": {
        "Size": 1,
        "Quantity": 0
    }
}

"""
function to print out all fleet as a table
"""
def printFleet():
    print("{:<20} {:<10} {:<10}".format("Ship Type", "Size", "Quantity"))
    print("="*40)
    for ship, details in battleshipFleet.items():
        size = details["Size"]
        quantity = details["Quantity"]
        print("{:<20} {:<10} {:<10}".format(ship, size, quantity)) 
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
            mapX,mapY = mapSize.split(',') # splitting user input into 2 separate parts 
            if mapX.isdigit() and mapY.isdigit(): # checking if both inputs parts are numbers
                mapSize = [int(X), int(Y)] #if both inputs are valid, assigning them to mapSize
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

