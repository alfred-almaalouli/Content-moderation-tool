import json
from collections import Counter

from moderator import moderate_text

ICONS = {"APPROVED": "✅", "FLAGGED": "⚠️", "REJECTED": "❌"}


def load_content(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file if line.strip()]


def run_moderation(filename="sample_content.txt", report="report.json"):
    results = [moderate_text(text) for text in load_content(filename)]

    for result in results:
        print(f"{ICONS[result['status']]} {result['status']} - \"{result['text']}\"")
        if result["reasons"]:
            print(f"   Reasons: {'; '.join(result['reasons'])}")

    summary = Counter(r["status"] for r in results)
    with open(report, "w") as report_file:
        json.dump({"summary": dict(summary), "results": results}, report_file, indent=2)

    print(f"\nApproved: {summary['APPROVED']} | Flagged: {summary['FLAGGED']} | "
          f"Rejected: {summary['REJECTED']}")
    print(f"📄 Report saved to {report}")
    return results


if __name__ == "__main__":
    run_moderation()
