import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import json
import os
import yaml

# Load configuration
def load_config():
    """Load configuration from config.yml"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "config.yml")
    
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    return config

# Load routes from config
config = load_config()
ROUTES = config.get('routes', [])

async def check_flight_price(origin, destination, date):
    """Check price for a single route"""
    url = f"https://www.airasia.com/flights/search/?origin={origin}&destination={destination}&departDate={date.replace('/', '%2F')}&tripType=O&adult=1&locale=en-gb&currency=THB"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # Navigate to search results
            print(f"  [DEBUG] Navigating to: {url}")
            try:
                await page.goto(url, wait_until='networkidle', timeout=60000)  # 60 second timeout
                print(f"  [DEBUG] Page loaded, network idle")
            except Exception as nav_error:
                print(f"  [DEBUG] Navigation warning: {nav_error}")
                print(f"  [DEBUG] Continuing anyway...")
            
            # Take initial screenshot
            screenshot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "debug_screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"{origin}_{destination}_initial.png")
            await page.screenshot(path=screenshot_path)
            print(f"  [DEBUG] Screenshot saved: {screenshot_path}")
            
            # Check page title and URL
            page_title = await page.title()
            current_url = page.url
            print(f"  [DEBUG] Page title: {page_title}")
            print(f"  [DEBUG] Current URL: {current_url}")
            
            # Poll for flights to appear (they load asynchronously)
            print(f"  [DEBUG] Waiting for flights to load...")
            max_attempts = 12  # 12 attempts * 5 seconds = 60 seconds max
            attempt = 0
            flights_found = False
            
            while attempt < max_attempts and not flights_found:
                attempt += 1
                await page.wait_for_timeout(5000)  # Wait 5 seconds between checks
                
                # Check if flights are loaded
                flight_info = await page.evaluate("""
                    () => {
                        const containers = document.querySelectorAll('[class*="Journey"][class*="Container"]');
                        const noFlightsMsg = document.querySelector('[class*="NoFlight"], [class*="no-flight"], .empty-state');
                        const loadingIndicator = document.querySelector('[class*="Loading"], [class*="loading"], [class*="spinner"]');
                        
                        return {
                            flightCount: containers.length,
                            hasNoFlightsMessage: !!noFlightsMsg,
                            noFlightsText: noFlightsMsg?.textContent || '',
                            isLoading: !!loadingIndicator,
                            bodyClasses: document.body.className,
                            hasSearchButton: !!document.querySelector('button:has-text("Search"), button[type="submit"]')
                        };
                    }
                """)
                
                print(f"  [DEBUG] Attempt {attempt}/{max_attempts}:")
                print(f"    - Flights found: {flight_info['flightCount']}")
                print(f"    - No flights message: {flight_info['hasNoFlightsMessage']}")
                print(f"    - Loading indicator: {flight_info['isLoading']}")
                print(f"    - Has search button: {flight_info['hasSearchButton']}")
                
                if flight_info['flightCount'] > 0:
                    flights_found = True
                    print(f"  [DEBUG] ✓ Found {flight_info['flightCount']} flights after {attempt * 5} seconds")
                    break
                
                # If we see "no flights" message or hit 30 seconds, try refreshing
                if (flight_info['hasNoFlightsMessage'] or attempt == 6) and not flights_found:
                    print(f"  [DEBUG] Triggering page refresh to force data reload...")
                    await page.reload(wait_until='networkidle')
                    await page.wait_for_timeout(5000)
                    
                    # Take screenshot after refresh
                    refresh_screenshot = os.path.join(screenshot_dir, f"{origin}_{destination}_after_refresh.png")
                    await page.screenshot(path=refresh_screenshot)
                    print(f"  [DEBUG] Post-refresh screenshot: {refresh_screenshot}")
            
            if not flights_found:
                print(f"  [DEBUG] ✗ No flights found after {max_attempts * 5} seconds")
                # Take final screenshot for debugging
                final_screenshot = os.path.join(screenshot_dir, f"{origin}_{destination}_final.png")
                await page.screenshot(path=final_screenshot)
                print(f"  [DEBUG] Final screenshot: {final_screenshot}")
                
                # Get page HTML for debugging
                html_content = await page.content()
                html_path = os.path.join(screenshot_dir, f"{origin}_{destination}_page.html")
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"  [DEBUG] Page HTML saved: {html_path}")


            
            # Extract prices using JavaScript
            prices = await page.evaluate("""
                () => {
                    const flights = [];
                    const containers = document.querySelectorAll('[class*="Journey"][class*="Container"]');
                    
                    console.log(`Found ${containers.length} flight containers`);
                    
                    containers.forEach(container => {
                        const priceEl = container.querySelector('[class*="Price"] [class*="gBxbny"]');
                        const times = container.querySelectorAll('[class*="Text"][class*="hBKgBd"], [class*="Text"][class*="eQIcKu"]');
                        
                        if (priceEl) {
                            const price = parseInt(priceEl.textContent.replace(/,/g, ''));
                            const departTime = times[0]?.textContent.trim() || '';
                            const arriveTime = times[1]?.textContent.trim() || '';
                            
                            flights.push({
                                price: price,
                                departTime: departTime,
                                arriveTime: arriveTime
                            });
                        }
                    });
                    
                    return flights.sort((a, b) => a.price - b.price);
                }
            """)
            
            await browser.close()
            
            return {
                "route": f"{origin} → {destination}",
                "date": date,
                "flights": prices,
                "cheapest": prices[0] if prices else None,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"  [ERROR] Exception occurred: {type(e).__name__}")
            print(f"  [ERROR] Error message: {str(e)}")
            import traceback
            print(f"  [ERROR] Traceback:")
            traceback.print_exc()
            
            try:
                await browser.close()
            except:
                pass
            
            return {
                "route": f"{origin} → {destination}",
                "date": date,
                "error": str(e),
                "error_type": type(e).__name__,
                "timestamp": datetime.now().isoformat()
            }

async def main():
    """Check all routes and save results"""
    results = []
    
    for route in ROUTES:
        print(f"Checking {route['origin']} → {route['destination']} on {route['date']}...")
        result = await check_flight_price(route['origin'], route['destination'], route['date'])
        results.append(result)
        
        if result.get('cheapest'):
            print(f"  ✓ Cheapest: THB {result['cheapest']['price']}")
        else:
            print(f"  ✗ No flights found")
    
    # Save results to file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "price_history.json")
    
    # Load existing history
    history = []
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            history = json.load(f)
    
    # Append new results
    history.append({
        "check_time": datetime.now().isoformat(),
        "results": results
    })
    
    # Save updated history
    with open(output_file, 'w') as f:
        json.dump(history, f, indent=2)
    
    print(f"\nResults saved to {output_file}")
    
    # Send notification (optional)
    send_notification(results)

def send_notification(results):
    """Send notification with results"""
    # Print to console (captured by cron email)
    print("\n" + "="*50)
    print("FLIGHT PRICE CHECK RESULTS")
    print("="*50)
    for result in results:
        print(f"\n{result['route']} on {result['date']}")
        if result.get('cheapest'):
            print(f"  Cheapest: THB {result['cheapest']['price']}")
            print(f"  Time: {result['cheapest']['departTime']} → {result['cheapest']['arriveTime']}")
        else:
            print(f"  No flights found")
    
    # TODO: Add email or Telegram notifications here
    # See deployment_guide.md for examples

if __name__ == "__main__":
    asyncio.run(main())
