# Debian 13 VM Setup Guide

## Why Debian 13?

- ✅ **Smaller:** ~1GB base install (vs 1.5GB Ubuntu Server)
- ✅ **Stable:** Rock-solid, well-tested packages
- ✅ **Lightweight:** Minimal resource usage
- ✅ **Perfect for:** Headless automation

## Installation

1. **Download Debian 13 (Trixie) netinstall**
   - URL: https://www.debian.org/devel/debian-installer/
   - Choose: `debian-testing-amd64-netinst.iso` (~400MB)

2. **VM Specs (Minimal)**
   - RAM: 2GB
   - Disk: 10GB
   - CPU: 1-2 cores
   - Network: NAT or Bridged

3. **During Installation:**
   - Choose: **Standard system utilities** only
   - Uncheck: Desktop environment, web server, etc.
   - Install: **SSH server** (for remote access)

## Setup Script (Debian-specific)

After installing Debian, run:

```bash
# Update package list
sudo apt update

# Clone your repo
git clone https://github.com/bamboosam/flightPriceChecker.git
cd flightPriceChecker

# Make setup script executable
chmod +x vm_setup.sh run.sh

# Run setup (works on Debian!)
./vm_setup.sh
```

The `vm_setup.sh` script works on **both Ubuntu and Debian** - no changes needed!

## Differences from Ubuntu

| Feature | Ubuntu Server | Debian 13 |
|---------|---------------|-----------|
| Base size | ~1.5GB | ~1GB |
| Package manager | apt | apt (same!) |
| Python version | 3.12 | 3.11+ |
| Setup script | ✅ Works | ✅ Works |
| Stability | Stable | Very stable |

## After Setup

```bash
# Test mouse control
./run.sh test

# Run visible mode (with VNC)
./run.sh visible

# Run invisible mode (headless)
./run.sh invisible
```

## VNC Access (for testing)

```bash
# Install VNC server
sudo apt install -y tightvncserver

# Start VNC
vncserver :1 -geometry 1280x720 -depth 24

# Connect from host
# VNC Viewer → VM_IP:5901
```

## Production (Automated)

```bash
# Add to crontab
crontab -e

# Run every hour
0 * * * * cd /home/user/flightPriceChecker && xvfb-run -a ./venv/bin/python3 check_prices_realmouse.py
```

## Troubleshooting

### If Python is 3.11 instead of 3.12:
No problem! The code works with Python 3.11+

### If git is not installed:
```bash
sudo apt install -y git
```

### If you get "command not found":
```bash
# Make sure you're in the right directory
cd ~/flightPriceChecker
```

## Quick Start Commands

```bash
# 1. Install Debian 13 (minimal)
# 2. SSH into VM
ssh user@vm-ip

# 3. Clone and setup
git clone https://github.com/bamboosam/flightPriceChecker.git
cd flightPriceChecker
chmod +x vm_setup.sh run.sh
./vm_setup.sh

# 4. Test
./run.sh test

# 5. Run
./run.sh invisible
```

Perfect for lightweight automation! 🚀
