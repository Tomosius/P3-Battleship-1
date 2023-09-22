
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
    

    

"""
function to check if shooting hit ship or not
"""
def shootCheck(coordX, coordY, map, fleet):
    checkCoordinates = [coordX,coordY]
    for shipData in fleet.values():
        for coordinatesAlships in shipData["Coordinates"]:
            if checkCoordinates not in coordinatesAlships:
                map[coordX][coordY] = colors["LIGHT_GRAY"] + chr(0x2022) + colors["RESET"] # marking spot as gray dot as shooting was a miss
            
                
















