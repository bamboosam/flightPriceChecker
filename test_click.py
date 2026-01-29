#!/usr/bin/env python3
"""
Simple test to move mouse to specific coordinates and click
"""

import pyautogui
import time

print("=" * 50)
print("MOUSE CLICK TEST")
print("=" * 50)
print()
print("Moving to (640, 1360) and clicking in 3 seconds...")
print()

# Countdown
for i in range(3, 0, -1):
    print(f"Starting in {i}...")
    time.sleep(1)

print()
print("Moving mouse to (640, 1360)...")
pyautogui.moveTo(640, 1360, duration=2.0)
print(f"Current position: {pyautogui.position()}")

print()
print("Clicking in 1 second...")
time.sleep(1)

pyautogui.click()
print("✓ Click performed!")

print()
print("=" * 50)
print("TEST COMPLETE!")
print("=" * 50)
