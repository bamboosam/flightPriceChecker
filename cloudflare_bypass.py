"""
Cloudflare Turnstile Bypass Module

This module provides experimental functionality to detect and interact with
Cloudflare's Turnstile challenge using image processing and human-like automation.

Approach:
1. Detect Cloudflare challenge presence
2. Take screenshot of the page
3. Use OpenCV to locate the checkbox
4. Simulate human-like mouse movement to the checkbox
5. Click with realistic timing variations
"""

import asyncio
import cv2
import numpy as np
from typing import Optional, Tuple, Dict
import random
import math


class CloudflareBypass:
    """Handles Cloudflare Turnstile challenge bypass using image processing"""
    
    def __init__(self, page):
        """
        Initialize the bypass handler
        
        Args:
            page: Playwright page object
        """
        self.page = page
        
    async def detect_challenge(self) -> bool:
        """
        Detect if Cloudflare challenge is present on the page
        
        Returns:
            bool: True if challenge detected, False otherwise
        """
        try:
            page_title = await self.page.title()
            page_content = await self.page.content()
            
            # Check for common Cloudflare indicators
            indicators = [
                "just a moment" in page_title.lower(),
                "cloudflare" in page_title.lower(),
                "cf-challenge" in page_content.lower(),
                "turnstile" in page_content.lower()
            ]
            
            return any(indicators)
        except Exception as e:
            print(f"  [DEBUG] Error detecting challenge: {e}")
            return False
    
    async def find_checkbox_in_screenshot(self, screenshot_path: str) -> Optional[Tuple[int, int]]:
        """
        Use OpenCV to find the Cloudflare checkbox in a screenshot
        
        Args:
            screenshot_path: Path to the screenshot image
            
        Returns:
            Tuple of (x, y) coordinates if found, None otherwise
        """
        try:
            # Load the screenshot
            img = cv2.imread(screenshot_path)
            if img is None:
                print(f"  [DEBUG] Could not load screenshot: {screenshot_path}")
                return None
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply binary threshold
            _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
            
            # Find contours
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Look for checkbox-like shapes (small squares)
            checkbox_candidates = []
            
            for contour in contours:
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)
                
                # Filter by size and aspect ratio
                # Cloudflare checkbox is typically 20-40 pixels
                if 15 <= w <= 50 and 15 <= h <= 50:
                    aspect_ratio = float(w) / h
                    # Should be roughly square
                    if 0.8 <= aspect_ratio <= 1.2:
                        # Check if it's in the upper portion of the page
                        # (Cloudflare challenge usually appears near top)
                        if y < img.shape[0] * 0.4:
                            checkbox_candidates.append((x, y, w, h))
            
            if checkbox_candidates:
                # Sort by how close to top-left (typical position)
                checkbox_candidates.sort(key=lambda c: c[0] + c[1])
                
                # Return center of the first candidate
                x, y, w, h = checkbox_candidates[0]
                center_x = x + w // 2
                center_y = y + h // 2
                
                print(f"  [DEBUG] Found checkbox candidate at ({center_x}, {center_y})")
                return (center_x, center_y)
            
            print(f"  [DEBUG] No checkbox found in screenshot")
            return None
            
        except Exception as e:
            print(f"  [DEBUG] Error finding checkbox: {e}")
            return None
    
    async def find_checkbox_in_dom(self) -> Optional[Dict]:
        """
        Try to find the Cloudflare checkbox using DOM inspection
        
        Returns:
            Dict with element info if found, None otherwise
        """
        try:
            # Cloudflare Turnstile is typically in an iframe
            # First, try to find the iframe
            iframe_info = await self.page.evaluate("""
                () => {
                    // Look for Cloudflare Turnstile iframe
                    const iframes = document.querySelectorAll('iframe');
                    for (const iframe of iframes) {
                        const src = iframe.src || '';
                        if (src.includes('cloudflare') || src.includes('turnstile')) {
                            const rect = iframe.getBoundingClientRect();
                            return {
                                found: true,
                                x: rect.x,
                                y: rect.y,
                                width: rect.width,
                                height: rect.height,
                                src: src
                            };
                        }
                    }
                    
                    // Also check for the challenge container
                    const container = document.querySelector('[class*="cf-challenge"]') ||
                                     document.querySelector('[id*="cf-challenge"]');
                    if (container) {
                        const rect = container.getBoundingClientRect();
                        return {
                            found: true,
                            x: rect.x,
                            y: rect.y,
                            width: rect.width,
                            height: rect.height,
                            src: 'container'
                        };
                    }
                    
                    return { found: false };
                }
            """)
            
            if iframe_info.get('found'):
                print(f"  [DEBUG] Found Cloudflare element: {iframe_info}")
                return iframe_info
            
            return None
            
        except Exception as e:
            print(f"  [DEBUG] Error finding checkbox in DOM: {e}")
            return None
    
    def generate_bezier_curve(self, start: Tuple[int, int], end: Tuple[int, int], 
                             num_points: int = 20) -> list:
        """
        Generate a Bezier curve for human-like mouse movement
        
        Args:
            start: Starting (x, y) coordinates
            end: Ending (x, y) coordinates
            num_points: Number of points in the curve
            
        Returns:
            List of (x, y) coordinates along the curve
        """
        # Add random control points for natural curve
        x1, y1 = start
        x2, y2 = end
        
        # Random control points
        ctrl1_x = x1 + random.randint(-50, 50) + (x2 - x1) * 0.3
        ctrl1_y = y1 + random.randint(-50, 50) + (y2 - y1) * 0.3
        ctrl2_x = x1 + random.randint(-50, 50) + (x2 - x1) * 0.7
        ctrl2_y = y1 + random.randint(-50, 50) + (y2 - y1) * 0.7
        
        points = []
        for i in range(num_points):
            t = i / (num_points - 1)
            
            # Cubic Bezier curve formula
            x = (1-t)**3 * x1 + 3*(1-t)**2*t * ctrl1_x + 3*(1-t)*t**2 * ctrl2_x + t**3 * x2
            y = (1-t)**3 * y1 + 3*(1-t)**2*t * ctrl1_y + 3*(1-t)*t**2 * ctrl2_y + t**3 * y2
            
            points.append((int(x), int(y)))
        
        return points
    
    async def move_mouse_human_like(self, target_x: int, target_y: int):
        """
        Move mouse to target coordinates with human-like movement
        
        Args:
            target_x: Target X coordinate
            target_y: Target Y coordinate
        """
        try:
            # Get current mouse position (start from a random position)
            viewport = self.page.viewport_size
            start_x = random.randint(100, viewport['width'] - 100)
            start_y = random.randint(100, viewport['height'] - 100)
            
            # Generate Bezier curve path
            path = self.generate_bezier_curve((start_x, start_y), (target_x, target_y))
            
            print(f"  [DEBUG] Moving mouse from ({start_x}, {start_y}) to ({target_x}, {target_y})")
            
            # Move along the path with random timing
            for i, (x, y) in enumerate(path):
                await self.page.mouse.move(x, y)
                
                # Random delay between movements (faster at start, slower near end)
                if i < len(path) - 5:
                    delay = random.uniform(5, 15)  # milliseconds
                else:
                    delay = random.uniform(20, 40)  # slow down near target
                
                await asyncio.sleep(delay / 1000)
            
            print(f"  [DEBUG] Mouse movement complete")
            
        except Exception as e:
            print(f"  [DEBUG] Error moving mouse: {e}")
    
    async def click_with_human_timing(self, x: int, y: int):
        """
        Click at coordinates with human-like timing
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        try:
            # Move to position with human-like movement
            await self.move_mouse_human_like(x, y)
            
            # Random delay before click (humans don't click instantly)
            await asyncio.sleep(random.uniform(0.1, 0.3))
            
            # Click with random duration
            await self.page.mouse.down()
            await asyncio.sleep(random.uniform(0.05, 0.15))  # Click duration
            await self.page.mouse.up()
            
            print(f"  [DEBUG] Clicked at ({x}, {y})")
            
            # Random delay after click
            await asyncio.sleep(random.uniform(0.2, 0.5))
            
        except Exception as e:
            print(f"  [DEBUG] Error clicking: {e}")
    
    async def attempt_bypass(self, screenshot_path: str) -> bool:
        """
        Attempt to bypass the Cloudflare challenge
        
        Args:
            screenshot_path: Path to save screenshot for analysis
            
        Returns:
            bool: True if bypass was attempted, False otherwise
        """
        try:
            print(f"  [DEBUG] Attempting Cloudflare bypass...")
            
            # First, try to find checkbox in DOM
            dom_info = await self.find_checkbox_in_dom()
            
            if dom_info:
                # Calculate click position (center of element)
                click_x = int(dom_info['x'] + dom_info['width'] / 2)
                click_y = int(dom_info['y'] + dom_info['height'] / 2)
                
                print(f"  [DEBUG] Using DOM-based coordinates: ({click_x}, {click_y})")
                
                # Attempt click with human-like behavior
                await self.click_with_human_timing(click_x, click_y)
                
                # Wait for challenge to process
                print(f"  [DEBUG] Waiting for challenge to process...")
                await asyncio.sleep(random.uniform(3, 5))
                
                return True
            
            # Fallback: Try image processing approach
            print(f"  [DEBUG] DOM approach failed, trying image processing...")
            
            # Take screenshot
            await self.page.screenshot(path=screenshot_path)
            
            # Find checkbox in screenshot
            coords = await self.find_checkbox_in_screenshot(screenshot_path)
            
            if coords:
                click_x, click_y = coords
                
                # Attempt click with human-like behavior
                await self.click_with_human_timing(click_x, click_y)
                
                # Wait for challenge to process
                print(f"  [DEBUG] Waiting for challenge to process...")
                await asyncio.sleep(random.uniform(3, 5))
                
                return True
            
            print(f"  [DEBUG] Could not locate checkbox with any method")
            return False
            
        except Exception as e:
            print(f"  [DEBUG] Error in bypass attempt: {e}")
            return False
    
    async def wait_for_challenge_completion(self, timeout: int = 30) -> bool:
        """
        Wait for the Cloudflare challenge to complete
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            bool: True if challenge passed, False if timeout
        """
        try:
            print(f"  [DEBUG] Waiting for challenge completion (timeout: {timeout}s)...")
            
            await self.page.wait_for_function(
                """
                () => {
                    const title = document.title.toLowerCase();
                    return title.indexOf('just a moment') === -1 && 
                           title.indexOf('cloudflare') === -1;
                }
                """,
                timeout=timeout * 1000
            )
            
            print(f"  [DEBUG] ✓ Challenge appears to have passed!")
            return True
            
        except Exception as e:
            print(f"  [DEBUG] ✗ Challenge did not complete: {e}")
            return False
