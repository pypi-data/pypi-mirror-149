#!/usr/bin/env python3

from dvk_archive.main.processing.string_processing import pad_num
from dvk_archive.main.processing.string_processing import remove_whitespace
from dvk_archive.main.processing.string_processing import get_filename
from dvk_archive.main.processing.string_processing import truncate_string
from dvk_archive.main.processing.string_processing import get_extension
from dvk_archive.main.processing.string_processing import get_url_directory
from dvk_archive.main.processing.string_processing import regex_replace
from dvk_archive.main.processing.string_processing import truncate_path

def test_regex_replace():
    """
    Tests the regex replace function.
    """
    # Test replacing regex matches
    replaced = regex_replace(get_extension, "[a-z]+\\.[a-z]+", "eh, bl.ah th.ing not")
    assert replaced == "eh, .ah .ing not"
    replaced = regex_replace(get_filename, "[a-z]+\\?[a-z]+|[a-z]+!", "why?not I Don't know!")
    assert replaced == "why-not I Don't know"
    # Test replacing strings with no regex match
    replaced = regex_replace(get_extension, "nope", "got nothing")
    assert replaced == "got nothing"
    # Test replacing strings with invalid parameters
    assert regex_replace(None, "pattern", "string") == "string"
    assert regex_replace(get_extension, None, "string") == "string"
    assert regex_replace(get_extension, "pattern", None) is None

def test_pad_num():
    """
    Tests the pad_num function.
    """
    # Test padding out number strings with zeros
    assert pad_num("2F", 2) == "2F"
    assert pad_num("2E", 5) == "0002E"
    assert pad_num("10F", 2) == "10F"
    # Test using invalid values
    assert pad_num("A3", 0) == ""
    assert pad_num("F3", -1) == ""
    assert pad_num(None, 2) == ""

def test_remove_whitespace():
    """
    Tests the remove_whitespace function.
    """
    # Test removing whitespace from the beginning and end of strings
    assert remove_whitespace("") == ""
    assert remove_whitespace(" ") == ""
    assert remove_whitespace(" \t  ") == ""
    assert remove_whitespace("  blah") == "blah"
    assert remove_whitespace("blah   ") == "blah"
    assert remove_whitespace(" \t blah  \t") == "blah"
    assert remove_whitespace(" Other Text \n") == "Other Text"
    assert remove_whitespace("   Yet \n more Text \n \r") == "Yet \n more Text"    
    assert remove_whitespace("blah") == "blah"
    # Test using invalid string
    assert remove_whitespace(None) == ""

def test_get_filename():
    """
    Tests the get_filename function
    """
    # Test getting file friendly names
    assert get_filename("This & That 2") == "This - That 2"
    assert get_filename("! !end filler!??  ") == "end filler"
    assert get_filename("thing--stuff  @*-   bleh") == "thing-stuff - bleh"
    assert get_filename("a% - !b @  ??c") == "a - b - c"
    assert get_filename("Test String", 5) == "Test"
    assert get_filename("Test String", -1) == "Test String"
    # Test converting from non-standard latin characters
    assert get_filename("ÀÁÂÃÄÅ") == "AAAAAA"
    assert get_filename("ÈÉÊË") == "EEEE"
    assert get_filename("ÌÍÎÏ") == "IIII"
    assert get_filename("ÑÒÓÔÕÖ") == "NOOOOO"
    assert get_filename("ÙÚÛÜÝ") == "UUUUY"
    assert get_filename("àáâãäå") == "aaaaaa"
    assert get_filename("èéêë") == "eeee"
    assert get_filename("ìíîï") == "iiii"
    assert get_filename("ñòóôõö") == "nooooo"
    assert get_filename("ùúûüýÿ") == "uuuuyy"
    # Test getting filenames with no length
    assert get_filename("") == "0"
    assert get_filename("$") == "0"
    # Test getting filename when given string is invalid
    assert get_filename(None) == "0"

def test_truncate_string():
    """
    Tests the truncate_string function.
    """
    # TEST TRUNCATING STRINGS
    assert truncate_string("blah", 0) == ""
    assert truncate_string("bleh", -1) == ""
    assert truncate_string("bleh", 4) == "bleh"
    assert truncate_string("words", 3) == "wor"
    assert truncate_string("word-stuff", 5) == "word"
    assert truncate_string("words n stuff", 4) == "stu"
    assert truncate_string("word stuff", 5) == "word"
    assert truncate_string("words-n-stuff", 4) == "stu"
    in_str = "This string is way too long to work as a title p25"
    out_str = "This string is way too long to work p25";
    assert truncate_string(in_str, 40) == out_str
    in_str = "HereIsA LongThingWithoutManySpacesWhichCanBeShort"
    out_str = "HereIsA WithoutManySpacesWhichCanBeShort"
    assert truncate_string(in_str, 40) == out_str
    in_str = "ThisMessageIsAbsolutelyWayToLongToWorkFor-"
    in_str = in_str + "AnyThingAtAllSoLetsSeeHowThisWillFareISuppose"
    out_str = "ThisMessageIsAbsolutelyWayToLongToWorkFo"
    assert truncate_string(in_str, 40) == out_str
    in_str = "ThisMessageIsAbsolutelyWayToLongToWorkForAnyThing-"
    in_str = in_str + "AtAllSoLetsSeeHowThisWillFareISuppose"
    out_str = "Th-AtAllSoLetsSeeHowThisWillFareISuppose"
    assert truncate_string(in_str, 40) == out_str
    in_str = "ThisLongTitleHasNoSpacesAtAllSoItHasAMiddleBreak"
    out_str = "ThisLongTitleHasAtAllSoItHasAMiddleBreak"
    assert truncate_string(in_str, 40) == out_str
    # TEST WHEN GIVEN STRING IS INVALID
    assert truncate_string(None, 2) == ""

def test_get_extension():
    """
    Tests the get_extension function.
    """
    # Test getting extensions from filenames
    assert get_extension("test.png") == ".png"
    assert get_extension(".long") == ".long"
    assert get_extension("test2.thing") == ".thing"
    assert get_extension("blah.test.png") == ".png"
    # Test getting extensions from URLs with tokens
    assert get_extension("test.mp4?extra_.thing") == ".mp4"
    assert get_extension("thing.test.thing?") == ".thing"
    assert get_extension("another.txt? test.png?extra.thing") == ".png"
    # Test getting invalid extensions
    assert get_extension("test.tolong") == ""
    assert get_extension("test.notextension") == ""
    assert get_extension("asdfasdfasdfasdf") == ""
    assert get_extension("test.tolong?extra") == ""
    # Test getting extension if given string is None
    assert get_extension(None) == ""

def test_get_url_directory():
    """
    Tests the get_url_directory function.
    """
    # Test getting last directory
    assert get_url_directory("a/b/c/url.txt") == "url.txt"
    assert get_url_directory("/url//test") == "test"
    # Test getting directory with ending slash
    assert get_url_directory("test/") == "test"
    assert get_url_directory("/other/thing//") == "thing"
    assert get_url_directory("///") == ""
    # Test getting directory from invalid URL
    assert get_url_directory("") == ""
    assert get_url_directory(None) == ""

def test_truncate_path():
    """
    Tests the truncate_path function.
    """
    # Test truncating paths
    assert truncate_path("/path/", "/path/file.txt") == ".../file.txt"
    assert truncate_path("main", "main/path.png") == ".../path.png"
    assert truncate_path("/a/b/c/", "/a/b/c/thing.jpg") == ".../thing.jpg"
    # Test truncating path if file is not in the given directory
    assert truncate_path("/a/b/c/", "/unrelated/f.txt") == "/unrelated/f.txt"
    assert truncate_path("/a/", "/A/file.png") == "/A/file.png"
    # Test if file and parent path are exactly the same
    assert truncate_path("/a/b/c", "/a/b/c") == "/a/b/c"
    # Test when the parent path is invalid
    assert truncate_path(None, "/other/file.txt") == "/other/file.txt"
    # Test when the file is invalid
    assert truncate_path("/path/", None) == ""
    assert truncate_path(None, None) == ""

def all_tests():
    """
    Runs all test for the string_processing module.
    """
    test_pad_num()
    test_remove_whitespace()
    test_get_filename()
    test_truncate_string()
    test_get_extension()
    test_get_url_directory()
    test_truncate_path()
    test_regex_replace()
