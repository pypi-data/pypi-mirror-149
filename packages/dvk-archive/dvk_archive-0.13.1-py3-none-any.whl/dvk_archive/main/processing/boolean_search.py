#!/usr/bin/env python3

from argparse import ArgumentParser
from dvk_archive.main.color_print import color_print
from dvk_archive.main.file.dvk_handler import DvkHandler
from dvk_archive.main.processing.html_processing import add_escapes
from dvk_archive.main.processing.html_processing import remove_html_tags
from dvk_archive.main.processing.list_processing import list_to_string
from dvk_archive.main.processing.string_processing import remove_whitespace
from dvk_archive.main.processing.string_processing import truncate_path
from os import getcwd
from os.path import abspath, exists, isdir
from tqdm import tqdm
from typing import List

def separate_into_chunks(search:str=None) -> List[str]:
    """
    Separates boolean search string into parsable chunks.

    :param search: String using boolean search logic, defaults to None
    :type search: str, optional
    :return: List of chunks for boolean logic
    :rtype: list[str]
    """
    # Remove whitespace from start and end of string
    string = remove_whitespace(search)
    # Run through string, separating components
    chunks = []
    while len(string) > 0:
        if string[0] == "!" or string[0] == "-":
            # Separate not operator
            chunks.append("!")
            string = string[1:]
        elif string[0] == "&" or string[0] == "+":
            # Separate and operator
            chunks.append("&")
            string = string[1:]
        elif string[0] == "|" or string[0] == "~":
            # Separate or operator
            chunks.append("|")
            string = string[1:]
        elif string[0] == "(" or string[0] == "[":
            # Separate left paren operator
            chunks.append("(")
            string = string[1:]
        elif string[0] == ")" or string[0] == "]":
            # Separate right paren operator
            chunks.append(")")
            string = string[1:]
        elif string[0] == "'" or string[0] == "\"" or string[0] == "=":
            # Separate string in quotation marks
            char = string[0]
            end = string.find(char, 1)
            if end == -1:
                end = len(string)
            chunks.append(string[1:end])
            string = string[end:]
            if string.startswith(char):
                string = string[1:]
        else:
            # Separates standard strings
            end = 0
            while (end < len(string)
                        and not string[end] == " "
                        and not string[end] == ")"
                        and not string[end] == "]"):
                end += 1
            word = string[:end]
            string = string[end:]
            # Check if separated string is an operator
            if word.lower() == "and":
                # Replace AND with "&" operator
                word = "&"
            elif word.lower() == "or":
                # Replace OR with "|" operator
                word = "|"
            elif word.lower() == "not":
                # Replace NOT with "!" operator
                word = "!"
            chunks.append(word)
        # Remove whitespace from the start of the string
        string = remove_whitespace(string)
    return chunks

def is_string(chunk:str=None) -> bool:
    """
    Returns whether given boolean chunk is a string.
    Returns False if chunk is an operator symbol.

    :param chunk: Boolean chunk, defaults to None
    :type chunk: str, optional
    :return: Whether given chunk is a string
    :rtype: bool
    """
    # Return False if parameter is invalid
    if chunk is None:
        return False
    # Check if given chunk is an operator symbol
    if (chunk == "&"
            or chunk == "|"
            or chunk == "!"
            or chunk == "("
            or chunk == ")"):
        return False
    return True

def fix_logic(chunks:List[str]=None) -> List[str]:
    """
    Fixes any logic errors in a boolean search expression.
    Uses boolean search chunks from separate_into_chunks function.

    :param chunks: Boolean search chunks, defaults to None
    :type chunks: list[str], optional
    :return: Fixed list of boolean search chunks
    :rtype: list[str]
    """
    # Return empty list if parameters are invalid
    if chunks is None:
        return []
    # Remove leading operators
    fixed = chunks
    while len(fixed) > 0 and (fixed[0] == "&" or fixed[0] == "|"):
        del fixed[0]
    # Remove trailing operators
    while len(fixed) > 0 and (fixed[-1] == "&" or fixed[-1] == "|" or fixed[-1] == "!"):
        del fixed[len(fixed)-1]
    if len(fixed) == 0:
        return []
    # Complete left parens
    if "(" in fixed:
        index = fixed.index("(") + 1
        # Count parens after the first left paren
        left = 1
        right = 0
        while index < len(fixed):
            if fixed[index] == "(":
                left += 1
            elif fixed[index] == ")":
                right += 1
            index += 1
        # Add right parens if necessary
        if left > right:
            for i in range(0, left-right):
                fixed.append(")")
    # Complete right parens
    if ")" in fixed:
        # Get last index of right paren
        index = len(fixed) - 1
        while not fixed[index] == ")":
            index -= 1
        # Count parens before the last right paren
        left = 0
        right = 1
        index -= 1
        while index > -1:
            if fixed[index] == "(":
                left += 1
            elif fixed[index] == ")":
                right += 1
            index -= 1
        # Add left parens if necessary
        if right > left:
            for i in range(0, right-left):
                fixed.insert(0, "(")
    # Add AND operator to unlinked logic
    index = 1
    while index < len(fixed):
        if is_string(fixed[index]) and (is_string(fixed[index-1]) or fixed[index-1] == ")"):
            fixed.insert(index, "&")
        elif fixed[index] == "(" and (fixed[index-1] == ")" or is_string(fixed[index-1])):
            fixed.insert(index, "&")
        elif fixed[index] == "!" and (fixed[index-1] == ")" or is_string(fixed[index-1])):
            fixed.insert(index, "&")
        index += 1
    # Add empty strings to hanging operators
    index = 0
    while index < len(fixed) - 1:
        if ((fixed[index] == "&" or fixed[index] == "|" or fixed[index] == "!")
                and (fixed[index+1] == "&" or fixed[index+1] == "|")):
            fixed.insert(index+1, "")
        if fixed[index] == "!" and fixed[index+1] == "!":
            fixed.insert(index+1, "")
        index += 1
    return fixed

def get_logic(chunks:List[str]=None) -> List:
    """
    Returns list with logic parameters from boolean logic chunks.
    [0] - Argument 1, string or nested logic
    [1] - Whether Argument 1 logic should be inverted
    [2] - Argument 2, string or nested logic
    [3] - Whether Argument 2 logic should be inverted
    [4] - Operator for comparing Arguments 1 and 2 (AND or OR)

    :param chunks: Valid boolean search chunks, defaults to None
    :type chunks: List[str]
    :return: Logic list
    :rtype: List
    """
    logic = [None, False, None, False, None]
    mod_chunks = []
    try:
        mod_chunks.extend(chunks)
        # Add first inversion if necessary
        if mod_chunks[0] == "!":
            logic[1] = True
            del mod_chunks[0]
        if mod_chunks[0] == "(":
            # Get nested statement, if necessary
            del mod_chunks[0]
            section = []
            left = 1
            right = 0
            while not left == right:
                if mod_chunks[0] == "(":
                    left += 1
                elif mod_chunks[0] == ")":
                    right += 1
                section.append(mod_chunks[0])
                del mod_chunks[0]
            del section[len(section) - 1]
            logic[0] = get_logic(section)
        else:
            # Get first search string
            logic[0] = mod_chunks[0]
            del mod_chunks[0]
        if len(mod_chunks) > 0:
            # Get operator
            logic[4] = mod_chunks[0]
            del mod_chunks[0]
            # Add second inversion if necessary
            if len(mod_chunks) == 2 and mod_chunks[0] == "!":
                logic[3] = True
                del mod_chunks[0]
            if len(mod_chunks) > 1:
                # Get nested statement if necessary.
                logic[2] = get_logic(mod_chunks)
            else:
                # Get second search string
                logic[2] = mod_chunks[0]
                del mod_chunks[0]
        # Simplify logic
        if not logic[1] and type(logic[0]) is list and logic[2] is None:
            return logic[0]
        # Return logic
        return logic
    except:
        return []

def get_logic_from_string(search:str=None, to_lower:bool=False) -> List:
    """
    Returns list with logic parameters from boolean search string.

    :param search: Boolean search string, defaults to None
    :type search: str, optional
    :param to_lower: Whether to convert strings to lowercase, defaults to False
    :type to_lower: bool, optional
    :return: Logic list
    :rtype: List
    """
    chunks = separate_into_chunks(search)
    chunks = fix_logic(chunks)
    logic = get_logic(chunks)
    if to_lower:
        return logic_to_lower(logic)
    return logic

def logic_to_lower(logic:List=None) -> List:
    """
    Converts all string arguments in a given logic list to lowercase.

    :param logic: Logic list, defaults to None
    :type logic: List, optional
    :return: Logic list with arguments converted to lowercase
    :rtype: List
    """
    try:
        converted = []
        converted.extend(logic)
        # Convert arg1 to lowercase
        if converted[0] is not None and type(converted[0]) is str:
            converted[0] = converted[0].lower()
        elif converted[0] is not None and type(converted[0]) is list:
            # Recurse if arg1 is a logic list
            converted[0] = logic_to_lower(converted[0])
        # Convert arg2 to lowercase
        if converted[2] is not None and type(converted[2]) is str:
            converted[2] = converted[2].lower()
        elif converted[2] is not None and type(converted[2]) is list:
            # Recurse if arg2 is a logic list
            converted[2] = logic_to_lower(converted[2])
        return converted
    except:
        return []

def add_escapes_to_logic(logic:List=None, add_commas:bool=False) -> List:
    """
    Adds HTML escape characters to strings in a given logic statement.
    Can also add commas to start and end of strings,
    useful for searching for exact items in lists converted to strings.

    :param logic: Logic to add escape chars to, defaults to None
    :type logic: list, optional
    :type add_commas: Adds commas to start and end of strings, defaults to False
    :param add_commas: bool, optional
    :return: Logic list with escape characters added to strings
    :rtype: List
    """
    try:
        converted = []
        converted.extend(logic)
        # Add escapes to arg1
        if converted[0] is not None and type(converted[0]) is str:
            converted[0] = add_escapes(converted[0])
            # Add commas if specified
            if add_commas:
                converted[0] = "," + converted[0] + ","
        elif converted[0] is not None and type(converted[0]) is list:
            # Recurse if arg1 is a logic list
            converted[0] = add_escapes_to_logic(converted[0], add_commas)
        # Add escapes to arg2
        if converted[2] is not None and type(converted[2]) is str:
            converted[2] = add_escapes(converted[2])
            # Add commas if specified
            if add_commas:
                converted[2] = "," + converted[2] + ","
        elif converted[2] is not None and type(converted[2]) is list:
            # Recurse if arg2 is a logic list
            converted[2] = add_escapes_to_logic(converted[2], add_commas)
        return converted
    except:
        return []

def get_arg_value(search=None,
            invert:bool=False,
            string:str=None,
            exact_match:bool=False) -> bool:
    """
    Returns whether given string matches the search string.
    Used for getting argument values in a greater search logic list.

    :param search: String to search for, defaults to None
    :type search: str, optional
    :param invert: Whether to invert the return bool, defaults to None
    :type invert: bool, optional
    :param string: String to search within, defaults to None
    :type string: str, optional
    :param exact_match: Whether strings have to match exactly or just contain value, defaults to False
    :type exact_match: bool, optional
    :return: Whether the given string matches the search
    :rtype: bool
    """
    value = False
    if type(search) is not list:
        # Compare strings if search is a string
        if exact_match:
            value = (search == string)
        else:
            value = search in string
    else:
        # get search_string result if search is a logic list
        value = search_string(search, string, exact_match)
    # Invert result if necessary
    if invert:
        return not value
    return value

def search_string(logic:List=None,
            string:str=None,
            exact_match:bool=False) -> bool:
    """
    Searches a given string for values specified in logic list.

    :param logic: Logic list to search string with, defaults to None
    :type logic: str, optional
    :param string: String to search for values within, defaults to None
    :type string: str, optional
    :param exact_match: Whether strings have to match exactly or just contain value, defaults to False
    :type exact_match:bool, optional
    :return: Whether given string matches the given logic
    :rtype: bool
    """
    try:
        if logic[4] == "&":
            # Compares argument values with AND operator
            return (get_arg_value(logic[0], logic[1], string, exact_match)
                        and get_arg_value(logic[2], logic[3], string, exact_match))
        elif logic[4] == "|":
            # Compares argument values with OR operator
            return (get_arg_value(logic[0], logic[1], string, exact_match)
                        or get_arg_value(logic[2], logic[3], string, exact_match))
        else:
            # Returns value of argument 1 if argument 2 doesn't exist
            return get_arg_value(logic[0], logic[1], string, exact_match)
    except:
        # Return False if comparing arguments fails
        return False

def search_dvks(dvk_handler:DvkHandler=None,
                case_sensitive:bool=False,
                title_search:str=None,
                title_exact:bool=False,
                artist_search:str=None,
                artist_exact:bool=False,
                web_tag_search:str=None,
                web_tag_exact:bool=False,
                desc_search:str=None,
                desc_exact:str=False,
                url_search:str=None,
                url_exact:bool=False) -> List[int]:
    """
    Searches DvkHandler for Dvks that match the given search parameters.

    :param dvk_handler: DvkHandler used to search for Dvks, defaults to None
    :type dvk_handler: DvkHandler, optional
    :param case_sensitive: Whether searches should be case sensitive, defaults to False
    :type case_sensitive: bool, optional
    :param title_search: Boolean search for Dvk title, defaults to None
    :type title_search: str, optional
    :param title_exact: Whether to search for exact title or just if it is contained, defaults to False
    :type title_exact: bool, optional
    :param artist_search: Boolean search for Dvk artists, defaults to None
    :type artist_search: str, optional
    :param artist_exact: Whether to search for exact artists or just if it is contained, defaults to False
    :type artist_exact: bool, optional
    :param web_tag_search: Boolean search for Dvk web tags, defaults to None
    :type web_tag_search: str, optional
    :param web_tag_exact: Whether to search for exact web tags or just if it is contained, defaults to False
    :type web_tag_exact: bool, optional
    :param desc_search: Boolean search for Dvk description, defaults to None
    :type desc_search: str, optional
    :param desc_exact: Whether to search for exact description with HTML tags intact, defaults to False
    :type desc_exact: bool, optional
    :param url_search: Boolean search for Dvk page URL, defaults to None
    :type url_search: str, optional
    :param url_exact: Whether to search for exact page URL or just if it is contained, defaults to False
    :type url_exact: bool, optional
    """
    # Return empty list if dvk_handler is invalid
    if dvk_handler is None:
        return []
    # Get Dvk indexes
    indexes = []
    for i in range(0 , dvk_handler.get_size()):
        indexes.append(i)
    # Get logic statements
    title_logic = get_logic_from_string(title_search, not case_sensitive)
    artist_logic = get_logic_from_string(artist_search, not case_sensitive)
    artist_logic = add_escapes_to_logic(artist_logic, artist_exact)
    web_tag_logic = get_logic_from_string(web_tag_search, not case_sensitive)
    web_tag_logic = add_escapes_to_logic(web_tag_logic, web_tag_exact)
    url_logic = get_logic_from_string(url_search, not case_sensitive)
    desc_logic = get_logic_from_string(desc_search, not case_sensitive)
    if not desc_exact:
        desc_logic = add_escapes_to_logic(desc_logic, False)
    # Filter out dvks
    size = len(indexes)
    print("Searching for DVKs...")
    for index in tqdm(range(0, size)):
        dvk = dvk_handler.get_dvk(indexes[index])
        # Filter out Dvks by title
        if title_search is not None:
            title = dvk.get_title()
            if not case_sensitive:
                title = title.lower()
            if not search_string(title_logic, title, title_exact):
                indexes[index] = None
                continue
        # Filter out Dvks by artist
        if artist_search is not None:
            artists = []
            artists.extend(dvk.get_artists())
            if not case_sensitive:
                for i in range(0, len(artists)):
                    artists[i] = artists[i].lower()
            artist_str = "," + list_to_string(artists, True) + ","
            if not search_string(artist_logic, artist_str, False):
                indexes[index] = None
                continue 
        # Filter out Dvks by web tags
        if web_tag_search is not None:
            tags = []
            tags.extend(dvk.get_web_tags())
            if not case_sensitive:
                for i in range(0, len(tags)):
                    tags[i] = tags[i].lower()
            tag_str = "," + list_to_string(tags, True) + ","
            if not search_string(web_tag_logic, tag_str, False):
                indexes[index] = None
                continue 
        # Filter out Dvks by description
        if desc_search is not None:
            desc = dvk.get_description()
            if desc is not None:
                if not case_sensitive:
                    desc = desc.lower()
                if not desc_exact:
                    desc = remove_html_tags(desc)
            if not search_string(desc_logic, desc, False):
                indexes[index] = None
                continue
        # Filter out Dvks by page_url
        if url_search is not None:
            url = dvk.get_page_url()
            if not case_sensitive:
                url = url.lower()
            if not search_string(url_logic, url, url_exact):
                indexes[index] = None
                continue
    # Remove None indexes
    index = 0
    while index < len(indexes):
        if indexes[index] == None:
            del indexes[index]
            continue
        index += 1
    # Return indexes that are left
    return indexes

def main():
    """
    Sets up commands for getting DVKs with missing media.
    """
    # Set up ArgumentParser
    parser = ArgumentParser()
    parser.add_argument(
        "-p",
        "--path",
        help="Path in which to search for DVKs",
        nargs="?",
        type=str,
        default=str(getcwd()))
    parser.add_argument(
        "-c",
        "--case_sensitive",
        help="Indicates string searches should be case sensitive",
        action="store_true")
    parser.add_argument(
        "-t",
        "--title",
        metavar="TITLE",
        help="Boolean search for DVK titles",
        type=str,
        default=None)
    parser.add_argument(
        "-T",
        "--TITLE_EXACT",
        help="Indicates title search should be an exact match",
        action="store_true")
    parser.add_argument(
        "-a",
        "--artist",
        metavar="ARTIST",
        help="Boolean search for DVK artist(s)",
        type=str,
        default=None)
    parser.add_argument(
        "-A",
        "--ARTIST_LOOSE",
        help="Indicates artist string doesn't have to be an exact match",
        action="store_true")
    parser.add_argument(
        "-w",
        "--web_tag",
        metavar="TAG",
        help="Boolean search for DVK web tags",
        type=str,
        default=None)
    parser.add_argument(
        "-W",
        "--WEB_TAG_LOOSE",
        help="Indicates web tag doesn't have to be an exact match",
        action="store_true")
    parser.add_argument(
        "-d",
        "--description",
        metavar="DESC",
        help="Boolean search for DVK descriptions",
        type=str,
        default=None)
    parser.add_argument(
        "-D",
        "--DESCRIPTION_EXACT",
        help="Indicates description search should include HTML tags and info",
        action="store_true")
    parser.add_argument(
        "-u",
        "--url",
        metavar="URL",
        help="Boolean search for DVK page URLs",
        type=str,
        default=None)
    parser.add_argument(
        "-U",
        "--URL_EXACT",
        help="Indicates page URL search should be an exact match",
        action="store_true")
    args = parser.parse_args()
    # Check if the given directory exists
    full_directory = abspath(args.path)
    if (full_directory is not None
            and exists(full_directory)
            and isdir(full_directory)):
        # Load all DVK files in the directory
        dvk_handler = DvkHandler(full_directory)
        dvk_handler.sort_dvks("a")
        # Search for DVKs
        indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=args.case_sensitive,
                title_search=args.title,
                title_exact=args.TITLE_EXACT,
                artist_search=args.artist,
                artist_exact=not args.ARTIST_LOOSE,
                web_tag_search=args.web_tag,
                web_tag_exact=not args.WEB_TAG_LOOSE,
                desc_search=args.description,
                desc_exact=args.DESCRIPTION_EXACT,
                url_search=args.url,
                url_exact=args.URL_EXACT)
        # Print list of found dvks
        if len(indexes) > 0:
            print()
            color_print("MATCHING SEARCHES:", "g")
            for index in indexes:
                path = dvk_handler.get_dvk(index).get_dvk_file()
                print(truncate_path(full_directory, path))
        else:
            color_print("No matching DVKs found.", "r")
    else:
        color_print("Invalid directory", "r")

if __name__ == "__main__":
    main
