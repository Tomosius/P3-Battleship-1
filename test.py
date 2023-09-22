import curses

# Define color pairs for curses
COLOR_PAIR_DARK_YELLOW = 1
COLOR_PAIR_LIGHT_GRAY = 2
COLOR_PAIR_DARK_BLUE = 3
COLOR_PAIR_DARK_GREEN = 4
COLOR_PAIR_DARK_RED = 5

# Initialize curses
stdscr = curses.initscr()
curses.start_color()
curses.init_pair(COLOR_PAIR_DARK_YELLOW, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(COLOR_PAIR_LIGHT_GRAY, curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(COLOR_PAIR_DARK_BLUE, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(COLOR_PAIR_DARK_GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(COLOR_PAIR_DARK_RED, curses.COLOR_RED, curses.COLOR_BLACK)

# Define color codes for formatting
colors = {
    "DARK_YELLOW": curses.color_pair(COLOR_PAIR_DARK_YELLOW),
    "LIGHT_GRAY": curses.color_pair(COLOR_PAIR_LIGHT_GRAY),
    "DARK_BLUE": curses.color_pair(COLOR_PAIR_DARK_BLUE),
    "DARK_GREEN": curses.color_pair(COLOR_PAIR_DARK_GREEN),
    "DARK_RED": curses.color_pair(COLOR_PAIR_DARK_RED),
    "RESET": curses.color_pair(0)  # Reset to default colors
}

# Your existing code for map rendering functions can remain mostly unchanged.

# Modify your deploySingleShip function to use curses color codes
def deploySingleShip(map, length, location, alignment):
    row, column = location
    if length == 1:
        color = colors["DARK_YELLOW"]
        map[row][column] = (chr(0x25C6), color)  # Store character and color pair
    else:
        if alignment == "H":
            color = colors["DARK_BLUE"]
            map[row][column] = (chr(0x25C0), color)
            for i in range(length - 1):
                map[row][column + i + 1] = (chr(0x25A0), color)
        else:
            color = colors["DARK_GREEN"]
            map[row][column] = (chr(0x25B2), color)
            for i in range(length - 1):
                map[row + i + 1][column] = (chr(0x25A0), color)

# Your printMap function can also be adapted to use curses color codes
def printMap(table):
    stdscr.addstr("   ")
    for col_index in range(len(table[0])):
        stdscr.addstr(f"{col_index}  ")
    stdscr.addstr("\n   " + "=" * (len(table[0]) * 3) + "\n")

    for row_index, row in enumerate(table):
        stdscr.addstr(f"{row_index} | ")
        for value, color in row:
            stdscr.addstr(value, color)
            stdscr.addstr("  ")
        stdscr.addstr("\n")

# Example usage of your functions with curses
def main(stdscr):
    # Initialize colors and maps
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    mapCPU = [[(" ", curses.color_pair(1))] * 10 for _ in range(10)]
    mapPlayer = [[(" ", curses.color_pair(1))] * 10 for _ in range(10)]

    # Deploy ships (modify as needed)
    deploySingleShip(mapCPU, 5, (0, 0), "H")
    deploySingleShip(mapPlayer, 4, (1, 1), "V")

    # Print maps
    stdscr.clear()
    stdscr.addstr("CPU Map:\n")
    printMap(mapCPU)
    stdscr.addstr("\nPlayer Map:\n")
    printMap(mapPlayer)
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
