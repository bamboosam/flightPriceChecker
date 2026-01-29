#!/bin/bash
# Minimal VM Setup - Ubuntu Server (No Desktop!)
# This installs ONLY what's needed for the flight price checker

set -e

echo "=========================================="
echo "Minimal VM Setup (No Desktop)"
echo "=========================================="
echo

# Update system
echo "📦 Updating system..."
sudo apt update

# Install minimal dependencies
echo "📦 Installing minimal dependencies..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-tk \
    python3-dev \
    build-essential \
    git \
    xvfb \
    tightvncserver \
    x11-utils \
    xdotool \
    wget \
    ca-certificates

# Install Chromium dependencies (needed for Playwright)
echo "📦 Installing browser dependencies..."
sudo apt install -y \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils

# Create venv
echo "🐍 Setting up Python environment..."
python3 -m venv venv

# Install Python packages
echo "📦 Installing Python packages..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
./venv/bin/playwright install chromium
./venv/bin/playwright install-deps

# Create .Xauthority
echo "🔐 Creating .Xauthority..."
touch ~/.Xauthority
chmod 600 ~/.Xauthority

# Test setup
echo
echo "=========================================="
echo "🧪 Testing Setup..."
echo "=========================================="

# Test Python
xvfb-run -a ./venv/bin/python3 -c "import pyautogui; print('✓ PyAutoGUI works')"

# Test Xvfb
echo "✓ Testing Xvfb..."
xvfb-run -a echo "✓ Xvfb works"

echo
echo "=========================================="
echo "✅ Minimal Setup Complete!"
echo "=========================================="
echo
echo "Total disk usage: $(du -sh . | cut -f1)"
echo
echo "To run the script:"
echo "  xvfb-run -a ./venv/bin/python3 check_prices_realmouse.py"
echo
echo "To run with visible display (for debugging):"
echo "  Xvfb :99 -screen 0 1280x720x24 &"
echo "  export DISPLAY=:99"
echo "  ./venv/bin/python3 check_prices_realmouse.py"
echo
echo "To schedule with cron:"
echo "  0 * * * * cd $(pwd) && xvfb-run -a ./venv/bin/python3 check_prices_realmouse.py"
echo
