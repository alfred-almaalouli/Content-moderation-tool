import re

BANNED_WORDS = [
    "spam", "scam", "fraud", "hate", "stupid", "idiot"
]

SPAM_KEYWORDS = [
    "click here", "buy now", "free money", "act now", "limited offer"
]

URL_PATTERN = re.compile(r"(https?://|www\.)\S+", re.IGNORECASE)

CAPS_RATIO_LIMIT = 0.5
MIN_LENGTH_FOR_CAPS_CHECK = 10
MAX_LINKS = 1


def _contains_phrase(text, phrase):
    # whole words only, so "hate" does not match "whatever" and "scam" does not match "scampi"
    return re.search(rf"\b{re.escape(phrase)}\b", text, re.IGNORECASE) is not None


def check_banned_words(text):
    return [word for word in BANNED_WORDS if _contains_phrase(text, word)]


def check_spam_patterns(text):
    found = [kw for kw in SPAM_KEYWORDS if _contains_phrase(text, kw)]

    letters = [c for c in text if c.isalpha()]
    caps_ratio = sum(1 for c in letters if c.isupper()) / max(len(letters), 1)
    if caps_ratio > CAPS_RATIO_LIMIT and len(text) > MIN_LENGTH_FOR_CAPS_CHECK:
        found.append("excessive_caps")

    if len(URL_PATTERN.findall(text)) > MAX_LINKS:
        found.append("excessive_links")

    return found
