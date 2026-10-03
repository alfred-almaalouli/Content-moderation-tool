# Content Moderation Tool

![Tests](https://github.com/alfred-almaalouli/Content-moderation-tool/actions/workflows/tests.yml/badge.svg)

A Python tool that automatically reviews short texts (comments, posts, messages) and decides whether they are **APPROVED**, **FLAGGED** for human review or **REJECTED**. It combines rule-based filtering with NLP sentiment analysis (VADER) and explains every decision.

The idea comes from my 6 years of work in content moderation: clear rules for obvious violations, and a "second look" for content that is not clearly against the rules but very negative.

## How a decision is made

| Condition | Result |
|-----------|--------|
| Contains a banned word or a spam pattern | **REJECTED** |
| No rule violation, but sentiment score ≤ -0.5 | **FLAGGED** (human review) |
| Everything else | **APPROVED** |

Checks:

- **Banned words** – matched as whole words only, so "whatever" does not trigger "hate" and "scampi" does not trigger "scam"
- **Spam keywords** – e.g. "click here", "buy now", "free money"
- **Excessive capitals** – more than 50 % capital letters (texts longer than 10 characters)
- **Excessive links** – more than one link in a text
- **Sentiment** – VADER compound score from -1 (very negative) to +1 (very positive)

## How to run

```bash
pip install -r requirements.txt
python main.py
```

The tool reads `sample_content.txt` (one text per line), prints every decision with its reasons and saves a JSON report with a summary:

```
❌ REJECTED - "CLICK HERE NOW FOR FREE MONEY!!!"
   Reasons: spam patterns: click here, free money, excessive_caps
⚠️ FLAGGED - "This is the worst, most terrible and awful experience"
   Reasons: highly negative sentiment (...)
✅ APPROVED - "Whatever happens, I will stay positive"
```

## Tests

```bash
pytest -v
```

The test suite uses **pytest** with test design techniques from software testing:

- **Decision table** tests for the APPROVED / FLAGGED / REJECTED logic
- **Boundary value** tests around the sentiment threshold (-0.51, -0.5, -0.49), the 10-character caps check and the link limit
- **Negative tests** for false positives (banned words inside other words)
- The sentiment function can be replaced with a fixed value in tests, so the decision logic is tested independently from the NLP model; separate integration tests use the real VADER model

All tests run automatically with **GitHub Actions** on every push.

## Project structure

```
rules.py        banned words, spam keywords, caps and link checks
moderator.py    sentiment analysis and final decision
main.py         reads the input file, prints results, writes report.json
tests/          unit and integration tests
```

## Tech stack

Python · VADER sentiment (NLP) · regular expressions · pytest · GitHub Actions
