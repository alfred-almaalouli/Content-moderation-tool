from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from rules import check_banned_words, check_spam_patterns

NEGATIVE_THRESHOLD = -0.5

analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text):
    scores = analyzer.polarity_scores(text)
    return scores["compound"]


def moderate_text(text, sentiment_fn=analyze_sentiment):
    """Returns APPROVED, FLAGGED or REJECTED with the reasons for the decision.

    sentiment_fn can be replaced in tests to check the decision logic
    without depending on the NLP model.
    """
    banned = check_banned_words(text)
    spam = check_spam_patterns(text)
    sentiment = sentiment_fn(text)

    reasons = []
    if banned:
        reasons.append(f"banned words: {', '.join(banned)}")
    if spam:
        reasons.append(f"spam patterns: {', '.join(spam)}")
    if sentiment <= NEGATIVE_THRESHOLD:
        reasons.append(f"highly negative sentiment ({sentiment})")

    if banned or spam:
        status = "REJECTED"
    elif sentiment <= NEGATIVE_THRESHOLD:
        status = "FLAGGED"
    else:
        status = "APPROVED"

    return {
        "text": text,
        "status": status,
        "sentiment": sentiment,
        "reasons": reasons
    }
