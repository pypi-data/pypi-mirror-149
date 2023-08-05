#!/usr/bin/env python3

from argparse import ArgumentParser
from dvk_archive.main.color_print import color_print
from dvk_archive.main.file.dvk_handler import DvkHandler
from dvk_archive.main.processing.string_processing import truncate_path
from os import getcwd
from os.path import abspath, exists, isdir
from tqdm import tqdm
from typing import List

def get_missing_sequence_info(directory:str=None) -> List[str]:
    """
    Returns list of Dvks that are missing prev_id or next_id values.

    :param directory: Directory in which to search, defaults to None
    :type directory: str, optional
    :return: List of paths of DVK files with missing sequence info
    :rtype: list[str]
    """
    # Return empty list if directory is invalid
    if directory is None or not exists(directory) or not isdir(directory):
        return []
    # Read Dvks for the given directory
    dvk_handler = DvkHandler(directory)
    dvk_handler.sort_dvks("a")
    # Check each dvk to see if they are missing sequence info
    missing = []
    size = dvk_handler.get_size()
    print("Finding DVKs with missing sequence info:")
    for dvk_num in tqdm(range(0, size)):
        dvk = dvk_handler.get_dvk(dvk_num)
        # Add DVK file path to missing list if sequence info is missing
        if dvk.get_prev_id() is None or dvk.get_next_id() is None:
            missing.append(dvk.get_dvk_file())
    # Return list of DVK files with missing sequence info
    return missing

def main():
    """
    Sets up commands for getting DVKs with missing sequence info.
    """
    parser = ArgumentParser()
    parser.add_argument(
            "directory",
            help="Directory in which to search for DVKs with missing sequence info.",
            nargs="?",
            type=str,
            default=str(getcwd()))
    args = parser.parse_args()
    full_directory = abspath(args.directory)
    # Check if directory exists
    if (full_directory is not None
            and exists(full_directory)
            and isdir(full_directory)):
        # Get list of dvks with missing sequence info
        missing = get_missing_sequence_info(full_directory)
        # Print list
        if len(missing) > 0:
            print()
            color_print("MISSING SEQUENCE INFO:", "r")
            for item in missing:
                print(truncate_path(full_directory, item))
        else:
            color_print("No DVKs with missing sequence info found.", "g")
    else:
        color_print("Invalid directory", "r")

if __name__ == "__main__":
    main()
