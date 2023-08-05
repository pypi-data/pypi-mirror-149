#!/usr/bin/env python3

from re import findall

def compare_strings(str1:str=None, str2:str=None) -> int:
    """
    Compares two strings alphabetically.
    Not case sensitive.

    :param str1: 1st string to compare, defaults to None
    :type str1: str, optional
    :param str2: 2nd string to compare, defaults to None
    :type str2: str, optional
    :return: String which should come first.
    :rtype: int
    """
    try:
        # Return which string should come first
        upper1 = str1.upper()
        sort = sorted([upper1, str2.upper()])
        if sort[0] == sort[1]:
            return 0
        if sort[0] == upper1:
            return -1
        return 1
    except AttributeError:
        # Return 0 if error thrown
        return 0

def is_number_string(input_str:str=None) -> bool:
    """
    Return whether a given string starts with numerical information.
    Returns True if first character is a digit or a decimal point/comma.

    :param input_str: Given string, default to None
    :type input_str: str, optional
    :return: Whether input_string starts with numerical information
    :rtype: bool
    """
    try:
        return len(findall("^[0-9]*[.,]{0,1}[0-9]+$", input_str)) == 1
    except TypeError:
        return False

def get_section(input_str:str=None) -> str:
    """
    Return the first section from a given string.
    Section will contain either only string data or numerical data.

    :param input_str: Given string, defaults to None
    :type input_str: str, optional
    :return: First section of the given string
    :rtype: str
    """
    try:
        # Return number if section starts with a number
        match = findall("^[0-9]*[.,]{0,1}[0-9]+", input_str)
        if len(match) == 1:
            return match[0]
        # Return non-number is section starts with a non-number
        match = findall("^[^0-9]+(?=[.,][0-9]+|(?<=[^,.])[0-9]|$)", input_str)
        if len(match) == 1:
            return match[0]
        # Return empty string if invalid
        return ""
    except TypeError:
        return ""

def compare_sections(str1:str=None, str2:str=None):
    """
    Compare to string sections.
    Sections should contain either only string data or numerical data.

    :param str1: 1st string to compare, defaults to None
    :type str1: str, optional
    :param str2: 2nd string to compare, defaults to None
    :type str2: str, optional
    :return: String which should come first
    :rtype: str
    """
    # Get whether each given string is a digit
    is_num_1 = is_number_string(str1)
    is_num_2 = is_number_string(str2)
    # Compare sections as floats if both strings are number strings
    if is_num_1 and is_num_2 and len(str1) < 11 and len(str2) < 11:
        val1 = float(str1.replace(",", "."))
        val2 = float(str2.replace(",", "."))
        if val1 < val2:
            return -1
        elif val1 > val2:
            return 1
        return 0
    # Compare strings regularly if not number strings
    return compare_strings(str1, str2)

def compare_alphanum(str1:str=None, str2:str=None):
    """
    Compare two strings alphabetically and numerically.
    Not case sensitive.

    :param str1: 1st string to compare, defaults to None
    :type str1: str, optional
    :param str2: 2nd string to compare, defaults to None
    :type str2: str, optional
    :return: String which should come first
    :rtype: str
    """
    # Return 0 if either string is invalid
    if str1 is None or str2 is None:
        return 0
    # Break into sections and compare
    result = 0
    end1 = str1
    end2 = str2
    while (result == 0 and (not end1 == "" or not end2 == "")):
        section1 = get_section(end1)
        section2 = get_section(end2)
        end1 = end1[len(section1):]
        end2 = end2[len(section2):]
        result = compare_sections(section1, section2)
    return result
