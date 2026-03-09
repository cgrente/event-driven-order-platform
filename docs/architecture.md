# Architecture

## Overview

This project demonstrates a minimal event-driven workflow using Kafka.

A producer publishes an order-created event to Kafka, and one or more consumer services handle that event asynchronously. The system is intentionally small, but it reflects core distributed-system ideas such as service decoupling, shared event contracts, and independent consumers.

## Components

### Kafka
Kafka acts as the message broker for the system.

In this project it is configured in single-node KRaft mode for local development.

### Kafka UI
Kafka UI is included to inspect brokers, topics, partitions, offsets, and consumer groups during development.

### order-service
The `order-service` service is currently modeled as a lightweight Python producer script.

It simulates the behavior of an order-facing service by building an order event, validating it against a shared schema, and publishing it to the `orders` topic.

### tracker-service
The `tracker-service` is a lightweight Kafka consumer.

Its responsibility is to subscribe to the `orders` topic and log incoming order events for tracking purposes.

### notification-service
The `notification-service` is a second Kafka consumer.

Its responsibility is to subscribe to the same `orders` topic and simulate sending a user-facing notification when a new order event is received.

## Event flow

```text
1. order-service builds an order payload
2. order-service validates the payload against the shared schema
3. order-service serializes the payload to JSON
4. order-service publishes the event to Kafka topic: orders
5. Kafka persists the record in a topic partition
6. tracker-service consumes the event and logs order activity
7. notification-service consumes the same event and simulates a user notification
8. Kafka UI can be used to inspect brokers, topics, offsets, and consumer groups
```
### Consumer model

Each consumer runs in its own consumer group.

This allows multiple services to consume the same event stream independently without being tightly coupled to each other.

### Kafka listener model

This project uses two listener addresses because local development mixes host-based scripts and Dockerized infrastructure.

Internal Docker listener

```text
kafka:9092
```
Used by:
- Kafka UI
- future containerized services

### Host listener

```text
localhost:29092
```
Used by:
- local Python scripts run from the host machine
- IntelliJ / terminal executions outside Docker

Why this design is useful

Even though the codebase is small, the design reflects real system concerns:
- producer and consumer are decoupled
- event contracts can be versioned independently
- consumers can evolve without changing producer request flow
- new consumers can be added later without modifying the producer

Current limitations

This is a local development demo, so the architecture is intentionally simplified:
- single broker only
- no schema registry
- no dead-letter topics
- no retries beyond client defaults
- no authentication or encryption
- no persistent application storage

Future extensions

This architecture can grow in a natural way by adding more consumers, for example:
- inventory-service
- analytics-service

Each additional consumer can subscribe to the same event stream or to derived topics depending on the workflow.