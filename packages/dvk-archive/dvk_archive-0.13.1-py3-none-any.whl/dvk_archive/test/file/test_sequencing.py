#!/usr/bin/env python3

from dvk_archive.main.file.dvk import Dvk
from dvk_archive.main.file.dvk_handler import DvkHandler
from dvk_archive.main.file.sequencing import get_default_sequence_order
from dvk_archive.main.file.sequencing import get_sequence
from dvk_archive.main.file.sequencing import remove_sequence_info
from dvk_archive.main.file.sequencing import separate_into_sections
from dvk_archive.main.file.sequencing import set_sequence
from dvk_archive.main.file.sequencing import set_sequence_from_indexes
from dvk_archive.test.temp_dir import get_test_dir
from os import mkdir
from os.path import abspath, exists, join

def create_test_dvks() -> str:
    """
    Creates test DVK files for running sequencing tests.

    :return: Temp directory that DVK files are stored in
    :rtype: str
    """
    test_dir = get_test_dir()
    # Create unrelated single Dvk
    single = Dvk()
    single.set_dvk_file(join(test_dir, "single.dvk"))
    single.set_dvk_id("SNG01")
    single.set_title("Single")
    single.set_artist("Artist")
    single.set_page_url("/url/")
    single.set_media_file("media.txt")
    single.write_dvk()
    assert exists(single.get_dvk_file())
    # Create pair of Dvks to link as a sequence
    couple = Dvk()
    couple.set_dvk_file(join(test_dir,"couple1.dvk"))
    couple.set_dvk_id("CPL01")
    couple.set_title("Couple P1")
    couple.set_artist("Artist")
    couple.set_page_url("/url/")
    couple.set_media_file("media.jpg")
    couple.write_dvk()
    assert exists(couple.get_dvk_file())
    couple.set_dvk_file(join(test_dir,"couple2.dvk"))
    couple.set_dvk_id("CPL02")
    couple.set_title("Couple P2")
    couple.set_media_file("media.jpg")
    couple.write_dvk()
    assert exists(couple.get_dvk_file())
    # Create group of 3 Dvks to link as a sequence
    triple = Dvk()
    triple.set_dvk_file(join(test_dir,"triple1.dvk"))
    triple.set_dvk_id("TRI01")
    triple.set_title("Triple P1")
    triple.set_artist("Artist")
    triple.set_page_url("/url/")
    triple.set_media_file("media.png")
    triple.write_dvk()
    assert exists(triple.get_dvk_file())
    triple.set_dvk_file(join(test_dir,"triple2.dvk"))
    triple.set_dvk_id("TRI02")
    triple.set_title("Triple P2")
    triple.set_media_file("media.png")
    triple.write_dvk()
    assert exists(triple.get_dvk_file())
    triple.set_dvk_file(join(test_dir,"triple3.dvk"))
    triple.set_dvk_id("TRI03")
    triple.set_title("Triple P3")
    triple.set_media_file("media.png")
    triple.write_dvk()
    assert exists(triple.get_dvk_file())
    # Test that Dvks were written properly
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    assert dvk_handler.get_size() == 6
    assert dvk_handler.get_dvk(0).get_dvk_id() == "CPL01"
    assert dvk_handler.get_dvk(1).get_dvk_id() == "CPL02"
    assert dvk_handler.get_dvk(2).get_dvk_id() == "SNG01"
    assert dvk_handler.get_dvk(3).get_dvk_id() == "TRI01"
    assert dvk_handler.get_dvk(4).get_dvk_id() == "TRI02"
    assert dvk_handler.get_dvk(5).get_dvk_id() == "TRI03"
    return test_dir

def test_set_sequence():
    # Set up test files
    test_dir = create_test_dvks()
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    assert dvk_handler.get_size() == 6
    dvk0 = dvk_handler.get_dvk(0)
    dvk1 = dvk_handler.get_dvk(1)
    dvk2 = dvk_handler.get_dvk(2)
    dvk3 = dvk_handler.get_dvk(3)
    dvk4 = dvk_handler.get_dvk(4)
    dvk5 = dvk_handler.get_dvk(5)
    # Test setting a sequence
    dvks = [dvk0, dvk1]
    seq_dvks = set_sequence(dvks)
    assert seq_dvks[0].get_dvk_id() == "CPL01"
    assert seq_dvks[0].is_first()
    assert seq_dvks[0].get_next_id() == "CPL02"
    assert seq_dvks[0].get_sequence_title() is None
    assert seq_dvks[0].get_sequence_number() == 1
    assert seq_dvks[0].get_sequence_total() == 2
    assert seq_dvks[1].get_dvk_id() == "CPL02"
    assert seq_dvks[1].is_last()
    assert seq_dvks[1].get_prev_id() == "CPL01"
    assert seq_dvks[1].get_sequence_title() is None
    assert seq_dvks[1].get_sequence_number() == 2
    assert seq_dvks[1].get_sequence_total() == 2
    # Test setting a sequence with sequence title
    dvks = [dvk3, dvk4, dvk5]
    seq_dvks = set_sequence(dvks, "Title!")
    assert len(seq_dvks) == 3
    assert seq_dvks[0].get_dvk_id() == "TRI01"
    assert seq_dvks[0].is_first()
    assert seq_dvks[0].get_next_id() == "TRI02"
    assert seq_dvks[0].get_sequence_title() == "Title!"
    assert seq_dvks[0].get_sequence_number() == 1
    assert seq_dvks[0].get_sequence_total() == 3
    assert seq_dvks[1].get_dvk_id() == "TRI02"
    assert seq_dvks[1].get_prev_id() == "TRI01"
    assert seq_dvks[1].get_next_id() == "TRI03"
    assert seq_dvks[1].get_sequence_title() == "Title!"
    assert seq_dvks[1].get_sequence_number() == 2
    assert seq_dvks[1].get_sequence_total() == 3    
    assert seq_dvks[2].get_dvk_id() == "TRI03"
    assert seq_dvks[2].is_last()
    assert seq_dvks[2].get_prev_id() == "TRI02"
    assert seq_dvks[2].get_sequence_title() == "Title!"
    assert seq_dvks[2].get_sequence_number() == 3
    assert seq_dvks[2].get_sequence_total() == 3
    # Test setting a single standalone Dvk file
    dvks = [dvk2]
    seq_dvks = set_sequence(dvks, "Other")
    assert seq_dvks[0].get_dvk_id() == "SNG01"
    assert seq_dvks[0].is_first()
    assert seq_dvks[0].is_last()
    assert seq_dvks[0].get_sequence_title() is None
    assert seq_dvks[0].get_sequence_number() == 0
    assert seq_dvks[0].get_sequence_total() == 1
    # Test that sequence data was written to disk
    dvk_handler = None
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    assert dvk_handler.get_dvk(0).get_next_id() == "CPL02"
    assert dvk_handler.get_dvk(1).get_prev_id() == "CPL01"
    assert dvk_handler.get_dvk(2).is_first()
    assert dvk_handler.get_dvk(3).get_next_id() == "TRI02"
    assert dvk_handler.get_dvk(3).get_sequence_number() == 1
    assert dvk_handler.get_dvk(4).get_next_id() == "TRI03"
    assert dvk_handler.get_dvk(4).get_sequence_number() == 2
    assert dvk_handler.get_dvk(5).get_prev_id() == "TRI02"
    assert dvk_handler.get_dvk(5).get_sequence_number() == 3
    # Test setting a sequence with invalid parameters
    assert set_sequence([]) == []
    assert set_sequence(None) == []
    dvk_handler = None
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    assert dvk_handler.get_dvk(0).get_next_id() == "CPL02"
    assert dvk_handler.get_dvk(1).get_prev_id() == "CPL01"
    assert dvk_handler.get_dvk(2).is_first()
    assert dvk_handler.get_dvk(3).get_next_id() == "TRI02"
    assert dvk_handler.get_dvk(4).get_next_id() == "TRI03"
    assert dvk_handler.get_dvk(5).get_prev_id() == "TRI02"

def test_set_sequence_from_indexes():
    """
    Tests the set_sequence function.
    """
    # Set up test files
    test_dir = create_test_dvks()
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    assert dvk_handler.get_size() == 6
    # Test setting a sequence
    set_sequence_from_indexes(dvk_handler, [0,1])
    assert dvk_handler.get_dvk(0).get_dvk_id() == "CPL01"
    assert dvk_handler.get_dvk(0).is_first()
    assert dvk_handler.get_dvk(0).get_next_id() == "CPL02"
    assert dvk_handler.get_dvk(0).get_sequence_title() is None
    assert dvk_handler.get_dvk(0).get_sequence_number() == 1
    assert dvk_handler.get_dvk(0).get_sequence_total() == 2
    assert dvk_handler.get_dvk(1).get_dvk_id() == "CPL02"
    assert dvk_handler.get_dvk(1).is_last()
    assert dvk_handler.get_dvk(1).get_prev_id() == "CPL01"
    assert dvk_handler.get_dvk(1).get_sequence_title() is None
    assert dvk_handler.get_dvk(1).get_sequence_number() == 2
    assert dvk_handler.get_dvk(1).get_sequence_total() == 2
    # Test setting a sequence with sequence title
    set_sequence_from_indexes(dvk_handler, [3,4,5], "Title!")
    assert dvk_handler.get_dvk(3).get_dvk_id() == "TRI01"
    assert dvk_handler.get_dvk(3).is_first()
    assert dvk_handler.get_dvk(3).get_next_id() == "TRI02"
    assert dvk_handler.get_dvk(3).get_sequence_title() == "Title!"
    assert dvk_handler.get_dvk(3).get_sequence_number() == 1
    assert dvk_handler.get_dvk(3).get_sequence_total() == 3
    assert dvk_handler.get_dvk(4).get_dvk_id() == "TRI02"
    assert dvk_handler.get_dvk(4).get_prev_id() == "TRI01"
    assert dvk_handler.get_dvk(4).get_next_id() == "TRI03"
    assert dvk_handler.get_dvk(4).get_sequence_title() == "Title!"
    assert dvk_handler.get_dvk(4).get_sequence_number() == 2
    assert dvk_handler.get_dvk(4).get_sequence_total() == 3
    assert dvk_handler.get_dvk(5).get_dvk_id() == "TRI03"
    assert dvk_handler.get_dvk(5).is_last()
    assert dvk_handler.get_dvk(5).get_prev_id() == "TRI02"
    assert dvk_handler.get_dvk(5).get_sequence_title() == "Title!"
    assert dvk_handler.get_dvk(5).get_sequence_number() == 3
    assert dvk_handler.get_dvk(5).get_sequence_total() == 3
    # Test setting a single standalone Dvk file
    set_sequence_from_indexes(dvk_handler, [2], "Other")
    assert dvk_handler.get_dvk(2).get_dvk_id() == "SNG01"
    assert dvk_handler.get_dvk(2).is_first()
    assert dvk_handler.get_dvk(2).is_last()
    assert dvk_handler.get_dvk(2).get_sequence_title() is None
    assert dvk_handler.get_dvk(2).get_sequence_number() == 0
    assert dvk_handler.get_dvk(2).get_sequence_total() == 1
    # Test that sequence data was written to disk
    dvk_handler = None
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    assert dvk_handler.get_dvk(0).get_next_id() == "CPL02"
    assert dvk_handler.get_dvk(0).get_sequence_number() == 1
    assert dvk_handler.get_dvk(0).get_sequence_total() == 2
    assert dvk_handler.get_dvk(1).get_prev_id() == "CPL01"
    assert dvk_handler.get_dvk(1).get_sequence_number() == 2
    assert dvk_handler.get_dvk(1).get_sequence_total() == 2
    assert dvk_handler.get_dvk(2).is_first()
    assert dvk_handler.get_dvk(3).get_next_id() == "TRI02"
    assert dvk_handler.get_dvk(4).get_next_id() == "TRI03"
    assert dvk_handler.get_dvk(5).get_prev_id() == "TRI02"
    # Test setting a sequence with invalid parameters
    set_sequence_from_indexes(None, [2])
    set_sequence_from_indexes(dvk_handler, None)
    set_sequence_from_indexes(dvk_handler, [])
    set_sequence_from_indexes()
    assert dvk_handler.get_dvk(0).get_next_id() == "CPL02"
    assert dvk_handler.get_dvk(1).get_prev_id() == "CPL01"
    assert dvk_handler.get_dvk(2).is_first()
    assert dvk_handler.get_dvk(3).get_next_id() == "TRI02"
    assert dvk_handler.get_dvk(4).get_next_id() == "TRI03"
    assert dvk_handler.get_dvk(5).get_prev_id() == "TRI02"

def test_get_sequence():
    """
    Tests the get_sequence method.
    """
    # Set up test files
    test_dir = create_test_dvks()
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    assert dvk_handler.get_size() == 6
    # Test getting sequence
    set_sequence_from_indexes(dvk_handler, [3,4,5])
    assert get_sequence(dvk_handler, 3) == [3,4,5]
    assert get_sequence(dvk_handler, 4) == [3,4,5]
    assert get_sequence(dvk_handler, 5) == [3,4,5]
    # Test getting sequence that forms a loop
    couple = dvk_handler.get_dvk(0)
    assert couple.get_dvk_id() == "CPL01"
    couple.set_prev_id("CPL02")
    couple.set_next_id("CPL02")
    couple.write_dvk()
    couple = dvk_handler.get_dvk(1)
    assert couple.get_dvk_id() == "CPL02"
    couple.set_prev_id("CPL01")
    couple.set_next_id("CPL01")
    couple.write_dvk()
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    assert get_sequence(dvk_handler, 0) == [0,1,0,1,0]
    assert get_sequence(dvk_handler, 1) == [1,0,1,0,1]
    # Test getting sequence from a single Dvk
    assert get_sequence(dvk_handler, 2) == [2]
    # Test getting sequence with invalid parameters
    assert get_sequence(dvk_handler, 6) == []
    assert get_sequence(dvk_handler, -1) == []
    assert get_sequence(dvk_handler, None) == []
    assert get_sequence(None, 2) == []
    assert get_sequence() == []

def test_get_default_sequence_order():
    """
    Tests the get_default_sequence_order function.
    """
    # Create test files
    test_dir = get_test_dir()
    path1 = abspath(join(test_dir, "1 - Prologue"))
    path2 = abspath(join(test_dir, "2 - Part 1"))
    path3 = abspath(join(test_dir, "3 - End"))
    mkdir(path1)
    mkdir(path2)
    mkdir(path3)
    dvk = Dvk()
    dvk.set_dvk_file(join(path1, "prologue.dvk"))
    dvk.set_dvk_id("PRO123")
    dvk.set_title("Prologue")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("media.txt")
    dvk.write_dvk()
    dvk.set_dvk_file(join(path2, "1.dvk"))
    dvk.set_dvk_id("PRT1")
    dvk.set_title("Part 1 - 01")
    dvk.write_dvk()
    dvk.set_dvk_file(join(path2, "2.dvk"))
    dvk.set_dvk_id("PRT2")
    dvk.set_title("Part 1 - 02")
    dvk.write_dvk()
    dvk.set_dvk_file(join(path3, "end.dvk"))
    dvk.set_dvk_id("END1")
    dvk.set_title("End")
    dvk.write_dvk()
    # Test that files were written correctly
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    assert dvk_handler.get_size() == 4
    assert dvk_handler.get_dvk(0).get_title() == "End"
    assert dvk_handler.get_dvk(1).get_title() == "Part 1 - 01"
    assert dvk_handler.get_dvk(2).get_title() == "Part 1 - 02"
    assert dvk_handler.get_dvk(3).get_title() == "Prologue"
    # Test getting the default sequence order
    dvks = get_default_sequence_order(dvk_handler)
    assert len(dvks) == 4
    assert dvks[0].get_title() == "Prologue"
    assert dvks[1].get_title() == "Part 1 - 01"
    assert dvks[2].get_title() == "Part 1 - 02"
    assert dvks[3].get_title() == "End"
    # Test getting default order with existing sequence data
    dvk_handler.sort_dvks("a")
    set_sequence_from_indexes(dvk_handler, [0, 2])
    dvks = get_default_sequence_order(dvk_handler, True)
    assert dvk_handler.get_size() == 4
    assert dvks[0].get_title() == "End"
    assert dvks[1].get_title() == "Part 1 - 02"    
    assert dvks[2].get_title() == "Prologue"
    assert dvks[3].get_title() == "Part 1 - 01"
    # Test getting default order while ignoring sequence data
    dvks = get_default_sequence_order(dvk_handler, False)
    assert len(dvks) == 4
    assert dvks[0].get_title() == "Prologue"
    assert dvks[1].get_title() == "Part 1 - 01"
    assert dvks[2].get_title() == "Part 1 - 02"
    assert dvks[3].get_title() == "End"
    # Test getting default order with invalid parameters
    dvk_handler = DvkHandler()
    assert get_default_sequence_order(dvk_handler) == []
    assert get_default_sequence_order(None) == []
    

def test_remove_sequence_info():
    """
    Tests the remove_sequence_info function.
    """
    # Create test dvks
    test_dir = create_test_dvks()
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    set_sequence_from_indexes(dvk_handler, [0, 1], "Couple")
    set_sequence_from_indexes(dvk_handler, [2])
    set_sequence_from_indexes(dvk_handler, [3, 4, 5])
    dvk = dvk_handler.get_dvk(0)
    dvk.set_section_title("Part 1")
    dvk.write_dvk()
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    # Test that sequence info is present
    dvk = dvk_handler.get_dvk(0)
    assert dvk.is_first()
    assert dvk.get_next_id() == "CPL02"
    assert dvk.get_sequence_number() == 1
    assert dvk.get_sequence_total() == 2
    assert dvk.get_sequence_title() == "Couple"
    assert dvk.get_section_title() == "Part 1"
    dvk = dvk_handler.get_dvk(1)
    assert dvk.get_prev_id() == "CPL01"
    assert dvk.is_last()
    dvk = dvk_handler.get_dvk(2)
    assert dvk.is_first()
    assert dvk.is_last()
    dvk = dvk_handler.get_dvk(3)
    assert dvk.is_first()
    assert dvk.get_next_id() == "TRI02"
    dvk = dvk_handler.get_dvk(4)
    assert dvk.get_prev_id() == "TRI01"
    assert dvk.get_next_id() == "TRI03"
    dvk = dvk_handler.get_dvk(5)
    assert dvk.get_prev_id() == "TRI02"
    assert dvk.is_last()
    # Test removing sequence info
    dvks = [dvk_handler.get_dvk(2)]
    removed = remove_sequence_info(dvks)
    assert len(removed) == 1
    assert removed[0].get_title() == "Single"
    assert removed[0].get_prev_id() is None
    assert removed[0].get_prev_id() is None
    assert removed[0].get_next_id() is None
    assert removed[0].get_sequence_number() == 0
    assert removed[0].get_sequence_total() == 1
    assert removed[0].get_sequence_title() is None
    assert removed[0].get_section_title() is None
    # Test that Dvks with removed media are saved to disk
    dvks = [dvk_handler.get_dvk(0), dvk_handler.get_dvk(1)]
    removed = remove_sequence_info(dvks)
    assert len(removed) == 2
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    dvk = dvk_handler.get_dvk(0)
    assert dvk.get_title() == "Couple P1"
    assert dvk.get_prev_id() is None
    assert dvk.get_next_id() is None
    assert dvk.get_sequence_number() == 0
    assert dvk.get_sequence_total() == 1
    assert dvk.get_sequence_title() is None
    assert dvk.get_section_title() is None
    dvk = dvk_handler.get_dvk(1)
    assert dvk.get_title() == "Couple P2"
    assert dvk.get_prev_id() is None
    assert dvk.get_next_id() is None
    # Test last sequence is still untouched
    dvk = dvk_handler.get_dvk(3)
    assert dvk.is_first()
    assert dvk.get_next_id() == "TRI02"
    dvk = dvk_handler.get_dvk(4)
    assert dvk.get_prev_id() == "TRI01"
    assert dvk.get_next_id() == "TRI03"
    dvk = dvk_handler.get_dvk(5)
    assert dvk.get_prev_id() == "TRI02"
    assert dvk.is_last()
    # Test removing sequence info with invalid parameters
    assert remove_sequence_info([]) == []
    assert remove_sequence_info(None) == []
    assert remove_sequence_info([None]) == []

def test_separate_into_sections():
    """
    Tests the separate_into_sections function.
    """
    # Create test files
    test_dir = get_test_dir()
    path1 = abspath(join(test_dir, "1 - Prologue"))
    path2 = abspath(join(test_dir, "2 - Part 1"))
    path3 = abspath(join(test_dir, "3 - End"))
    mkdir(path1)
    mkdir(path2)
    mkdir(path3)
    dvk = Dvk()
    dvk.set_dvk_file(join(path1, "prologue.dvk"))
    dvk.set_dvk_id("PRO123")
    dvk.set_title("Prologue")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("media.txt")
    dvk.write_dvk()
    dvk.set_dvk_file(join(path2, "1.dvk"))
    dvk.set_dvk_id("PRT1")
    dvk.set_title("Part 1 - 01")
    dvk.set_section_title("Part 1")
    dvk.write_dvk()
    dvk.set_dvk_file(join(path2, "2.dvk"))
    dvk.set_dvk_id("PRT2")
    dvk.set_title("Part 1 - 02")
    dvk.set_section_title()
    dvk.write_dvk()
    dvk.set_dvk_file(join(path3, "end.dvk"))
    dvk.set_dvk_id("END1")
    dvk.set_title("End")
    dvk.set_section_title("End")
    dvk.write_dvk()
    # Test that files were written correctly
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    assert dvk_handler.get_size() == 4
    assert dvk_handler.get_dvk(0).get_title() == "End"
    assert dvk_handler.get_dvk(0).get_section_title() == "End"
    assert dvk_handler.get_dvk(1).get_title() == "Part 1 - 01"
    assert dvk_handler.get_dvk(1).get_section_title() == "Part 1"
    assert dvk_handler.get_dvk(2).get_title() == "Part 1 - 02"
    assert dvk_handler.get_dvk(2).get_section_title() is None
    assert dvk_handler.get_dvk(3).get_title() == "Prologue"
    assert dvk_handler.get_dvk(3).get_section_title() is None
    # Test separating Dvks into sections
    sections = separate_into_sections(dvk_handler, False, False)
    assert len(sections) == 3
    assert len(sections[0]) == 2
    assert sections[0][0] == False
    assert sections[0][1].get_title() == "Prologue"
    assert len(sections[1]) == 3
    assert sections[1][0] == False
    assert sections[1][1].get_title() == "Part 1 - 01"
    assert sections[1][2].get_title() == "Part 1 - 02"
    assert len(sections[2]) == 2
    assert sections[2][0] == False
    assert sections[2][1].get_title() == "End"
    # Test separating Dvks into sections while attempting to keep section titles
    sections = separate_into_sections(dvk_handler, False, True)
    assert len(sections) == 3
    assert len(sections[0]) == 2
    assert sections[0][0] == False
    assert sections[0][1].get_title() == "Prologue"
    assert len(sections[1]) == 3
    assert sections[1][0] == False
    assert sections[1][1].get_title() == "Part 1 - 01"
    assert sections[1][2].get_title() == "Part 1 - 02"
    assert len(sections[2]) == 2
    assert sections[2][0] == True
    assert sections[2][1].get_title() == "End"
    # Test separating into sections with only one section
    dvk_handler = DvkHandler(path3)
    dvk_handler.sort_dvks("a")
    sections = separate_into_sections(dvk_handler, False, True)
    assert len(sections) == 1
    assert len(sections[0]) == 2
    assert sections[0][0] == False
    assert sections[0][1].get_title() == "End"
    # Test separating into sections with existing sequence data breaking up sections
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    set_sequence_from_indexes(dvk_handler, [1, 0])
    sections = separate_into_sections(dvk_handler, True, False)
    assert len(sections) == 4
    assert len(sections[0]) == 2
    assert sections[0][0] == False
    assert sections[0][1].get_title() == "Part 1 - 01"
    assert len(sections[1]) == 2
    assert sections[1][0] == False
    assert sections[1][1].get_title() == "End"
    assert len(sections[2]) == 2
    assert sections[2][0] == False
    assert sections[2][1].get_title() == "Prologue"
    assert len(sections[3]) == 2
    assert sections[3][0] == False
    assert sections[3][1].get_title() == "Part 1 - 02"
    # Test separating into sections with invalid parameters
    dvk_handler = DvkHandler()
    assert separate_into_sections(dvk_handler) == []
    assert separate_into_sections(None, False) == []

def all_tests():
    """
    Runs all tests for the sequencing.py module.
    """
    test_set_sequence()
    test_set_sequence_from_indexes()
    test_get_sequence()
    test_get_default_sequence_order()
    test_remove_sequence_info()
    test_separate_into_sections()
    
