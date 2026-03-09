import os
import json

from confluent_kafka import Consumer

def build_consumer() -> Consumer:
    """
    Build a Kafka consumer using environment-driven configuration.

    The default bootstrap server targets the host listener because this script
    is intended to run directly from the local machine during development.
    """
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092")

    config = {
        "bootstrap.servers": bootstrap_servers,
        "group.id": "order-tracker",
        "auto.offset.reset": "earliest",
    }

    return Consumer(config)

def main() -> None:
    """
    Subscribe to the orders topic and continuously poll for new messages.

    This service intentionally keeps processing simple and logs the decoded
    event payload so the end-to-end Kafka flow is easy to demonstrate.
    """
    topic_name = os.getenv("KAFKA_TOPIC_ORDERS", "orders")

    consumer = build_consumer()

    # Subscribe once at startup so Kafka can assign partitions for the
    # configured consumer group.
    consumer.subscribe([topic_name])

    print(f"Tracker consumer started and subscribed to '{topic_name}'")

    try:
        while True:
            message = consumer.poll(timeout=1.0)

            if message is None:
                continue

            if message.error():
                print(f"Consumer error: {message.error()}")
                continue

            order_event = json.loads(message.value().decode("utf-8"))

            print("Received order event")
            print(f"Order ID: {order_event['orderId']}")
            print(f"User: {order_event['user']}")
            print(f"Item: {order_event['item']}")
            print(f"Quantity: {order_event['quantity']}")
            print(f"Partition: {message.partition()}")
            print(f"Offset: {message.offset()}")
            print("-" * 60)

    except KeyboardInterrupt:
        print("Stopping consumer")

    finally:
        consumer.close()

if __name__ == "__main__":
    main()

