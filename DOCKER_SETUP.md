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
# Build and start the container
docker compose up -d --build

# Wait ~2 minutes for build to complete
docker compose logs -f
```

## Access the Desktop

**Option 1: Browser (noVNC)**
- Open: `http://localhost:6901`
- Password: `flightcheck`

**Option 2: VNC Viewer**
- Connect: `localhost:5901`
- Password: `flightcheck`

## Run the Price Checker

Inside the VNC desktop, open a terminal and run:

```bash
cd /app
./run_checker.sh
```

Or from your host machine:

```bash
docker exec flight-checker /app/run_checker.sh
```

## View Results

Results are saved to your local `price_history.json` (mounted volume).

```bash
cat price_history.json
```

## Stop Container

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
