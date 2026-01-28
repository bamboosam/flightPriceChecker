# Headed Browser Setup

This version runs with a **visible browser window** to bypass Cloudflare's bot detection.

## Requirements

You need a display server (X11) to run the headed browser.

### On Linux Desktop

If you're on a Linux desktop with a GUI, you can run directly:

```bash
python3 check_prices_headed.py
```

### On Linux Server (Headless)

If you're on a server without a display, you need to set up a virtual display:

#### Option 1: Using Xvfb (Virtual Framebuffer)

```bash
# Install Xvfb
sudo apt-get install xvfb

# Run with virtual display
xvfb-run -a python3 check_prices_headed.py
```

#### Option 2: Using VNC

```bash
# Install VNC server
sudo apt-get install tightvncserver

# Start VNC server
vncserver :1

# Set DISPLAY and run
export DISPLAY=:1
python3 check_prices_headed.py
```

### On macOS

Should work directly:

```bash
python3 check_prices_headed.py
```

### On Windows (WSL)

You need an X server like VcXsrv or Xming:

1. Install VcXsrv: https://sourceforge.net/projects/vcxsrv/
2. Start XLaunch with default settings
3. In WSL:
   ```bash
   export DISPLAY=:0
   python3 check_prices_headed.py
   ```

## How It Works

**Differences from headless version:**
- `headless=False` - Shows actual browser window
- Browser stays open for 5 seconds after completion
- You can see what's happening in real-time

**Why this might work:**
- Headed browsers have different fingerprints
- Cloudflare detection is less aggressive
- More realistic browser behavior

## Running

### Direct Execution

```bash
# Install dependencies first
pip install playwright pyyaml
playwright install chromium

# Run the headed version
python3 check_prices_headed.py
```

### With Xvfb (Recommended for Servers)

```bash
# Install Xvfb
sudo apt-get install xvfb

# Run
xvfb-run -a python3 check_prices_headed.py
```

### Scheduled with Cron

```bash
crontab -e
```

Add:
```cron
# Run daily at 8 AM using virtual display
0 8 * * * cd /home/bamboosam/AI\ Coding/flightPriceChecker && xvfb-run -a python3 check_prices_headed.py >> cron.log 2>&1
```

## Docker Version

To run headed browser in Docker, you need to:

1. Install Xvfb in the container
2. Use `xvfb-run` to provide virtual display

Updated Dockerfile coming soon if this approach works!

## Troubleshooting

### "Could not find display"

You need a display server. Use `xvfb-run`:
```bash
xvfb-run -a python3 check_prices_headed.py
```

### Browser doesn't open

Check if X server is running:
```bash
echo $DISPLAY
```

Should show something like `:0` or `:1`.

### Still getting Cloudflare

If headed browser still gets blocked:
1. Try adding more delays
2. Consider using a proxy
3. May need to explore API options

## Next Steps

1. Test if headed browser bypasses Cloudflare
2. If it works, update Docker setup to use Xvfb
3. Set up scheduled execution with cron

Good luck! 🚀
