#!/usr/bin/env python3

from dvk_archive.main.processing.string_processing import regex_replace
from dvk_archive.main.processing.string_processing import remove_whitespace
from html import unescape
from typing import List
from re import findall

def escape_to_char(escape:str=None) -> str:
    """
    Returns single character for a given HTML escape character.
    Returned in string format. Empty if escape is invalid.

    :param escape: HTML escape character, defaults to None
    :type escape: str, optional
    :return: Unicode escape character
    :rtype: str
    """
    try:
        # Find escape character for given string
        match = findall("^&[^&;]+;$", escape)
        replace = unescape(match[0])
        # Return empty string valid replacement wasn't found
        if replace == escape:
            return ""
        # Return replacement character
        return replace
    except (IndexError, TypeError):
        return ""

def replace_escapes(text:str=None) -> str:
    """
    Replaces all HTML escape characters in a string with Unicode characters.

    :param text: Given string, defaults to None
    :type text: str, optional
    :return: String with HTML escape characters replaced
    :rtype: str
    """
    return regex_replace(escape_to_char, "&[^&;]+;", text)

def char_to_escape(char:str=None) -> str:
    """
    Converts a single character into an HTML escape string.

    :param char: Single character to convert into an HTML escape, defaults to None
    :type char: str, optional
    :return: HTML escape string for the given character
    :rtype: str
    """
    try:
        # Convert character to HTML escape
        value = str(ord(char))
        escape = f"&#{value};"
        return escape
    except TypeError:
        # Returns empty string if given character is invalid
        return ""

def add_escapes(text:str=None) -> str:
    """
    Replaces all uncommon characters in a String with HTML escapes.

    :param text: Given string, defaults to None
    :type text: str, optional
    :return: String with added HTML escape characters
    :rtype: str
    """
    return regex_replace(char_to_escape, "[^A-Za-z0-9 ]", text)
    
    # RETURNS AN EMPTY STRING IF THE GIVEN STRING IS NONE
    if text is None:
        return ""
    # RUN THROUGH EACH CHARACTER IN THE GIVEN STRING
    i = 0
    out = ""
    while i < len(text):
        value = ord(text[i])
        if ((value > 47 and value < 58)
                or (value > 64 and value < 91)
                or (value > 96 and value < 124)
                or value == ord(" ")):
            # IF CHARACTER IS ALPHA-NUMERIC, USE THE SAME CHARACTER
            out = out + text[i]
        else:
            # IF CHARACTER IS NOT ALPHA-NUMERIC, USE ESCAPE CHARACTER
            out = out + "&#" + str(value) + ";"
        # INCREMENT COUNTER
        i = i + 1
    return out

def get_blocks(text:str=None) -> List[str]:
    """
    Returns a list of string blocks from given HTML text.
    Broken up into normal text and HTML blocks.

    :param text: HTML text to split into blocks, defaults to None
    :type text: str, optional
    :return: List of string blocks from HTML text.
    :rtype: List[str]
    """
    try:
        # Get all HTML elements
        elements = findall("<[^<>]+>", text)
        # Separate out elements from text
        blocks = []
        left_text = text
        for element in elements:
            index = left_text.find(element)
            blocks.append(left_text[:index])
            blocks.append(element)
            left_text = left_text[index+len(element):]
        blocks.append(left_text)
        # Remove empty items from block list
        while True:
            try:
                index = blocks.index("")
                del blocks[index]
            except ValueError:
                break
        # Return blocks
        return blocks
    except TypeError:
        return []

def add_escapes_to_html(text:str=None) -> str:
    """
    Replaces all uncommon characters in a String with HTML escapes.
    Keeps HTML tags and structures intact.

    :param text: Given HTML String, defaults to None
    :type text: str, optional
    :return: String with added HTML escape characters
    :rtype: str
    """
    # Split text into blocks
    blocks = get_blocks(text)
    # Run through blocks, appending to HTML string
    html = ""
    for block in blocks:
        if block[0] == "<":
            # Keep HTML block intact
            html = html + block
        else:
            # Add HTML escape characters to normal text
            string = replace_escapes(block)
            string = add_escapes(string)
            html = html + string
    # Return updated HTML string
    return html
            

def clean_element(html:str=None, remove_ends:str=False) -> str:
    """
    Cleans up HTML element.
    Removes whitespace and removes header and footer tags.

    :param html: HTML element, defaults to None
    :type html: str, optional
    :param remove_ends: Whether to remove header and footer tags, defaults to None
    :type remove_ends: bool, optional
    :return: Cleaned HTML element
    :rtype: str
    """
    # RETURNS EMPTY STRING IF GIVEN ELEMENT IS NONE
    if html is None:
        return ""
    # REMOVE NEW LINE AND CARRIAGE RETURN CHARACTERS
    text = html.replace("\n", "")
    text = text.replace("\r", "")
    # REMOVE WHITESPACE BETWEEN TAGS
    while "  <" in text:
        text = text.replace("  <", " <")
    while ">  " in text:
        text = text.replace(">  ", "> ")
    # REMOVE HEADER AND FOOTER, IF SPECIFIED
    if remove_ends:
        text = remove_whitespace(text)
        # REMOVE HEADER
        if len(text) > 0 and text[0] == "<":
            start = text.find(">")
            if not start == -1:
                text = text[start + 1:len(text)]
        # REMOVE FOOTER
        if len(text) > 0 and text[-1] == ">":
            end = text.rfind("<")
            if not end == -1:
                text = text[0:end]
    # REMOVE WHITESPACE FROM THE START AND END OF STRING
    text = remove_whitespace(text)
    return text

def remove_html_tags(text:str=None) -> str:
    """
    Removes HTML from given text, leaving only standard text.

    :param text: HTML text to remove tags from, defaults to None
    :type text: str, optional
    :return: HTML with the HTML tags removed
    :rtype: str
    """
    # Separate HTML into blocks
    blocks = get_blocks(text)
    # Remove HTML tags from blocks
    index = 0
    while index < len(blocks):
        if blocks[index][0] == "<":
            del blocks[index]
            continue
        index += 1
    # Combine remaining blocks into HTML string
    html = ""
    for i in range(0, len(blocks)):
        if i > 0:
            html = html + " "
        html = html + blocks[i]
    # Return HTML with tags removed
    return html

def create_html_tag(tag:str=None,
            attributes:List[List[str]]=None,
            text:str=None,
            pad_text:bool=True) -> str:
    """
    Creates an HTML tag with given parameters and contained text.

    :param tag: String for the tag itself (a, div, etc.), defaults to None
    :type tag: str, optional
    :param attributes: List of tag attribute pairs (Organized [attr, value]), defaults to None
    :type attributes: list[list[str]]
    :param text: Text to put inside the HTML tag, defaults to None
    :type text: str, optional
    :param pad_text: Whether to put internal text on a new line with tabs, defaults to True
    :type pad_text: bool, optional
    :return: HTML tag
    :rtype: str
    """
    # Return empty string if parameters are invalid
    if tag is None:
        return ""
    try:
        # Create the end of the HTML tag
        tag_end = ""
        if text is not None:
            tag_end = "</" + tag + ">"
        # Create the start of the HTML tag
        tag_start = "<" + tag
        # Add attributes to HTML tag
        if attributes is not None:
            for attribute in attributes:
                tag_start = tag_start + " " + attribute[0]\
                            +"=\"" + attribute[1] + "\""
        tag_start = tag_start + ">"
        # Add padding to the internal text of the tag if specified
        inner_text = text
        if inner_text is None:
            inner_text = ""
        if pad_text and text:
            inner_text = inner_text.replace("\n", "\n    ")
            inner_text = "\n    " + inner_text + "\n"
        # Create and return the full HTML tag
        tag = tag_start + inner_text + tag_end
        return tag
    except (IndexError, TypeError):
        # Return empty string if creating HTML tag fails
        return ""
