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
    "LIGHT_GRAY": "\033[37m",    # Light Gray - empty space on map,. no need to shoot, or miss shooting
    "DARK_BLUE": "\033[34m",     # Dark Blue - horizontal ships
    "DARK_GREEN": "\033[32m",    # Dark Green - vertical ships
    "DARK_RED": "\033[31m",      # Dark Red - damaged ship
    "RESET": "\033[0m"           # Reset color to default
}


"""
will create ship patterns how they will be displayed
"""
shipSymbols = {
    "Single": [colors["DARK_YELLOW"] + chr(0x25C6) + colors["RESET"]], # ship will be displayed as ◆ in DARK_YELOW
    "Horizontal": [[colors["DARK_BLUE"] + chr(0x25C0) + colors["RESET"]],[colors["DARK_BLUE"] + chr(0x25A4) + colors["RESET"]]], # ship will be displayed as ◂▤▤▤ in DARK_BLUE
    "Vertical": [[colors["DARK_GREEN"] + chr(0x25B2) + colors["RESET"]],[colors["DARK_GREEN"] + chr(0x25A5) + colors["RESET"]]], # ship will be displayed as ▲ and below it ▥
    "Hit": [colors["DARK_RED"] + chr(0x25A6) + colors["RESET"]], # if hit, will mark as ▦ in DARK_RED color
    "Miss": [colors["LIGHT_GRAY"] + chr(0x2022) + colors["RESET"]] # if miss, will mark as • in LIGHT_GRAY
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
function to search map by given pattern
"""
def searchMap(map, width, height):
    coordinatesList = []
    for i in range(len(map) - height + 1):
        for j in range(len(map[0]) - width + 1):
            subgrid = [row[j:j + width] for row in map[i:i + height]]
            if all(cell == 0 for row in subgrid for cell in row):
                coordinatesList.append((i, j))
    if not coordinatesList: # Check if no coordinates were fuound, so coordinatesList is empty
        return 'noneFound'
    return coordinatesList


def deploySingleShip(map, length, location, alignment, ship, fleet):
    global shipSymbols
    row, column = location  # getting row and column numbers
    print(location)
    shipCoordinates = []  # this will be coordinates appended to fleet
    if length == 1:  # if ship is made just of one cell, then we will show only:
        map[row][column] = shipSymbols["Single"][0]
        shipCoordinates.append([row, column])
    else:  # if ship is or longer then 2 cells:
        if alignment == "H":
            map[row][column] = shipSymbols["Horizontal"][0][0]
            shipCoordinates.append([row, column])
            for i in range(length - 1):
                map[row][column + i + 1] = shipSymbols["Horizontal"][1][0]
                shipCoordinates.append([row, column + i + 1])
        else:
            map[row][column] = shipSymbols["Vertical"][0][0]
            shipCoordinates.append([row, column])
            for i in range(length - 1):
                map[row + i + 1][column] = shipSymbols["Vertical"][1][0]
                shipCoordinates.append([row + i + 1, column])
    fleet[ship]["Coordinates"].append(shipCoordinates)
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



"""
function to find biggest ship not sunk in Players fleet
"""
def findBiggestShipInPlayerFleet():
    global fleetPlayer # importing global variable
    biggestShipName = None
    biggestShipSize = 0
    for ship, details in fleetPlayer.items(): # cycling thorough all ships in players fleet
        size = details["Size"] # getting size info
        quantity = details["Quantity"] # getting quontity information
        if quantity > 0 and size > biggestShipSize: # Check if the quantity of the ship is above zero and if its size is greater than the current biggest ship size
            biggestShipName = ship
            biggestShipSize = size
    return biggestShipName, biggestShipSize


"""
now will search for given ship on Players
"""
def searchForPlayerShipAndHit():
    global mapPlayer, fleetPlayer
    shipName, shipSize = findBiggestShipInPlayerFleet()
    width = shipSize * 2 - 1
    height = shipSize * 2 -1
    while coordinates == "noneFound" : # creating loop, if there was no such big pattern found on map for deployed ship, will start making it smaller and keep searching for it till we find one pattern
        coordinates = searchMap(mapPlayer,width,height) # looking for given ship, so we will make huge square, 2x size of ship and will look for that on map
        orientation = random.choice("width", "height") # choosing how we will reduce searching block, horizontaly or verticaly
        if orientation == "width":
            width = width - 1 # reducing width
            coordinates = searchMap(mapPlayer,width,height) #searching with lest wide pattern
            if coordinates == "noneFound":
                break #if there was no pattern found, now we will swap to height and search again, so we use break to keep searching
        else:
            height = height - 1 # reducing height
            width = width + 1 # making width same again, as now will search with lower height
            coordinates = searchMap(mapPlayer,width,height) # searching again
            if coordinates == "noneFound":
                break # we have found again nothing, so breaking 
        width = width - 1
        height = height - 1
    #now we have found coordinates list
    shootingCoordinates = random.choice(coordinates) # choosing random spot to shoot
    coordinatesX, coordinatesY = shootingCoordinates.split(',') # getting X and Y where we will be shooting
    #now we have X, Y, ship width, we will select center of that area if possible
    coordinatesX = coordinatesX // 2 + 1 - (random.choice([0, 1]) if coordinatesX % 2 == 1 else 0) # now choosing middle of X coordinates, but with random choice, as if X = 5, then it would be 3, but if X = 6, then it can be 3 or 4
    coordinatesY = coordinatesY // 2 + 1 - (random.choice([0, 1]) if coordinatesY % 2 == 1 else 0) # now choosing middle of X coordinates, but with random choice, as if X = 5, then it would be 3, but if X = 6, then it can be 3 or 4
    shootCheck(coordinatesX,coordinatesY,mapPlayer,fleetPlayer)

    

"""
function to check if shooting hit ship or not, if hit is it sunken
"""
cpuSHOOT = [] #global, where infoormation of shooting will be stored
def shootCheck(coordX, coordY, map, fleet):
    global shipSymbols, cpuSHOOT
    checkCoordinates = [coordX,coordY]
    shootHit = None
    wholeShipCoordinates = []
    for shipName,shipData in fleet.values():
        for coordinatesAllShips in shipData["Coordinates"]:
            if checkCoordinates in coordinatesAllShips: # if it was hit:
                map[coordX,coordY] = shipSymbols["Hit"][0]
                shootHit = shipName # storing ship name if hit, so it is not None, what will make next If condition to work
                wholeShipCoordinates = coordinatesAllShips # storing all coordinates for particular ship
    if shootHit: # now we know we hit the ship
        cpuSHOOT.append(["Hit",coordX,coordY]) # storing shooting info
        for singleCoordinate in wholeShipCoordinates: #checking map if ship is fully sunk after our hit
            if map[singleCoordinate[0],singleCoordinate[1]] != shipSymbols["Hit"][0]:
                break # one or more parts of ship is not damaged
            else: # if there was no break, it means whole ship was sunken !!!
                cpuSHOOT.clear() # clearing all shooting log for particular ship, as it is sunken
                shipInfo = fleetRemoveShip(shipName, singleCoordinate, fleet)
                print(shipInfo + "was sunken")
    if not shootHit:
        map[coordX][coordY] = shipSymbols["Miss"][0]
        cpuSHOOT.append(["Miss",coordX,coordY])

"""
function to remove given ship from fleet
"""
def fleetRemoveShip(shipName, coordinates, fleet):
    removedShipInfo = None  # Initialize to None

    if shipName in fleet:
        shipData = fleet[shipName]

        # Check if the ship has more than one quantity
        if shipData["Quantity"] > 1:
            for index, coordinatesFleet in enumerate(shipData["Coordinates"]):
                if coordinates in coordinatesFleet:
                    removedCoordinates = shipData["Coordinates"].pop(index)
                    shipData["Quantity"] -= 1
                    removedShipInfo = {
                        "ShipName": shipName,
                        "RemovedCoordinates": removedCoordinates
                    }
                    if shipData["Quantity"] == 0:
                        del fleet[shipName]
                    break  # Exit the loop after removing the coordinates
        else:
            # If there is only one ship, remove the entire ship from the fleet
            del fleet[shipName]
            removedShipInfo = {
                "ShipName": shipName,
                "RemovedCoordinates": shipData["Coordinates"]
            }
    return removedShipInfo
