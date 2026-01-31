FROM consol/ubuntu-xfce-vnc:latest

# Switch to root for installation
USER root

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    xdotool \
    libx11-dev \
    libxtst-dev \
    libxinerama-dev \
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

# Switch back to default user
USER 1000

# Default command starts VNC desktop
# Run the checker manually via VNC terminal or: docker exec flight-checker /app/run_checker.sh
