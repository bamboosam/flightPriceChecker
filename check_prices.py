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
            await page.wait_for_timeout(10000)  # Wait 10 seconds
            
            # Click search button if needed (troubleshooting)
            try:
                search_btn = await page.wait_for_selector('button:has-text("Search")', timeout=5000)
                await search_btn.click()
                await page.wait_for_timeout(10000)
            except:
                pass  # Search button not needed
            
            # Extract prices using JavaScript
            prices = await page.evaluate("""
                () => {
                    const flights = [];
                    const containers = document.querySelectorAll('[class*="Journey"][class*="Container"]');
                    
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
