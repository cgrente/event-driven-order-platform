.PHONY: up down reset logs ps topics produce consume-tracker consume-notifier

# Start all infrastructure in detached mode.
up:
	docker compose up -d

# Stop containers but keep volumes.
down:
	docker compose down

# Stop containers and delete volumes to reset Kafka state.
reset:
	docker compose down -v

# Follow logs for all services.
logs:
	docker compose logs -f

# Show running Compose services.
ps:
	docker compose ps

# Create Kafka topics used by the project.
topics:
	bash topics/create_topics.sh

# Run the producer from the host machine.
produce:
	python services/order_service/producer.py

# Run tracker consumer.
consume-tracker:
	python services/tracker_service/tracker.py

# Run notification consumer.
consume-notifier:
	python services/notification_service/notifier.py