#!/usr/bin/env python3

from _functools import cmp_to_key
from argparse import ArgumentParser
from dvk_archive.main.color_print import color_print
from dvk_archive.main.file.dvk_handler import Dvk
from dvk_archive.main.file.dvk_handler import DvkHandler
from dvk_archive.main.processing.list_processing import clean_list
from dvk_archive.main.processing.string_compare import compare_alphanum
from dvk_archive.main.processing.string_processing import pad_num
from os import getcwd, pardir
from os.path import abspath, basename, exists, isdir, join
from tqdm import tqdm
from typing import List

def set_sequence_from_indexes(dvk_handler:DvkHandler=None,
                indexes:List[int]=[],
                seq_title:str=None):
    """
    Sets a group of Dvks as a sequence from DvkHandler indexes.

    :param dvk_handler: DvkHandler used to source Dvks, defaults to None
    :type dvk_handler: DvkHandler, optional
    :param indexes: Indexes of the Dvks to put in sequence, defaults to None
    :type indexes: list[int], optional
    :param seq_title: Sequence title for Dvk if desired, defaults to None
    :type seq_title: str, optional
    """
    if dvk_handler is not None and indexes is not None:
        # Get list of Dvks
        dvks = []
        for index in indexes:
            dvks.append(dvk_handler.get_dvk(index))
        # Set the sequence
        dvks = set_sequence(dvks, seq_title)
        # Set dvks in dvk_handler to thier new values
        for i in range(0, len(dvks)):
            dvk_handler.set_dvk(dvks[i], indexes[i])

def set_sequence(dvks:List[Dvk], seq_title:str=None) -> List[Dvk]:
    """
    Sets a group of Dvks as a sequence.

    :param dvks: List of Dvks to turn into a sequence, defaults to None
    :type dvks: list[Dvk] optional
    :param seq_title: Sequence title for Dvk if desired, defaults to None
    :type seq_title: str, optional
    :return: List of Dvks wit sequence data added
    :rtype: List[Dvk]
    """
    if dvks is None:
        return []
    sequenced = []
    sequenced.extend(dvks)
    total = len(sequenced)
    for i in range(0, total):
        # Get Dvk to edit from index
        edit_dvk = sequenced[i]
        # Set the previous ID
        if i == 0:
            # Set to first if first in the sequence
            edit_dvk.set_first()
        else:
            prev_dvk = sequenced[i-1]
            edit_dvk.set_prev_id(prev_dvk.get_dvk_id())
        # Set the next ID
        if i == len(sequenced) - 1:
            # Set to last if last in the sequence
            edit_dvk.set_last()
        else:
            next_dvk = sequenced[i+1]
            edit_dvk.set_next_id(next_dvk.get_dvk_id())
        # Set the sequence title
        if len(sequenced) > 1:
            edit_dvk.set_sequence_title(seq_title)
        else:
            edit_dvk.set_sequence_title()
        # Set the sequence number and total
        edit_dvk.set_sequence_total(total)
        edit_dvk.set_sequence_number(0)
        if total > 1:
            edit_dvk.set_sequence_number(i + 1)
        # Write Dvk and update the DvkHandler
        edit_dvk.write_dvk()
        sequenced[i] = edit_dvk
    return sequenced

def get_sequence(dvk_handler:DvkHandler=None, index:int=None) -> List[int]:
    """
    Gets a group of Dvks in a sequence from a given starting index.

    :param dvk_handler: DvkHandler to search through for Dvks, defaults to None
    :type dvk_handler: DvkHandler, optional
    :param index: Index of a Dvk in she sequence, defaults to None
    :type index: int, optional
    :return: List of indexes for the Dvks in the sequence
    :rtype: list[int]
    """
    try:
        # Get all Dvks from after the given index
        next_ids = []
        if index > -1:
            dvk = dvk_handler.get_dvk(index)
        while not dvk.is_last() and dvk.get_next_id() is not None:
            # Get next Dvk
            next_id = dvk.get_next_id()
            cur_index = dvk_handler.get_dvk_by_id(next_id)
            if cur_index == -1 or cur_index in next_ids:
                # Stop if Dvk doesn't exist or is already in sequence
                break
            next_ids.append(cur_index)
            dvk = dvk_handler.get_dvk(cur_index)
        # Get all Dvks from before the given index
        ids = []
        dvk = dvk_handler.get_dvk(index)
        while not dvk.is_first() and dvk.get_prev_id() is not None:
            # Get prev Dvk
            prev_id = dvk.get_prev_id()
            cur_index = dvk_handler.get_dvk_by_id(prev_id)
            if cur_index == -1 or cur_index in ids:
                # Stop if Dvk doesn't exist or is already in sequence
                break
            ids.append(cur_index)
            dvk = dvk_handler.get_dvk(cur_index)
        ids.reverse()
        # Combine lists of indexes
        ids.append(index)
        ids.extend(next_ids)
        return ids
    except:
        return []

def get_default_sequence_order(dvk_handler:DvkHandler=None, respect_seq:bool=True) -> List[Dvk]:
    """
    Returns a list of Dvks in the order they would be expected to be in a sequence.

    :param directory: DvkHandler with loaded Dvks, defaults to None
    :type directory: DvkHandler, optional
    :param respect_seq: Whether to keep order of existing sequence, defaults to True
    :type respect_seq: bool, optional
    :return: List of Dvks in the default sequence order
    :rtype: list[Dvk]
    """
    # Return empty list if parameters are invalid
    if dvk_handler is None:
        return []
    # Sort Dvks
    dvk_handler.sort_dvks("a")
    # Get list of parent directories
    size = dvk_handler.get_size()
    parents = []
    for i in range(0, size):
        parent = abspath(join(dvk_handler.get_dvk(i).get_dvk_file(), pardir))
        parents.append(str(parent))
    # Get list of unique parent directories
    directories = []
    directories.extend(parents)
    directories = clean_list(directories)
    comparator = cmp_to_key(compare_alphanum)
    directories = sorted(directories, key=comparator)
    # Add Dvks by directory
    indexes = []
    for directory in directories:
        for i in range(0, size):
            # Add Dvk if in the right directory
            if directory == parents[i]:
                indexes.append(i)
    # Get sequence order, if specified
    if respect_seq:
        new_indexes = []
        while len(indexes) > 0:
            # Add sequence to indexes
            seq = get_sequence(dvk_handler, indexes[0])
            if len(seq) > 1:
                seq.extend(new_indexes)
                new_indexes = []
            new_indexes.extend(seq)
            # Remove sequence from existing indexes
            for index in seq:
                try:
                    del_num = indexes.index(index)
                    del indexes[del_num]
                except ValueError:
                    continue
        indexes = new_indexes
    # Convert Indexes to List of Dvks
    dvks = []
    for index in indexes:
        dvks.append(dvk_handler.get_dvk(index))
    # Return list of Dvks
    return dvks  

def remove_sequence_info(dvks:List[Dvk]=None) -> List[Dvk]:
    """
    Removes all sequence information from a given list of Dvks.

    :param dvks: List of Dvk to remove sequence info from, defaults to None
    :type dvks: List[Dvk], optional
    :return: Given list of Dvks with all the sequence data removed
    :rtype: List[Dvk]
    """
    try:
        removed = []
        removed.extend(dvks)
        for i in range(0, len(removed)):
            # Remove all sequence information
            removed[i].set_prev_id()
            removed[i].set_next_id()
            removed[i].set_sequence_number()
            removed[i].set_sequence_total()
            removed[i].set_sequence_title()
            removed[i].set_section_title()
            removed[i].write_dvk()
        return removed
    except (AttributeError, TypeError):
        return []

def separate_into_sections(dvk_handler:DvkHandler=None, respect_seq:bool=True, keep_existing:bool=True) -> List[List[Dvk]]:
    """
    Groups Dvks from a DvkHandler into sequence sections.
    Each list item starts with a bool showing whether to keep a section's existing title.
    The rest of each list item contains the Dvks of the given section.

    :param dvk_handler: DvkHandler containing Dvks, defaults to None
    :type dvk_handler: DvkHandler, optional
    :param respect_seq: Whether to keep order of existing sequence when getting default Dvk order, defaults to True
    :type respect_seq: bool, optional
    :param keep_existing: Whether to keep existing section titles, defaults to True
    :type keep_existing: bool, optional
    :return: List of Dvks grouped into sections along with whether section titles should be kept
    :rtype: List[List[Dvk]]
    """
    # Gets the default sequence order
    dvks = get_default_sequence_order(dvk_handler, respect_seq)
    # Return empty list if no dvks were found
    if len(dvks) == 0:
        return []
    # Separate Dvks into sections based on their parent directory
    path = abspath(join(dvks[0].get_dvk_file(), pardir))
    group = [False]
    sections = []
    for dvk in dvks:
        # Check if parent matches the path of the last
        parent = abspath(join(dvk.get_dvk_file(), pardir))
        if not path == parent:
            # Start a new group
            sections.append(group)
            group = [False, dvk]
        else:
            # Add dvk to the current group
            group.append(dvk)
        path = parent
    sections.append(group)
    # Check if sections contain section titles if section titles are to be kept
    if keep_existing and len(sections) > 1:
        for sec_num in range(0, len(sections)):
            keep_section = True
            for i in range(1, len(sections[sec_num])):
                if sections[sec_num][i].get_section_title() is None:
                    keep_section = False
                    break
            sections[sec_num][0] = keep_section
    # Return section groups
    return sections

def user_create_standalone(directory:str=None) -> bool:
    """
    Allows the user to set all the DVKs from a given directory as standalone media.

    :param directory: Directory in which to create the Dvk sequence, defaults to None
    :type directory: str, optional
    :return: Whether or not writing standalone sequence info was successful
    :rtype: bool
    """
    # Get Dvks and sort them alphabetimally
    dvk_handler = DvkHandler(directory)
    dvk_handler.sort_dvks("a")
    # Print List of Dvks
    size = dvk_handler.get_size()
    for i in range(0, size):
        print(dvk_handler.get_dvk(i).get_title())
    # Ask user if all the listed files should be listed as sequence singles
    print()
    response = str(input("Set all listed DVKs as single? (Y/N): ")).upper()
    # Add single sequence info if requested
    if response == "Y":
        print("Setting sequence info:")
        for i in tqdm(range(0, size)):
            # Remove existing sequenc info from the Dvk
            dvk = dvk_handler.get_dvk(i)
            dvks = remove_sequence_info([dvk])
            # Set Dvk as a standalone media file
            dvks = set_sequence(dvks)
            # Rename file
            parent = abspath(join(abspath(dvk.get_dvk_file()), pardir))
            dvk.rename_files(dvk.get_filename(parent, False), dvk.get_filename(parent, True))
        color_print("Finished writing sequence data!", "g")
        return True
    return False

def user_create_sequence(directory:str=None, respect_seq:bool=True, keep_sections:bool=True) -> bool:
    """
    Allows the user to create a sequence out of the Dvks from a given directory.

    :param directory: Directory in which to create the Dvk sequence, defaults to None
    :type directory: str, optional
    :param keep_sections: Whether to keep the existing section titles of Dvks, defaults to True
    :type respect_seq: bool, optional
    :param keep_existing: Whether to keep existing section titles, defaults to True
    :type keep_sections:bool, optional
    :return: Whether or not creating the sequence was successful
    :rtype: bool
    """
    # Get Dvks separated into sections based on directory
    dvk_handler = DvkHandler(directory)
    sections = separate_into_sections(dvk_handler, respect_seq, keep_sections)
    # Return False if no sections were found
    if len(sections) == 0:
        return False
    # Get Dvks and print them in order
    dvks = []
    for section in sections:
        for i in range(1, len(section)):
            dvks.append(section[i])
            print(section[i].get_title())
    # Get sequence title from the user
    write_sequence = True
    print()
    seq_title = str(input("Sequence Title (q to cancel): "))
    if seq_title == "q":
        return False
    # Get section titles
    section_titles = [None]
    if len(sections) > 1:
        section_titles = []
        for section in sections:
            sec_title = None
            if not section[0]:
                # Only ask the user for a section title if needed
                path = abspath(join(section[1].get_dvk_file(), pardir))
                show = "Section Title for: " + basename(path) + " (q to cancel):"
                sec_title = str(input(show))
                if sec_title == "q":
                    return False
            # Add section title to the list of titles
            section_titles.append(sec_title)
    # Set section titles and create dvk list
    dvks = []
    for sec_num in range(0, len(sections)):
        group = []
        for i in range(1, len(sections[sec_num])):
            group.append(sections[sec_num][i])
        if not sections[sec_num][0]:
            for i in range(0, len(group)):
                group[i].set_section_title(section_titles[sec_num])
        dvks.extend(group)
    # Set sequence
    dvks = set_sequence(dvks, seq_title)
    # Renmame files
    for dvk in dvks:
        parent = abspath(join(abspath(dvk.get_dvk_file()), pardir))
        dvk.rename_files(dvk.get_filename(parent, False), dvk.get_filename(parent, True))
    color_print("Finished writing sequence!", "g")
    return True

def main():
    """
    Sets up commands for adding sequence data to DVK files.
    """
    parser = ArgumentParser()
    parser.add_argument(
            "directory",
            help="Directory in which to search for DVKs with missing linked media.",
            nargs="?",
            type=str,
            default=str(getcwd()))
    parser.add_argument(
                "-s",
                "--standalone",
                help="DVKs will be set as standalone media files not part of a sequence.",
                action="store_true")
    parser.add_argument(
                "-o",
                "--overwrite",
                help="Whether to overwrite section titles or keep existing ones.",
                action="store_true")
    parser.add_argument(
                "-i",
                "--ignore",
                help="Whether to ignore existing sequence info.",
                action="store_true")
    args = parser.parse_args()
    full_directory = abspath(args.directory)
    # Check if directory exists
    if (full_directory is not None
                and exists(full_directory)
                and isdir(full_directory)):
        if not args.standalone:
            user_create_sequence(full_directory, not args.ignore, not args.overwrite)
        else:
            user_create_standalone(full_directory)
    else:
        color_print("Invalid directory", "r")

if __name__ == "__main__":
    main()

