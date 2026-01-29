# Testing the Cloudflare Bypass

## Quick Test with Visible Browser

Run the headed browser script to **watch the bypass in action**:

```bash
./venv/bin/python3 check_prices_headed.py
```

## What You'll See

1. **Browser opens** (visible window)
2. **Navigates to AirAsia**
3. **Cloudflare challenge appears**
4. **Script detects it** and prints: `👀 WATCH THE BROWSER - You'll see the mouse move and click!`
5. **Mouse moves** in a curved path (Bezier curve)
6. **Clicks the checkbox**
7. **Waits** for challenge to resolve

## Debugging the Bypass

### If the checkbox is clicked but challenge doesn't pass:

This means Cloudflare detected the automation. Possible reasons:

1. **Mouse movement too fast/perfect** - The Bezier curve might not be random enough
2. **Click timing suspicious** - Cloudflare analyzes click patterns
3. **Browser fingerprint detected** - They know it's Playwright
4. **No prior mouse activity** - Real users move mouse before clicking

### What to watch for:

- Does the mouse movement look natural?
- Does the checkbox get checked?
- Does a loading spinner appear?
- Does an error message show up?
- Does it ask for additional verification (image selection)?

## Next Steps if Bypass Fails

### Option 1: Enhance Stealth (Recommended)
- Add more random mouse movements before clicking
- Vary timing more aggressively
- Add browser fingerprint randomization
- Simulate scrolling and other human behaviors

### Option 2: Manual Intervention
When Cloudflare appears, you can:
1. Manually click the checkbox
2. Let the script continue automatically
3. This is the most reliable for now

### Option 3: CAPTCHA Solving Service
Use 2Captcha or CapSolver (costs ~$1-3 per 1000 solves)

## Current Test Results

From your last run:
```
[DEBUG] Found checkbox candidate at (511, 206)
[DEBUG] Moving mouse from (377, 105) to (511, 206)
[DEBUG] Clicked at (511, 206)
[DEBUG] ✗ Challenge did not complete: Timeout 30000ms exceeded.
```

**Analysis**: The bypass successfully:
- ✅ Detected the challenge
- ✅ Found the checkbox location
- ✅ Moved the mouse
- ✅ Clicked the checkbox

But Cloudflare still detected it as a bot. This suggests we need to improve the **human-like behavior** aspects.
