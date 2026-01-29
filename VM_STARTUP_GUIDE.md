# VM Startup Guide - Flight Price Checker

Quick reference for starting VNC and running the price checker on your Debian 13 VM.

## 1. Start the VM

Power on your VM and SSH into it:
```bash
ssh bamboosam@192.168.122.145
```

## 2. Configure VNC for XFCE (First Time Only)

If VNC shows GNOME instead of XFCE, reconfigure the startup script:

```bash
# Update VNC startup script to use XFCE
cat > ~/.vnc/xstartup << 'EOF'
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
startxfce4 &
EOF
chmod +x ~/.vnc/xstartup
```

## 3. Start VNC Server

Run these commands to start XFCE with VNC:

```bash
# Navigate to project
cd ~/flightPriceChecker

# Kill any existing processes
pkill -9 Xvfb
pkill -9 xfce4-session
pkill -9 x11vnc
sudo rm -rf /tmp/.X11-unix /tmp/.X*-lock

# Recreate X11 directory
sudo mkdir -p /tmp/.X11-unix
sudo chmod 1777 /tmp/.X11-unix

# Start Xvfb (virtual display)
Xvfb :1 -screen 0 1280x720x24 &
sleep 3

# Start XFCE desktop
DISPLAY=:1 startxfce4 &
sleep 5

# Start VNC server on port 5901
x11vnc -display :1 -rfbport 5901 -forever -shared &
```

## 4. Connect with VNC Viewer

On your **local machine** (not in SSH):

1. Open **TigerVNC Viewer**
2. Connect to: `192.168.122.146:5901`
3. No password required
4. You should see the XFCE desktop

## 5. Run the Price Checker

### Option A: Visible Mode (Watch in VNC)

Keep VNC connected and run:
```bash
cd ~/flightPriceChecker
DISPLAY=:1 ./venv/bin/python3 check_prices_realmouse.py
```

You'll see the browser open in VNC and watch the Cloudflare bypass in action!

### Option B: Invisible Mode (Headless)

No need for VNC to be connected:
```bash
cd ~/flightPriceChecker
./run.sh invisible
```

This runs in the background using the existing Xvfb display.

### Option C: Run Multiple Times (Test Cloudflare)

```bash
cd ~/flightPriceChecker
for i in {1..10}; do 
  echo "========== Run $i/10 =========="
  DISPLAY=:1 ./venv/bin/python3 check_prices_realmouse.py
done
```

## 6. Check Results

View the price history:
```bash
cat price_history.json
```

View debug screenshots:
```bash
ls -lh debug_screenshots/
```

## 7. Shutdown

When done, you can safely shutdown:
```bash
sudo shutdown -h now
```

The VNC processes will be killed automatically.

---

## Troubleshooting

### VNC won't connect
```bash
# Check if x11vnc is running
ps aux | grep x11vnc

# Check if port 5901 is listening
sudo ss -tulpn | grep 5901
```

### Mouse not moving
```bash
# Test xdotool
DISPLAY=:1 xdotool mousemove 640 360

# Test PyAutoGUI
DISPLAY=:1 ./venv/bin/python3 test_click.py
```

### Cloudflare coordinates wrong
The checkbox is at **(207, 397)**. If it changes, find new coordinates:
```bash
# In VNC terminal, run this and move mouse over checkbox:
while true; do DISPLAY=:1 xdotool getmouselocation; sleep 0.5; done
```

Then update `check_prices_realmouse.py` line 108:
```python
page_x, page_y = 207, 397  # Update these values
```

---

## Quick Start (Copy-Paste)

**Start everything:**
```bash
cd ~/flightPriceChecker
pkill -9 Xvfb xfce4-session x11vnc
sudo rm -rf /tmp/.X11-unix /tmp/.X*-lock
sudo mkdir -p /tmp/.X11-unix && sudo chmod 1777 /tmp/.X11-unix
Xvfb :1 -screen 0 1280x720x24 &
sleep 3
DISPLAY=:1 startxfce4 &
sleep 5
x11vnc -display :1 -rfbport 5901 -forever -shared &
```

**Run visible mode:**
```bash
DISPLAY=:1 ./venv/bin/python3 check_prices_realmouse.py
```

**Run invisible mode:**
```bash
./run.sh invisible
```

That's it! 🚀
