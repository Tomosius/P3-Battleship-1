def printMap(printMap):
    column_width = [max(len(str(item)) for item in column) for column in zip(*printMap)]
    for column, width in zip(printMap[0], column_width):
        print(f"{column:{width}}", end="  ")  # Use two spaces instead of " | "
    print()
    for row in printMap[1:]:
        for item, width in zip(row, column_width):
            print(f"{item:{width}}", end="  ")  # Use two spaces instead of " | "
        print()
