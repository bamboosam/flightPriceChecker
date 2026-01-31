# Docker Desktop Setup

Run the flight price checker in a Docker container with desktop environment and VNC access.

## Install Docker (Debian 13)

```bash
# One-line installer
curl -fsSL https://get.docker.com | sh

# Add your user to docker group (no sudo needed)
sudo usermod -aG docker $USER

# Apply group changes (or logout/login)
newgrp docker

# Verify installation
docker --version
docker compose version
```

## Quick Start

```bash
# Build and start the containers (flight-checker-1 and flight-checker-2)
docker compose up -d --build

# Wait ~2 minutes for build to complete
docker compose logs -f
```

## Access the Desktop

**Container 1** (`flight-checker-1`)
- Browser: `http://localhost:6901`
- VNC: `localhost:5901`
- Password: `flightcheck`

**Container 2** (`flight-checker-2`)
- Browser: `http://localhost:6902`
- VNC: `localhost:5902`
- Password: `flightcheck`

## Run the Price Checker

**Option 1: Run on ONE container**
```bash
docker exec flight-checker-1 /app/run_checker.sh
```

**Option 2: Run on ALL containers (Parallel)**
```bash
./run_all.sh
```

**Option 3: Interactive (Debug)**
Inside the VNC desktop terminal:
```bash
cd /app
./run_checker.sh
```

## View Results

Both containers write to the **same** local `price_history.json` file (shared volume):

```bash
cat price_history.json
```

```bash
docker compose down
```

## Running Multiple Containers

To scale up for parallel checking:

```bash
# Edit docker-compose.yml to add more services with different ports
# Or run multiple with different names:
docker compose up -d --scale flight-checker=5
```

## Memory Requirements

- Single container: ~1.5-2GB RAM
- Recommended shm_size: 2GB (for browser)
