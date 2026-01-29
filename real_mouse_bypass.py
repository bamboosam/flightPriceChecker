"""
Real Mouse Control for Cloudflare Bypass

This module uses PyAutoGUI to control the ACTUAL physical mouse cursor,
generating trusted (isTrusted=true) events that Cloudflare cannot detect.

Unlike Playwright's synthetic events, this moves the real cursor on your screen.
"""

import warnings
warnings.filterwarnings('ignore')  # Suppress X11 auth warnings

import pyautogui
import time
import random
from typing import Tuple, Optional


class RealMouseBypass:
    """Controls the actual physical mouse cursor to bypass Cloudflare"""
    
    # Fixed browser window position and size
    # These will be set when the browser launches
    BROWSER_X = 0
    BROWSER_Y = 0
    BROWSER_WIDTH = 1280
    BROWSER_HEIGHT = 720
    
    def __init__(self):
        """Initialize PyAutoGUI with safety settings"""
        # Safety: Disable fail-safe in virtual display to avoid (0,0) triggering it
        pyautogui.FAILSAFE = False
        
        # Disable pauses for smoother movement
        pyautogui.PAUSE = 0
    
    def set_browser_position(self, x: int, y: int):
        """
        Set the browser window position on screen
        
        Args:
            x: X coordinate of browser window top-left corner
            y: Y coordinate of browser window top-left corner
        """
        self.BROWSER_X = x
        self.BROWSER_Y = y
        print(f"  [MOUSE] Browser window at screen position: ({x}, {y})")
    
    def page_to_screen_coords(self, page_x: int, page_y: int) -> Tuple[int, int]:
        """
        Convert page coordinates to absolute screen coordinates
        
        Args:
            page_x: X coordinate within the page
            page_y: Y coordinate within the page
            
        Returns:
            Tuple of (screen_x, screen_y)
        """
        screen_x = self.BROWSER_X + page_x
        screen_y = self.BROWSER_Y + page_y
        return (screen_x, screen_y)
    
    def move_mouse_human_like(self, target_x: int, target_y: int, duration: float = 0.5):
        """
        Move the REAL mouse cursor to target coordinates with human-like movement
        
        Args:
            target_x: Target screen X coordinate
            target_y: Target screen Y coordinate
            duration: Time to take for movement (seconds)
        """
        try:
            current_x, current_y = pyautogui.position()
            print(f"  [MOUSE] Moving real cursor from ({current_x}, {current_y}) to ({target_x}, {target_y})")
            
            # Use easeInOutQuad for natural acceleration/deceleration
            pyautogui.moveTo(target_x, target_y, duration=duration, tween=pyautogui.easeInOutQuad)
            
            # Small random pause after movement (humans don't click instantly)
            time.sleep(random.uniform(0.1, 0.3))
            
            print(f"  [MOUSE] ✓ Real cursor moved to ({target_x}, {target_y})")
            
        except Exception as e:
            print(f"  [MOUSE] ✗ Error moving mouse: {e}")
    
    def random_mouse_movements(self, num_movements: int = 5):
        """
        Perform random mouse movements across the screen to simulate human behavior
        
        Args:
            num_movements: Number of random movements to perform (default: 5)
        """
        try:
            screen_width, screen_height = self.get_screen_size()
            print(f"  [MOUSE] Performing {num_movements} random mouse movements...")
            print(f"  [MOUSE] Screen size: {screen_width}x{screen_height}")
            
            # Use center area of screen for more visible movements
            center_x = screen_width // 2
            center_y = screen_height // 2
            movement_range = 400  # Move within 400 pixels of center
            
            for i in range(num_movements):
                # Random position near center of screen (more visible)
                target_x = center_x + random.randint(-movement_range, movement_range)
                target_y = center_y + random.randint(-movement_range, movement_range)
                
                # Clamp to screen bounds
                target_x = max(100, min(target_x, screen_width - 100))
                target_y = max(100, min(target_y, screen_height - 100))
                
                # Get current position before moving
                current_pos = pyautogui.position()
                print(f"  [MOUSE] Movement {i+1}/{num_movements}: ({current_pos.x}, {current_pos.y}) → ({target_x}, {target_y})")
                
                # Move SLOWLY so you can see it (2-3 seconds per movement)
                move_duration = random.uniform(2.0, 3.0)
                print(f"  [MOUSE] Moving slowly over {move_duration:.1f} seconds...")
                pyautogui.moveTo(target_x, target_y, duration=move_duration, tween=pyautogui.easeInOutQuad)
                
                # Verify we actually moved
                new_pos = pyautogui.position()
                print(f"  [MOUSE] Arrived at: ({new_pos.x}, {new_pos.y})")
                
                # Pause after movement so you can see where it is
                print(f"  [MOUSE] Pausing for 5 seconds...")
                time.sleep(5.0)
            
            # Final position
            final_pos = pyautogui.position()
            print(f"  [MOUSE] Final position: ({final_pos.x}, {final_pos.y})")
            print(f"  [MOUSE] ✓ Completed {num_movements} random movements")
            
        except Exception as e:
            print(f"  [MOUSE] ✗ Error during random movements: {e}")
    
    def click_at_position(self, x: int, y: int):
        """
        Click the REAL mouse at the given screen coordinates
        
        Args:
            x: Screen X coordinate
            y: Screen Y coordinate
        """
        try:
            # Move to position first
            self.move_mouse_human_like(x, y)
            
            # Random delay before click
            time.sleep(random.uniform(0.05, 0.15))
            
            # Perform real click
            pyautogui.click()
            
            print(f"  [MOUSE] ✓ Real click performed at ({x}, {y})")
            
            # Small delay after click
            time.sleep(random.uniform(0.2, 0.4))
            
        except Exception as e:
            print(f"  [MOUSE] ✗ Error clicking: {e}")
    
    def click_checkbox(self, page_x: int, page_y: int) -> bool:
        """
        Click the Cloudflare checkbox using real mouse control
        
        Args:
            page_x: X coordinate of checkbox within the page
            page_y: Y coordinate of checkbox within the page
            
        Returns:
            bool: True if click was performed, False otherwise
        """
        try:
            # Convert page coordinates to screen coordinates
            screen_x, screen_y = self.page_to_screen_coords(page_x, page_y)
            
            print(f"  [MOUSE] 🖱️  Taking control of your mouse!")
            print(f"  [MOUSE] Page coords: ({page_x}, {page_y})")
            print(f"  [MOUSE] Screen coords: ({screen_x}, {screen_y})")
            print(f"  [MOUSE] ⚠️  Don't touch your mouse for 30 seconds...")
            
            # Wait a moment before taking control
            time.sleep(0.5)
            
            # Click the checkbox directly with real mouse
            self.click_at_position(screen_x, screen_y)
            
            print(f"  [MOUSE] ✓ Checkbox clicked with REAL mouse!")
            
            return True
            
        except Exception as e:
            print(f"  [MOUSE] ✗ Error clicking checkbox: {e}")
            return False
    
    def get_screen_size(self) -> Tuple[int, int]:
        """
        Get the screen size
        
        Returns:
            Tuple of (width, height)
        """
        size = pyautogui.size()
        return (size.width, size.height)
    
    def test_mouse_control(self):
        """
        Test that mouse control is working
        Moves mouse in a small circle
        """
        print(f"  [MOUSE] Testing mouse control...")
        print(f"  [MOUSE] Screen size: {self.get_screen_size()}")
        
        # Get current position
        start_x, start_y = pyautogui.position()
        print(f"  [MOUSE] Current position: ({start_x}, {start_y})")
        
        # Move in a small square
        print(f"  [MOUSE] Moving in a square pattern...")
        pyautogui.moveTo(start_x + 50, start_y, duration=0.3)
        time.sleep(0.1)
        pyautogui.moveTo(start_x + 50, start_y + 50, duration=0.3)
        time.sleep(0.1)
        pyautogui.moveTo(start_x, start_y + 50, duration=0.3)
        time.sleep(0.1)
        pyautogui.moveTo(start_x, start_y, duration=0.3)
        
        print(f"  [MOUSE] ✓ Mouse control test complete!")


# Helper function to get browser window position
def get_browser_window_position() -> Optional[Tuple[int, int]]:
    """
    Try to get the browser window position
    
    Returns:
        Tuple of (x, y) if found, None otherwise
    """
    try:
        # On Linux with X11, we can use xdotool
        import subprocess
        result = subprocess.run(
            ['xdotool', 'search', '--name', 'Chromium', 'getwindowgeometry'],
            capture_output=True,
            text=True,
            timeout=2
        )
        
        # Parse output to get position
        # Example: "Position: 100,50 (screen: 0)"
        for line in result.stdout.split('\n'):
            if 'Position:' in line:
                coords = line.split('Position:')[1].split('(')[0].strip()
                x, y = map(int, coords.split(','))
                return (x, y)
        
    except Exception as e:
        print(f"  [MOUSE] Could not auto-detect window position: {e}")
    
    return None
