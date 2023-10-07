def remove_common_coordinates(a, b):
    """
    Remove coordinates from list a if they exist in list b.

    Parameters:
    - a (list): The list from which coordinates will be removed.
    - b (list): The list containing coordinates to be checked against.

    Returns:
    - list: Updated list a with common coordinates removed.
    """
    # Create a new list to store the updated coordinates from list a.
    updated_a = []
    
    try:
        # Iterate through each coordinate in list a.
        for coord_in_a in a:
            # Use a flag to indicate whether the coordinate is found in list b.
            is_in_b = False
            
            # Iterate through each coordinate in list b.
            for coord_in_b in b:
                # If a match is found, set the flag to True.
                if coord_in_a == coord_in_b:
                    is_in_b = True
                    break
            
            # If the coordinate is not in list b, add it to the updated list.
            if not is_in_b:
                updated_a.append(coord_in_a)
        
        return updated_a

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
a = [[1, 2], [3, 4], [5, 6]]
b = [[3, 4], [7, 8], [9, 10]]
updated_a = remove_common_coordinates(a, b)
print("Updated List A:", updated_a)
print("Updated List b:", b)

