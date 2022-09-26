"""Test name-matching regular expression."""
import re

import pytest


# *** ADD YOUR PATTERN BELOW *** #
pattern = r"^[A-Z][\w\.]*(\s|,|.)\w*(\s|, |-)([A-Z][\w\.]*)+$"
if pattern == []:
    raise NotImplementedError("Add your pattern to the test file.")
# *** ADD YOUR PATTERN ABOVE *** #


test_cases = [
    ("Quan Hongchan", True),
    ("Philip Seymour Hoffman", True),
    ("Dr. Nicki Washington", True),
    ("Joseph Gordon-Levitt", True),
    ("Ken Griffey, Jr.", True),
    ("John von Neumann", True),
    ("Cher", False),
    ("not a name", False),
    ("happy feet", False),
    ("The end", False),
]


@pytest.mark.parametrize("string,matches", test_cases)
def test_name_matching(string, matches: bool):
    """Test whether pattern correctly matches or does not match input."""
    assert (re.fullmatch(pattern, string) is not None) == matches
