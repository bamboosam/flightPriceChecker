/**
 * AirAsia Price Extractor
 * Extracts flight prices and details from AirAsia search results page
 */

/**
 * Wait for flight results to load on the page
 * @param {number} timeout - Maximum wait time in milliseconds (default: 15000)
 * @returns {Promise<boolean>} True if results loaded, false if timeout
 */
async function waitForFlightResults(timeout = 15000) {
    console.log('[Price Extractor] Waiting for flight results to load...');

    const startTime = Date.now();

    return new Promise((resolve) => {
        const checkInterval = setInterval(() => {
            // Look for flight containers
            const flightContainers = document.querySelectorAll('[class*="Journey"][class*="Container"], [class*="flight-card"], [class*="FlightCard"]');

            // Look for price elements
            const priceElements = document.querySelectorAll('[class*="Price"][class*="Container"], [class*="price"]');

            if (flightContainers.length > 0 && priceElements.length > 0) {
                console.log(`[Price Extractor] Found ${flightContainers.length} flights`);
                clearInterval(checkInterval);
                resolve(true);
            } else if (Date.now() - startTime > timeout) {
                console.warn('[Price Extractor] Timeout waiting for results');
                clearInterval(checkInterval);
                resolve(false);
            }
        }, 500);
    });
}

/**
 * Extract all flight prices from the current page
 * @returns {Array} Array of flight objects with price, currency, times, etc.
 */
function extractFlightPrices() {
    console.log('[Price Extractor] Extracting flight prices from page...');

    const flights = [];

    // Find all flight containers
    const flightContainers = document.querySelectorAll('[class*="Journey"][class*="Container"], [class*="flight-card"], [class*="FlightCard"]');

    console.log(`[Price Extractor] Found ${flightContainers.length} flight containers`);

    flightContainers.forEach((container, index) => {
        try {
            // Extract price
            const priceContainer = container.querySelector('[class*="Price"][class*="Container"]');
            if (!priceContainer) {
                console.warn(`[Price Extractor] No price container found for flight ${index + 1}`);
                return;
            }

            // Try multiple selectors for price amount
            let priceText = null;
            const priceSelectors = [
                '[class*="gBxbny"]',
                '[class*="price-amount"]',
                '[class*="PriceAmount"]',
                'span[class*="price"]'
            ];

            for (const selector of priceSelectors) {
                const priceEl = priceContainer.querySelector(selector);
                if (priceEl && priceEl.textContent.trim()) {
                    priceText = priceEl.textContent.trim();
                    break;
                }
            }

            if (!priceText) {
                // Fallback: get all text from price container
                priceText = priceContainer.textContent.trim();
            }

            // Extract numeric price
            const priceMatch = priceText.match(/[\d,]+/);
            const price = priceMatch ? parseInt(priceMatch[0].replace(/,/g, '')) : null;

            if (!price) {
                console.warn(`[Price Extractor] Could not parse price from: ${priceText}`);
                return;
            }

            // Extract currency
            let currency = 'THB'; // default
            const currencySelectors = [
                '[class*="jdXHQd"]',
                '[class*="currency"]',
                '[class*="Currency"]'
            ];

            for (const selector of currencySelectors) {
                const currencyEl = priceContainer.querySelector(selector);
                if (currencyEl && currencyEl.textContent.trim()) {
                    currency = currencyEl.textContent.trim();
                    break;
                }
            }

            // Extract times
            const timeElements = container.querySelectorAll('[class*="time"], [class*="Time"]');
            let departTime = null;
            let arriveTime = null;

            if (timeElements.length >= 2) {
                departTime = timeElements[0].textContent.trim();
                arriveTime = timeElements[1].textContent.trim();
            }

            // Extract carrier/airline
            let carrier = 'AirAsia'; // default
            const carrierEl = container.querySelector('[class*="Carrier"], [class*="airline"], [alt*="AirAsia"]');
            if (carrierEl) {
                carrier = carrierEl.getAttribute('alt') || carrierEl.textContent.trim() || 'AirAsia';
            }

            // Extract duration
            let duration = null;
            const durationEl = container.querySelector('[class*="duration"], [class*="Duration"]');
            if (durationEl) {
                duration = durationEl.textContent.trim();
            }

            flights.push({
                price,
                currency,
                departTime,
                arriveTime,
                duration,
                carrier,
                priceDisplay: `${currency} ${price.toLocaleString()}`
            });

            console.log(`[Price Extractor] Flight ${index + 1}:`, {
                price,
                currency,
                departTime,
                arriveTime,
                carrier
            });

        } catch (error) {
            console.error(`[Price Extractor] Error extracting flight ${index + 1}:`, error);
        }
    });

    // Sort by price (cheapest first)
    flights.sort((a, b) => a.price - b.price);

    console.log(`[Price Extractor] Successfully extracted ${flights.length} flights`);
    console.log('[Price Extractor] Cheapest flight:', flights[0]);

    return flights;
}

/**
 * Get the cheapest flight from the current page
 * @returns {Object|null} Cheapest flight object or null if no flights found
 */
function getCheapestFlight() {
    const flights = extractFlightPrices();
    return flights.length > 0 ? flights[0] : null;
}

/**
 * Extract low fare calendar data (prices for adjacent dates)
 * @returns {Array} Array of {date, price, currency} objects
 */
function extractLowFareCalendar() {
    console.log('[Price Extractor] Extracting low fare calendar...');

    const calendarData = [];

    // Find calendar carousel
    const calendarItems = document.querySelectorAll('[class*="LFC"], [class*="calendar"], [class*="date-picker"] button, [class*="date-picker"] div[role="button"]');

    calendarItems.forEach((item) => {
        try {
            const dateText = item.querySelector('[class*="date"]')?.textContent.trim();
            const priceText = item.querySelector('[class*="price"]')?.textContent.trim();

            if (dateText && priceText) {
                const priceMatch = priceText.match(/[\d,]+/);
                const price = priceMatch ? parseInt(priceMatch[0].replace(/,/g, '')) : null;

                if (price) {
                    calendarData.push({
                        date: dateText,
                        price,
                        priceDisplay: priceText
                    });
                }
            }
        } catch (error) {
            // Ignore errors for individual calendar items
        }
    });

    console.log(`[Price Extractor] Found ${calendarData.length} calendar dates`);

    return calendarData;
}

// Export functions
window.waitForFlightResults = waitForFlightResults;
window.extractFlightPrices = extractFlightPrices;
window.getCheapestFlight = getCheapestFlight;
window.extractLowFareCalendar = extractLowFareCalendar;

// Example usage:
// await waitForFlightResults();
// const flights = extractFlightPrices();
// const cheapest = getCheapestFlight();
