#!/usr/bin/env/ python3

from dvk_archive.main.file.dvk import Dvk
from dvk_archive.main.file.dvk_handler import DvkHandler
from dvk_archive.main.processing.boolean_search import add_escapes_to_logic
from dvk_archive.main.processing.boolean_search import get_arg_value
from dvk_archive.main.processing.boolean_search import get_logic
from dvk_archive.main.processing.boolean_search import get_logic_from_string
from dvk_archive.main.processing.boolean_search import is_string
from dvk_archive.main.processing.boolean_search import fix_logic
from dvk_archive.main.processing.boolean_search import logic_to_lower
from dvk_archive.main.processing.boolean_search import search_dvks
from dvk_archive.main.processing.boolean_search import search_string
from dvk_archive.main.processing.boolean_search import separate_into_chunks
from dvk_archive.test.temp_dir import get_test_dir
from os.path import join

def test_separate_into_chunks():
    """
    Tests the separate into chunks method.
    """
    # Test standard strings and getting operators
    chunks = separate_into_chunks("  This  And test   ")
    assert chunks == ["This", "&", "test"]
    chunks = separate_into_chunks(" NOT word or other ")
    assert chunks == ["!", "word", "|", "other"]
    chunks = separate_into_chunks("No operators here")
    assert chunks == ["No", "operators", "here"]
    # Test using operator symbols
    chunks = separate_into_chunks("!test  &  -word  or - next")
    assert chunks == ["!", "test", "&", "!","word", "|", "!", "next"]
    chunks = separate_into_chunks("blah &other +word & stuff")
    assert chunks == ["blah", "&", "other", "&", "word", "&", "stuff"]
    chunks = separate_into_chunks("this |that ~other ~ thing")
    assert chunks == ["this", "|", "that", "|", "other", "|", "thing"]
    chunks = separate_into_chunks("[thing & ( other thing )]")
    assert chunks == ["(", "thing", "&", "(", "other", "thing", ")", ")"]
    # Test having strings within quotations
    chunks = separate_into_chunks("\" ('keep all!') \" & \"~-[]&\"")
    assert chunks == [" ('keep all!') ", "&", "~-[]&"]
    chunks = separate_into_chunks("' thing = stuff' ~'whatever '")
    assert chunks == [" thing = stuff", "|", "whatever "]
    chunks = separate_into_chunks(" = \"things\" = or =!&|=")
    assert chunks == [" \"things\" ", "|", "!&|"]
    # Test with incomplete quotations
    chunks = separate_into_chunks("thing & \"stuff & =whatever= | thing")
    assert chunks == ["thing", "&", "stuff & =whatever= | thing"]
    chunks = separate_into_chunks("'word & \"next\" word")
    assert chunks == ["word & \"next\" word"]
    chunks = separate_into_chunks("thing =word & stuff")
    assert chunks == ["thing", "word & stuff"]
    # Test strings within parans
    chunks = separate_into_chunks("(words and stuff) or [thing]")
    assert chunks == ["(", "words", "&", "stuff", ")", "|", "(", "thing", ")"]
    # Test using invalid parameters
    assert separate_into_chunks("") == []
    assert separate_into_chunks(None) == []

def test_is_string():
    """
    Tests the is_string function.
    """
    # Test operators
    assert not is_string("&")
    assert not is_string("!")
    assert not is_string("|")
    assert not is_string("(")
    assert not is_string(")")
    # Test normal strings
    assert is_string("String")
    assert is_string("thing")
    # Test strings with operators
    assert is_string("&thing")
    assert is_string("!thing")
    assert is_string("|thing")
    assert is_string("(thing")
    assert is_string(")thing")
    # Test invalid input
    assert not is_string(None)

def test_fix_logic():
    """
    Tests the fix_logic function.
    """
    # Test removing leading and trailing opreators
    fixed = fix_logic(["&", "|", "!", "thing", "|", "|", "&", "!"])
    assert fixed == ["!", "thing"]
    fixed = fix_logic(["&", "!", "|", "&"])
    assert fixed == []
    # Test fixing incomplete parenthesis pairs
    fixed = fix_logic(["(", "thing", "&", "next", "|", "(", "word"])
    assert fixed == ["(", "thing", "&", "next", "|", "(", "word", ")", ")"]
    fixed = fix_logic(["word", ")", "|", "next", ")"])
    assert fixed == ["(", "(", "word", ")", "|", "next", ")"]
    fixed = fix_logic(["(", "word", ")", "&", "next", ")"])
    assert fixed == ["(", "(", "word", ")", "&", "next", ")"]
    fixed = fix_logic(["(", "blah", ")", "|", "thing", ")"])
    assert fixed == ["(", "(", "blah", ")", "|", "thing", ")"]
    fixed = fix_logic(["test", ")", "&", "(", "word"])
    assert fixed == ["(", "test", ")", "&", "(", "word", ")"]
    # Test adding AND operator to unlinked logic statements
    fixed = fix_logic(["word", "next"])
    assert fixed == ["word", "&", "next"]
    fixed = fix_logic(["(", "thing", ")", "word"])
    assert fixed == ["(", "thing", ")", "&", "word"]
    fixed = fix_logic(["(", "word", ")", "(", "next", ")"])
    assert fixed == ["(", "word", ")", "&", "(", "next", ")"]
    fixed = fix_logic(["thing", "(", "word", ")"])
    assert fixed == ["thing", "&", "(", "word", ")"]
    fixed = fix_logic(["word", "!", "other"])
    assert fixed == ["word", "&", "!", "other"]
    fixed = fix_logic(["(", "thing", ")", "!", "word"])
    assert fixed == ["(", "thing", ")", "&", "!", "word"]
    # Test adding empty strings to hanging AND operator
    fixed = fix_logic(["word", "&", "&", "other"])
    assert fixed == ["word", "&", "", "&", "other"]
    fixed = fix_logic(["thing", "&", "|", "next"])
    assert fixed == ["thing", "&", "", "|", "next"]
    # Test adding empty strings to hanging OR operator
    fixed = fix_logic(["word", "|", "&", "other"])
    assert fixed == ["word", "|", "", "&", "other"]
    fixed = fix_logic(["thing", "|", "|", "next"])
    assert fixed == ["thing", "|", "", "|", "next"]
    # Test adding empty strings to hanging NOT operator
    fixed = fix_logic(["!", "&", "other"])
    assert fixed == ["!", "", "&", "other"]
    fixed = fix_logic(["!", "|", "word"])
    assert fixed == ["!", "", "|", "word"]
    fixed = fix_logic(["!", "!", "thing"])
    assert fixed == ["!", "", "!", "thing"]
    # Test invalid parameters
    assert fix_logic([]) == []
    assert fix_logic(None) == []

def test_get_logic():
    """
    Tests the get_logic method.
    """
    # Test simple logic statements
    logic = get_logic(["thing"])
    assert logic == ["thing", False, None, False, None]
    logic = get_logic(["word", "&", "!", "other"])
    assert logic == ["word", False, "other", True, "&"]
    # Test longer non-nested logic
    logic = get_logic(["!", "this", "&", "!", "that", "|", "!", "other"])
    assert logic == ["this", True, ["that", True, "other", True, "|"], False, "&"]
    # Test nested logic
    logic = get_logic(["!", "(", "Thing", "&", "!", "other", ")", "|", "Last"])
    assert logic == [["Thing", False, "other", True, "&"], True, "Last", False, "|"]
    logic = get_logic(["(", "what", "&", "word", ")", "|", "!", "(", "!", "this", "&", "that", ")"])
    assert logic == [["what", False, "word", False, "&"], False,
                     [["this", True, "that", False, "&"], True, None, False, None], False, "|"]
    # Test very nested logic
    logic = get_logic(["(", "(", "(", "this", ")", "&", "!", "(", "that", ")", ")", ")"])
    assert logic == [["this", False, None, False, None], False,
                     [["that", False, None, False, None], True, None, False, None], False, "&"]
    # Test with invalid parameters
    assert get_logic(None) == []
    assert get_logic([]) == []
    assert get_logic(["(", ")"]) == []
    assert get_logic(["not", "chunks"]) == []

def test_get_logic_from_string():
    """
    Tests the get_logic_from_string function.
    """
    # Test simple logic statements
    logic = get_logic_from_string("test")
    assert logic == ["test", False, None, False, None]
    logic = get_logic_from_string("-word =Small String!=")
    assert logic == ["word", True, "Small String!", False, "&"]
    # Test nested logic
    logic = get_logic_from_string("[word and not thing] OR other")
    assert logic == [["word", False, "thing", True, "&"], False, 'other', False, '|']
    # Test the to_lower parameter
    logic = get_logic_from_string("[WORD and not tHiNg] OR Other", True)
    assert logic == [["word", False, "thing", True, "&"], False, 'other', False, '|']
    # Test invalid parameters
    assert get_logic_from_string(None) == []
    assert get_logic_from_string("") == []

def test_logic_to_lower():
    """
    Tests the logic_to_lower function.
    """
    # Test converting simple logic list
    logic = get_logic_from_string("THING")
    assert logic == ["THING", False, None, False, None]
    logic = logic_to_lower(logic)
    assert logic == ["thing", False, None, False, None]
    logic = get_logic_from_string("Test !\"STRING!\"")
    assert logic == ["Test", False, "STRING!", True, "&"]
    logic = logic_to_lower(logic)
    assert logic == ["test", False, "string!", True, "&"]
    # Test converting nested logic
    logic = get_logic_from_string("(Word & Thing) | (!OTHER & (next | Object))")
    assert logic == [["Word", False, "Thing", False, "&"], False, ["OTHER", True,
                ["next", False, "Object", False, "|"], False, "&"], False, "|"]
    logic = logic_to_lower(logic)
    assert logic == [["word", False, "thing", False, "&"], False, ["other", True,
                ["next", False, "object", False, "|"], False, "&"], False, "|"]
    # Test converting with invalid parameters
    assert logic_to_lower(None) == []
    assert logic_to_lower(["word", "word"]) == []

def test_add_escapes_to_logic():
    """
    Tests the add_escapes_to_logic function.
    """
    # Test adding escapes to simple logic
    logic = get_logic_from_string("=Thing!!=")
    assert logic == ["Thing!!", False, None, False, None]
    logic = add_escapes_to_logic(logic)
    assert logic == ["Thing&#33;&#33;", False, None, False, None]
    logic = get_logic_from_string("test !,,,")
    assert logic == ["test", False, ",,,", True, "&"]
    logic = add_escapes_to_logic(logic)
    assert logic == ["test", False, "&#44;&#44;&#44;", True, "&"]
    # Test adding escapes to nested logic
    logic = get_logic_from_string("('Word!' & Thing) | (!part; & (=Don't= | 'Object!'))")
    assert logic == [["Word!", False, "Thing", False, "&"], False,
                ["part;", True, ["Don't", False, "Object!", False, "|"], False, "&"], False, "|"]
    logic = add_escapes_to_logic(logic)
    assert logic == [["Word&#33;", False, "Thing", False, "&"], False,
                ["part&#59;", True, ["Don&#39;t", False, "Object&#33;", False, "|"], False, "&"], False, "|"]
    # Test adding escapes with commas
    logic = get_logic_from_string(",, | (This and !=that,thing!=)")
    assert logic == [",,", False, ["This", False, "that,thing!", True, "&"], False, "|"]
    logic = add_escapes_to_logic(logic, True)
    assert logic == [",&#44;&#44;,", False, [",This,", False, ",that&#44;thing&#33;,", True, "&"], False, "|"]
    # Test adding escapes with invalid parameters
    assert add_escapes_to_logic(None) == []
    assert add_escapes_to_logic(["word", "word"]) == []

def test_get_arg_value():
    """
    Tests the get_arg_value function.
    """
    # Test finding search in string
    assert get_arg_value("string", False, "This is a string", False)
    assert not get_arg_value("blah", False, "This is a string", False)
    assert not get_arg_value("IS", False, "This is a string", False)
    # Test finding exact match for a string
    assert get_arg_value("thing", False, "thing", True)
    assert not get_arg_value("Thing", False, "thing", True)
    assert not get_arg_value("t", False, "thing", True)
    # Test inverting value
    assert get_arg_value("blah", True, "not contains", False)
    assert not get_arg_value("s", True, "string", False)
    assert get_arg_value("word", True, "other", True)
    assert not get_arg_value("word", True, "word", True)
    # Test nested search value
    logic = get_logic_from_string("word")
    assert get_arg_value(logic, False, "word & stuff", False)
    assert not get_arg_value(logic, True, "words", False)
    assert not get_arg_value(logic, False, "thing", False)
    assert get_arg_value(logic, False, "word", True)
    assert not get_arg_value(logic, True, "word", True)
    assert not get_arg_value(logic, False, "word thing", True)
    # Test with empty value
    assert get_arg_value("", False, "thing", False)
    assert not get_arg_value("", False, "thing", True)
    # Test invalid paramers
    assert not get_arg_value(None, False, "thing", True)
    assert not get_arg_value("thing", False, None, True)
    assert not get_arg_value([], False, "thing", True)

def test_search_string():
    """
    Tests the search_string function.
    """
    # Test search with single argument
    logic = get_logic_from_string("!word")
    assert search_string(logic, "blah", True)
    assert not search_string(logic, "word", True)
    # Test more complex search
    logic = get_logic_from_string("(thing ~ other) & (Word ~ last) & !this")
    assert not search_string(logic, "thing", False)
    assert not search_string(logic, "other", False)
    assert not search_string(logic, "thing other", False)
    assert not search_string(logic, "word last", False)
    assert not search_string(logic, "thing word", False)
    assert search_string(logic, "thing Word other", False)
    assert search_string(logic, "other last blah", False)
    assert search_string(logic, "other Word", False)
    assert not search_string(logic, "other Word this", False)
    # Test exact match
    logic = get_logic_from_string("(this | that) | (!this & thing)")
    assert not search_string(logic, "word", True)
    assert not search_string(logic, "this that", True)
    assert not search_string(logic, "Thing", True)
    assert search_string(logic, "this", True)
    assert search_string(logic, "that", True)
    assert search_string(logic, "thing", True)
    # Test empty search
    logic = get_logic_from_string("== and ==")
    assert search_string(logic, "blah words", False)
    assert not search_string(logic, "blah words", True)
    # Test invalid parameters
    assert not search_string(get_logic(""), "thing", False)
    assert not search_string(get_logic(None), "thing", False)
    assert not search_string(None, "this", True)
    assert not search_string(logic, None, True)

def test_search_dvks():
    """
    Tests the search_dvks function.
    """
    # Create Test Dvks
    test_dir = get_test_dir()
    basic = Dvk()
    basic.set_dvk_file(join(test_dir, "basic.dvk"))
    basic.set_dvk_id("BSE123")
    basic.set_title("Basic")
    basic.set_artist("person")
    basic.set_page_url("https://hopefullynonexistant.io")
    basic.set_media_file("media.txt")
    basic.write_dvk()
    full = Dvk()
    full.set_dvk_file(join(test_dir, "full.dvk"))
    full.set_dvk_id("FLL246")
    full.set_title("Full")
    full.set_artists(["Person", "Other", "artist"])
    full.set_description("Don't forget the <b>escapes</b>, okay!")
    full.set_web_tags(["tags", "Punctuation!!", ",commas,"])
    full.set_page_url("http://othersite.pizza/page/")
    full.set_media_file("thing.txt")
    full.write_dvk()
    other = Dvk()
    other.set_dvk_file(join(test_dir, "other.dvk"))
    other.set_dvk_id("OTH987")
    other.set_title("Other full")
    other.set_artists(["Artist", "Name!"])
    other.set_description("Okay, plain description.")
    other.set_web_tags(["tag", "Thing"])
    other.set_page_url("HTTP://othersite.pizza/")
    other.set_media_file("other.txt")
    other.write_dvk()
    last = Dvk()
    last.set_dvk_file(join(test_dir, "last.dvk"))
    last.set_dvk_id("LST123")
    last.set_title("Last File")
    last.set_artists([",,,", "Comma Guy"])
    last.set_description("<a href=\"notrealurl\">Last one!</a>")
    last.set_web_tags(["Tag", "Time!"])
    last.set_page_url("http://brokenlink.notrealsite")
    last.set_media_file("last.txt")
    last.write_dvk()
    # Test that Dvks were written correctly
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    assert dvk_handler.get_size() == 4
    assert dvk_handler.get_dvk(0).get_title() == "Basic"
    assert dvk_handler.get_dvk(1).get_title() == "Full"
    assert dvk_handler.get_dvk(2).get_title() == "Last File"
    assert dvk_handler.get_dvk(3).get_title() == "Other full"
    # Test searching by title
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=False,
                title_search="FuLL & l",
                title_exact=False)
    assert indexes == [1,3]
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=True,
                title_search="full",
                title_exact=False)
    assert indexes == [3]
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=False,
                title_search="other | basic",
                title_exact=True)
    assert indexes == [0]
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=False,
                title_search="full",
                title_exact=True)
    assert indexes == [1]
    # Test searching by artist
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=False,
                artist_search="art & !blah",
                artist_exact=False)
    assert indexes == [1, 3]
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=True,
                artist_search="pers",
                artist_exact=False)
    assert indexes == [0]
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=False,
                artist_search="art | person",
                artist_exact=True)
    assert indexes == [0, 1]
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=True,
                artist_search=",,, | =Name!= | Oth | other",
                artist_exact=True)
    assert indexes == [2, 3]
    # Test searching by web tags
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=False,
                web_tag_search="tag & (pun | tim)",
                web_tag_exact=False)
    assert indexes == [1, 2]
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=True,
                web_tag_search="Tag | commas,",
                web_tag_exact=False)
    assert indexes == [1, 2]
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=False,
                web_tag_search="tag",
                web_tag_exact=True)
    assert indexes == [2, 3]
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=True,
                web_tag_search="Tag",
                web_tag_exact=True)
    indexes == [3]
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=False,
                web_tag_search="punct | time! | thin",
                web_tag_exact=True)
    assert indexes == [2]
    # Test searching by description
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=False,
                desc_search="(last | okay,)& !notrealurl",
                desc_exact=False)
    assert indexes == [2, 3]
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=True,
                desc_search="Okay",
                desc_exact=False)
    assert indexes == [3]
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=False,
                desc_search="/b | NOTREALURL",
                desc_exact=True)
    assert indexes == [1, 2]
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=True,
                desc_search="<B> | ('href=\"' & one&#33;)",
                desc_exact=True)
    assert indexes == [2]
    # Test searching by page_url
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=False,
                url_search="Othersite.PIZZA/ & http",
                url_exact=False)
    assert indexes == [1, 3]
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=True,
                url_search="http://othersite.pizza/",
                url_exact=False)
    assert indexes == [1]
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=True,
                url_search="http://brokenlink.notrealsite | othersite",
                url_exact=True)
    assert indexes == [2]
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=False,
                url_search="http://Othersite.PIZZA/ | nothing",
                url_exact=True)
    assert indexes == [3]
    # Test searching by multiple parameters at once
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=False,
                title_search="full",
                artist_search="!other")
    assert indexes == [3]
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=False,
                web_tag_search="PUNCTUATION!",
                desc_search="okay")
    assert indexes == [1]
    indexes = search_dvks(dvk_handler=dvk_handler,
                case_sensitive=False,
                title_search="FULL",
                url_search="!page")
    assert indexes == [3]
    # Test searching with invalid parameters
    indexes = search_dvks(dvk_handler=None,
                case_sensitive=False,
                title_search="FuLL & l",
                title_exact=False)
    assert indexes == []

def all_tests():
    """
    Runs all tests for the html_processing module
    """
    test_separate_into_chunks()
    test_is_string()
    test_fix_logic()
    test_get_logic()
    test_get_logic_from_string()
    test_logic_to_lower()
    test_add_escapes_to_logic()
    test_get_arg_value()
    test_search_string()
    test_search_dvks()
