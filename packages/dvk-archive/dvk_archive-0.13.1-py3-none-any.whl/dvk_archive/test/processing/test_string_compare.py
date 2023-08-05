#!/usr/bin/env python3

from dvk_archive.main.processing.string_compare import compare_alphanum
from dvk_archive.main.processing.string_compare import compare_sections
from dvk_archive.main.processing.string_compare import compare_strings
from dvk_archive.main.processing.string_compare import is_number_string
from dvk_archive.main.processing.string_compare import get_section

def test_compare_strings():
    """
    Tests the compare_strings function.
    """
    # Test comparing strings
    assert compare_strings("B", "a") == 1
    assert compare_strings("a", "B") == -1
    assert compare_strings("Test1", "Test2") == -1
    assert compare_strings("Same", "same") == 0
    # Test comparing invalid strings
    assert compare_strings() == 0
    assert compare_strings(None, "a") == 0
    assert compare_strings("b", None) == 0
    assert compare_strings(None, None) == 0

def test_is_number_string():
    """
    Tests the is_number_string function.
    """
    # Test simple number strings
    assert not is_number_string("Thing")
    assert not is_number_string("string")
    assert is_number_string("23")
    assert is_number_string("0.24")
    assert is_number_string("2,39")
    assert is_number_string(".9")
    assert is_number_string(",23")
    # Test strings that are combinations of numbers and text
    assert not is_number_string("Thing23")
    assert not is_number_string("Thing.5")
    assert not is_number_string("Thing20,5")
    assert not is_number_string("Thing,5")
    assert not is_number_string("30other")
    assert not is_number_string("2.5Thing")
    assert not is_number_string(",5Next")
    assert not is_number_string("0,5blah")
    # Test strings with too many or too few decimals
    assert not is_number_string("1.0.3")
    assert not is_number_string("1,6,4")
    assert not is_number_string("20.")
    assert not is_number_string("30,")
    # Tests is_number_string for invalid strings
    assert not is_number_string()
    assert not is_number_string("")
    assert not is_number_string(None)

def test_get_section():
    """
    Tests the get_section function.
    """
    assert get_section("256") == "256"
    assert get_section("Some Text") == "Some Text"
    assert get_section("Test#1 - Other") == "Test#"
    assert get_section("15 Thing") == "15"
    assert get_section("10.5") == "10.5"
    assert get_section(".25 Text") == ".25"
    assert get_section(",50.2 Thing") == ",50"
    assert get_section("..50") == "."
    assert get_section("38,,5") == "38"
    assert get_section("Test, and stuff.!") == "Test, and stuff.!"
    assert get_section("Number: .02!") == "Number: "
    assert get_section("# ,40") == "# "
    # Tests getting sections on invalid strings
    assert get_section() == ""
    assert get_section("") == ""
    assert get_section(None) == ""

def test_compare_sections():
    """
    Tests the compare_sections function.
    """
    # Test comparing numerical strings
    assert compare_sections("2.5", "2.5") == 0
    assert compare_sections("10", "1") == 1
    assert compare_sections("10.05", "010.5") == -1
    assert compare_sections(".2", ".02") == 1
    assert compare_sections("10,05", "010,5") == -1
    assert compare_sections(",2", ",02") == 1
    assert compare_sections("0000000001", "0") == 1
    assert compare_sections("12.05.03", "2") == -1
    # Test comparing standard strings
    assert compare_sections("a", "B") == -1
    assert compare_sections("", "a") == -1
    assert compare_sections("word", "") == 1
    # Test comparing numerical and standard strings
    assert compare_sections("text", "58") == 1
    assert compare_sections("24", "string") == -1
    assert compare_sections("text", ".58") == 1
    assert compare_sections(",24", "string") == -1
    # Test comparing numerical strings that are too long
    section1 = "12345678900000000000000000000000000000000000000000000"
    section2 = "12345678900000000000000000000000000000000000000000001"
    assert compare_sections(section1, section2) == -1
    section1 = "0.12345678900000000000000000000000000000000000000000000"
    section2 = "0.12345678900000000000000000000000000000000000000000001"
    assert compare_sections(section1, section2) == -1
    # Test comparing invalid strings
    assert compare_sections() == 0
    assert compare_sections("string", None) == 0
    assert compare_sections(None, "string") == 0
    assert compare_sections(None, None) == 0

def test_compare_alphanum():
    """
    Tests the compare_alphanum function.
    """
    assert compare_alphanum("B", "a") == 1
    assert compare_alphanum("a", "B") == -1
    assert compare_alphanum("Test1", "Test2") == -1
    assert compare_alphanum("string 100", "String 2") == 1
    assert compare_alphanum("Same25", "same25") == 0
    assert compare_alphanum("Test 0.5", "Test 0,05") == 1
    assert compare_alphanum("v1.2.10", "v1.2.02") == 1
    assert compare_alphanum("Thing 5 Extra", "Thing 20") == -1
    assert compare_alphanum("", "thing") == -1
    assert compare_alphanum("thing", "") == 1
    # Tests comparing invalid strings
    assert compare_alphanum() == 0
    assert compare_alphanum(None, "a") == 0
    assert compare_alphanum("b", None) == 0
    assert compare_alphanum(None, None) == 0

def all_tests():
    """
    Runs all tests for the string_compare module.
    """
    test_compare_strings()
    test_get_section()
    test_is_number_string()
    test_compare_sections()
    test_compare_alphanum()
