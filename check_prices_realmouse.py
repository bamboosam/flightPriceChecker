#!/usr/bin/env python3
"""
Cloudflare Bypass with REAL Mouse Control

This version uses PyAutoGUI to control the actual physical mouse cursor,
generating trusted events that Cloudflare cannot detect.

IMPORTANT: 
- Browser will open at a FIXED position and size
- Don't touch your mouse when Cloudflare appears
- The script will take control of your mouse to click the checkbox
"""

import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import json
import os
import yaml
from cloudflare_bypass import CloudflareBypass
from real_mouse_bypass import RealMouseBypass

# Fixed browser dimensions for consistent coordinate mapping
BROWSER_WIDTH = 1280
BROWSER_HEIGHT = 720
BROWSER_X = 100  # Position on screen
BROWSER_Y = 100

async def check_flight_price(origin, destination, date):
    """Check price for a single route using REAL MOUSE CONTROL"""
    url = f"https://www.airasia.com/flights/search/?origin={origin}&destination={destination}&departDate={date.replace('/', '%2F')}&tripType=O&adult=1&locale=en-gb&currency=THB"
    
    # Initialize real mouse controller
    real_mouse = RealMouseBypass()
    real_mouse.set_browser_position(BROWSER_X, BROWSER_Y)
    
    async with async_playwright() as p:
        # Launch browser in HEADED mode with FIXED size and position
        print(f"  [DEBUG] Launching HEADED browser at ({BROWSER_X}, {BROWSER_Y})...")
        browser = await p.chromium.launch(
            headless=False,  # ← HEADED MODE (visible)
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                f'--window-position={BROWSER_X},{BROWSER_Y}',
                f'--window-size={BROWSER_WIDTH},{BROWSER_HEIGHT}',
            ]
        )
        
        # Create context with FIXED viewport
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': BROWSER_WIDTH, 'height': BROWSER_HEIGHT},
            locale='en-GB',
            timezone_id='Asia/Bangkok',
        )
        
        # Hide webdriver property
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        page = await context.new_page()
        
        try:
            # Navigate to search results
            print(f"  [DEBUG] Navigating to: {url}")
            await page.goto(url, timeout=60000)
            print(f"  [DEBUG] Page loaded")
            
            # Wait a bit for page to settle
            await page.wait_for_timeout(5000)
            
            # Check page title
            page_title = await page.title()
            print(f"  [DEBUG] Page title: {page_title}")
            
            # Take screenshot right after page load for debugging
            screenshot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "debug_screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            initial_screenshot = os.path.join(screenshot_dir, f"{origin}_{destination}_initial_load.png")
            await page.screenshot(path=initial_screenshot)
            print(f"  [DEBUG] Screenshot saved: {initial_screenshot}")

            
            # Check for Cloudflare challenge and attempt REAL MOUSE bypass
            bypass = CloudflareBypass(page)
            if await bypass.detect_challenge():
                print(f"  [DEBUG] ⚠ Cloudflare challenge detected!")
                print(f"  [DEBUG] 🖱️  REAL MOUSE CONTROL MODE ACTIVATED!")
                print(f"  [DEBUG] ⚠️  DON'T TOUCH YOUR MOUSE!")
                
                # Create screenshots directory
                screenshot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "debug_screenshots")
                os.makedirs(screenshot_dir, exist_ok=True)
                cf_screenshot = os.path.join(screenshot_dir, f"{origin}_{destination}_cloudflare_realmouse.png")
                
                # Take screenshot for debugging
                await page.screenshot(path=cf_screenshot)
                print(f"  [DEBUG] Screenshot saved: {cf_screenshot}")
                
                # Use manually found checkbox coordinates (more reliable than OpenCV)
                # Coordinates found using xdotool: (207, 397)
                page_x, page_y = 207, 397
                print(f"  [DEBUG] Using manual checkbox coords: ({page_x}, {page_y})")
                
                # Use REAL MOUSE to click the checkbox
                print(f"  [DEBUG] Taking control of your mouse in 2 seconds...")
                await page.wait_for_timeout(2000)
                
                # Click with real mouse
                success = real_mouse.click_checkbox(page_x, page_y)
                
                if success:
                    print(f"  [DEBUG] ✓ Checkbox clicked with REAL mouse!")
                    print(f"  [DEBUG] Waiting for challenge to resolve...")
                    
                    # Wait for challenge to complete
                    challenge_passed = await bypass.wait_for_challenge_completion(timeout=10)
                    
                    if challenge_passed:
                        print(f"  [DEBUG] ✓ Cloudflare challenge PASSED!")
                        await page.wait_for_timeout(3000)
                        page_title = await page.title()
                        print(f"  [DEBUG] New page title: {page_title}")
                    else:
                        print(f"  [DEBUG] ✗ Challenge did not resolve")
                        print(f"  [DEBUG] 💡 The checkbox might need to be clicked again")
                else:
                    print(f"  [DEBUG] ✗ Failed to click checkbox")
            
            # Continue with normal flow...
            print(f"  [DEBUG] Looking for search button...")
            
            # Click on page body to remove focus from URL bar and dismiss popups
            try:
                await page.click('body')
                await page.wait_for_timeout(2000)
                print(f"  [DEBUG] Clicked on page to remove URL bar focus")
                print(f"  [DEBUG] Waiting 2 seconds before clicking search button...")
            except Exception as e:
                pass
            
            # Try to find and click search button
            try:
                search_btn = await page.wait_for_selector('#home_Search', timeout=20000, state='visible')
                if search_btn:
                    print(f"  [DEBUG] Found search button, clicking...")
                    await search_btn.click()
                    print(f"  [DEBUG] Waiting for results...")
                    await page.wait_for_timeout(10000)
            except Exception as e:
                print(f"  [DEBUG] No search button found, trying to extract anyway...")
                await page.wait_for_timeout(10000)
            
            # Extract prices (same as before)
            print(f"  [DEBUG] Extracting prices...")
            
            # Click "View details" buttons
            view_details_clicked = await page.evaluate("""
                () => {
                    const viewDetailsButtons = document.querySelectorAll('p[type="small"]');
                    let clicked = 0;
                    viewDetailsButtons.forEach(btn => {
                        if (btn.textContent.includes('View details')) {
                            btn.click();
                            clicked++;
                        }
                    });
                    return clicked;
                }
            """)
            print(f"  [DEBUG] Clicked {view_details_clicked} 'View details' buttons")
            
            await page.wait_for_timeout(1000)
            
            # Extract flight data
            prices = await page.evaluate(r"""
                () => {
                    const flights = [];
                    const uniqueKeys = new Set();
                    
                    const allFlightNumbers = [];
                    const allParagraphs = document.querySelectorAll('p');
                    for (const p of allParagraphs) {
                        const text = p.textContent.trim();
                        const match = text.match(/([A-Z]{2})\s*(\d{3,4})/);
                        if (match && text.toLowerCase().includes('air')) {
                            const flightNum = `${match[1]} ${match[2]}`;
                            allFlightNumbers.push(flightNum);
                        }
                    }
                    
                    const containers = document.querySelectorAll('[class*="Journey"][class*="Container"]');
                    let flightIndex = 0;
                    
                    containers.forEach(container => {
                        const priceEl = container.querySelector('[class*="Price"] [class*="gBxbny"]');
                        const times = container.querySelectorAll('[class*="Text"][class*="hBKgBd"], [class*="Text"][class*="eQIcKu"]');
                        
                        if (priceEl && times.length >= 2) {
                            const departTime = times[0]?.textContent.trim() || '';
                            const arriveTime = times[1]?.textContent.trim() || '';
                            
                            if (departTime && arriveTime) {
                                const price = parseInt(priceEl.textContent.replace(/,/g, ''));
                                const key = `${price}-${departTime}-${arriveTime}`;
                                
                                if (!uniqueKeys.has(key)) {
                                    uniqueKeys.add(key);
                                    const flightNum = flightIndex < allFlightNumbers.length ? allFlightNumbers[flightIndex] : "N/A";
                                    
                                    flights.push({
                                        flightNumber: flightNum,
                                        price: price,
                                        currency: 'THB',
                                        departTime: departTime,
                                        arriveTime: arriveTime
                                    });
                                    flightIndex++;
                                }
                            }
                        }
                    });
                    
                    return flights.sort((a, b) => a.price - b.price);
                }
            """)
            
            if prices:
                print(f"  ✓ Found {len(prices)} flights")
                print(f"  ✓ Cheapest: {prices[0]['currency']} {prices[0]['price']:,}")
            else:
                print(f"  ✗ No flights found")
            
            # Keep browser open for 5 seconds
            print(f"  [DEBUG] Keeping browser open for 5 seconds...")
            await page.wait_for_timeout(5000)
            
            await context.close()
            await browser.close()
            
            return {
                "route": f"{origin} → {destination}",
                "date": date,
                "flights": prices,
                "cheapest": prices[0] if prices else None,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"  [ERROR] Exception: {type(e).__name__}: {str(e)}")
            try:
                await context.close()
                await browser.close()
            except:
                pass
            
            return {
                "route": f"{origin} → {destination}",
                "date": date,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

async def main():
    """Check all routes and save results"""
    # Load config
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)
    
    results = []
    
    for route in config['routes']:
        print(f"\nChecking {route['origin']} → {route['destination']} on {route['date']}...")
        result = await check_flight_price(route['origin'], route['destination'], route['date'])
        results.append(result)
    
    # Save results
    with open('price_history.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to price_history.json")

if __name__ == "__main__":
    asyncio.run(main())
