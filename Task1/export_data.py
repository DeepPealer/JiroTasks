import json
from decimal import Decimal
from datetime import date, datetime


def dump_json(data, filename: str):
    with open(f"{filename}.json", 'w', encoding="utf-8") as f:
        json.dump(serialize_data(data), f, ensure_ascii=False, indent=2)


def serialize_data(data):
    if isinstance(data, dict):
        return {k: serialize_data(v) for k, v in data.items()}
    elif isinstance(data, (list, tuple)):
        return [serialize_data(item) for item in data]
    elif isinstance(data, (Decimal, date, datetime)):
        return str(data)
    else:
        return data
