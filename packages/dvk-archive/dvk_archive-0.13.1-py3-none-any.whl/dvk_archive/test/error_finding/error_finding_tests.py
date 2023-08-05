#!/usr/bin/env python3

from dvk_archive.test.error_finding.test_same_ids import all_tests as same_ids
from dvk_archive.test.error_finding.test_missing_media import all_tests as missing
from dvk_archive.test.error_finding.test_missing_sequence_info import all_tests as missing_sequence
from dvk_archive.test.error_finding.test_unlinked_media import all_tests as unlinked
from dvk_archive.test.error_finding.test_sequence_errors import all_tests as sequencing

"""
Combined unit tests for the error_finding package
"""

def test_all():
    """
    Runs all error_finding tests.
    """
    same_ids()
    unlinked()
    missing()
    sequencing()
    missing_sequence()
