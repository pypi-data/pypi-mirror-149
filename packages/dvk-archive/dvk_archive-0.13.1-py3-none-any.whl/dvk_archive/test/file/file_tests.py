#!/usr/bin/env python3

"""
Combined unit tests for the file package
"""

from dvk_archive.test.file.test_dvk import all_tests as test_dvk
from dvk_archive.test.file.test_dvk_handler import all_tests as test_handler
from dvk_archive.test.file.test_dvk_html import all_tests as test_dvk_html
from dvk_archive.test.file.test_reformat import all_tests as test_reformat
from dvk_archive.test.file.test_rename import all_tests as test_rename
from dvk_archive.test.file.test_sequencing import all_tests as test_sequencing
from dvk_archive.test.file.test_manual_dvk import all_tests as test_manual

def test_all():
    """
    Runs all file tests.
    """
    test_dvk()
    test_handler()
    test_manual()
    test_dvk_html()
    test_sequencing()
    test_reformat()
    test_rename()
