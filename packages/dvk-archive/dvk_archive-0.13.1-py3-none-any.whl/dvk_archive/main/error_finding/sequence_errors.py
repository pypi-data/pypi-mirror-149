#!/usr/bin/env python3

from argparse import ArgumentParser
from dvk_archive.main.color_print import color_print
from dvk_archive.main.file.dvk import Dvk
from dvk_archive.main.file.dvk_handler import DvkHandler
from dvk_archive.main.file.sequencing import get_sequence
from dvk_archive.main.file.sequencing import remove_sequence_info
from dvk_archive.main.processing.list_processing import clean_list
from dvk_archive.main.processing.string_processing import truncate_path
from os import getcwd
from os.path import abspath, exists, isdir
from tqdm import tqdm
from typing import List

def is_invalid_single(dvk_handler:DvkHandler=None,
            seq_indexes:List[int]=None) -> bool:
    """
    Returns whether sequence with only a single Dvk is valid.

    :param dvk_handler: DvkHandler holding Dvks, defaults to None
    :type dvk_handler: DvkHandler, optional
    :param seq_indexes: Indexes of Dvks forming a sequence, defaults to None
    :type seq_indexes: list[int], optional
    :return: Whether sequence single is invalid
    :rtype: bool
    """
    # Return False if parameters are invalid
    if dvk_handler is None or seq_indexes is None or not len(seq_indexes) == 1:
        return False
    # Check if single file sequence is valid
    dvk = dvk_handler.get_dvk(seq_indexes[0])
    if ((dvk.is_first() and dvk.is_last())
            or (dvk.get_prev_id() is None and dvk.get_next_id() is None)):
        return False
    return True

def contains_invalid_sequence_number(dvk_handler:DvkHandler=None,
            seq_indexes:List[int]=None) -> bool:
    """
    Returns whether any Dvk in a given sequence has an invalid sequence number or total.

    :param dvk_handler: DvkHandler holding Dvks, defaults to None
    :type dvk_handler: DvkHandler, optional
    :param seq_indexes: Indexes of Dvks forming a sequence, defaults to None
    :type seq_indexes: list[int], optional
    :return: Whether sequence numbers or totals are invalid
    :rtype: bool
    """
    # Return False if parameters are invalid
    if dvk_handler is None or seq_indexes is None or len(seq_indexes) < 2:
        return False
    # Run through sequence indexes
    total = len(seq_indexes)
    try:
        for i in range(0, total):
            dvk = dvk_handler.get_dvk(seq_indexes[i])
            # Check if sequence total is correct
            if not dvk.get_sequence_total() == total:
                return True
            # Check if sequence number is correct
            if not dvk.get_sequence_number() == (i + 1):
                return True
        # Return False if no errors were found
        return False
    except IndexError:
        return False

def contains_invalid_prev_next(dvk_handler:DvkHandler=None,
            seq_indexes:List[int]=None) -> bool:
    """
    Returns whether any Dvk in a sequence has an invalid prev_id or next_id.

    :param dvk_handler: DvkHandler holding Dvks, defaults to None
    :type dvk_handler: DvkHandler, optional
    :param seq_indexes: Indexes of Dvks forming a sequence, defaults to None
    :type seq_indexes: list[int], optional
    :return: Whether prev_ids and next_ids are invalid
    :rtype: bool
    """
    # Return False if parameters are invalid
    if seq_indexes is None or len(seq_indexes) < 2 or dvk_handler is None:
        return False
    try:
        # Check previous ids
        total = len(seq_indexes)
        for i in range(1, total):
            dvk = dvk_handler.get_dvk(seq_indexes[i])
            prev_dvk = dvk_handler.get_dvk(seq_indexes[i-1])
            if not dvk.get_prev_id() == prev_dvk.get_dvk_id():
                return True
        # Check next ids
        for i in range(0, total-1):
            dvk = dvk_handler.get_dvk(seq_indexes[i])
            next_dvk = dvk_handler.get_dvk(seq_indexes[i+1])
            if not dvk.get_next_id() == next_dvk.get_dvk_id():
                return True
        # Returns False if no errors were found
        return False
    except IndexError:
        return False
def contains_invalid_start_end(dvk_handler:DvkHandler=None,
            seq_indexes:List[int]=None) -> bool:
    """
    Returns whether a sequence is invalid due to missing start and end tags.

    :param dvk_handler: DvkHandler holding Dvks, defaults to None
    :type dvk_handler: DvkHandler, optional
    :param seq_indexes: Indexes of Dvks forming a sequence, defaults to None
    :type seq_indexes: list[int], optional
    :return: Whether start and end Dvks are invalid
    :rtype: bool
    """
    # Return false if parameters are invalid
    if seq_indexes is None or len(seq_indexes) < 2 or dvk_handler is None:
        return False
    try:
        # Check if first Dvk in sequence is correctly labeled
        if not dvk_handler.get_dvk(seq_indexes[0]).is_first():
            return True
        # Check if last Dvk in sequence is correctly labeled
        if not dvk_handler.get_dvk(seq_indexes[len(seq_indexes)-1]).is_last():
            return True
        # Return False if no errors were found
        return False
    except IndexError:
        return False
    
def get_sequence_errors(directory:str=None) -> List[List[str]]:
    """
    Gets a list of DVK files with sequence errors in a given directory.

    :param directory: Directory in which to search for errors, defaults to None
    :type directory: str, optional
    :return: List of DVK paths grouped by sequence with sequence errors
    :rtype: list[list[str]]
    """
    # Return empty list if directory is invalid
    if directory is None or not exists(directory) or not isdir(directory):
        return []
    # Read Dvks for the given directory
    dvk_handler = DvkHandler(directory)
    dvk_handler.sort_dvks("a")
    # Run through all the dvks in the DvkHandler
    error_indexes = []
    checked_indexes = []
    size = dvk_handler.get_size()
    print("Finding sequence errors:")
    for index in tqdm(range(0, size)):
        # Only check Dvk if not alreadiy in checked list.
        if not index in checked_indexes:
            # Get sequence, then add to checked indexes
            seq = get_sequence(dvk_handler, index)
            checked_indexes.extend(seq)
            # Check if sequence is invalid
            if (is_invalid_single(dvk_handler, seq) 
                        or contains_invalid_start_end(dvk_handler, seq)
                        or contains_invalid_sequence_number(dvk_handler, seq)
                        or contains_invalid_prev_next(dvk_handler, seq)):
                error_indexes.append(seq)
    # Get paths for the Dvks with sequence errors
    error_paths = []
    for seq in error_indexes:
        path_group = []
        for index in seq:
            path_group.append(dvk_handler.get_dvk(index).get_dvk_file())
        error_paths.append(clean_list(path_group))
    return error_paths

def main():
    """
    Sets up commands for finding sequence errors.
    """
    parser = ArgumentParser()
    parser.add_argument(
            "directory",
            help="Directory in which to search for broken DVK sequences",
            nargs="?",
            type=str,
            default=str(getcwd()))
    parser.add_argument(
                "-r",
                "--remove",
                help="Removes sequence info from broken sequences without asking",
                action="store_true")
    args = parser.parse_args()
    full_directory = abspath(args.directory)
    remove_all = args.remove
    # Check if directory exists
    if (full_directory is not None
            and exists(full_directory)
            and isdir(full_directory)):
        # Get list of sequence errors
        errors = get_sequence_errors(full_directory)
        # Print list
        if len(errors) > 0:
            for group in errors:
                # Print group
                dvk = Dvk(group[0])
                print()
                color_print("SEQUENCE: " + str(dvk.get_sequence_title()), "r")
                for item in group:
                    print(truncate_path(full_directory, item))
                # Ask if sequence info should be deleted
                delete = remove_all
                if not remove_all:
                    answer = str(input("Delete sequence info? [y/n]: ")).lower()
                    delete = (answer == "y")
                # Remove sequence info is specified
                if delete:
                    dvks = []
                    for item in group:
                        dvk = Dvk(item)
                        dvks.append(dvk)
                    remove_sequence_info(dvks)
                    color_print("Sequence data removed.", "g")
        else:
            color_print("No sequence errors found.", "g")
    else:
        color_print("Invalid directory", "r")

if __name__ == "__main__":
    main()
