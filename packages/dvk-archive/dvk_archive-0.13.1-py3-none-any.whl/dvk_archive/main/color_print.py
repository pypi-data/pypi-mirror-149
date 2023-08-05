#!/usr/bin/env python3

def color_print(text:str=None, color:str=None) -> bool:
    """
    Prints text to the terminal in a given color.

    :param text: Text to print, defaults to None
    :type text: str, optional
    :param color: Color to print in (r - Red, g - Green), defaults to None
    :type color:
    :return: Whether printing was successful
    :rtype: bool
    """
    # Don't print if no text or color is provided.
    if text is None or color is None:
        return False
    # Print colored text
    if color == "g":
        print("\033[32m" + text + "\033[0m")
    elif color == "r":
        print("\033[31m" + text + "\033[0m")
    else:
        # Print text in default color if appropriate color not found.
        print(text)
    return True
