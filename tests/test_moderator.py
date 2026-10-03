import pytest

from moderator import NEGATIVE_THRESHOLD, moderate_text


def fixed_sentiment(value):
    return lambda text: value


# Decision table: banned/spam -> REJECTED, very negative -> FLAGGED, otherwise APPROVED
@pytest.mark.parametrize("text, sentiment, expected", [
    ("Have a nice day", 0.6, "APPROVED"),
    ("This is a scam", 0.0, "REJECTED"),
    ("Buy now, limited offer", 0.4, "REJECTED"),
    ("This is a scam and I am furious", -0.9, "REJECTED"),   # rules win over sentiment
    ("Everything went wrong today", -0.8, "FLAGGED"),
])
def test_decision_table(text, sentiment, expected):
    assert moderate_text(text, fixed_sentiment(sentiment))["status"] == expected


@pytest.mark.parametrize("sentiment, expected", [
    (NEGATIVE_THRESHOLD - 0.01, "FLAGGED"),
    (NEGATIVE_THRESHOLD, "FLAGGED"),          # exactly on the threshold
    (NEGATIVE_THRESHOLD + 0.01, "APPROVED"),
])
def test_sentiment_threshold_boundary(sentiment, expected):
    assert moderate_text("Neutral words only", fixed_sentiment(sentiment))["status"] == expected


def test_reasons_explain_the_decision():
    result = moderate_text("Click here, this is a scam", fixed_sentiment(-0.7))

    assert result["reasons"] == [
        "banned words: scam",
        "spam patterns: click here",
        "highly negative sentiment (-0.7)",
    ]


# Integration tests with the real VADER sentiment model
def test_real_model_approves_neutral_text():
    assert moderate_text("The weather today is quite nice")["status"] == "APPROVED"


def test_real_model_flags_very_negative_text():
    result = moderate_text("This is the worst, most terrible and awful experience")

    assert result["status"] == "FLAGGED"
    assert result["sentiment"] <= NEGATIVE_THRESHOLD
