#!/usr/bin/env python3

from dvk_archive.main.file.dvk import Dvk
from dvk_archive.main.file.dvk_handler import DvkHandler
from dvk_archive.main.file.manual_dvk import create_dvks
from dvk_archive.main.file.manual_dvk import get_data_dvk
from dvk_archive.main.file.manual_dvk import get_data_dvks
from dvk_archive.main.file.manual_dvk import read_file_as_lines
from dvk_archive.test.temp_dir import get_test_dir
from os import mkdir, pardir
from os.path import abspath, exists, join

def test_read_file_as_lines():
    """
    Tests the read_file_as_lines function.
    """
    # Create test files
    test_dir = get_test_dir()
    one_line = abspath(join(test_dir, "one.txt"))
    with open(one_line, "w") as out_file:
        out_file.write("text")
    multiline = abspath(join(test_dir, "multi.txt"))
    with open(multiline, "w") as out_file:
        out_file.write("Line One\nNext\nThird")
    carriage = abspath(join(test_dir, "carriage.txt"))
    with open(carriage, "w") as out_file:
        out_file.write("Carriage\r\nReturn\n\rThings\r")
    # Test that files were created
    assert exists(one_line)
    assert exists(multiline)
    assert exists(carriage)
    # Test reading file with only one line
    lines = read_file_as_lines(one_line)
    assert lines == ["text"]
    # Test reading file with multiple lines
    lines = read_file_as_lines(multiline)
    assert lines == ["Line One", "Next", "Third"]
    # Test reading file with carriage returns
    lines = read_file_as_lines(carriage)
    assert lines == ["Carriage", "Return", "Things"]
    # Test reading non-existant file
    non_existant = abspath(join(test_dir, "non.txt"))
    assert read_file_as_lines(non_existant) == []
    # Test reading file with invalid parameters
    assert read_file_as_lines(None) == []
    assert read_file_as_lines() == []

def test_get_data_dvk():
    """
    Tests the get_data_dvk function.
    """
    test_dir = get_test_dir()
    file = abspath(join(test_dir, "data.txt"))
    # Test getting all data from lines
    lines = "I|sep\n\n"\
                +"A| Other A, ,Person,  Guy ,\n"\
                +"pointless text\n"\
                +"P|2022-03-12-11-26\n\r"\
                +"T| Tag , , Other, web tag , \r"\
                +"d| Test<br/>Thing \r\n"\
                +"u| /page/url/    \n"\
                +"m|  /direct/url/1  "
    with open(file, "w") as out_file:
        out_file.write(lines)
    data = get_data_dvk(file, Dvk())
    assert data.get_dvk_file() == file
    assert data.get_dvk_id() == "SEP"
    assert data.get_artists() == ["Guy", "Other A", "Person"]
    assert data.get_time() == "2022/03/12|11:26"
    assert data.get_web_tags() == ["Tag", "Other", "web tag"]
    assert data.get_description() == "Test<br/>Thing"
    assert data.get_page_url() == "/page/url/"
    assert data.get_direct_url() == "/direct/url/1"
    # Test getting data with only base Dvk
    base_dvk = Dvk()
    base_dvk.set_dvk_file("/non/existant/")
    base_dvk.set_dvk_id("dvk")
    base_dvk.set_artists(["Artist1", "Art2"])
    base_dvk.set_time("2010/05/15|22:32")
    base_dvk.set_web_tags(["Some", "Web", "Tags"])
    base_dvk.set_description("New description")
    base_dvk.set_page_url("pageurl/url")
    base_dvk.set_direct_url("/direct/")
    non_existant = abspath(join(test_dir, "nonexistant.txt"))
    data = get_data_dvk(non_existant, base_dvk)
    assert data.get_dvk_file() == non_existant
    assert data.get_dvk_id() == "DVK"
    assert data.get_artists() == ["Art2", "Artist1"]
    assert data.get_time() == "2010/05/15|22:32"
    assert data.get_web_tags() == ["Some", "Web", "Tags"]
    assert data.get_description() == "New description"
    assert data.get_page_url() == "pageurl/url"
    assert data.get_direct_url() == "/direct/"
    # Test getting data while overriding existing base data Dvk
    file = abspath(join(test_dir, "other.txt"))
    lines = "Artist| Single\n"\
                +"Published|2002/05/24\n\n"\
                +"Tags| item \r"\
                +"direct_url| new/url/"
    with open(file, "w") as out_file:
        out_file.write(lines)
    data = get_data_dvk(file, base_dvk)
    assert data.get_dvk_file() == file
    assert data.get_dvk_id() == "DVK"
    assert data.get_artists() == ["Single"]
    assert data.get_time() == "2002/05/24|00:00"
    assert data.get_web_tags() == ["item"]
    assert data.get_description() == "New description"
    assert data.get_page_url() == "pageurl/url"
    assert data.get_direct_url() == "new/url/"
    # Test getting incomplete data
    data = get_data_dvk(file, Dvk())
    assert data.get_dvk_file() == file
    assert data.get_dvk_id() is None
    assert data.get_artists() == ["Single"]
    assert data.get_time() == "2002/05/24|00:00"
    assert data.get_web_tags() == ["item"]
    assert data.get_description() is None
    assert data.get_page_url() is None
    assert data.get_direct_url() == "new/url/"
    # Test getting data Dvk with invalid parameters
    data = get_data_dvk(file, None)
    assert data.get_dvk_file() is None
    data = get_data_dvk(None, base_dvk)
    assert data.get_dvk_file() is None
    data = get_data_dvk(None, None)
    assert data.get_dvk_file() is None

def test_create_dvks():
    """
    Tests the create_dvks function.
    """
    # Create test files
    test_dir = get_test_dir()
    sub_dir = abspath(join(test_dir, "sub"))
    mkdir(sub_dir)
    page1 = abspath(join(test_dir, "Page 1.txt"))
    with open(page1, "w") as out_file:
        out_file.write("Page 1 test")
    page2 = abspath(join(test_dir, "Page 2.png"))
    with open(page2, "w") as out_file:
        out_file.write("Page 2 test")
    other = abspath(join(test_dir, "Other Page!.txt"))
    with open(other, "w") as out_file:
        out_file.write("other page TEST")
    no_extension = abspath(join(test_dir, "No Extension"))
    with open(no_extension, "w") as out_file:
        out_file.write("NO EXTENSION")
    no_dvk = abspath(join(sub_dir, "No DVK.txt"))
    with open(no_dvk, "w") as out_file:
        out_file.write("no dvk!")
    data_file = abspath(join(sub_dir, "data.txt"))
    with open(data_file, "w") as out_file:
        out_file.write("dvk_id|NEW\nArtists|Person\rPage_url|/url/12")
    assert exists(page1)
    assert exists(page2)
    assert exists(other)
    assert exists(no_extension)
    assert exists(no_dvk)
    assert exists(data_file)
    # Test creating Dvks
    base_dvk = Dvk()
    base_dvk.set_dvk_file(join(test_dir, "data.txt"))
    base_dvk.set_dvk_id("DVK")
    base_dvk.set_artists(["Other", "People"])
    base_dvk.set_time("2012/06/13|08:45")
    base_dvk.set_web_tags(["Some", "tags"])
    base_dvk.set_description("Some words")
    base_dvk.set_page_url("/url/test")
    base_dvk.set_direct_url("direct/url")
    dvks = create_dvks(base_dvk)
    assert len(dvks) == 4
    assert dvks[0].get_title() == "No Extension"
    assert dvks[0].get_dvk_id() == "DVKNO-EXTENSION"
    assert dvks[1].get_title() == "Other Page!"
    assert dvks[1].get_dvk_id() == "DVKOTHER-PAGE"
    assert dvks[2].get_title() == "Page 1"
    assert dvks[2].get_dvk_id() == "DVKPAGE-1"
    assert dvks[3].get_title() == "Page 2"
    assert dvks[3].get_dvk_id() == "DVKPAGE-2"
    assert dvks[3].get_artists() == ["Other", "People"]
    assert dvks[3].get_time() == "2012/06/13|08:45"
    assert dvks[3].get_web_tags() == ["Some", "tags"]
    assert dvks[3].get_description() == "Some words"
    assert dvks[3].get_page_url() == "/url/test"
    assert dvks[3].get_direct_url() == "direct/url"
    dvk_handler = DvkHandler(test_dir)
    dvk_handler.sort_dvks("a")
    assert dvk_handler.get_size() == 4
    assert dvk_handler.get_dvk(0).get_title() == "No Extension"
    assert dvk_handler.get_dvk(1).get_title() == "Other Page!"
    assert dvk_handler.get_dvk(2).get_title() == "Page 1"
    assert dvk_handler.get_dvk(3).get_title() == "Page 2"
    # Test that data file is deleted
    base_dvk = get_data_dvk(data_file, Dvk())
    dvks = create_dvks(base_dvk)
    assert len(dvks) == 1
    assert dvks[0].get_title() == "No DVK"
    assert dvks[0].get_dvk_id() == "NEWNO-DVK"
    assert dvks[0].get_artists() == ["Person"]
    assert dvks[0].get_time() == "0000/00/00|00:00"
    assert dvks[0].get_web_tags() == []
    assert dvks[0].get_description() is None
    assert dvks[0].get_page_url() == "/url/12"
    assert dvks[0].get_direct_url() is None
    dvk_handler = DvkHandler(sub_dir)
    assert dvk_handler.get_size() == 1
    assert dvk_handler.get_dvk(0).get_title() == "No DVK"
    assert not exists(data_file)
    # Test creating Dvks with invalid base_dvk
    base_dvk.set_dvk_id(None)
    assert create_dvks(base_dvk) == []
    assert create_dvks(None) == []

def test_get_data_dvks():
    """
    Tests the get_data_dvks function.
    """
    # Create test directories
    test_dir = get_test_dir()
    folder = abspath(join(test_dir, "folder"))
    another = abspath(join(test_dir, "another"))
    sub1 = abspath(join(another, "sub1"))
    sub2 = abspath(join(another, "sub2"))
    mkdir(folder)
    mkdir(another)
    mkdir(sub1)
    mkdir(sub2)
    # Create test files
    base_file = abspath(join(another, "dvk_data.txt"))
    lines = "dvk_id|TNG\nArtists|person"
    with open(base_file, "w") as out_file:
        out_file.write(lines)
    sub_file = abspath(join(sub1, "dvk_data.txt"))
    lines = "Time_Published|2009/08/15\r\nPage_url|/url/\nWeb_Tags|tag,other"
    with open(sub_file, "w") as out_file:
        out_file.write(lines)
    non_data = abspath(join(sub1, "blah.txt"))
    lines = "Tags|this,won't,count"
    with open(non_data, "w") as out_file:
        out_file.write(lines)
    assert exists(base_file)
    assert exists(sub_file)
    assert exists(non_data)
    # Test getting data dvks
    dvks = get_data_dvks(test_dir, Dvk())
    assert len(dvks) == 5
    # Test empty Dvks
    assert abspath(join(dvks[0].get_dvk_file(), pardir)) == test_dir
    assert dvks[0].get_dvk_id() is None
    assert abspath(join(dvks[4].get_dvk_file(), pardir)) == folder
    assert dvks[4].get_dvk_id() is None
    # Test Dvks with base info set
    assert abspath(join(dvks[1].get_dvk_file(), pardir)) == another
    assert dvks[1].get_dvk_id() == "TNG"
    assert dvks[1].get_artists() == ["person"]
    assert dvks[1].get_time() == "0000/00/00|00:00"
    assert dvks[1].get_web_tags() == []
    assert dvks[1].get_description() is None
    assert dvks[1].get_page_url() is None
    assert dvks[1].get_direct_url() is None
    assert abspath(join(dvks[3].get_dvk_file(), pardir)) == sub2
    assert dvks[3].get_dvk_id() == "TNG"
    assert dvks[3].get_artists() == ["person"]
    assert dvks[3].get_time() == "0000/00/00|00:00"
    assert dvks[3].get_web_tags() == []
    assert dvks[3].get_description() is None
    assert dvks[3].get_page_url() is None
    assert dvks[3].get_direct_url() is None
    # Test getting Dvks that override info
    assert abspath(join(dvks[2].get_dvk_file(), pardir)) == sub1
    assert dvks[2].get_dvk_id() == "TNG"
    assert dvks[2].get_artists() == ["person"]
    assert dvks[2].get_time() == "2009/08/15|00:00"
    assert dvks[2].get_web_tags() == ["tag", "other"]
    assert dvks[2].get_description() is None
    assert dvks[2].get_page_url() == "/url/"
    assert dvks[2].get_direct_url() is None
    # Test getting dvks with invalid parameters
    dvks = get_data_dvks(test_dir, None)
    assert len(dvks) == 5
    assert get_data_dvks(None, Dvk()) == []
    assert get_data_dvks("/non/existant/dir/", Dvk()) == []

def all_tests():
    """
    Runs all tests for the manual_dvk.py module.
    """
    test_read_file_as_lines()
    test_get_data_dvk()
    test_create_dvks()
    test_get_data_dvks()
