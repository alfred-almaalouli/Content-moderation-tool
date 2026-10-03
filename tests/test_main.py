import json

from main import load_content, run_moderation


def test_load_content_skips_empty_lines(tmp_path):
    file = tmp_path / "content.txt"
    file.write_text("first\n\n  second  \n")

    assert load_content(file) == ["first", "second"]


def test_report_has_summary_and_results(tmp_path):
    content = tmp_path / "content.txt"
    content.write_text("The weather today is quite nice\nThis is a scam\n")
    report = tmp_path / "report.json"

    run_moderation(content, report)
    data = json.loads(report.read_text())

    assert data["summary"] == {"APPROVED": 1, "REJECTED": 1}
    assert [r["status"] for r in data["results"]] == ["APPROVED", "REJECTED"]
