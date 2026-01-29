import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import json
import os
import yaml
from cloudflare_bypass import CloudflareBypass

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
        # Launch browser with stealth mode to bypass Cloudflare
        print(f"  [DEBUG] Launching browser with stealth mode...")
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',  # Hide automation
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
            ]
        )
        
        # Create context with realistic user agent and settings
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='en-GB',
            timezone_id='Asia/Bangkok',
            extra_http_headers={
                'Accept-Language': 'en-GB,en;q=0.9',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            }
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
            
            # Check for Cloudflare challenge and attempt bypass
            bypass = CloudflareBypass(page)
            if await bypass.detect_challenge():
                print(f"  [DEBUG] ⚠ Cloudflare challenge detected! Attempting bypass...")
                
                # Take screenshot for analysis
                cf_screenshot = os.path.join(screenshot_dir, f"{origin}_{destination}_cloudflare.png")
                
                # Attempt to bypass the challenge
                bypass_attempted = await bypass.attempt_bypass(cf_screenshot)
                
                if bypass_attempted:
                    print(f"  [DEBUG] Bypass attempt completed, waiting for challenge to resolve...")
                    
                    # Wait for challenge to complete
                    challenge_passed = await bypass.wait_for_challenge_completion(timeout=30)
                    
                    if challenge_passed:
                        print(f"  [DEBUG] ✓ Cloudflare challenge passed!")
                        await page.wait_for_timeout(3000)  # Extra wait for page to stabilize
                        
                        # Update page info
                        page_title = await page.title()
                        print(f"  [DEBUG] New page title: {page_title}")
                    else:
                        print(f"  [DEBUG] ✗ Cloudflare challenge did not resolve in time")
                        print(f"  [DEBUG] Screenshot saved: {cf_screenshot}")
                else:
                    print(f"  [DEBUG] ✗ Could not attempt bypass (checkbox not found)")
                    print(f"  [DEBUG] Screenshot saved: {cf_screenshot}")
            
            # CRITICAL: Find and click the search button
            print(f"  [DEBUG] Waiting 10 seconds before searching...")
            await page.wait_for_timeout(10000)
            print(f"  [DEBUG] Looking for search button...")
            
            # Dismiss any login popup that might be covering the search button
            try:
                await page.keyboard.press('Escape')
                await page.wait_for_timeout(500)
                print(f"  [DEBUG] Pressed Escape to dismiss any popups")
            except Exception as e:
                pass
            
            # Strategy 1: Try to find all buttons on the page
            all_buttons = await page.evaluate("""
                () => {
                    const buttons = document.querySelectorAll('button');
                    return Array.from(buttons).map(btn => ({
                        text: btn.textContent.trim(),
                        type: btn.type,
                        id: btn.id,
                        classes: btn.className,
                        visible: btn.offsetParent !== null
                    }));
                }
            """)
            
            print(f"  [DEBUG] Found {len(all_buttons)} buttons on page:")
            for i, btn in enumerate(all_buttons[:10]):  # Show first 10
                print(f"    {i+1}. Text: '{btn['text'][:50]}', Type: {btn['type']}, ID: {btn['id']}, Visible: {btn['visible']}")
            
            # Strategy 2: Try multiple selectors to find and click search button
            search_clicked = False
            selectors_to_try = [
                ('button:has-text("Search")', 'Text contains "Search"'),
                ('button:has-text("search")', 'Text contains "search" (lowercase)'),
                ('button[type="submit"]', 'Submit button'),
                ('button.btn-primary', 'Primary button class'),
                ('button[class*="search" i]', 'Class contains "search"'),
                ('button[class*="Search"]', 'Class contains "Search"'),
                ('#search-button', 'ID search-button'),
                ('#searchButton', 'ID searchButton'),
                ('button[aria-label*="search" i]', 'Aria-label contains search'),
            ]
            
            for selector, description in selectors_to_try:
                try:
                    print(f"  [DEBUG] Trying selector: {selector} ({description})")
                    button = await page.wait_for_selector(selector, timeout=3000, state='visible')
                    if button:
                        # Get button details before clicking
                        button_text = await button.text_content()
                        print(f"  [DEBUG] Found button with text: '{button_text}'")
                        
                        await button.click()
                        print(f"  [DEBUG] ✓ Clicked search button using: {selector}")
                        search_clicked = True
                        break
                except Exception as e:
                    print(f"  [DEBUG] Selector failed: {str(e)[:100]}")
                    continue
            
            if not search_clicked:
                print(f"  [DEBUG] ⚠ Could not find search button with any selector")
                print(f"  [DEBUG] Trying JavaScript click on any button with 'search' text...")
                
                # Strategy 3: Use JavaScript to find and click
                js_clicked = await page.evaluate("""
                    () => {
                        const buttons = Array.from(document.querySelectorAll('button'));
                        const searchBtn = buttons.find(btn => 
                            btn.textContent.toLowerCase().includes('search') ||
                            btn.className.toLowerCase().includes('search') ||
                            btn.id.toLowerCase().includes('search')
                        );
                        
                        if (searchBtn) {
                            searchBtn.click();
                            return {
                                success: true,
                                text: searchBtn.textContent.trim(),
                                id: searchBtn.id,
                                classes: searchBtn.className
                            };
                        }
                        return { success: false };
                    }
                """)
                
                if js_clicked['success']:
                    print(f"  [DEBUG] ✓ JavaScript click succeeded!")
                    print(f"  [DEBUG] Button: text='{js_clicked['text']}', id='{js_clicked['id']}'")
                    search_clicked = True
                else:
                    print(f"  [DEBUG] ✗ JavaScript click also failed")
            
            # Wait for results to load after clicking
            if search_clicked:
                print(f"  [DEBUG] Waiting 15 seconds for flight results to load...")
                await page.wait_for_timeout(15000)
                
                # Take screenshot after search
                post_search_screenshot = os.path.join(screenshot_dir, f"{origin}_{destination}_after_search.png")
                await page.screenshot(path=post_search_screenshot)
                print(f"  [DEBUG] Post-search screenshot: {post_search_screenshot}")
            else:
                print(f"  [DEBUG] No search button clicked, trying page reload...")
                await page.reload(wait_until='networkidle')
                await page.wait_for_timeout(10000)
            
            # Check for flights
            print(f"  [DEBUG] Checking for flight results...")
            flight_count = await page.evaluate("""
                () => {
                    const containers = document.querySelectorAll('[class*="Journey"][class*="Container"]');
                    return containers.length;
                }
            """)
            
            print(f"  [DEBUG] Found {flight_count} flight containers")
            
            if flight_count == 0:
                print(f"  [DEBUG] Still no flights, saving debug info...")
                # Save final state
                final_screenshot = os.path.join(screenshot_dir, f"{origin}_{destination}_final.png")
                await page.screenshot(path=final_screenshot)
                print(f"  [DEBUG] Final screenshot: {final_screenshot}")
                
                html_content = await page.content()
                html_path = os.path.join(screenshot_dir, f"{origin}_{destination}_page.html")
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"  [DEBUG] Page HTML saved: {html_path}")


            
            # Extract prices using JavaScript
            print(f"  [DEBUG] Clicking 'View details' buttons to expand flight info...")
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
            
            # Wait for details to expand
            await page.wait_for_timeout(5000)
            
            prices = await page.evaluate("""
                () => {
                    const flights = [];
                    const uniqueKeys = new Set();
                    const containers = document.querySelectorAll('[class*="Journey"][class*="Container"]');
                    
                    console.log(`Found ${containers.length} flight containers`);
                    
                    // First, collect ALL flight numbers from the entire page
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
                    
                    let flightIndex = 0;
                    
                    containers.forEach(container => {
                        const priceEl = container.querySelector('[class*="Price"] [class*="gBxbny"]');
                        const times = container.querySelectorAll('[class*="Text"][class*="hBKgBd"], [class*="Text"][class*="eQIcKu"]');
                        
                        if (priceEl) {
                            const price = parseInt(priceEl.textContent.replace(/,/g, ''));
                            const departTime = times[0]?.textContent.trim() || '';
                            const arriveTime = times[1]?.textContent.trim() || '';
                            
                            // Deduplicate based on price and times ONLY (not flight number)
                            const key = `${price}-${departTime}-${arriveTime}`;
                            
                            if (!uniqueKeys.has(key)) {
                                uniqueKeys.add(key);
                                
                                // Assign flight number by index if available
                                const flightNum = flightIndex < allFlightNumbers.length ? allFlightNumbers[flightIndex] : "N/A";
                                
                                flights.push({
                                    flightNumber: flightNum,
                                    price: price,
                                    departTime: departTime,
                                    arriveTime: arriveTime
                                });
                                flightIndex++;
                            }
                        }
                    });
                    
                    return flights.sort((a, b) => a.price - b.price);
                }
            """)
            
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
            print(f"  [ERROR] Exception occurred: {type(e).__name__}")
            print(f"  [ERROR] Error message: {str(e)}")
            import traceback
            print(f"  [ERROR] Traceback:")
            traceback.print_exc()
            
            try:
                await context.close()
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
