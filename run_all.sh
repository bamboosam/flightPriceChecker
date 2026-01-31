#!/bin/bash

echo "Starting flight checks on all containers..."

# Run on container 1 (Background)
echo "Triggering flight-checker-1..."
docker exec -d flight-checker-1 /app/run_checker.sh

# Run on container 2 (Background)
echo "Triggering flight-checker-2..."
docker exec -d flight-checker-2 /app/run_checker.sh

echo "All checks started in background!"
echo "monitor with: docker compose logs -f"
