# Complete Setup Guide - Fresh Debian 13 Installation

This guide walks you through setting up the flight price checker with Cloudflare bypass on a **fresh Debian 13 VM without desktop environment**.

---

## Prerequisites

- Fresh Debian 13 installation (minimal/server install)
- SSH access to the VM
- Internet connection
- TigerVNC Viewer on your local machine

---

## Step 1: Initial System Setup

SSH into your fresh Debian VM:

```bash
ssh your_username@your_vm_ip
```

Update the system:

```bash
sudo apt update
sudo apt upgrade -y
```

Install essential tools:

```bash
sudo apt install -y git curl wget build-essential
```

---

## Step 2: Install XFCE Desktop Environment

Install XFCE (lightweight desktop for VNC):

```bash
sudo apt install -y xfce4 xfce4-goodies
```

**Note:** When prompted to choose a display manager, select **lightdm** (or skip if not prompted).

---

## Step 3: Install X11 Libraries (Critical for Mouse Control)

These libraries are **essential** for PyAutoGUI and xdotool to work:

```bash
sudo apt install -y \
    libx11-dev \
    libxtst-dev \
    libxinerama-dev \
    libxkbcommon-x11-0 \
    x11-xserver-utils \
    xdotool
```

---

## Step 4: Install VNC Server

Install x11vnc and Xvfb:

```bash
sudo apt install -y x11vnc xvfb
```

Configure VNC startup script:

```bash
mkdir -p ~/.vnc
cat > ~/.vnc/xstartup << 'EOF'
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
startxfce4 &
EOF
chmod +x ~/.vnc/xstartup
```

---

## Step 5: Clone the Repository

```bash
cd ~
git clone https://github.com/bamboosam/flightPriceChecker.git
cd flightPriceChecker
git checkout bypass-cloudflare
```

---

## Step 6: Run the Setup Script

Make the setup script executable and run it:

```bash
chmod +x vm_setup.sh
./vm_setup.sh
```

This will install:
- Python 3 and pip
- Virtual environment
- Playwright and browsers
- PyAutoGUI
- All dependencies

**This takes 5-10 minutes.**

---

## Step 7: Configure Your Routes

Edit the configuration file:

```bash
nano config.yml
```

Update with your desired routes:

```yaml
schedule:
  cron: '0 1 * * *'  # 8 AM Bangkok time

routes:
  - origin: KOP
    destination: DMK
    date: '03/02/2026'
  
  - origin: DMK
    destination: KOP
    date: '10/02/2026'
```

Save and exit (Ctrl+X, Y, Enter).

---

## Step 8: Start VNC Server

Run these commands to start XFCE with VNC:

```bash
# Clean up any existing processes
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

---

## Step 9: Connect with VNC Viewer

On your **local machine**:

1. Open **TigerVNC Viewer**
2. Connect to: `your_vm_ip:5901`
3. No password required
4. You should see the XFCE desktop

---

## Step 10: Test the Setup

### Test Mouse Control

In the VNC terminal or SSH:

```bash
cd ~/flightPriceChecker
DISPLAY=:1 xdotool mousemove 640 360
```

You should see the mouse move in VNC!

### Test PyAutoGUI

```bash
DISPLAY=:1 ./venv/bin/python3 test_click.py
```

Watch the mouse move and click in VNC.

---

## Step 11: Run the Price Checker

### Visible Mode (Watch in VNC)

Keep VNC connected:

```bash
cd ~/flightPriceChecker
DISPLAY=:1 ./venv/bin/python3 check_prices_realmouse.py
```

You'll see the browser open and watch the Cloudflare bypass!

### Invisible Mode (Headless)

No VNC needed:

```bash
cd ~/flightPriceChecker
./run.sh invisible
```

---

## Step 12: Check Results

View price history:

```bash
cat price_history.json
```

View screenshots:

```bash
ls -lh debug_screenshots/
```

---

## Important Notes

### Cloudflare Checkbox Coordinates

The checkbox is hardcoded at **(207, 397)**. If Cloudflare changes its layout, find new coordinates:

```bash
# In VNC terminal, run this and move mouse over checkbox:
while true; do DISPLAY=:1 xdotool getmouselocation; sleep 0.5; done
```

Press Ctrl+C when done, then update `check_prices_realmouse.py` line 108:

```python
page_x, page_y = 207, 397  # Update these values
```

### Timing Configuration

Current timings:
- **Cloudflare bypass timeout:** 10 seconds
- **Post-bypass page load:** 10 seconds  
- **Page settle before search:** 2 seconds

These can be adjusted in `check_prices_realmouse.py` if needed.

---

## Automated Runs (Optional)

Set up a cron job for automated price checking:

```bash
crontab -e
```

Add this line to run every hour:

```bash
0 * * * * cd /home/your_username/flightPriceChecker && ./run.sh invisible >> /tmp/price_checker.log 2>&1
```

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
# Verify X11 libraries are installed
dpkg -l | grep libxtst

# Test xdotool
DISPLAY=:1 xdotool mousemove 640 360
```

### Cloudflare bypass fails

- Check the screenshot in `debug_screenshots/`
- Verify checkbox coordinates with xdotool
- Watch in VNC to see what's happening

---

## Quick Reference Commands

**Start VNC:**
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

**Update code:**
```bash
git pull origin bypass-cloudflare
```

---

## Summary

You now have a fully functional flight price checker with Cloudflare bypass! The key components:

✅ Debian 13 with XFCE desktop  
✅ X11 libraries for mouse control  
✅ VNC server for visual debugging  
✅ PyAutoGUI for real mouse control  
✅ Hardcoded Cloudflare checkbox coordinates (207, 397)  
✅ Optimized timing for reliable bypass  

Happy price checking! 🚀
