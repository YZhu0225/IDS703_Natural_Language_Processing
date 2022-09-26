"""Test name-matching regular expression."""
import re

import pytest


# *** ADD YOUR PATTERN BELOW *** #
pattern = r"\b[a-z]{2,}ing\b"
if pattern == []:
    raise NotImplementedError("Add your pattern to the test file.")
# *** ADD YOUR PATTERN ABOVE *** #


test_cases = [
    ("harry loves to sing while showering.", True),
    (
        "swimming in the ocean has been Sharon's passion since she was five years old.",
        True,
    ),
    ("the ballerina taught us dancing", True),
    ("she is afraid of flying", True),
    ("they are capable of doing hard work.", True),
    ("sam cooked a tasty dinner yesterday.", False),
    ("i've been to paris.", False),
    ("he goes to work everyday", False),
    ("i will help you with the projet", False),
]


@pytest.mark.parametrize("string,matches", test_cases)
def test_gerund_matching(string, matches: bool):
    """Test whether pattern correctly matches or does not match input."""
    result = []
    for element in string.split():
        result.append(re.match(pattern, element))
    assert any(result) == matches
