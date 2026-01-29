#!/usr/bin/env python3
"""
Simple test script to verify PyAutoGUI mouse control is working

This will move your mouse immediately so you can see if it's working.
"""

import warnings
warnings.filterwarnings('ignore')

from real_mouse_bypass import RealMouseBypass
import time

def main():
    print("=" * 70)
    print("MOUSE MOVEMENT TEST")
    print("=" * 70)
    print()
    print("This will move your mouse in 3 seconds...")
    print("⚠️  DON'T TOUCH YOUR MOUSE!")
    print()
    
    # Countdown
    for i in range(3, 0, -1):
        print(f"Starting in {i}...")
        time.sleep(1)
    
    print()
    print("🖱️  STARTING MOUSE MOVEMENTS NOW!")
    print()
    
    # Create mouse controller
    mouse = RealMouseBypass()
    
    # Perform 5 slow random movements
    mouse.random_mouse_movements(num_movements=5)
    
    print()
    print("🖱️  Now testing CLICK...")
    print()
    
    # Get screen size for click position
    screen_width, screen_height = mouse.get_screen_size()
    center_x = screen_width // 2
    center_y = screen_height // 2
    
    print(f"  [MOUSE] Moving to center of screen ({center_x}, {center_y})...")
    mouse.move_mouse_human_like(center_x, center_y, duration=2.0)
    
    print(f"  [MOUSE] Clicking in 2 seconds...")
    time.sleep(2)
    
    import pyautogui
    pyautogui.click()
    print(f"  [MOUSE] ✓ CLICK performed at ({center_x}, {center_y})")
    
    print()
    print("=" * 70)
    print("TEST COMPLETE!")
    print("=" * 70)
    print()
    print("Did you see:")
    print("1. Your mouse cursor moving? (5 movements)")
    print("2. Your mouse move to center of screen?")
    print("3. A click happen at the center?")
    print()
    print("- YES to all: Perfect! Mouse control is fully working!")
    print("- NO to movements but YES to click: Mouse works but movements might be too fast")
    print("- NO to everything: There might be a display/permission issue")
    print()

if __name__ == "__main__":
    main()
