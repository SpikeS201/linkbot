import json


def write_json_report(page_data: dict, filename="report.json"):
    pages: list = sorted(page_data.values(), key=lambda p: p["url"])
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(pages, file, indent=2)