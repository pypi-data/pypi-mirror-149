#!/usr/bin/env python3

from dvk_archive.main.processing.html_processing import add_escapes
from dvk_archive.main.processing.html_processing import add_escapes_to_html
from dvk_archive.main.processing.html_processing import char_to_escape
from dvk_archive.main.processing.html_processing import clean_element
from dvk_archive.main.processing.html_processing import create_html_tag
from dvk_archive.main.processing.html_processing import escape_to_char
from dvk_archive.main.processing.html_processing import get_blocks
from dvk_archive.main.processing.html_processing import remove_html_tags
from dvk_archive.main.processing.html_processing import replace_escapes

def test_escape_to_char():
    """
    Tests the escape_to_char function.
    """
    # TEST REPLACING HTML ESCAPE CHARACTERS
    assert escape_to_char("&quot;") == "\""
    assert escape_to_char("&apos;") == "'"
    assert escape_to_char("&amp;") == "&"
    assert escape_to_char("&lt;") == "<"
    assert escape_to_char("&gt;") == ">"
    assert escape_to_char("&nbsp;") == " "
    assert escape_to_char("&#60;") == "<"
    assert escape_to_char("&#38;") == "&"
    # TEST NON-LATIN HTML ENTITIES
    assert escape_to_char("&Agrave;") == "À"
    assert escape_to_char("&Aacute;") == "Á"
    assert escape_to_char("&Auml;") == "Ä"
    assert escape_to_char("&Atilde;") == "Ã"
    assert escape_to_char("&Aring;") == "Å"
    # TEST REPLACING INVALID ESCAPE CHARACTERS
    assert escape_to_char(None) == ""
    assert escape_to_char("") == ""
    assert escape_to_char(" ") == ""
    assert escape_to_char("&;") == ""
    assert escape_to_char("&nope;") == ""
    assert escape_to_char("&#nope;") == ""
    assert escape_to_char("&#;") == ""

def test_replace_escapes():
    """
    Tests the replace_escapes function.
    """
    # TEST REPLACING HTML ESCAPE CHARACTERS IN STRING
    in_str = "&lt;i&gt;T&euml;st HTML&#60;&#47;i&#62;"
    assert replace_escapes(in_str) == "<i>Tëst HTML</i>"
    in_str = "this&that"
    assert replace_escapes(in_str) == "this&that"
    in_str = "remove&this;"
    assert replace_escapes(in_str) == "remove"
    # TEST REPLACING ESCAPE CHARACTERS IN INVALID TEST
    assert replace_escapes(None) == None

def test_char_to_escape():
    """
    Tests the char_to_escape function.
    """
    # Test converting characters into html escape characters
    assert char_to_escape("&") == "&#38;"
    assert char_to_escape("/") == "&#47;"
    assert char_to_escape("<") == "&#60;"
    # Test converting strings that are too long
    assert char_to_escape("string") == ""
    assert char_to_escape("<>") == ""
    # Test converting invalid characters
    assert char_to_escape(None) == ""
    assert char_to_escape("") == ""
    assert char_to_escape() == ""

def test_add_escapes():
    """
    Tests the add_escapes function.
    """
    # TEST REPLACING NON-STANDARD CHARACTERS WITH HTML ESCAPE CHARACTERS
    in_str = "<b>Fake tags.</b>"
    out_str = "&#60;b&#62;Fake tags&#46;&#60;&#47;b&#62;";
    assert add_escapes(in_str) == out_str
    in_str = "normal"
    assert add_escapes(in_str) == "normal"
    # TEST ADDING ESCAPE CHARACTERS TO INVALID STRING
    assert add_escapes(None) == None

def test_get_blocks():
    """
    Tests the get_blocks function.
    """
    # Test getting blocks from HTML text
    text = "<a href=\"thing\"><b>Text</b></a> block! "
    assert get_blocks(text) == ["<a href=\"thing\">", "<b>", "Text", "</b>", "</a>", " block! "]
    assert get_blocks("No HTML?") == ["No HTML?"]
    assert get_blocks("<p><b></b></i>") == ["<p>", "<b>", "</b>", "</i>"]
    assert get_blocks(" <b> </b> ") == [" ", "<b>", " ", "</b>", " "]
    # Test getting blocks with inomplete HTML blocks
    text = "thing <a href=\"other\""
    assert get_blocks(text) == ["thing <a href=\"other\""]
    text = "text> blah </i> other</p>"
    assert get_blocks(text) == ["text> blah ", "</i>", " other", "</p>"]
    # Test getting blocks with invalid text
    assert get_blocks() == []
    assert get_blocks(None) == []

def test_add_escapes_to_html():
    """
    Tests the add_escapes_to_html function.
    """
    # Test that HTML blocks are kept intact while text is converted
    in_str = "<a href=\"Sommarfågel\">Sommarfågel</a>"
    out_str = "<a href=\"Sommarfågel\">Sommarf&#229;gel</a>"
    assert add_escapes_to_html(in_str) == out_str
    in_str = "/blah! <a href=\"Sommarfågel"
    out_str = "&#47;blah&#33; &#60;a href&#61;&#34;Sommarf&#229;gel"
    assert add_escapes_to_html(in_str) == out_str
    # Test that existing escape characters remain intact
    in_str = "<b>&lt;Thing?&#33;&gt;</b>"
    out_str = "<b>&#60;Thing&#63;&#33;&#62;</b>"
    assert add_escapes_to_html(in_str) == out_str
    # Test adding escape characters to invalid string
    assert add_escapes_to_html(None) == ""

def test_clean_element():
    """
    Tests the clean_element function.
    """
    # TEST REMOVING LINE BREAKS IN ELEMENTS
    in_str = "<p> Start \r\n <b> \r Mid \n </b> \n\r End </p>"
    assert clean_element(in_str, False) == "<p> Start <b> Mid </b> End </p>"
    assert clean_element(in_str, True) == "Start <b> Mid </b> End"
    # TEST REMOVING WHITESPACE BETWEEN ELEMENT TAGS
    in_str = "<div>   Start  <i>  Mid     </i>   End     </div>"
    assert clean_element(in_str) == "<div> Start <i> Mid </i> End </div>"
    assert clean_element(in_str, True) == "Start <i> Mid </i> End"
    # TEST REMOVING WHITESPACE AT THE BEGINNING AND END OF THE GIVEN ELEMENT
    in_str = "     <span>Start<i>Mid</i>End</span> "
    assert clean_element(in_str) == "<span>Start<i>Mid</i>End</span>"
    assert clean_element(in_str, True) == "Start<i>Mid</i>End"
    # TEST REMOVING TAG ELEMENTS WHEN START AND/OR END TAGS ARE MISSING
    in_str = "A normal sentence."
    assert clean_element(in_str, True) == "A normal sentence."
    in_str = " Start <b> mid </b> End    "
    assert clean_element(in_str, True) == "Start <b> mid </b> End"
    in_str = " <p> Start <i> Mid </i> end  "
    assert clean_element(in_str, True) == "Start <i> Mid </i> end"
    in_str = "  start <b> mid </b> end </p>    "
    assert clean_element(in_str, True) == "start <b> mid </b> end"
    # TEST REMOVING TAG ELEMENTS WITH INVALID TAG
    in_str = "  < open   "
    assert clean_element(in_str, True) == "< open"
    in_str = "    open >  "
    assert clean_element(in_str, True) == "open >"
    in_str = "< single >"
    assert clean_element(in_str, True) == ""
    # TEST CLEANING AN INVALID HTML ELEMENT
    assert clean_element(None, True) == ""
    assert clean_element(None, False) == ""

def test_remove_html_tags():
    """
    Tests the remove_html_tags function.
    """
    # Test removing HTML tags
    text = "<b>some</b><p>text</p>"
    assert remove_html_tags(text) == "some text"
    text = "test <a href=\"blah\"> & </a> stuff&gt;"
    assert remove_html_tags(text) == "test   &   stuff&gt;"
    # Test removing HTML tags from text with only one type of text
    assert remove_html_tags("Other Thing") == "Other Thing"
    assert remove_html_tags("<b><i></i><b></p>") == ""
    # Test removing HTML tags that are incomplete
    text = "thing <a href=\"blah\""
    assert remove_html_tags(text) == "thing <a href=\"blah\""
    text = "other > text </b>"
    assert remove_html_tags(text) == "other > text "
    # Test removing HTML tags from invalid
    assert remove_html_tags() == ""
    assert remove_html_tags(None) == ""

def test_create_html_tag():
    """
    Tests the create_html_tag function.
    """
    # Test creating HTML Tag with no parameters or padding
    tag = create_html_tag("b", text="Bold Text!", pad_text=False)
    assert tag == "<b>Bold Text!</b>"
    tag = create_html_tag("i", text="<b>tag</b>", pad_text=False)
    assert tag == "<i><b>tag</b></i>"
    # Test creating HTML Tag with padding
    tag = create_html_tag("div", [], "Text.")
    assert tag == "<div>\n    Text.\n</div>"
    tag = create_html_tag("span", text="<b>\n    Thing\n</b>")
    assert tag == "<span>\n    <b>\n        Thing\n    </b>\n</span>"
    # Test creating HTML Tag with tag attributes
    tag = create_html_tag("a", [["href", "/url/"]], "Link", pad_text=False)
    assert tag == "<a href=\"/url/\">Link</a>"
    attr = [["id", "Name"], ["class", "Thing"]]
    tag = create_html_tag("div", attr, "Text!", pad_text=False)
    assert tag == "<div id=\"Name\" class=\"Thing\">Text!</div>"
    # Test creating HTML tag with attributes and padding
    tag = create_html_tag("div", [["id", "thing"]], "<b>\n    Text\n</b>")
    assert tag == "<div id=\"thing\">\n    <b>\n        Text\n    </b>\n</div>"
    # Test creating HTML tag with no end tag
    tag = create_html_tag("hr")
    assert tag == "<hr>"
    tag = create_html_tag("meta", [["thing","other"]])
    assert tag == "<meta thing=\"other\">"
    # Test creating HTML tag with invalid parameters
    assert create_html_tag(None, [["id", "thing"]], "text") == ""
    assert create_html_tag("a", [[None, "thing"]], "text") == ""
    assert create_html_tag("a", [["id", None]], "text") == ""
    assert create_html_tag("a", [[], []], "text") == ""

def all_tests():
    """
    Runs all tests for the html_processing module.
    """
    test_escape_to_char()
    test_replace_escapes()
    test_char_to_escape()
    test_add_escapes()
    test_get_blocks()
    test_add_escapes_to_html()
    test_clean_element()
    test_remove_html_tags()
    test_create_html_tag()

