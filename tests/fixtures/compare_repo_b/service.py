import json


def load_orders(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def summarize_orders(orders):
    return {"count": len(orders), "names": [item["name"] for item in orders]}
