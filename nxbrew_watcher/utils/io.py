import json


def load_json(file):
    """Load json file"""

    with open(file, "r", encoding="utf-8") as f:
        j = json.load(f)

    return j


def save_json(data, out_file):
    """Save json in a pretty way"""

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4,
        )
