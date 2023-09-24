








"""
function to deploy CPU ships
"""
def cpuDeployAllShips():
    global fleetCPU, battleShipFleetDefault, mapCPU
    fleetCPU = copy.deepcopy(battleShipFleetDefault) # making fresh copy, in case there were any changes made for map size or fleet
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
shotInfo = [] #global, where infoormation of shooting will be stored

def shootCheck(coordX, coordY, map, fleet):
    global shipSymbols, shotInfo
    checkCoordinates = [coordX,coordY]
    shootHit = None # this will be ship name
    wholeShipCoordinates = []
    for shipName,shipData in fleet.values():
        for coordinatesAllShips in shipData["Coordinates"]:
            if checkCoordinates in coordinatesAllShips: # if it was hit:
                map[coordX,coordY] = shipSymbols["Hit"][0]
                shootHit = shipName # storing ship name if hit, so it is not None, what will make next If condition to work
                wholeShipCoordinates = coordinatesAllShips # storing all coordinates for particular ship
    if shootHit: # now we know we hit the ship
        shotInfo.append(["Hit",coordX,coordY]) # storing shooting info
        for singleCoordinate in wholeShipCoordinates: #checking map if ship is fully sunk after our hit
            if map[singleCoordinate[0],singleCoordinate[1]] != shipSymbols["Hit"][0]:
                break # one or more parts of ship is not damaged
            else: # if there was no break, it means whole ship was sunken !!!
                shotInfo.clear() # clearing all shooting log for particular ship, as it is sunken
                shipInfo = fleetRemoveShip(shipName, singleCoordinate, fleet)
                print(shipInfo + "was sunken")
    if not shootHit:
        map[coordX][coordY] = shipSymbols["Miss"][0]
        shotInfo.append(["Miss",coordX,coordY])
    return shootHit, shotInfo

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
            print("removed ship info" + removedShipInfo)
    return removedShipInfo


"""
function to check is there any more ships remaining in fleet
"""
def fleetCheck(fleet):
    ships_to_remove = []  # List to store ship names with quantity 0
    # Find ships with quantity 0
    for ship_name, ship_data in fleet.items():
        if ship_data["Quantity"] == 0:
            ships_to_remove.append(ship_name)
    # Remove ships with quantity 0
    for ship_name in ships_to_remove:
        del fleet[ship_name]
    if not fleet: # if there is nor remaining ships in fleet
        print("game over")


"""
function for player to input shoot coordinates
"""
def playerShoot(): #function for user to input map size
    while True:
        # user will be requested to input map size
        coordinatesPlayerShoot = input("Please select coordinates X and Y where you would like to shoot. First number - Horizontal, second number - Vertical. Example: 3,6 \n")
        try: #testing if user used correct pattern to input map size
            coordX,coordY = coordinatesPlayerShoot.split(',') # splitting user input into 2 separate parts 
            if coordX.isdigit() and coordY.isdigit(): # checking if both inputs parts are numbers
                break #now function can stop as all is correct
            else:  #if any part of inout is not numeric, printing out message
                print("Invalid input. Please enter two numbers separated by a comma.")
        except ValueError: #if user input can not be split in 2 parts will raise an issue:
            print("Invalid input. Please enter two numbers separated by a comma.")
    return coordX,coordY

