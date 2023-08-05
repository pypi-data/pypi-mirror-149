#!/usr/bin/env python3

from dvk_archive.main.processing.html_processing import add_escapes
from dvk_archive.main.processing.string_processing import remove_whitespace as rw
from typing import List

def clean_list(lst:List[str]=None, remove_whitespace:bool=True) -> List[str]:
    """
    Removes all duplicate, None, and blank entries from a String array.

    :param lst: Given string list
    :type lst: list[str], optional
    :param remove_whitespace: Whether to remove whitespace from list entries, defaults to True
    :type remove_whitespace: bool, optional
    :return: List without duplicate or None entries
    :rtype: list[str]
    """
    try:
        # Remove entries with None value
        out = lst
        while True:
            try:
                index = out.index(None)
                del out[index]
            except ValueError:
                break
        # Remove whitespace if specified
        if remove_whitespace:
            size = len(out)
            for i in range(0, size):
                out[i] = rw(out[i])
        # Remove entries with blank value
        while True:
            try:
                index = out.index("")
                del out[index]
            except ValueError:
                break
        # Remove duplicate entries
        out = list(dict.fromkeys(out))
        # Return modified list
        return out
    except AttributeError:
        return []

def list_to_string(lst:List[str]=None,
                use_escapes:bool=False,
                indent:int=0) -> str:
    """
    Converts list[str] into a string with items separated by commas.

    :param lst: List[str] to convert to string, defaults to None
    :type lst: list[str], optional
    :param use_escapes: Whether to add HTML escape chars to items, defaults to None
    :type use_escapes: bool, optional
    :param indent: Number of spaces to add after separating commas, defaults to 0
    :type indent: int, optional
    :return: String with original items separated by commas
    :rtype: str
    """
    try:
        my_list = []
        my_list.extend(lst)
        # Add HTML escape characters if specified
        if use_escapes:
            for i in range(0, len(my_list)):
                my_list[i] = add_escapes(my_list[i])
        # Convert list into string
        string = ""
        for i in range(0, len(my_list)):
            # Add comma if necessary
            if i > 0:
                string = string + ","
                # Add indent
                for k in range(0, indent):
                    string = string + " "
            # Add string from list
            string = string + my_list[i]
        # Return string
        return string
    except:
        return ""
    
