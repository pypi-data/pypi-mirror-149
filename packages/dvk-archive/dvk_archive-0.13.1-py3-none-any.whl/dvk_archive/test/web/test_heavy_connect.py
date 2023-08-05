#!/usr/bin/env python3

from bs4 import BeautifulSoup
from dvk_archive.main.web.heavy_connect import HeavyConnect
from dvk_archive.test.temp_dir import get_test_dir
from os import stat
from os.path import abspath, exists, join

def test_download():
    """
    Tests the download method.
    """
    connect = HeavyConnect()
    try:
        # Test downloading a given file
        test_dir = get_test_dir()
        file = abspath(join(test_dir, "image.jpg"))
        url = "https://www.pythonscraping.com/img/gifts/img6.jpg"
        connect.download(url, file)
        assert exists(file)
        assert stat(file).st_size == 39785
        file = abspath(join(test_dir, "next.jpg"))
        url = "http://www.pythonscraping.com/img/gifts/img4.jpg"
        connect.download(url, file)
        assert exists(file)
        assert stat(file).st_size == 85007
        # Test downloading with invalid parameters
        file = join(test_dir, "invalid.jpg")
        connect.download(None, None)
        assert not exists(file)
        connect.download(None, file)
        assert not exists(file)
        connect.download("asdfasdf", file)
        assert not exists(file)
        connect.download(url, None)
        assert not exists(file)
    finally:
        connect.close_driver()

def test_get_page():
    """
    Tests the get_page method.
    """
    # Test loading elements from a web page
    connect = HeavyConnect()
    try:
        url = "https://pythonscraping.com/exercises/exercise1.html"
        page = connect.get_page(url)
        assert page is not None
        assert page.find("h1").get_text() == "An Interesting Title"
        assert page.find("title").get_text() == "A Useful Page"
        # Test waiting for element
        url = "https://pythonscraping.com/pages/javascript/ajaxDemo.html"
        page = connect.get_page(url, "//button[@id='loadedButton']")
        assert page is not None
        element = page.find("button", {"id":"loadedButton"}).get_text()
        assert element  == "A button to click!"
        # Test waiting for non-existant element
        url = "https://pythonscraping.com/exercises/exercise1.html"
        page = connect.get_page(url, "//a[href='non-existant']")
        assert page is None
        # Test loading with invalid URL
        page = connect.get_page(None, None)
        assert page is None
        url = "qwertyuiopasdfghjkl"
        page = connect.get_page(url, None)
        assert page is None
    finally:
        # Close driver
        connect.close_driver()

def test_get_json():
    """
    Tests the get_json function.
    """
    connect = HeavyConnect()
    try:
        # Test loading page as a JSON object
        json = connect.get_json("https://jsonplaceholder.typicode.com/users/3/posts")
        assert len(json) == 10
        element = json[0]
        assert element["userId"] == 3
        assert element["id"] == 21
        assert element["title"] == "asperiores ea ipsam voluptatibus modi minima quia sint"
        # Test loading an invalid page
        json = connect.get_json("asdfghjkl")
        assert json is None
        json = connect.get_json(None)
        assert json is None
    finally:
        connect.close_driver()

def all_tests():
    """
    Runs all tests for the heavy_connect module.
    """
    test_get_json()
    test_get_page()
    test_download()
