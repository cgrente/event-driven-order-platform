import os
import datetime
import json
import uuid
from pathlib import Path

from confluent_kafka import Producer
from jsonschema import validate
from jsonschema.exceptions import ValidationError

def build_producer() -> Producer:
    """
    Build a Kafka producer using environment-driven configuration.

    The default bootstrap server targets the host listener because this script
    is intended to be runnable directly from the local machine during
    development.
    """
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092")

    config = {
        "bootstrap.servers": bootstrap_servers,
        "client.id": "order_service-producer",
        "acks": "all",
        "message.timeout.ms": 10000,
    }

    return Producer(config)

def build_order_event(user, item, quantity) -> dict:
    """
    Build a sample order-created event.

    In a real application this would likely come from an API request body,
    a database write result, or an internal domain event.
    """
    return {
        "orderId": str(uuid.uuid4()),
        "orderDate": datetime.datetime.now(datetime.UTC).isoformat(),
        "user": user,
        "item": item,
        "quantity": quantity,
    }

def load_order_schema() -> dict:
    """
    Load the JSON schema used to validate outgoing order-created events.

    Keeping the schema outside the code makes the message contract explicit
    and easier to evolve independently of the producer logic.
    """
    project_root = Path(__file__).resolve().parents[2]
    schema_path = project_root / "schemas" / "order-created.json"

    with schema_path.open("r", encoding="utf-8") as schema_file:
        return json.load(schema_file)


def validate_order_event(order_event: dict, schema: dict) -> None:
    """
    Validate the generated order event against the shared JSON schema.

    The producer fails fast if the payload does not match the expected
    contract. This mirrors a common best practice in event-driven systems.
    """
    validate(instance=order_event, schema=schema)

def delivery_report(err, msg) -> None:
    """
    Kafka delivery callback.

    This callback is triggered asynchronously by the client once Kafka
    acknowledges the message or the client decides delivery has failed.
    """
    if err is not None:
        print(f"Message delivery failed: {err}")
        return

    print("Message delivered successfully")
    print(f"Topic: {msg.topic()}")
    print(f"Partition: {msg.partition()}")
    print(f"Offset: {msg.offset()}")
    print(f"Key: {msg.key().decode('utf-8') if msg.key() else None}")
    print(f"Value: {msg.value().decode('utf-8')}")

def main() -> None:
    """
    Produce a single order-created event to Kafka.

    A message key is used so records for the same logical entity can be routed
    consistently by Kafka's partitioner when applicable.
    """

    topic_name = os.getenv("KAFKA_TOPIC_ORDERS", "orders")

    producer = build_producer()
    order_event = build_order_event("laura", "margarita", 3)
    schema = load_order_schema()

    try:
        validate_order_event(order_event, schema)
    except ValidationError as err:
        print("Order event validation failed")
        print(err)
        raise

    event_key = order_event["orderId"].encode("utf-8")
    event_value = json.dumps(order_event).encode("utf-8")

    producer.produce(
        topic=topic_name,
        key=event_key,
        value=event_value,
        callback=delivery_report,
    )

    # flush(timeout) blocks until queued messages are delivered or the timeout
    # is reached. It returns the number of messages still pending.
    remaining_messages = producer.flush(10)

    if remaining_messages > 0:
        print(f"Timeout reached. Remaining messages: {remaining_messages}")

if __name__ == "__main__":
    main()