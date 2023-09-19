#Section for Global Variables
X = 10           # default map size X - horizontal
Y = 10          # default map size Y - vertical
mapSize = [X,Y]   # first number - horizontal lines, second - vertical, by default it will be 10 x 10

# default Battleship fleet - i use as dictionary, so in case if player changes map size or ships quantities, it will be easier to play
battleship_fleet = {
    "Aircraft Carrier": {
        "Size": 5,
        "Quantity": 1
    },
    "Battleship": {
        "Size": 4,
        "Quantity": 1
    },
    "Cruiser": {
        "Size": 3,
        "Quantity": 1
    },
    "Submarine": {
        "Size": 3,
        "Quantity": 1
    },
    "Destroyer": {
        "Size": 2,
        "Quantity": 1
    }
}



# section for imports of libraries
import curses

def map_size(): #function for user to inoput map size
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

def newGame(): #function to start new game
    map_size() #asking user to input new map size


# creating an array thatt will be reperesenting map based on X and Y
map = [[0 for j in range(Y)] for i in range(X)]

# Print the CPU MAP array to the console - will create function, later will be easier to print the map
def printCpuMap():
    for row in map:
        print(row)

printCpuMap()

