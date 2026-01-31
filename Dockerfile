FROM dorowu/ubuntu-desktop-lxde-vnc:focal

# Switch to root for installation
USER root

# Fix broken repos and install dependencies
RUN rm -f /etc/apt/sources.list.d/google-chrome.list 2>/dev/null || true && \
    apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    xdotool \
    libx11-dev \
    libxtst-dev \
    libxinerama-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN python3 -m venv venv && \
    ./venv/bin/pip install --upgrade pip && \
    ./venv/bin/pip install -r requirements.txt && \
    ./venv/bin/pip install pyautogui python-xlib

# Install Playwright and browsers
RUN ./venv/bin/pip install playwright && \
    ./venv/bin/playwright install chromium && \
    ./venv/bin/playwright install-deps chromium

# Copy application files
COPY check_prices_realmouse.py .
COPY config.yml .

# Create run script
RUN echo '#!/bin/bash\n\
sleep 5\n\
cd /app\n\
export DISPLAY=:1\n\
./venv/bin/python3 check_prices_realmouse.py\n\
' > /app/run_checker.sh && chmod +x /app/run_checker.sh

# VNC is already set up by base image
# Access via http://localhost:6901 or VNC :5901
