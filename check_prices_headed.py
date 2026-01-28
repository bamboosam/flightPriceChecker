import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import json
import os
import yaml

async def check_flight_price(origin, destination, date):
    """Check price for a single route using HEADED browser"""
    url = f"https://www.airasia.com/flights/search/?origin={origin}&destination={destination}&departDate={date.replace('/', '%2F')}&tripType=O&adult=1&locale=en-gb&currency=THB"
    
    async with async_playwright() as p:
        # Launch browser in HEADED mode (visible window)
        print(f"  [DEBUG] Launching HEADED browser (visible window)...")
        browser = await p.chromium.launch(
            headless=False,  # ← HEADED MODE
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
            ]
        )
        
        # Create context with realistic settings
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
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
            
            # Check for Cloudflare
            if "just a moment" in page_title.lower():
                print(f"  [DEBUG] ⚠ Cloudflare detected, waiting 30 seconds...")
                await page.wait_for_timeout(30000)
                page_title = await page.title()
                print(f"  [DEBUG] New page title: {page_title}")
            
            # Look for search button (it's actually an <a> tag with id="home_Search")
            print(f"  [DEBUG] Looking for search button...")
            
            # Try to find and click search button using the correct ID
            try:
                search_btn = await page.wait_for_selector('#home_Search', timeout=20000, state='visible')
                if search_btn:
                    print(f"  [DEBUG] Found search button (#home_Search), clicking...")
                    await search_btn.click()
                    print(f"  [DEBUG] Waiting for results...")
                    await page.wait_for_timeout(20000)  # Wait 20 seconds for results
            except Exception as e:
                print(f"  [DEBUG] No search button found or click failed, trying to extract anyway...")
                await page.wait_for_timeout(10000)  # Wait a bit more
            
            # Extract prices
            print(f"  [DEBUG] Extracting prices...")
            prices = await page.evaluate("""
                () => {
                    const flights = [];
                    const containers = document.querySelectorAll('[class*="Journey"][class*="Container"]');
                    
                    containers.forEach(container => {
                        const priceEl = container.querySelector('[class*="Price"] [class*="gBxbny"]');
                        const times = container.querySelectorAll('[class*="Text"][class*="hBKgBd"], [class*="Text"][class*="eQIcKu"]');
                        
                        // Only add if we have a price AND valid times
                        if (priceEl && times.length >= 2) {
                            const departTime = times[0]?.textContent.trim() || '';
                            const arriveTime = times[1]?.textContent.trim() || '';
                            
                            // Filter out empty times
                            if (departTime && arriveTime) {
                                const price = parseInt(priceEl.textContent.replace(/,/g, ''));
                                
                                flights.push({
                                    price: price,
                                    currency: 'THB',
                                    departTime: departTime,
                                    arriveTime: arriveTime
                                });
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
            
            # Keep browser open for 5 seconds so you can see the result
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
    
    # Print summary
    print("\n" + "="*70)
    print("FLIGHT PRICE CHECK RESULTS")
    print("="*70)
    for result in results:
        print(f"\n{result['route']} on {result['date']}")
        print("-" * 70)
        
        if result.get('error'):
            print(f"  ❌ Error: {result['error']}")
        elif result.get('flights'):
            flights = result['flights']
            print(f"  ✅ Found {len(flights)} flight(s)\n")
            
            for i, flight in enumerate(flights, 1):
                is_cheapest = (i == 1)  # First flight is cheapest (already sorted)
                prefix = "  🌟 CHEAPEST" if is_cheapest else f"  {i}."
                
                print(f"{prefix}")
                print(f"     Price: {flight['currency']} {flight['price']:,}")
                print(f"     Depart: {flight['departTime']}")
                print(f"     Arrive: {flight['arriveTime']}")
                if not is_cheapest:
                    print()
            
            # Summary
            cheapest = flights[0]
            print(f"\n  💰 Best Price: {cheapest['currency']} {cheapest['price']:,}")
            print(f"     ({cheapest['departTime']} → {cheapest['arriveTime']})")
        else:
            print(f"  ⚠️  No flights found")
    
    print("\n" + "="*70)
    print(f"Results saved to price_history.json")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())
