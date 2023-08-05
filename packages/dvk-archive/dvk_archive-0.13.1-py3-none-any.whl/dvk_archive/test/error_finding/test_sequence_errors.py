#!/usr/bin/env python3

from dvk_archive.main.file.dvk import Dvk
from dvk_archive.main.file.dvk_handler import DvkHandler
from dvk_archive.main.file.sequencing import set_sequence_from_indexes
from dvk_archive.main.error_finding.sequence_errors import contains_invalid_prev_next
from dvk_archive.main.error_finding.sequence_errors import contains_invalid_sequence_number
from dvk_archive.main.error_finding.sequence_errors import contains_invalid_start_end
from dvk_archive.main.error_finding.sequence_errors import get_sequence_errors
from dvk_archive.main.error_finding.sequence_errors import is_invalid_single
from dvk_archive.test.temp_dir import get_test_dir
from os.path import basename, join

def test_is_invalid_single():
    """
    Tests the is_invalid_single function.
    """
    # Create test files
    test_dir = get_test_dir()
    valid = Dvk()
    valid.set_dvk_file(join(test_dir, "none.dvk"))
    valid.set_dvk_id("VAL01")
    valid.set_title("None")
    valid.set_artist("artist")
    valid.set_page_url("/url")
    valid.set_media_file("media.txt")
    valid.write_dvk()
    valid.set_dvk_file(join(test_dir, "single.dvk"))
    valid.set_dvk_id("VAL02")
    valid.set_title("Single")
    valid.set_first()
    valid.set_last()
    valid.write_dvk()
    mismatch = Dvk()
    mismatch.set_dvk_file(join(test_dir, "mismatch1.dvk"))
    mismatch.set_dvk_id("MIS01")
    mismatch.set_title("Mismatch 01")
    mismatch.set_artist("artist")
    mismatch.set_page_url("/url")
    mismatch.set_media_file("media.txt")
    mismatch.set_first()
    mismatch.write_dvk()
    mismatch.set_dvk_file(join(test_dir, "mismatch2.dvk"))
    mismatch.set_dvk_id("MIS02")
    mismatch.set_title("Mismatch 02")
    mismatch.set_prev_id(None)
    mismatch.set_last()
    mismatch.write_dvk()
    invalid = Dvk()
    invalid.set_dvk_file(join(test_dir, "invalid1.dvk"))
    invalid.set_dvk_id("INV01")
    invalid.set_title("Invalid 1")
    invalid.set_artist("artist")
    invalid.set_page_url("/url")
    invalid.set_media_file("media.txt")
    invalid.set_first()
    invalid.set_next_id("Blah")
    invalid.write_dvk()
    invalid.set_dvk_file(join(test_dir, "invalid2.dvk"))
    invalid.set_dvk_id("INV02")
    invalid.set_title("Invalid 2")
    invalid.set_prev_id(None)
    invalid.write_dvk()
    invalid.set_dvk_file(join(test_dir, "invalid3.dvk"))
    invalid.set_dvk_id("INV03")
    invalid.set_title("Invalid 3")
    invalid.set_prev_id("Blah")
    invalid.set_last()
    invalid.write_dvk()
    invalid.set_dvk_file(join(test_dir, "invalid4.dvk"))
    invalid.set_dvk_id("INV04")
    invalid.set_title("Invalid 4")
    invalid.set_next_id(None)
    invalid.write_dvk()
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    assert dvk_handler.get_size() == 8
    assert dvk_handler.get_dvk(0).get_title() == "Invalid 1"
    assert dvk_handler.get_dvk(1).get_title() == "Invalid 2"
    assert dvk_handler.get_dvk(2).get_title() == "Invalid 3"
    assert dvk_handler.get_dvk(3).get_title() == "Invalid 4"
    assert dvk_handler.get_dvk(4).get_title() == "Mismatch 01"
    assert dvk_handler.get_dvk(5).get_title() == "Mismatch 02"
    assert dvk_handler.get_dvk(6).get_title() == "None"
    assert dvk_handler.get_dvk(7).get_title() == "Single"
    # Test that sequences with more than one Dvk are not counted
    assert not is_invalid_single(dvk_handler, [0,3])
    assert not is_invalid_single(dvk_handler, [4, 5, 6])
    # Test that valid single sequences are not counted
    assert not is_invalid_single(dvk_handler, [6])
    assert not is_invalid_single(dvk_handler, [7])
    # Test that single sequences with mismatched prev/next id tags are counted
    assert is_invalid_single(dvk_handler, [4])
    assert is_invalid_single(dvk_handler, [5])
    # Test than single sequences that try connecting to more Dvks are counted
    assert is_invalid_single(dvk_handler, [0])
    assert is_invalid_single(dvk_handler, [1])
    assert is_invalid_single(dvk_handler, [2])
    assert is_invalid_single(dvk_handler, [3])
    # Test using invalid parameters
    assert not is_invalid_single(None, [6])
    assert not is_invalid_single(None, [12])
    assert not is_invalid_single(dvk_handler, None)

def test_contains_invalid_start_end():
    """
    Tests the contains_invalid_start_end function.
    """
    # Create test files
    test_dir = get_test_dir()
    null = Dvk()
    null.set_dvk_file(join(test_dir, "null01.dvk"))
    null.set_dvk_id("NUL01")
    null.set_title("Null Start")
    null.set_artist("Artist")
    null.set_page_url("/url/")
    null.set_media_file("media.txt")
    null.set_prev_id(None)
    null.set_next_id("ID123")
    null.write_dvk()
    null.set_dvk_file(join(test_dir, "null02.dvk"))
    null.set_dvk_id("NUL02")
    null.set_title("Null End")
    null.set_prev_id("ID123")
    null.set_next_id(None)
    null.write_dvk()
    not_end = Dvk()
    not_end.set_dvk_file(join(test_dir, "ne1.dvk"))
    not_end.set_dvk_id("NTE01")
    not_end.set_title("Not End 01")
    not_end.set_artist("artist")
    not_end.set_page_url("/url/")
    not_end.set_media_file("media.txt")
    not_end.set_prev_id("ID123")
    not_end.set_next_id("ID245")
    not_end.write_dvk()
    not_end.set_dvk_file(join(test_dir, "ne2.dvk"))
    not_end.set_dvk_id("NTE02")
    not_end.set_title("Not End 02")
    not_end.write_dvk()
    valid = Dvk()
    valid.set_dvk_file(join(test_dir, "valid1.dvk"))
    valid.set_dvk_id("VAL01")
    valid.set_title("Valid Start")
    valid.set_artist("artist")
    valid.set_page_url("/url/")
    valid.set_media_file("media.txt")
    valid.set_first()
    valid.set_next_id("ID245")
    valid.write_dvk()
    valid.set_dvk_file(join(test_dir, "valid2.dvk"))
    valid.set_dvk_id("VAL02")
    valid.set_title("Valid End")
    valid.set_prev_id("ID123")
    valid.set_last()
    valid.write_dvk()
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    assert dvk_handler.get_size() == 6
    assert dvk_handler.get_dvk(0).get_title() == "Not End 01"
    assert dvk_handler.get_dvk(1).get_title() == "Not End 02"
    assert dvk_handler.get_dvk(2).get_title() == "Null End"
    assert dvk_handler.get_dvk(3).get_title() == "Null Start"
    assert dvk_handler.get_dvk(4).get_title() == "Valid End"
    assert dvk_handler.get_dvk(5).get_title() == "Valid Start"
    # Test that sequences with only one Dvk are not counted
    assert not contains_invalid_start_end(dvk_handler, [4])
    assert not contains_invalid_start_end(dvk_handler, [0])
    # Test sequences with valid start and end
    assert not contains_invalid_start_end(dvk_handler, [5, 4])
    assert not contains_invalid_start_end(dvk_handler, [5, 0, 1, 2, 3, 4])
    # Test sequences with an invalid start
    assert contains_invalid_start_end(dvk_handler, [3, 4])
    assert contains_invalid_start_end(dvk_handler, [3, 5, 4])
    assert contains_invalid_start_end(dvk_handler, [0, 4])
    assert contains_invalid_start_end(dvk_handler, [0, 1])
    # Test sequences with an invalid end
    assert contains_invalid_start_end(dvk_handler, [5, 2])
    assert contains_invalid_start_end(dvk_handler, [5, 4, 2])
    assert contains_invalid_start_end(dvk_handler, [5, 0])
    assert contains_invalid_start_end(dvk_handler, [1, 0])
    # Test with invalid parameters
    assert not contains_invalid_start_end(None, [5, 2])
    assert not contains_invalid_start_end(dvk_handler, None)
    assert not contains_invalid_start_end(dvk_handler, [7, 8, 9])

def test_contains_invalid_sequence_number():
    """
    Tests the contains_invalid_sequence_number function.
    """
    # Create test files
    test_dir = get_test_dir()
    total = Dvk()
    total.set_dvk_file(join(test_dir, "tot01.dvk"))
    total.set_dvk_id("TOT01")
    total.set_title("Invalid Sequence Total 01")
    total.set_artist("artist")
    total.set_page_url("/url/")
    total.set_media_file("media.txt")
    total.write_dvk()
    total.set_dvk_file(join(test_dir, "tot02.dvk"))
    total.set_dvk_id("TOT02")
    total.set_title("Invalid Sequence Total 02")
    total.write_dvk()
    number = Dvk()
    number.set_dvk_file(join(test_dir, "num01.dvk"))
    number.set_dvk_id("NUM01")
    number.set_title("Invalid Sequence Number 01")
    number.set_artist("artist")
    number.set_page_url("/url/")
    number.set_media_file("media.txt")
    number.write_dvk()
    total.set_dvk_file(join(test_dir, "num02.dvk"))
    total.set_dvk_id("NUM02")
    total.set_title("Invalid Sequence Number 02")
    total.write_dvk()
    total.set_dvk_file(join(test_dir, "num03.dvk"))
    total.set_dvk_id("NUM03")
    total.set_title("Invalid Sequence Number 03")
    total.write_dvk()
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    assert dvk_handler.get_size() == 5
    assert dvk_handler.get_dvk(0).get_title() == "Invalid Sequence Number 01"
    assert dvk_handler.get_dvk(1).get_title() == "Invalid Sequence Number 02"
    assert dvk_handler.get_dvk(2).get_title() == "Invalid Sequence Number 03"
    assert dvk_handler.get_dvk(3).get_title() == "Invalid Sequence Total 01"
    assert dvk_handler.get_dvk(4).get_title() == "Invalid Sequence Total 02"
    # Test that sequences with only one Dvk are not counted
    assert not contains_invalid_sequence_number(dvk_handler, [1])
    assert not contains_invalid_sequence_number(dvk_handler, [4])
    # Test that sequences with valid numbers are not counted
    set_sequence_from_indexes(dvk_handler, [0, 1, 2])
    set_sequence_from_indexes(dvk_handler, [3, 4])
    assert not contains_invalid_sequence_number(dvk_handler, [0, 1, 2])
    assert not contains_invalid_sequence_number(dvk_handler, [3, 4])
    # Test that sequences with invalid sequence totals are caught
    dvk = dvk_handler.get_dvk(3)
    dvk.set_sequence_total(1)
    dvk_handler.set_dvk(dvk, 3)
    assert contains_invalid_sequence_number(dvk_handler, [0, 1])
    assert contains_invalid_sequence_number(dvk_handler, [3, 4])
    # Test that sequences with invalid sequence numbers are caught
    dvk = dvk_handler.get_dvk(2)
    dvk.set_sequence_number(2)
    dvk_handler.set_dvk(dvk, 2)
    assert contains_invalid_sequence_number(dvk_handler, [0, 1, 2])
    # Test using invalid parameters
    assert not contains_invalid_sequence_number(None, [0, 1, 2])
    assert not contains_invalid_sequence_number(dvk_handler, None)
    assert not contains_invalid_sequence_number(dvk_handler, [5, 6, 7])

def test_contains_invalid_prev_next():
    """
    Tests the contains_invalid_link function.
    """
    # Create test files
    test_dir = get_test_dir()
    valid = Dvk()
    valid.set_dvk_file(join(test_dir, "valid01.dvk"))
    valid.set_dvk_id("VAL01")
    valid.set_title("Valid 01")
    valid.set_artist("artist")
    valid.set_page_url("/url/")
    valid.set_media_file("media.txt")
    valid.write_dvk()
    valid.set_dvk_file(join(test_dir, "valid02.dvk"))
    valid.set_dvk_id("VAL02")
    valid.set_title("Valid 02")
    valid.write_dvk()
    valid.set_dvk_file(join(test_dir, "valid03.dvk"))
    valid.set_dvk_id("VAL03")
    valid.set_title("Valid 03")
    valid.write_dvk()
    prev = Dvk()
    prev.set_dvk_file(join(test_dir, "prev01.dvk"))
    prev.set_dvk_id("PRV01")
    prev.set_title("Prev Invalid 01")
    prev.set_artist("artist")
    prev.set_page_url("/url/")
    prev.set_media_file("media.txt")
    prev.write_dvk()
    prev.set_dvk_file(join(test_dir, "prev02.dvk"))
    prev.set_dvk_id("PRV02")
    prev.set_title("Prev Invalid 02")
    prev.write_dvk()
    prev.set_dvk_file(join(test_dir, "prev03.dvk"))
    prev.set_dvk_id("PRV03")
    prev.set_title("Prev Invalid 03")
    prev.write_dvk()
    nxt = Dvk()
    nxt.set_dvk_file(join(test_dir, "next01.dvk"))
    nxt.set_dvk_id("NXT01")
    nxt.set_title("Next Invalid 01")
    nxt.set_artist("artist")
    nxt.set_page_url("/url/")
    nxt.set_media_file("media.txt")
    nxt.write_dvk()
    nxt.set_dvk_file(join(test_dir, "next02.dvk"))
    nxt.set_dvk_id("NXT02")
    nxt.set_title("Next Invalid 02")
    nxt.write_dvk()
    nxt.set_dvk_file(join(test_dir, "next03.dvk"))
    nxt.set_dvk_id("NXT03")
    nxt.set_title("Next Invalid 03")
    nxt.write_dvk()
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    assert dvk_handler.get_size() == 9
    assert dvk_handler.get_dvk(0).get_title() == "Next Invalid 01"
    assert dvk_handler.get_dvk(1).get_title() == "Next Invalid 02"
    assert dvk_handler.get_dvk(2).get_title() == "Next Invalid 03"
    assert dvk_handler.get_dvk(3).get_title() == "Prev Invalid 01"
    assert dvk_handler.get_dvk(4).get_title() == "Prev Invalid 02"
    assert dvk_handler.get_dvk(5).get_title() == "Prev Invalid 03"
    assert dvk_handler.get_dvk(6).get_title() == "Valid 01"
    assert dvk_handler.get_dvk(7).get_title() == "Valid 02"
    assert dvk_handler.get_dvk(8).get_title() == "Valid 03"
    set_sequence_from_indexes(dvk_handler, [0, 1, 2])
    set_sequence_from_indexes(dvk_handler, [3, 4, 5])
    set_sequence_from_indexes(dvk_handler, [6, 7, 8])
    # Test sequences with only one Dvk are not counted
    assert not contains_invalid_prev_next(dvk_handler, [0])
    assert not contains_invalid_prev_next(dvk_handler, [8])
    # Test sequences with properly linked Dvks
    assert not contains_invalid_prev_next(dvk_handler, [0, 1, 2])
    assert not contains_invalid_prev_next(dvk_handler, [3, 4, 5])
    assert not contains_invalid_prev_next(dvk_handler, [6, 7, 8])
    # Test sequences with broken next_id
    dvk = dvk_handler.get_dvk(1)
    dvk.set_next_id("invalid")
    dvk_handler.set_dvk(dvk, 1)
    assert contains_invalid_prev_next(dvk_handler, [0, 1, 2])
    assert contains_invalid_prev_next(dvk_handler, [8, 7, 8])
    # Test sequences with broken prev_id
    dvk = dvk_handler.get_dvk(4)
    dvk.set_prev_id("PRV03")
    dvk_handler.set_dvk(dvk, 4)
    assert contains_invalid_prev_next(dvk_handler, [3, 4, 5])
    assert contains_invalid_prev_next(dvk_handler, [6, 7, 6])
    # Test with invalid parameters
    assert not contains_invalid_prev_next(None, [3, 4, 5])
    assert not contains_invalid_prev_next(dvk_handler, None)
    assert not contains_invalid_prev_next(dvk_handler, [9, 10, 11])

def test_get_sequence_errors():
    """
    Tests the get_sequence_errors function.
    """
    # Test with valid sequences
    test_dir = get_test_dir()
    valid = Dvk()
    valid.set_dvk_file(join(test_dir, "valid1.dvk"))
    valid.set_dvk_id("VAL01")
    valid.set_title("Valid 01")
    valid.set_artist("artist")
    valid.set_page_url("/url/")
    valid.set_media_file("media.txt")
    valid.write_dvk()
    valid.set_dvk_file(join(test_dir, "valid2.dvk"))
    valid.set_dvk_id("VAL02")
    valid.set_title("Valid 02")
    valid.write_dvk()
    valid.set_dvk_file(join(test_dir, "valid3.dvk"))
    valid.set_dvk_id("VAL03")
    valid.set_title("Valid 03")
    valid.write_dvk()
    valid.set_dvk_file(join(test_dir, "single1.dvk"))
    valid.set_dvk_id("OTH01")
    valid.set_title("Single 01")
    valid.write_dvk()
    valid.set_dvk_file(join(test_dir, "single2.dvk"))
    valid.set_dvk_id("OTH02")
    valid.set_title("Single 02")
    valid.write_dvk()
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    assert dvk_handler.get_size() == 5
    assert dvk_handler.get_dvk(0).get_title() == "Single 01"
    assert dvk_handler.get_dvk(1).get_title() == "Single 02"
    assert dvk_handler.get_dvk(2).get_title() == "Valid 01"
    assert dvk_handler.get_dvk(3).get_title() == "Valid 02"
    assert dvk_handler.get_dvk(4).get_title() == "Valid 03"
    set_sequence_from_indexes(dvk_handler, [0])
    set_sequence_from_indexes(dvk_handler, [2, 3, 4])
    assert get_sequence_errors(test_dir) == []
    # Test finding invalid single Dvks
    valid1 = dvk_handler.get_dvk(2)
    valid2 = dvk_handler.get_dvk(3)
    valid3 = dvk_handler.get_dvk(4)
    test_dir = get_test_dir()
    single = Dvk()
    single.set_dvk_file(join(test_dir, "single1.dvk"))
    single.set_dvk_id("SNG01")
    single.set_title("Single 01")
    single.set_artist("artist")
    single.set_page_url("/url/")
    single.set_media_file("media.txt")
    single.set_first()
    single.set_next_id(None)
    single.write_dvk()
    single.set_dvk_file(join(test_dir, "single2.dvk"))
    single.set_dvk_id("SNG02")
    single.set_title("Single 02")
    single.set_prev_id(None)
    single.set_last()
    single.write_dvk()
    valid1.write_dvk()
    valid2.write_dvk()
    valid3.write_dvk()
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    assert dvk_handler.get_size() == 5
    assert dvk_handler.get_dvk(0).get_title() == "Single 01"
    assert dvk_handler.get_dvk(1).get_title() == "Single 02"
    assert dvk_handler.get_dvk(2).get_title() == "Valid 01"
    assert dvk_handler.get_dvk(3).get_title() == "Valid 02"
    assert dvk_handler.get_dvk(4).get_title() == "Valid 03"
    errors = get_sequence_errors(test_dir)
    assert len(errors) == 2
    assert len(errors[0]) == 1
    assert basename(errors[0][0]) == "single1.dvk"
    assert len(errors[1]) == 1
    assert basename(errors[1][0]) == "single2.dvk"
    # Test finding sequences with invalid start and/or end
    test_dir = get_test_dir()
    start = Dvk()
    start.set_dvk_file(join(test_dir, "start1.dvk"))
    start.set_dvk_id("SRT01")
    start.set_title("Invalid Start 1")
    start.set_artist("artist")
    start.set_page_url("/url/")
    start.set_media_file("media.txt")
    start.write_dvk()
    start.set_dvk_file(join(test_dir, "start2.dvk"))
    start.set_dvk_id("SRT02")
    start.set_title("Invalid Start 2")
    start.write_dvk()
    valid1.write_dvk()
    valid2.write_dvk()
    valid3.write_dvk()
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    assert dvk_handler.get_size() == 5
    assert dvk_handler.get_dvk(0).get_title() == "Invalid Start 1"
    assert dvk_handler.get_dvk(1).get_title() == "Invalid Start 2"
    assert dvk_handler.get_dvk(2).get_title() == "Valid 01"
    assert dvk_handler.get_dvk(3).get_title() == "Valid 02"
    assert dvk_handler.get_dvk(4).get_title() == "Valid 03"
    set_sequence_from_indexes(dvk_handler, [0, 1])
    dvk = dvk_handler.get_dvk(0)
    dvk.set_prev_id("INV123")
    dvk.write_dvk()
    assert contains_invalid_start_end(dvk_handler, [0,1])
    errors = get_sequence_errors(test_dir)
    assert len(errors) == 1
    assert len(errors[0]) == 2
    assert basename(errors[0][0]) == "start1.dvk"
    assert basename(errors[0][1]) == "start2.dvk"
    # Test finding sequence with invalid sequence numbers
    test_dir = get_test_dir()
    num = Dvk()
    num.set_dvk_file(join(test_dir, "num1.dvk"))
    num.set_dvk_id("NUM01")
    num.set_title("Invalid Num 01")
    num.set_artist("artist")
    num.set_page_url("/page/")
    num.set_media_file("media.txt")
    num.write_dvk()
    num.set_dvk_file(join(test_dir, "num2.dvk"))
    num.set_dvk_id("NUM02")
    num.set_title("Invalid Num 02")
    num.write_dvk()
    num.set_dvk_file(join(test_dir, "other1.dvk"))
    num.set_dvk_id("OTH01")
    num.set_title("Other 1")
    num.write_dvk()
    num.set_dvk_file(join(test_dir, "other2.dvk"))
    num.set_dvk_id("OTH02")
    num.set_title("Other 2")
    num.write_dvk()
    valid1.write_dvk()
    valid2.write_dvk()
    valid3.write_dvk()
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    assert dvk_handler.get_size() == 7
    assert dvk_handler.get_dvk(0).get_title() == "Invalid Num 01"
    assert dvk_handler.get_dvk(1).get_title() == "Invalid Num 02"
    assert dvk_handler.get_dvk(2).get_title() == "Other 1"
    assert dvk_handler.get_dvk(3).get_title() == "Other 2"
    assert dvk_handler.get_dvk(4).get_title() == "Valid 01"
    assert dvk_handler.get_dvk(5).get_title() == "Valid 02"
    assert dvk_handler.get_dvk(6).get_title() == "Valid 03"
    set_sequence_from_indexes(dvk_handler, [0, 1])
    set_sequence_from_indexes(dvk_handler, [2, 3])
    dvk = dvk_handler.get_dvk(1)
    dvk.set_sequence_number(1)
    dvk.write_dvk()
    dvk = dvk_handler.get_dvk(2)
    dvk.set_sequence_total(5)
    dvk.write_dvk()
    errors = get_sequence_errors(test_dir)
    assert len(errors) == 2
    assert len(errors[0]) == 2
    assert basename(errors[0][0]) == "num1.dvk"
    assert basename(errors[0][1]) == "num2.dvk"
    assert len(errors[1]) == 2
    assert basename(errors[1][0]) == "other1.dvk"
    assert basename(errors[1][1]) == "other2.dvk"
    # Test getting sequence with invalid prev/next ids
    test_dir = get_test_dir()
    link = Dvk()
    link.set_dvk_file(join(test_dir, "link1.dvk"))
    link.set_dvk_id("LNK01")
    link.set_title("Invalid Link 01")
    link.set_artist("artist")
    link.set_page_url("/page/")
    link.set_media_file("media.txt")
    link.write_dvk()
    link.set_dvk_file(join(test_dir, "link2.dvk"))
    link.set_dvk_id("LNK02")
    link.set_title("Invalid Link 02")
    link.write_dvk()
    link.set_dvk_file(join(test_dir, "link3.dvk"))
    link.set_dvk_id("LNK03")
    link.set_title("Invalid Link 03")
    link.write_dvk()
    valid1.write_dvk()
    valid2.write_dvk()
    valid3.write_dvk()
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    assert dvk_handler.get_size() == 6
    assert dvk_handler.get_dvk(0).get_title() == "Invalid Link 01"
    assert dvk_handler.get_dvk(1).get_title() == "Invalid Link 02"
    assert dvk_handler.get_dvk(2).get_title() == "Invalid Link 03"
    assert dvk_handler.get_dvk(3).get_title() == "Valid 01"
    assert dvk_handler.get_dvk(4).get_title() == "Valid 02"
    assert dvk_handler.get_dvk(5).get_title() == "Valid 03"
    set_sequence_from_indexes(dvk_handler, [0, 1, 2])
    dvk = dvk_handler.get_dvk(1)
    dvk.set_prev_id("BLH123")
    dvk.write_dvk()
    errors = get_sequence_errors(test_dir)
    assert len(errors) == 1
    assert len(errors[0]) == 3
    assert basename(errors[0][0]) == "link1.dvk"
    assert basename(errors[0][1]) == "link2.dvk"
    assert basename(errors[0][2]) == "link3.dvk"
    # Test getting Dvks using invalid parameters
    assert get_sequence_errors("/non/existant/dir/") == []
    assert get_sequence_errors(dvk.get_dvk_file()) == []
    assert get_sequence_errors(None) == []

def all_tests():
    """
    Runs all tests for the sequence_errors.py module.
    """
    test_is_invalid_single()
    test_contains_invalid_start_end()
    test_contains_invalid_sequence_number()
    test_contains_invalid_prev_next()
    test_get_sequence_errors()
