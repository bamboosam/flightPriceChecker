#!/usr/bin/env python3
"""
Test clicking the Cloudflare checkbox at exact coordinates
"""

import pyautogui
import time

print("=" * 50)
print("CLOUDFLARE CHECKBOX CLICK TEST")
print("=" * 50)
print()
print("Moving to Cloudflare checkbox (207, 397) in 3 seconds...")
print()

# Countdown
for i in range(3, 0, -1):
    print(f"Starting in {i}...")
    time.sleep(1)

print()
print("Moving mouse to (207, 397)...")
pyautogui.moveTo(207, 397, duration=1.5)
print(f"Current position: {pyautogui.position()}")

print()
print("Waiting 2 seconds before clicking...")
time.sleep(2)

print("Clicking now...")
pyautogui.click()
print("✓ Click performed!")

print()
print("=" * 50)
print("TEST COMPLETE!")
print("=" * 50)
print()
print("Check the VNC window - did the checkbox get clicked?")
