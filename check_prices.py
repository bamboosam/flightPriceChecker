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
            await page.goto(url)
            await page.wait_for_timeout(15000)  # Wait 15 seconds for page to fully load
            
            # Check if flights are loaded
            flights_loaded = await page.evaluate("""
                () => {
                    const containers = document.querySelectorAll('[class*="Journey"][class*="Container"]');
                    return containers.length > 0;
                }
            """)
            
            # If no flights found, click search button to trigger data fetch
            if not flights_loaded:
                print(f"  [DEBUG] No flights initially loaded, trying to click search button...")
                try:
                    # Try multiple selectors for the search button
                    selectors = [
                        'button:has-text("Search")',
                        'button[type="submit"]',
                        'button.btn-primary',
                        '#home_Search',
                        'button[class*="Search"]',
                        'button[class*="submit"]'
                    ]
                    
                    clicked = False
                    for selector in selectors:
                        try:
                            search_btn = await page.wait_for_selector(selector, timeout=2000)
                            if search_btn:
                                await search_btn.click()
                                print(f"  [DEBUG] Clicked search button using selector: {selector}")
                                clicked = True
                                break
                        except:
                            continue
                    
                    if clicked:
                        await page.wait_for_timeout(10000)  # Wait for results
                    else:
                        print(f"  [DEBUG] Could not find search button, trying to reload page...")
                        await page.reload()
                        await page.wait_for_timeout(10000)
                        
                except Exception as e:
                    print(f"  [DEBUG] Search button workaround failed: {e}")
                    # Try one more time by reloading
                    try:
                        await page.reload()
                        await page.wait_for_timeout(10000)
                    except:
                        pass
            
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
            await browser.close()
            return {
                "route": f"{origin} → {destination}",
                "date": date,
                "error": str(e),
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
