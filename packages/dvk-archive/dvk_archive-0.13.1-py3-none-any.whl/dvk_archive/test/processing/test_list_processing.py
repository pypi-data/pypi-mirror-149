#!/usr/bin/env python3

from dvk_archive.main.processing.list_processing import clean_list
from dvk_archive.main.processing.list_processing import list_to_string

def test_clean_list():
    """
    Tests the clean_list function.
    """
    # Test cleaning list
    lst = clean_list(["these", "are", "things", None, "are"])
    assert lst == ["these", "are", "things"]
    lst = clean_list([None, None, "Not", "not", "same", "Same", "but", "but", "but"])
    assert lst == ["Not", "not", "same", "Same", "but"]
    # Test removing empty strings from list
    lst = clean_list(["", "Item", "", "next", None])
    assert lst == ["Item", "next"]
    # Test removing whitespace from list
    lst = clean_list(["   ", "  Other", " Items  ", "whitespace   ", "    "], True)
    assert lst == ["Other", "Items", "whitespace"]
    lst = clean_list(["   ", "  Other", " Items  ", "whitespace   ", "    "], False)
    assert lst == ["   ", "  Other", " Items  ", "whitespace   ", "    "]
    # Test cleaning an invalid list
    assert clean_list(None) == []
    assert clean_list() == []

def test_list_to_string():
    """
    Tests the list_to_string function.
    """
    # Test getting strings with no indent
    string = list_to_string(["List", "of", "items!"])
    assert string == "List,of,items!"
    # Test getting string with indent
    string = list_to_string(["things", "stuff!"], indent=1)
    assert string == "things, stuff!"
    string = list_to_string(["some", "more", "Things."], indent=4)
    assert string == "some,    more,    Things."
    # Test getting string with invalid indent value
    string = list_to_string(["False", "Indent"], indent=-1)
    assert string == "False,Indent"
    string = list_to_string(["other", "indent", "value"], indent=-29)
    assert string == "other,indent,value"
    # Test adding escape characters to items
    string = list_to_string(["item!", ",,", "Other Item"], True)
    assert string == "item&#33;,&#44;&#44;,Other Item"
    string = list_to_string(["Don't", "forget", "Escapes!"], True, 1)
    assert string == "Don&#39;t, forget, Escapes&#33;"
    # Test getting string with invalid list
    assert list_to_string([]) == ""
    assert list_to_string(None) == ""

def all_tests():
    """
    Runs all tests for the list_processing module:
    """
    test_clean_list()
    test_list_to_string()

