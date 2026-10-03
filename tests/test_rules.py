import pytest

from rules import check_banned_words, check_spam_patterns


@pytest.mark.parametrize("text, expected", [
    ("This is a scam", ["scam"]),
    ("You are STUPID", ["stupid"]),
    ("spam and fraud everywhere", ["spam", "fraud"]),
    ("A normal friendly message", []),
])
def test_banned_words_are_found(text, expected):
    assert check_banned_words(text) == expected


@pytest.mark.parametrize("text", [
    "Whatever you think is fine",   # contains "hate"
    "We had scampi for dinner",     # contains "scam"
    "That was a fraudulently low price",  # whole word "fraud" is not used
])
def test_no_false_positives_inside_other_words(text):
    assert check_banned_words(text) == []


def test_spam_keywords_are_found():
    assert check_spam_patterns("Click here to get free money") == ["click here", "free money"]


@pytest.mark.parametrize("text, flagged", [
    ("THIS IS ALL IN CAPITALS", True),
    ("This Has Some Capitals", False),
    ("OK GO NOW", False),           # short texts are not checked (boundary: 10 characters)
])
def test_excessive_caps(text, flagged):
    assert ("excessive_caps" in check_spam_patterns(text)) is flagged


@pytest.mark.parametrize("text, flagged", [
    ("More info at https://example.com", False),                         # 1 link is allowed
    ("Visit https://a.example and www.b.example now", True),            # 2 links
    ("https://a.example https://b.example https://c.example", True),
])
def test_excessive_links(text, flagged):
    assert ("excessive_links" in check_spam_patterns(text)) is flagged
