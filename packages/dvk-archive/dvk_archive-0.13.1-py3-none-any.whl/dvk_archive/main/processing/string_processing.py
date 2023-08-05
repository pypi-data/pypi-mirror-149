#!/usr/bin/env python3

from math import floor
from os.path import abspath
from re import findall, sub

def regex_replace(funct, pattern:str=None, string:str=None) -> str:
    """
    Replaces text matching regex pattern with said matching text run though a given function.

    :param funct: Function to run matching text through, required
    :type funct: function, required
    :param pattern: Regex pattern to search for in string, defaults to None
    :type pattern: str, optional
    :param string: String to search for pattern within, defaults to None
    :type string: str, optional
    :return: Given string with pattern matched text replaced
    :rtype: str
    """
    try:
        # Get all strings that match the regex pattern
        matched = findall(pattern, string)
        # Run through all matches to replace text
        new_text = ""
        left_text = string
        for match in matched:
            # Keep all text before the match
            index = left_text.find(match)
            new_text = new_text + left_text[:index]
            # Add replacement for the match
            new_text = new_text + funct(match)
            # Set the remaining text for after the match
            index += len(match)
            left_text = left_text[index:]
        # Keep all the text left in the initial string
        new_text = new_text + left_text
        # Return the string with matching patterns replaced
        return new_text
    except TypeError:
        return string

def pad_num(num:str=None, length:int=0) -> str:
    """
    Returns a String for a given String of a given length.
    If too small, pads out String with zeros.

    :param input: Number string to extend, defaults to None
    :type input: str, optional
    :param length: Length of returned String
    :type length: int, optional
    :return: Padded string
    :rtype: str
    """
    # Returns an empty string if the given string or length is invalid
    if num is None or length < 1:
        return ""
    # Pad out the string with zeros to reach the given string length
    new_num = num
    while len(new_num) < length:
        new_num = f"0{new_num}"
    return new_num

def remove_whitespace(text:str=None) -> str:
    """
    Removes the whitespace at the beginning and end of a given String.

    :param text: Given string, defaults to None
    :type text: str, optional
    :return: String without whitespace
    :rtype: str
    """
    # Return an empty string if the given string is invalid
    if text is None:
        return ""
    # Remove leading and ending whitespace
    new_text = sub("^\\s+|\\s+$", "", text)
    # Return the new text
    return new_text

def truncate_string(text:str=None, length:int=90) -> str:
    """
    Shortens a given string to be at or below a given length.
    Attempts to keep readable by removing characters at break-points.

    :param text: Given string, defaults to None
    :type text: str, optional
    :param length: Maximum length of the returned string, defaults to None
    :type length: str, optional
    :return: Shortened string
    :rtype: str
    """
    # RETURN AN EMPTY STRING IF GIVEN STRING IS NONE OR EMPTY
    if text is None or length < 1:
        return ""
    # RETURN GIVEN STRING IF IT'S LENGTH IS <= THE VARIABLE LENGTH
    if len(text) <= length:
        return text
    # FIND INDEX TO START REMOVING CHARACTERS FROM.
    # ATTEMPTS TO BREAK AT A SPACE OR HYPHEN
    if " " in text:
        index = text.rfind(" ")
    elif "-" in text:
        index = text.rfind("-")
    else:
        index = floor(len(text)/2)
    # DELETE CHARACTERS FROM THE INDEX POSITION
    out = text
    if index < len(out) - index:
        index = index + 1
        while index < len(out) and length < len(out):
            out = out[:index] + out[index+1:]
    else:
        index = index - 1;
        while index > -1 and len(out) > length:
            out = out[:index] + out[index+1:]
            index = index - 1
        if (index > -1
                and index < len(out) -1
                and out[index] == out[index+1]
                and (out[index] == " " or out[index] == "-")):
            out = out[:index] + out[index+1:]
    # IF STILL TOO LONG, REMOVE CHARACTERS FROM THE END OF THE STRING
    if len(out) > length:
        out = out[:length]
    # REMOVE START AND END SPACERS
    while len(out) > 0 and (out[0] == " " or out[0] == "-"):
        out = out[1:]
    while len(out) > 0 and (out[len(out)-1] == " " or out[len(out)-1] == "-"):
        out = out[:-1]
    return out

def get_filename(text:str=None, length:int=90) -> str:
    """
    Returns a version of a given String that is safe for use as a filename.

    :param text: Given string, defaults to None
    :type text: str, optional
    :param length: Maximum length of the returned filename, defaults to 90
    :type length: int, optional
    :return: Filename
    :rtype: str
    """
    # If given string is invalid, return string "0"
    if text is None:
        return "0"
    # Replace accented characters with nearest ASCII equivalents
    new_text = sub("[À-Å]", "A", text)
    new_text = sub("[È-Ë]", "E", new_text)
    new_text = sub("[Ì-Ï]", "I", new_text)
    new_text = sub("[Ò-Ö]", "O", new_text)
    new_text = sub("[Ù-Ü]", "U", new_text)
    new_text = sub("[à-å]", "a", new_text)
    new_text = sub("[è-ë]", "e", new_text)
    new_text = sub("[ì-ï]", "i", new_text)
    new_text = sub("[ò-ö]", "o", new_text)
    new_text = sub("[ù-ü]", "u", new_text)
    new_text = sub("[ýÿ]", "y", new_text)
    new_text = new_text.replace("Ñ", "N")
    new_text = new_text.replace("Ý", "Y")
    new_text = new_text.replace("ñ", "n")
    # Replace all non-alphanumeric characters with hyphens
    new_text = sub("[^a-zA-Z0-9 ]", "-", new_text)
    # Remove whitespace and hyphens at begining and end of text
    new_text = sub("^[\\s-]+|[\\s-]+$", "", new_text)
    # Remove duplicate spacers
    new_text = sub("-{2,}", "-", new_text)
    new_text = sub(" {2,}", " ", new_text)
    # Remove hanging hyphens
    new_text = sub("(?<= )-(?=[a-zA-Z0-9])|(?<=[a-zA-Z0-9])-(?= )", "", new_text)
    # Truncate string
    if length != -1:
        new_text = truncate_string(new_text, length)
    # Return cleaned string
    if len(new_text) == 0:
        # If final string has no length, return string "0"
        return "0"
    return new_text

def get_extension(filename:str=None) -> str:
    """
    Returns the extension for a given filename or direct file URL.
    If extension does not exist, returns empty.

    :param filename: Given filename, defaults to None
    :type filename: str, optional
    :return: Extension for the filename
    :rtype: str
    """
    # Returns an empty string if the filename is invalid
    if filename is None:
        return ""
    # Find extension
    match = findall("\\.[a-zA-Z0-9]{1,5}\\?|\\.[a-zA-Z0-9]{1,5}$", filename)
    if len(match) == 0:
        return ""
    # Return extension
    extension = match[0]
    for item in match:
        if item.endswith("?"):
            extension = item[:len(item)-1]
    return extension

def get_url_directory(url:str=None) -> str:
    """
    Returns the last sub-directory for a given URL.

    :param url: Given URL, defaults to None
    :type url: str, optional
    :return: Last sub-directory of the given URL
    :rtype: str
    """
    # Return empty string if url is invalid
    if url is None:
        return ""
    # Remove last forward slash from the URL
    main = sub("\\/+$", "", url)
    # Get last sub-directory
    last = main.rfind("/") + 1
    return main[last:]

def truncate_path(parent:str=None, file:str=None) -> str:
    # Return empty string if file is invalid
    if file is None:
        return ""
    # Return file if parent path is invalid
    if parent is None:
        return file
    # Return file if parent is not actually a parent directory
    full_parent = abspath(parent)
    full_file = abspath(file)
    if (full_parent == full_file
            or not full_file.startswith(full_parent)):
        return full_file
    # Truncate the file path of the given file
    truncated = full_file[len(full_parent):]
    return "..." + truncated
