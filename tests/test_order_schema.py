import json

from pathlib import Path
from jsonschema import validate

def load_schema() -> dict:
    project_root = Path(__file__).resolve().parents[1]
    schema_path = project_root / "schemas" / "order-created.json"

    with schema_path.open("r", encoding="utf-8") as schema_file:
        return json.load(schema_file)

def test_valid_order_event_matches_schema() -> None:
    schema = load_schema()

    valid_order_event = {
        "orderId": "8e88d6b8-6844-4ed9-b840-d30fb62f5802",
        "orderDate": "2026-03-09T15:35:00+00:00",
        "user": "Olivier",
        "item": "margarita",
        "quantity": 2,
    }

    validate(instance=valid_order_event, schema=schema)