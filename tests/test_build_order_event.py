from pathlib import Path
import sys

from jsonschema import validate

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORDER_SERVICE_PATH = PROJECT_ROOT / "services" / "order_service"

sys.path.insert(0, str(ORDER_SERVICE_PATH))

from producer import build_order_event, load_order_schema

def test_build_order_event_produces_valid_payload() -> None:
    order_event = build_order_event("Marie", "burger", 2)
    schema = load_order_schema()

    validate(instance=order_event, schema=schema)

    assert isinstance(order_event["orderId"], str)
    assert isinstance(order_event["orderDate"], str)
    assert isinstance(order_event["user"], str)
    assert isinstance(order_event["item"], str)
    assert isinstance(order_event["quantity"], int)
    assert order_event["quantity"] >= 1