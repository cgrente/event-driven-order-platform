#!/usr/bin/env bash

set -euo pipefail

# Create the primary topic used by the demo.
# The script is safe to run multiple times because --if-not-exists is used.
docker exec kafka kafka-topics \
  --create \
  --if-not-exists \
  --topic orders \
  --bootstrap-server kafka:9092 \
  --partitions 3 \
  --replication-factor 1

echo "Current topics:"
docker exec kafka kafka-topics \
  --list \
  --bootstrap-server kafka:9092