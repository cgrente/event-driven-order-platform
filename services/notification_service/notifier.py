import json
import os

from confluent_kafka import Consumer

def build_consumer() -> Consumer:
    """
    Build a Kafka consumer for the notification service.

    This service listens to order-created events and simulates the sending of
    a user notification after an order is received.
    """
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092")

    config = {
        "bootstrap.servers": bootstrap_servers,
        "group.id": "notification_service",
        "auto.offset.reset": "earliest",
    }

    return Consumer(config)

def send_notification(order_event: dict) -> None:
    """
    Simulate sending a notification for an order-created event.

    In a real system, this would likely call an email provider, SMS gateway,
    push notification service, or internal notification API.
    """
    print("Notification sent")
    print(f"User: {order_event['user']}")
    print(
        f"Message: Your order for {order_event['quantity']} "
        f"x {order_event['item']} has been received."
    )
    print("-" * 60)

def main() -> None:
    """
    Continuously consume order events and simulate notification delivery.
    """
    topic_name = os.getenv("KAFKA_TOPIC_ORDERS", "orders")

    consumer = build_consumer()
    consumer.subscribe([topic_name])

    print(f"Notification service started and subscribed to '{topic_name}'")

    try:
        while True:
            message = consumer.poll(timeout=1.0)

            if message is None:
                continue

            if message.error():
                print(f"Consumer error: {message.error()}")
                continue

            order_event = json.loads(message.value().decode("utf-8"))
            send_notification(order_event)
    except KeyboardInterrupt:
        print("Stopping notification service")
    finally:
        consumer.close()

if __name__ == "__main__":
    main()