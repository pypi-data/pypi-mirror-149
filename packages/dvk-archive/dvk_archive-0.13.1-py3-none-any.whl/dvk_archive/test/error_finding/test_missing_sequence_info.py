#!/usr/bin/env python3

from dvk_archive.main.file.dvk import Dvk
from dvk_archive.main.file.dvk_handler import DvkHandler
from dvk_archive.main.error_finding.missing_sequence_info import get_missing_sequence_info
from dvk_archive.test.temp_dir import get_test_dir
from os import pardir
from os.path import abspath, basename, join

def test_get_missing_sequence_info():
    """
    Tests the get_missing_sequence_info function.
    """
    # Create test files
    test_dir = get_test_dir()
    missing = Dvk()
    missing.set_dvk_file(join(test_dir, "missing_first.dvk"))
    missing.set_dvk_id("MIS01")
    missing.set_title("Missing First")
    missing.set_artist("artist")
    missing.set_page_url("/url/")
    missing.set_media_file("media.txt")
    missing.set_last()
    missing.write_dvk()
    missing.set_dvk_file(join(test_dir, "missing_last.dvk"))
    missing.set_dvk_id("MIS02")
    missing.set_title("Missing Last")
    missing.set_prev_id("NON123")
    missing.set_next_id(None)
    missing.write_dvk()
    missing.set_dvk_file(join(test_dir, "missing_both.dvk"))
    missing.set_dvk_id("MIS03")
    missing.set_title("Missing Both")
    missing.set_prev_id(None)
    missing.set_next_id(None)
    missing.write_dvk()
    valid = Dvk()
    valid.set_dvk_file(join(test_dir, "valid01.dvk"))
    valid.set_dvk_id("VAL01")
    valid.set_title("Valid Single")
    valid.set_artist("artist")
    valid.set_page_url("/url/")
    valid.set_media_file("media.txt")
    valid.set_first()
    valid.set_last()
    valid.write_dvk()
    valid.set_dvk_file(join(test_dir, "valid02.dvk"))
    valid.set_dvk_id("VAL02")
    valid.set_title("Valid First")
    valid.set_first()
    valid.set_next_id("ID123")
    valid.write_dvk()
    valid.set_dvk_file(join(test_dir, "valid03.dvk"))
    valid.set_dvk_id("VAL03")
    valid.set_title("Valid Last")
    valid.set_prev_id("ID123")
    valid.set_last()
    valid.write_dvk()
    valid.set_dvk_file(join(test_dir, "valid04.dvk"))
    valid.set_dvk_id("VAL04")
    valid.set_title("Valid Middle")
    valid.set_prev_id("ID123")
    valid.set_next_id("ID246")
    valid.write_dvk()
    # Test files were written correctly
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    assert dvk_handler.get_size() == 7
    assert dvk_handler.get_dvk(0).get_title() == "Missing Both"
    assert dvk_handler.get_dvk(1).get_title() == "Missing First"
    assert dvk_handler.get_dvk(2).get_title() == "Missing Last"
    assert dvk_handler.get_dvk(3).get_title() == "Valid First"
    assert dvk_handler.get_dvk(4).get_title() == "Valid Last"
    assert dvk_handler.get_dvk(5).get_title() == "Valid Middle"
    assert dvk_handler.get_dvk(6).get_title() == "Valid Single"
    # Test finding dvks with missing sequence info
    paths = get_missing_sequence_info(test_dir)
    assert len(paths) == 3
    assert abspath(join(paths[0], pardir)) == abspath(test_dir)
    assert basename(paths[0]) == "missing_both.dvk"
    assert basename(paths[1]) == "missing_first.dvk"
    assert basename(paths[2]) == "missing_last.dvk"
    # Test finding dvks in emty directory
    test_dir = get_test_dir()
    assert get_missing_sequence_info(test_dir) == []
    # Test finding dvks with invalid parameters
    assert get_missing_sequence_info(None) == []
    assert get_missing_sequence_info("/non/existant/dir/") == []

def all_tests():
    """
    Runs all tests for the missing_sequence_info.py module.
    """
    test_get_missing_sequence_info()
