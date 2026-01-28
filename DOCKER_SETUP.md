# Docker Setup Guide

Run the flight price checker locally using Docker and Docker Compose.

## Prerequisites

Install Docker and Docker Compose:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose

# Or use Docker Desktop (Windows/Mac/Linux)
# Download from: https://www.docker.com/products/docker-desktop
```

## Quick Start

### 1. Build the Docker Image

```bash
cd /home/bamboosam/AI\ Coding/flightPriceChecker
docker-compose build
```

This will:
- Create a Python 3.11 container
- Install Playwright and Chromium
- Install all dependencies
- Set up the environment

### 2. Configure Your Routes

Edit `config.yml` to set your desired routes:
```yaml
routes:
  - origin: KOP
    destination: DMK
    date: '04/04/2026'
```

### 3. Run the Price Checker

**One-time run:**
```bash
docker-compose run --rm flight-checker
```

**Run and view output:**
```bash
docker-compose run --rm flight-checker python3 check_prices.py
```

## Scheduled Runs

### Option 1: Docker Compose with Loop

Edit `docker-compose.yml` and uncomment the command line:
```yaml
command: sh -c "while true; do python3 check_prices.py && sleep 86400; done"
```

Then run as a service:
```bash
docker-compose up -d
```

This will run the checker every 24 hours (86400 seconds).

### Option 2: Host Cron Job

Add to your crontab:
```bash
crontab -e
```

Add this line (runs daily at 8 AM):
```cron
0 8 * * * cd /home/bamboosam/AI\ Coding/flightPriceChecker && docker-compose run --rm flight-checker >> cron.log 2>&1
```

### Option 3: Custom Schedule Script

Create `run_scheduled.sh`:
```bash
#!/bin/bash
cd /home/bamboosam/AI\ Coding/flightPriceChecker

while true; do
    echo "Running price check at $(date)"
    docker-compose run --rm flight-checker
    
    # Wait 24 hours (or customize)
    sleep 86400
done
```

Make it executable and run:
```bash
chmod +x run_scheduled.sh
./run_scheduled.sh &
```

## Viewing Results

### Check Price History
```bash
cat price_history.json | python3 -m json.tool
```

### View Debug Screenshots
```bash
ls -lh debug_screenshots/
```

### View Logs
```bash
# If running as service
docker-compose logs -f flight-checker

# If using cron
tail -f cron.log
```

## Useful Commands

### Rebuild After Code Changes
```bash
docker-compose build --no-cache
```

### Stop Running Service
```bash
docker-compose down
```

### Run with Custom Config
```bash
docker-compose run --rm -v ./custom-config.yml:/app/config.yml flight-checker
```

### Interactive Shell (for debugging)
```bash
docker-compose run --rm flight-checker /bin/bash
```

### Clean Up
```bash
# Remove containers
docker-compose down

# Remove images
docker-compose down --rmi all

# Remove volumes
docker-compose down -v
```

## Advantages of Docker

✅ **Consistent Environment** - Same setup everywhere  
✅ **No System Pollution** - Dependencies isolated in container  
✅ **Easy Updates** - Just rebuild the image  
✅ **Portable** - Run on any machine with Docker  
✅ **Local IP** - Uses your home IP, not GitHub's  

## Troubleshooting

### Cloudflare Still Blocking?

If Cloudflare still blocks even with Docker:

1. **Try non-headless mode** (requires X server):
   ```python
   # In check_prices.py, change:
   browser = await p.chromium.launch(headless=False, ...)
   ```

2. **Add delays**:
   ```python
   await page.wait_for_timeout(5000)  # Wait 5 seconds
   ```

3. **Use residential proxy** (requires proxy service)

### Permission Issues

```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

### Container Won't Start

```bash
# Check logs
docker-compose logs

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up
```

## Testing

Test the setup:
```bash
# Run once
docker-compose run --rm flight-checker

# Check if it worked
cat price_history.json
ls debug_screenshots/
```

You should see:
- Updated `price_history.json`
- Screenshots in `debug_screenshots/`
- Flight prices in the output

## Next Steps

1. Test with `docker-compose run --rm flight-checker`
2. Check if Cloudflare is bypassed (look for flight prices)
3. Set up scheduled runs using your preferred method
4. Monitor `price_history.json` for results

Good luck! 🚀
