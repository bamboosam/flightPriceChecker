# Docker Desktop Setup

Run the flight price checker in a Docker container with desktop environment and VNC access.

## Install Docker (Debian 13)

```bash
# Update packages
sudo apt update

# Install prerequisites
sudo apt install -y ca-certificates curl gnupg

# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add Docker repository (use bookworm for Debian 13/Trixie)
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian bookworm stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

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
