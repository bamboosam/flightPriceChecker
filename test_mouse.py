#!/usr/bin/env python3
"""
Test script for PyAutoGUI mouse control

This will test that PyAutoGUI can control your mouse.
Run this to verify everything is working before using it with Cloudflare.
"""

from real_mouse_bypass import RealMouseBypass
import time

def main():
    print("=" * 70)
    print("PyAutoGUI Mouse Control Test")
    print("=" * 70)
    print()
    
    mouse = RealMouseBypass()
    
    # Test 1: Get screen info
    print("Test 1: Screen Information")
    print("-" * 70)
    width, height = mouse.get_screen_size()
    print(f"Screen size: {width}x{height}")
    print()
    
    # Test 2: Test mouse control
    print("Test 2: Mouse Movement Test")
    print("-" * 70)
    print("⚠️  Your mouse will move in a square pattern in 3 seconds...")
    print("⚠️  Move your mouse to the top-left corner to abort (FAILSAFE)")
    time.sleep(3)
    
    mouse.test_mouse_control()
    print()
    
    # Test 3: Set browser position (simulated)
    print("Test 3: Coordinate Conversion")
    print("-" * 70)
    mouse.set_browser_position(100, 100)
    
    # Simulate checkbox at page coords (511, 206)
    page_x, page_y = 511, 206
    screen_x, screen_y = mouse.page_to_screen_coords(page_x, page_y)
    print(f"Page coordinates: ({page_x}, {page_y})")
    print(f"Screen coordinates: ({screen_x}, {screen_y})")
    print()
    
    # Test 4: Simulated checkbox click
    print("Test 4: Simulated Checkbox Click")
    print("-" * 70)
    print("⚠️  In 3 seconds, the mouse will move to simulated checkbox position")
    print("⚠️  and perform a click. Watch your cursor!")
    time.sleep(3)
    
    success = mouse.click_checkbox(page_x, page_y)
    
    if success:
        print("✓ Test completed successfully!")
    else:
        print("✗ Test failed")
    
    print()
    print("=" * 70)
    print("All tests complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
