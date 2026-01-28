---
name: getting-airasia-prices
description: Searches for flight prices on AirAsia.com for a specific route and date. Use when the user wants to find the cheapest flights or check availability for a specific day.
---

# Getting AirAsia Prices

## When to use this skill
- User asks to "check flight prices" on AirAsia.
- User wants to find the cheapest fare for a specific route.
- User needs to verify flight availability for a date.

## Workflow
## Workflow
- [ ] Start browser and navigate to AirAsia.
- [ ] Read and execute the optimization script (`scripts/airasia-search.js`).
- [ ] Wait for search results and verify date.
- [ ] Capture screenshot and report prices.

## Instructions

> [!IMPORTANT]
> **New Approach**: This skill now uses direct URL navigation instead of form automation. This is faster, more reliable, and eliminates all form interaction issues.

### Workflow

1. **Build Search URL**
   - Read the URL builder script from filesystem (use `view_file` tool)
   - Build the URL directly or execute the script to construct it
   - Parameters: origin, destination, date, options (adult count, trip type, etc.)

2. **Navigate to Results Page**
   - Open the constructed URL directly in browser
   - The URL format: `https://www.airasia.com/flights/search/?origin=XXX&destination=YYY&departDate=DD%2FMM%2FYYYY&tripType=O&adult=N&locale=en-gb&currency=THB`
   - Wait 5-10 seconds for results to load

3. **Extract Flight Prices**
   - Read the price extractor script from filesystem (use `view_file` tool)
   - Execute the script in the browser console on the results page
   - The script will automatically find all flights and extract prices
   - Get the cheapest flight details

4. **Report Findings**
   - Report the cheapest flight price and details
   - Include departure and arrival times
   - List all available flight options sorted by price
   - Note any special deals or promotions visible

### Quick Reference

**URL Construction:**
```javascript
// One-way flight
https://www.airasia.com/flights/search/?origin=BKK&destination=CNX&departDate=20%2F02%2F2026&tripType=O&adult=2&locale=en-gb&currency=THB

// Round-trip flight
https://www.airasia.com/flights/search/?origin=BKK&destination=CNX&departDate=20%2F02%2F2026&returnDate=25%2F02%2F2026&tripType=R&adult=2&locale=en-gb&currency=THB
```

**Price Extraction:**
- Read `/home/bamboosam/AI Coding/flightPriceChecker/.agent/skills/getairasiaprice/scripts/airasia-price-extractor.js`
- Execute on the results page
- Use `window.extractFlightPrices()` or `window.getCheapestFlight()`

### Troubleshooting

**If "No flights found" message appears:**
1. Wait 5 seconds for the page to fully load
2. Click the green "Search" button again to trigger a fresh data fetch
3. Wait another 5-10 seconds for results to appear
4. This forces the page to reload flight data from the server

**Note:** Sometimes the initial URL navigation doesn't trigger the flight search properly. Clicking the search button manually resolves this issue.

### Parameters

**URL Builder accepts:**
- `origin`: Airport code (e.g., 'BKK') or city name (e.g., 'Bangkok')
- `destination`: Airport code or city name
- `departDate`: Date in 'DD/MM/YYYY' or 'YYYY-MM-DD' format
- `options` (optional):
  - `tripType`: 'O' (one-way, default) or 'R' (round-trip)
  - `returnDate`: Required if tripType is 'R'
  - `adult`: Number of adults (default: 1)
  - `child`: Number of children (default: 0)
  - `infant`: Number of infants (default: 0)
  - `currency`: Currency code (default: 'THB')

### Example Usage

**One-way flight:**
```javascript
const url = buildAirAsiaSearchUrl('Bangkok', 'Chiang Mai', '15/02/2026');
// Opens: https://www.airasia.com/flights/search/?origin=BKK&destination=CNX&departDate=15%2F02%2F2026&tripType=O&adult=1&locale=en-gb&currency=THB
```

**Round-trip flight:**
```javascript
const url = buildAirAsiaSearchUrl('BKK', 'SIN', '2026-03-01', {
  tripType: 'R',
  returnDate: '2026-03-05',
  adult: 2,
  currency: 'SGD'
});
```
