#!/usr/bin/env python3

from dvk_archive.main.file.dvk import Dvk
from dvk_archive.main.file.dvk_html import create_css
from dvk_archive.main.file.dvk_html import get_dvk_header_html
from dvk_archive.main.file.dvk_html import get_dvk_html
from dvk_archive.main.file.dvk_html import get_dvk_info_html
from dvk_archive.main.file.dvk_html import get_file_as_url
from dvk_archive.main.file.dvk_html import get_media_html
from dvk_archive.main.file.dvk_html import get_navbar_html
from dvk_archive.main.file.dvk_html import get_page_link_html
from dvk_archive.main.file.dvk_html import get_tag_info_html
from dvk_archive.main.file.dvk_html import get_temp_directory
from dvk_archive.main.file.dvk_html import get_time_string
from dvk_archive.main.file.dvk_html import is_image_extension
from dvk_archive.main.file.dvk_html import list_to_lines
from dvk_archive.main.file.dvk_html import write_dvk_html
from dvk_archive.main.file.dvk_html import write_dvk_html_list
from dvk_archive.test.temp_dir import get_test_dir
from os import pardir
from os.path import abspath, basename, exists, isdir, join

def test_get_file_as_url():
    """
    Tests the get_file_as_url function.
    """
    # Test getting files as URL paths
    url = get_file_as_url("/path/file/#3 Thing?.txt")
    assert url == "file:///path/file/%233%20Thing%3F.txt"
    url = get_file_as_url("C:\\dir\\Text 100%.png")
    assert url == "file://C%3A\\dir\\Text%20100%25.png"
    # Test using invalid parameters
    assert get_file_as_url("") == ""
    assert get_file_as_url(None) == ""

def test_get_temp_directory():
    """
    Tests the get_temp_directory function.
    """
    # Test getting the temporary directory.
    temp_dir = get_temp_directory(True)
    assert exists(temp_dir)
    assert isdir(temp_dir)
    assert basename(temp_dir) == "dvk_html"
    # Test getting temp directory with file already inside
    file = abspath(join(temp_dir, "file.txt"))
    assert not exists(file)
    with open(file, "w") as out_file:
        out_file.write("TEST")
    assert exists(file)
    temp_dir = get_temp_directory()
    assert exists(temp_dir)
    assert exists(file)
    # Test deleting directory
    temp_dir = get_temp_directory(True)
    assert exists(temp_dir)
    assert not exists(file)

def test_list_to_lines():
    """
    Tests the list_to_lines function.
    """
    # Test separating list of items into lines
    lines = list_to_lines(["Things", "in", "list"])
    assert lines == "Things\nin\nlist"
    lines = list_to_lines(["Item"])
    assert lines == "Item"
    # Test separating list with invalid parameters
    assert list_to_lines([]) == ""
    assert list_to_lines(None) == ""

def test_get_time_string():
    """
    Tests the get_time_string function.
    """
    # Test getting time strings with 24 hour clock
    dvk = Dvk()
    dvk.set_time("2012/01/01|13:45")
    assert get_time_string(dvk, False) == "Posted <b>01 Jan 2012 - 13:45</b>"
    dvk.set_time("2017/02/14|02:16")
    assert get_time_string(dvk, False) == "Posted <b>14 Feb 2017 - 02:16</b>"
    dvk.set_time("2009/03/30|23:05")
    assert get_time_string(dvk, False) == "Posted <b>30 Mar 2009 - 23:05</b>"
    dvk.set_time("2012/04/01|06:50")
    assert get_time_string(dvk, False) == "Posted <b>01 Apr 2012 - 06:50</b>"
    dvk.set_time("1997/05/02|13:45")
    assert get_time_string(dvk, False) == "Posted <b>02 May 1997 - 13:45</b>"
    dvk.set_time("2085/06/26|09:23")
    assert get_time_string(dvk, False) == "Posted <b>26 Jun 2085 - 09:23</b>"
    # Test getting time strings with 12 hour clock
    dvk.set_time("2156/07/24|00:30")
    assert get_time_string(dvk) == "Posted <b>24 Jul 2156 - 12:30 AM</b>"
    dvk.set_time("2012/08/01|04:02")
    assert get_time_string(dvk) == "Posted <b>01 Aug 2012 - 04:02 AM</b>"
    dvk.set_time("2012/09/01|11:45")
    assert get_time_string(dvk) == "Posted <b>01 Sep 2012 - 11:45 AM</b>"
    dvk.set_time("2012/10/01|12:23")
    assert get_time_string(dvk) == "Posted <b>01 Oct 2012 - 12:23 PM</b>"
    dvk.set_time("2012/11/01|15:30")
    assert get_time_string(dvk) == "Posted <b>01 Nov 2012 - 03:30 PM</b>"
    dvk.set_time("2012/12/01|23:15")
    assert get_time_string(dvk) == "Posted <b>01 Dec 2012 - 11:15 PM</b>"
    # Test getting time string with invalid parameters
    dvk.set_time(None)
    assert get_time_string(dvk) == "Unknown Publication Date"
    assert get_time_string(None) == "Unknown Publication Date"

def test_is_image_extension():
    """
    Tests the is_image_extension function.
    """
    # Test extensions that are images
    assert is_image_extension(".png")
    assert is_image_extension(".jpg")
    assert is_image_extension(".jpeg")
    assert is_image_extension(".gif")
    assert is_image_extension(".svg")
    assert is_image_extension(".webp")
    # Test extensions that are not images
    assert not is_image_extension(".txt")
    assert not is_image_extension(".html")
    assert not is_image_extension(".pdf")
    assert not is_image_extension(".mp4")
    # Test invalid parameters
    assert not is_image_extension("not extension")
    assert not is_image_extension("")
    assert not is_image_extension(None)

def test_get_media_html():
    """
    Tests the get_media_html function.
    """
    # Test getting media tag for Dvk with a linked image file
    test_dir = get_test_dir()
    dvk = Dvk()
    dvk.set_dvk_file(join(test_dir, "img.dvk"))
    dvk.set_title("Image DVK!")
    dvk.set_media_file("image.jpg")
    media_tag = get_media_html(dvk)
    assert "<img id=\"dvk_image\" src=\"file://" in media_tag
    assert "image.jpg" in media_tag
    assert get_file_as_url(dvk.get_media_file()) in media_tag
    assert "\" alt=\"Image DVK&#33;\">" in media_tag
    # Test getting media tag for Dvk with a linked PDF file
    dvk.set_media_file("doc.pdf")
    media_tag = get_media_html(dvk)
    assert "<iframe id=\"dvk_pdf\" src=\"file://" in media_tag
    assert "doc.pdf" in media_tag
    assert get_file_as_url(dvk.get_media_file()) in media_tag
    assert "</iframe>" in media_tag
    # Test getting media tag for Dvk with a linked text file
    dvk.set_title("TEXT!!")
    dvk.set_media_file("text.txt")
    with open(dvk.get_media_file(), "w") as out_file:
        out_file.write("Test text!!\n<html> Should remain.")
    assert get_media_html(dvk) == "<div id=\"dvk_text_media\" class=\"dvk_info\">"\
                +"\n    <div id=\"dvk_text_header\" class=\"dvk_padded\"><b>TEXT&#33;&#33;</b></div>"\
                +"\n    <div id=\"dvk_text_container\" class=\"dvk_padded\">"\
                +"\n        Test text&#33;&#33;<br/>&#60;html&#62; Should remain&#46;"\
                +"\n    </div>\n</div>"
    # Test getting media tag with secondary image
    dvk.set_media_file("html.htm")
    dvk.set_secondary_file("image.jpg")
    with open(dvk.get_media_file(), "w") as out_file:
        out_file.write("<!DOCTYPE html><html>Blah <b>stuff</b>\nMore</html>")
    text_container = "<div id=\"dvk_text_media\" class=\"dvk_info\">"\
                +"\n    <div id=\"dvk_text_header\" class=\"dvk_padded\"><b>TEXT&#33;&#33;</b></div>"\
                +"\n    <div id=\"dvk_text_container\" class=\"dvk_padded\">"\
                +"\n        Blah <b>stuff</b>\n        More\n    </div>\n</div>"
    media_html = get_media_html(dvk)
    assert text_container in media_html
    assert "<img id=\"dvk_image\" src=\"file://" in media_html
    assert "alt=\"TEXT&#33;&#33;\">" in media_html
    # Test getting media tag for Dvk whose media can't be shown in HTML
    dvk.set_secondary_file(None)
    dvk.set_media_file("media.xdf")
    assert get_media_html(dvk) == ""
    # Test getting media tag with invalid parameters
    dvk.set_media_file("thing.png")
    dvk.set_title(None)
    assert get_media_html(dvk) == ""
    dvk.set_title("Title")
    dvk.set_media_file(None)
    assert get_media_html(dvk) == ""
    assert get_media_html(None) == ""

def test_get_tag_info_html():
    """
    Tests the get_tag_info_html function.
    """
    # Test getting tag info HTML block.
    dvk = Dvk()
    dvk.set_web_tags(["Test", "tags!"])
    html = get_tag_info_html(dvk)
    assert html == "<div id=\"dvk_tag_info\" class=\"dvk_info\">"\
                +"\n    ""<div id=\"dvk_web_tag_header\" class=\"dvk_padded\"><b>Web Tags</b></div>"\
                +"\n    <div id=\"dvk_tags\" class=\"dvk_padded\">"\
                +"\n        <span class=\"dvk_tag\">Test</span>"\
                +"\n        <span class=\"dvk_tag\">tags&#33;</span>"\
                +"\n    </div>\n</div>"
    # Test getting tag info block when there are no tags
    dvk.set_web_tags(None)
    assert get_tag_info_html(dvk) == ""
    assert get_tag_info_html(None) == ""

def test_get_dvk_header_html():
    """
    Tests the get_dvk_header_html function.
    """
    # Test getting dvk_header tag
    dvk = Dvk()
    dvk.set_title("Title!")
    dvk.set_artists(["Person", "Other..."])
    dvk.set_time("2020/10/12|19:00")
    header = get_dvk_header_html(dvk)
    assert header == "<div id=\"dvk_header\" class=\"dvk_padded\">"\
                +"\n    <div id=\"dvk_title\"><b>Title&#33;</b></div>"\
                +"\n    <div id=\"dvk_pub\">By <b>Other&#46;&#46;&#46;, Person</b>, "\
                +"Posted <b>12 Oct 2020 - 07:00 PM</b></div>\n</div>"
    # Test getting dvk_header tag with no publication time
    dvk.set_title("Thing")
    dvk.set_artist("Artist")
    dvk.set_time(None)
    header = get_dvk_header_html(dvk)
    assert header == "<div id=\"dvk_header\" class=\"dvk_padded\">"\
                +"\n    <div id=\"dvk_title\"><b>Thing</b></div>"\
                +"\n    <div id=\"dvk_pub\">By <b>Artist</b>, "\
                +"Unknown Publication Date</div>\n</div>"
    # Test getting dvk_header tag with invalid parameters
    dvk.set_title(None)
    assert get_dvk_header_html(dvk) == ""
    dvk.set_title("Title")
    dvk.set_artists(None)
    assert get_dvk_header_html(dvk) == ""
    assert get_dvk_header_html(None) == ""

def test_get_dvk_info_html():
    """
    Tests the get_dvk_info_html function.
    """
    # Test getting the dvk_info_base tag
    dvk = Dvk()
    dvk.set_title("Title")
    dvk.set_artist("Artist")
    dvk.set_time("2020/10/12|19:00")
    dvk.set_description("Some words!<br/><br/>Thing")
    info = get_dvk_info_html(dvk)
    assert info == "<div id=\"dvk_info_base\" class=\"dvk_info\">"\
                +"\n    <div id=\"dvk_header\" class=\"dvk_padded\">"\
                +"\n        <div id=\"dvk_title\"><b>Title</b></div>"\
                +"\n        <div id=\"dvk_pub\">By <b>Artist</b>, "\
                +"Posted <b>12 Oct 2020 - 07:00 PM</b></div>"\
                +"\n    </div>"\
                +"\n    <div id=\"dvk_description\" class=\"dvk_padded\">"\
                +"\n        Some words&#33;<br/><br/>Thing\n    </div>"\
                +"\n</div>"
    # Test getting dvk_info_base when there is no description
    dvk.set_time(None)
    dvk.set_description(None)
    info = get_dvk_info_html(dvk)
    assert info == "<div id=\"dvk_info_base\" class=\"dvk_info\">"\
                +"\n    <div id=\"dvk_header\" class=\"dvk_padded\">"\
                +"\n        <div id=\"dvk_title\"><b>Title</b></div>"\
                +"\n        <div id=\"dvk_pub\">By <b>Artist</b>, "\
                +"Unknown Publication Date</div>\n    </div>"\
                +"\n    <div id=\"dvk_description\" class=\"dvk_padded\">"\
                +"\n        <i>No Description</i>\n    </div>\n</div>"
    # Test Invalid parameters
    dvk.set_title(None)
    assert get_dvk_info_html(dvk) == ""
    assert get_dvk_info_html(None) == ""

def test_get_page_link_html():
    """
    Tests the get_page_link_html function.
    """
    # Test getting page_link tag with three links
    dvk = Dvk()
    dvk.set_page_url("/page/url")
    dvk.set_direct_url("/direct.txt")
    dvk.set_secondary_url("/second.png")
    html = get_page_link_html(dvk)
    assert html == "<div id=\"dvk_page_links\" class=\"dvk_three_grid\">"\
                +"\n    <a class=\"dvk_link\" href=\"/page/url\">Page URL</a>"\
                +"\n    <a class=\"dvk_link\" href=\"/direct.txt\">Direct URL</a>"\
                +"\n    <a class=\"dvk_link\" href=\"/second.png\">Secondary URL</a>"\
                +"\n</div>"
    # Test getting page_link tag with two links
    dvk.set_page_url(None)
    html = get_page_link_html(dvk)
    assert html == "<div id=\"dvk_page_links\" class=\"dvk_two_grid\">"\
                +"\n    <a class=\"dvk_link\" href=\"/direct.txt\">Direct URL</a>"\
                +"\n    <a class=\"dvk_link\" href=\"/second.png\">Secondary URL</a>"\
                +"\n</div>"
    # Test getting page_link tag with single link
    dvk.set_secondary_url(None)
    html = get_page_link_html(dvk)
    assert html == "<div id=\"dvk_page_links\" class=\"dvk_one_grid\">"\
                +"\n    <a class=\"dvk_link\" href=\"/direct.txt\">Direct URL</a>"\
                +"\n</div>"
    # Test getting page_link tag with no links
    dvk.set_direct_url(None)
    assert get_page_link_html(dvk) == ""
    # Test getting page_link tag with invalid Dvk
    assert get_page_link_html(None) == ""

def test_get_navbar_html():
    # Try getting navbar html
    html = get_navbar_html("/prev/path.html", "/next?/path.html")
    assert html == "<div id=\"dvk_navbar\" class=\"dvk_two_grid\">"\
                +"\n    <a class=\"dvk_link\" href=\"file:///prev/path.html\">&lt; PREV</a>"\
                +"\n    <a class=\"dvk_link\" href=\"file:///next%3F/path.html\">NEXT &gt;</a>"\
                +"\n</div>"
    # Try getting navbar html with no previous path
    html = get_navbar_html(None, "/path/txt.html")
    assert html == "<div id=\"dvk_navbar\" class=\"dvk_two_grid\">"\
                +"\n    <span class=\"dvk_muted_link\">&lt; PREV</span>"\
                +"\n    <a class=\"dvk_link\" href=\"file:///path/txt.html\">NEXT &gt;</a>"\
                +"\n</div>"
    # Try getting navbar html with no next path
    html = get_navbar_html("/prev thing.txt", None)
    assert html == "<div id=\"dvk_navbar\" class=\"dvk_two_grid\">"\
               +"\n    <a class=\"dvk_link\" href=\"file:///prev%20thing.txt\">&lt; PREV</a>"\
               +"\n    <span class=\"dvk_muted_link\">NEXT &gt;</span>\n</div>"
    # Try getting navbar with no links
    assert get_navbar_html(None, None) == ""

def test_create_css():
    """
    Tests the create_css function.
    """
    # Test creating a CSS file
    test_dir = get_test_dir()
    css_file = create_css(test_dir)
    assert exists(css_file)
    assert basename(css_file) == "dvk_style.css"
    with open(css_file) as f:
        contents = f.read()
    assert "body {\n    background-color: " in contents
    assert "font-family: Arial, sans-serif;" in contents
    # Test creating CSS file with invalid parameters
    assert create_css("/non/existant/dir/") == ""
    assert create_css(None) == ""

def test_get_dvk_html():
    """
    Tests the get_dvk_html function.
    """
    # Create test DVK
    test_dir = get_test_dir()
    dvk = Dvk()
    dvk.set_dvk_file(join(test_dir, "file.dvk"))
    dvk.set_title("Something!")
    dvk.set_artist("Artist Person")
    dvk.set_time("2012/12/21|00:00")
    dvk.set_description("Some Words.")
    dvk.set_web_tags(["Tag", "Other"])
    dvk.set_page_url("/page/url/")
    dvk.set_direct_url("/page/direct/")
    dvk.set_secondary_url("/page/second/")
    dvk.set_media_file("media.png")
    css_file = create_css(test_dir)
    # Test getting dvk_html
    html = get_dvk_html(dvk, css_file, "/prev.html", "/next.html")
    assert html == "<!DOCTYPE html>\n<html>\n    <head>"\
                +"\n        <link rel=\"stylesheet\" type=\"text/css\" href=\""\
                + abspath(css_file) + "\">"\
                +"\n        <title>Something&#33;</title>"\
                +"\n        <meta charset=\"UTF-8\">"\
                +"\n    </head>\n    <body>\n        <div id=\"dvk_content\">"\
                +"\n            <img id=\"dvk_image\" src=\""\
                + get_file_as_url(dvk.get_media_file()) + "\" alt=\"Something&#33;\">"\
                +"\n            <div id=\"dvk_navbar\" class=\"dvk_two_grid\">"\
                +"\n                <a class=\"dvk_link\" href=\"file:///prev.html\">&lt; PREV</a>"\
                +"\n                <a class=\"dvk_link\" href=\"file:///next.html\">NEXT &gt;</a>"\
                +"\n            </div>"\
                +"\n            <div id=\"dvk_info_base\" class=\"dvk_info\">"\
                +"\n                <div id=\"dvk_header\" class=\"dvk_padded\">"\
                +"\n                    <div id=\"dvk_title\"><b>Something&#33;</b></div>"\
                +"\n                    <div id=\"dvk_pub\">By <b>Artist Person</b>, "\
                +"Posted <b>21 Dec 2012 - 12:00 AM</b></div>\n                </div>"\
                +"\n                <div id=\"dvk_description\" class=\"dvk_padded\">"\
                +"\n                    Some Words&#46;\n                </div>"\
                +"\n            </div>\n            <div id=\"dvk_tag_info\" class=\"dvk_info\">"\
                +"\n                <div id=\"dvk_web_tag_header\" class=\"dvk_padded\"><b>Web Tags</b></div>"\
                +"\n                <div id=\"dvk_tags\" class=\"dvk_padded\">"\
                +"\n                    <span class=\"dvk_tag\">Tag</span>"\
                +"\n                    <span class=\"dvk_tag\">Other</span>"\
                +"\n                </div>\n            </div>"\
                +"\n            <div id=\"dvk_page_links\" class=\"dvk_three_grid\">"\
                +"\n                <a class=\"dvk_link\" href=\"/page/url/\">Page URL</a>"\
                +"\n                <a class=\"dvk_link\" href=\"/page/direct/\">Direct URL</a>"\
                +"\n                <a class=\"dvk_link\" href=\"/page/second/\">Secondary URL</a>"\
                +"\n            </div>\n        </div>\n    </body>\n</html>"
    # Tests getting dvk_html with invalid Dvk
    assert get_dvk_html(dvk, None) == ""
    dvk.set_title(None)
    assert get_dvk_html(dvk, css_file) == ""
    assert get_dvk_html(None, css_file) == ""

def test_write_dvk_html():
    """
    Tests the write_dvk_html function.
    """
    # Test writing an HTML file from a given Dvk.
    dvk = Dvk()
    dvk.set_title("Thing")
    dvk.set_artist("Blah")
    path = write_dvk_html(dvk, "html-1.html", delete=True)
    assert exists(path)
    assert basename(abspath(join(path, pardir))) == "dvk_html"
    assert basename(path) == "html-1.html"
    with open(path) as f:
        contents = f.read()
    html = "<div id=\"dvk_pub\">By <b>Blah</b>, Unknown Publication Date</div>"
    assert html in contents
    # Test writing HTML without deleting temp directory
    new_path = write_dvk_html(dvk, "new.txt", delete=False)
    assert exists(path)
    assert exists(new_path)
    assert basename(new_path) == "new.txt"
    # Test writing HTML while deleting temp directory
    new_path = write_dvk_html(dvk, "next.html", delete=True)
    assert not exists(path)
    assert exists(new_path)
    assert basename(new_path) == "next.html"
    # Test adding navbar links
    new_path = write_dvk_html(dvk,
                filename="links.html",
                prev_path="/previous.html",
                next_path="/nxt.htm",
                delete=True)
    assert exists(new_path)
    assert basename(new_path) == "links.html"
    with open(new_path) as f:
        contents = f.read()
    html = "<a class=\"dvk_link\" href=\"file:///previous.html\">&lt; PREV</a>"
    assert html in contents
    # Test writing invalid dvks
    assert write_dvk_html(dvk, None) == ""
    dvk.set_title(None)
    assert write_dvk_html(dvk, "new") == ""
    assert write_dvk_html(None, "new") == ""

def test_write_dvk_html_list():
    # Create test Dvks
    dvk1 = Dvk()
    dvk1.set_title("Thing 1")
    dvk1.set_artist("Artist")
    dvk2 = Dvk()
    dvk2.set_title("Next")
    dvk2.set_artist("Other")
    dvk3 = Dvk()
    dvk3.set_title("Third")
    dvk3.set_artist("Person")
    # Test writing dvk HTML files
    paths = write_dvk_html_list([dvk1,dvk2,dvk3])
    assert len(paths) == 3
    assert basename(paths[0]) == "0.html"
    assert basename(paths[1]) == "1.html"
    assert basename(paths[2]) == "2.html"
    with open(paths[0]) as f:
        contents = f.read()
    assert "<span class=\"dvk_muted_link\">&lt; PREV</span>" in contents
    assert "<a class=\"dvk_link\" href=\"file://" in contents
    assert "1.html\">NEXT &gt;</a>" in contents
    with open(paths[1]) as f:
        contents = f.read()
    assert "<a class=\"dvk_link\" href=\"file://" in contents
    assert "0.html\">&lt; PREV</a>" in contents
    assert "2.html\">NEXT &gt;</a>" in contents
    with open(paths[2]) as f:
        contents = f.read()
    assert "<a class=\"dvk_link\" href=\"file://" in contents
    assert "1.html\">&lt; PREV</a>" in contents
    assert "<span class=\"dvk_muted_link\">NEXT &gt;</span>" in contents
    # Test writing Dvks with invalid parameters
    assert write_dvk_html_list([]) == []
    assert write_dvk_html_list(None) == []

def all_tests():
    """
    Runs all tests for the dvk_html.py module.
    """
    test_get_file_as_url()
    test_get_temp_directory()
    test_list_to_lines()
    test_get_time_string()
    test_is_image_extension()
    test_get_media_html()
    test_get_dvk_header_html()
    test_get_dvk_info_html()
    test_get_tag_info_html()
    test_get_page_link_html()
    test_get_navbar_html()
    test_create_css()
    test_get_dvk_html()
    test_write_dvk_html()
    test_write_dvk_html_list()
