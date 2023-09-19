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
        "Quantity": 1
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
        "Quantity": 1
    }
}


"""
section for imports of libraries
"""
import curses # want to implement mouse activity for game, not just terminal, but this for future, depends how project will go
import random # i believe this import is self explaining


"""
Function for player to change map size
"""
def select_map_size(): #function for user to input map size
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
    select_map_size() #asking user to input new map size


"""
creating an array that will be representing map based on X and Y
"""
mapCPU = [[0 for j in range(Y)] for i in range(X)]
mapPlayer = [[0 for j in range(Y)] for i in range(X)]


"""
Print the CPU MAP array to the console - will create function, later will be easier to print the map
"""
def printMap(map):
    column_width = [max(len(str(item)) for item in column) for column in zip(*map)] # calculating maximum width of column through all map
    for column, width in zip(map[0], column_width): # printing table headers
        print(f"{column:{width}}", end=" | ") # aligning all columns as text using f-string
    print() # printing new line to separate headers from data
    for row in map[1:]: #printing table data
        for item, width in zip(row, column_width):
            # Format and align each data item in the row using f-strings
            # The width specifier ensures that the column has a minimum width of 'width'
            print(f"{item:{width}}", end=" | ")
        print()  # Print a newline to separate rows


"""
now will create columns of map, so i can use later in game to search for ships
"""
def mapFlip(map):
    num_columns = len(map[0])  # Assuming all rows have the same number of columns
    for col in range(num_columns):
        column_data = [row[col] for row in map]
        print(f"Column {col + 1}: {column_data}")

printMap(mapCPU) # printing out map to see how it looks empty


"""
creating loop for all battleships, starting name and then going to sublevel - QTY of each of them
"""
def deployAllShips():
    for shipName, shipInfo in battleshipFleet.items():
        print(shipName)
        quantity = shipInfo["Quantity"]
        print(quantity)
        size = shipInfo["Size"]
        print(f"cheking if loop works in or shipName, shipInfo in battleshipFleet.items() {size}")
        for i in range(quantity):
            location = findShipLocation(mapCPU, size,0) # 0 - Zero --> empty space on map
            print(location)
            if location is not None:
                shipDeploy(mapCPU, size, location,"X") # deploy ship as an 'X'
            else:
                print(f"Error: Cannot deploy {shipName}. No valid location found.")


"""
function to find given ship on map (search by rows), if needed to search by columns, searchMap columns should be converted to rows and rows to columns, use function mapConvertRowsToColumns(map)
"""
def findShipLocation(searchMap, shipLength, cellValue):
    validLocations = []  # List to store valid ship deployment locations
    mapSizeX = len(searchMap[0])
    mapSizeY = len(searchMap)
    for c in range(mapSizeY):  # Loop through all columns
        for r in range(mapSizeX - shipLength + 1):  # Loop through row cells
            print(c,r)
            if all(cell == cellValue for cell in searchMap[c][r:r + shipLength]):
                # Check if the ship can fit in the row
                validLocations.append((c, r))  # Store valid location as (row, column)
                print(c,r)
    if validLocations:
        return random.choice(validLocations)  # Choose a random valid location
    else:
        return None  # No valid location found for the ship


"""
function to deploy ship to map by given location
"""
def shipDeploy(map,shipLength,location,symbol): # value symbol - is what will be placed on map
    row, column = location # getting row and column numbers
    for i in range(shipLength): # looping through given location
        map[row][column + i] = symbol #deploying ship

deployAllShips()
printMap(mapCPU)