#!/usr/bin/env python3

from argparse import ArgumentParser
from dvk_archive.main.color_print import color_print
from dvk_archive.main.file.dvk import Dvk
from dvk_archive.main.file.rename import rename_directory
from dvk_archive.main.processing.string_processing import get_filename
from dvk_archive.main.processing.string_processing import remove_whitespace
from os import getcwd, listdir, pardir, remove
from os.path import abspath, basename, exists, isdir, join
from traceback import print_exc
from tqdm import tqdm
from typing import List
from re import findall

def read_file_as_lines(file:str=None) -> List[str]:
    """
    Reads a given text file and separates lines into separate list entries.

    :param file: Text file to read, defaults to None
    :type file: str, optional
    :return: List of lines in the given text file
    :rtype: str
    """
    try:
        # Read text file
        with open(file) as f:
            contents = f.read()
        # Separate into separate lines.
        regex = "^[^\\n\\r]+(?=[\\n\\r]+)"\
                    +"|(?<=[\\n\\r])[^\\n\\r]+(?=[\\n\\r]+)"\
                    +"|^[^\\n\\r]+$"\
                    +"|(?<=[\\n\\r])[^\\n\\r]+$"
        lines = findall(regex, contents)
        # Return lines
        return lines
    except (FileNotFoundError, TypeError):
        return []

def get_data_dvk(file:str=None, parent_dvk:Dvk=Dvk()) -> Dvk:
    """
    Turns user created media data file into a Dvk containing the same data.

    :param file: Text file with media info, defaults to None
    :type file: str, optional
    :param parent_dvk: Dvk to fill in gaps in media info that's absent in file, defaults to None
    :type parent_dvk: Dvk, optional
    :return: Dvk with media info
    :rtype: Dvk
    """
    try:
        # Use parameters from the parent Dvk
        data_dvk = Dvk()
        data_dvk.set_dvk_file(file)
        data_dvk.set_dvk_id(parent_dvk.get_dvk_id())
        data_dvk.set_artists(parent_dvk.get_artists())
        data_dvk.set_time(parent_dvk.get_time())
        data_dvk.set_web_tags(parent_dvk.get_web_tags())
        data_dvk.set_description(parent_dvk.get_description())
        data_dvk.set_page_url(parent_dvk.get_page_url())
        data_dvk.set_direct_url(parent_dvk.get_direct_url())
    except (AttributeError, TypeError):
        return Dvk()
    # Get lines from the data file
    lines = read_file_as_lines(file)
    # Run through all lines
    for line in lines:
        lower = line.lower()
        if not len(findall("^dvk_id\\||^id\\||i\\|", lower)) == 0:
            # Get dvk ID
            data_dvk.set_dvk_id(line[line.find("|")+1:])
        elif not len(findall("^artists?\\||^a\\|", lower)) == 0:
            # Get artists
            data_dvk.set_artists(line[line.find("|")+1:].split(","))
        elif not len(findall("^time\\||^published\\||^time_published\\||^p\\|", lower)) == 0:
            # Get time published
            time = line[line.find("|")+1:]
            data_dvk.set_time(time)
            if data_dvk.get_time() == "0000/00/00|00:00":
                data_dvk.set_time(f"{time}|00:00")
        elif not len(findall("^web_tags\\||^tags\\||^t\\|", lower)) == 0:
            # Get web tags
            data_dvk.set_web_tags(line[line.find("|")+1:].split(","))
        elif not len(findall("^d\\||^description\\|", lower)) == 0:
            # Get description
            data_dvk.set_description(line[line.find("|")+1:])
        elif not len(findall("^page\\||^url\\||^page_url\\||^u\\|", lower)) == 0:
            # Get page URL
            data_dvk.set_page_url(remove_whitespace(line[line.find("|")+1:]))
        elif not len(findall("^direct_url\\||^media_url\\||^direct\\||^media\\||^m\\|", lower)) == 0:
            # Get direct URL
            data_dvk.set_direct_url(remove_whitespace(line[line.find("|")+1:]))
    # Return the data Dvk
    return data_dvk

def create_dvks(data_dvk:Dvk=None) -> List[Dvk]:
    """
    Creates Dvks for files in directory of the given data_dvk.
    Uses data_dvk for info about the media.

    :param data_dvk: Dvk to use media info from, defaults to None
    :type data_dvk: Dvk, optional
    :return: List of Dvks for all the files in the directory
    :rtype: list[Dvk]
    """
    try:
        # Get list of files in the Dvk's directory
        parent = abspath(join(data_dvk.get_dvk_file(), pardir))
        files = listdir(parent)
        files.sort()
        try:
            del files[files.index(basename(data_dvk.get_dvk_file()))]
        except ValueError: pass
    except AttributeError:
        print_exc()
        return []
    try:
        # Create dvks for each file
        dvks = []
        for file in files:
            # Skip if file is a directory
            if isdir(abspath(join(parent, file))):
                continue
            # Get title for the Dvk based on the filename
            dvk = Dvk()
            dvk.set_title(findall(".+(?=\\.[A-Za-z0-9]{1,5}$)|^.+$", file)[0])
            # Set the Dvk ID
            dvk.set_dvk_id(data_dvk.get_dvk_id() + get_filename(dvk.get_title().replace(" ","-")))
            # Set info inherited from the data_dvk
            dvk.set_artists(data_dvk.get_artists())
            dvk.set_time(data_dvk.get_time())
            dvk.set_web_tags(data_dvk.get_web_tags())
            dvk.set_description(data_dvk.get_description())
            dvk.set_page_url(data_dvk.get_page_url())
            dvk.set_direct_url(data_dvk.get_direct_url())
            # Set the Dvk and media filenames
            filename = dvk.get_filename(parent)
            dvk.set_dvk_file(join(parent, filename + ".dvk"))
            dvk.set_media_file(file)
            # Write dvk and add to list of Dvks
            dvk.write_dvk()
            dvks.append(dvk)
        # Delete data file
        try:
            remove(data_dvk.get_dvk_file())
        except FileNotFoundError: pass
        # Return list of Dvks
        return dvks
    except TypeError:
        print_exc()
        return []

def get_data_dvks(directory:str=None, base_dvk:Dvk=Dvk()) -> List[Dvk]:
    """
    Gets a list of data Dvks for every subdirectory in the given directory.
    Uses data from text files named dvk_data in each directory.

    :param directory: Directory in which to look for dvk_data.txt files, defaults to None
    :type directory: str, optional
    :param base_dvk: Parent Dvk with info to fill in gaps in text info, defaults to Dvk()
    :type base_dvk: Dvk, optional
    :return: List of data Dvks for evvery subdirectory
    :rytpe: list[Dvk]
    """
    try:
        # Get Dvk data text file for the current directory
        main_dir = abspath(directory)
        data_dvk = get_data_dvk(abspath(join(main_dir, "dvk_data.txt")), base_dvk)
        data_dvks = [data_dvk]
        # Get list of files in the given directory
        files = listdir(main_dir)
        files.sort()
        # Get subdirectories
        for filename in files:
            file = abspath(join(main_dir, filename))
            if isdir(file):
                # Get data dvks for the subdirectory
                data_dvks.extend(get_data_dvks(file, data_dvk))
        # Return the list of data Dvks
        return data_dvks
    except (FileNotFoundError, TypeError):
        return []

def main():
    """
    Argument parser for manually creating Dvks.
    """
    parser = ArgumentParser()
    parser.add_argument(
            "directory",
            help="Directory in which to create Dvks",
            nargs="?",
            type=str,
            default=str(getcwd()))
    args = parser.parse_args()
    full_directory = abspath(args.directory)
    # Check if directory exists
    if (full_directory is not None
            and exists(full_directory)
            and isdir(full_directory)):
        # Create Dvks
        print("Creating Dvks...")
        data_dvks = get_data_dvks(full_directory, Dvk())
        for data_dvk in tqdm(data_dvks):
            create_dvks(data_dvk)
        # Rename files
        rename_directory(full_directory)
    else:
        color_print("Invalid directory", "r")

if __name__ == "__main__":
    main()
