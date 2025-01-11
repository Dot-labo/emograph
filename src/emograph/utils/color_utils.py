def hex_to_tuple(color_str: str) -> tuple:
    """
    Convert a hex color string to a tuple of RGB values.
    Remove the '#' character from the string and convert each pair of characters to an integer.

    Args:
        color_str (str): A hex color string.

    Returns:
        tuple: A tuple of RGB values.
    """
    return tuple(int(color_str[i:i+2], 16) for i in (1, 3, 5))
