def update_cpu_shot_log(coordinates_list):
    """
    Update the CPU shot log by removing coordinates that are present in
    the provided coordinates_list, implying that a ship has been sunk.

    Parameters:
    - coordinates_list (list): A list of coordinates that are to be removed.

    Returns:
    - list: Updated CPU shot log.
    """

    # Declare global variable to access and modify CPU shot log
    global cpu_shot_log_tmp

    # Exception handling to gracefully manage any runtime errors
    try:
        # Loop through each coordinate pair in coordinates_list
        for coord in coordinates_list:
            # Remove the coordinate pair from cpu_shot_log_tmp
            cpu_shot_log_tmp.remove(coord)

    except ValueError as e:
        print(f"Coordinate not found in log: {e}")

    return cpu_shot_log_tmp

# Initialize cpu_shot_log_tmp
cpu_shot_log_tmp = [[7, 2], [6, 2]]

# Test 1: Remove multiple coordinates
coords_to_remove = [[7, 2], [6, 2]]
new_log = update_cpu_shot_log(coords_to_remove)
print(new_log)  # Should print []

# Reset cpu_shot_log_tmp
cpu_shot_log_tmp = [[7, 2], [6, 2]]

# Test 2: Remove a single coordinate
single_coord_to_remove = [[7, 2]]
new_log = update_cpu_shot_log(single_coord_to_remove)
print(new_log)  # Should print [[6, 2]]
