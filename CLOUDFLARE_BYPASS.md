# Cloudflare Bypass Implementation

This implementation uses **image processing** and **human-like mouse automation** to attempt to bypass Cloudflare's Turnstile challenge.

## How It Works

1. **Detection**: Automatically detects when a Cloudflare challenge appears
2. **Checkbox Location**: Uses two methods to find the checkbox:
   - **DOM Inspection**: Searches for Cloudflare iframe elements
   - **Image Processing**: Uses OpenCV to detect checkbox in screenshots (fallback)
3. **Human-like Clicking**: Simulates realistic mouse movement using Bezier curves
4. **Timing Variations**: Adds random delays to mimic human behavior

## Installation

### Dependencies

Install the required Python packages:

```bash
# If using a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
pip install -r requirements.txt

# Or install individually
pip install opencv-python==4.9.0.80 numpy==1.26.4
```

### DevContainer Setup

If you're using the DevContainer, the dependencies should be installed automatically. If not, run:

```bash
pip install opencv-python numpy
```

## Files Modified/Created

- **`cloudflare_bypass.py`** (NEW): Main bypass module with all the logic
- **`check_prices.py`** (MODIFIED): Integrated bypass module
- **`requirements.txt`** (MODIFIED): Added opencv-python and numpy

## Usage

The bypass is **automatic**. When you run `check_prices.py`, it will:

1. Navigate to AirAsia
2. Detect if Cloudflare challenge appears
3. Automatically attempt to bypass it
4. Continue with flight price checking if successful

```bash
python check_prices.py
```

## Debug Output

The script provides detailed debug output:

```
[DEBUG] ⚠ Cloudflare challenge detected! Attempting bypass...
[DEBUG] Found Cloudflare element: {...}
[DEBUG] Moving mouse from (x1, y1) to (x2, y2)
[DEBUG] Clicked at (x, y)
[DEBUG] Waiting for challenge to process...
[DEBUG] ✓ Cloudflare challenge passed!
```

## Success Rate

> **Note**: This is an **experimental approach**. Success rate depends on:
> - Cloudflare's current detection algorithms
> - Network conditions
> - Random timing variations
> - Whether additional challenges appear (image selection, etc.)

**Expected success rate**: 30-60% (varies)

## Troubleshooting

### Checkbox Not Found

If the bypass can't find the checkbox:
- Check `debug_screenshots/` for the Cloudflare screenshot
- The checkbox might be in a different location
- Cloudflare might be showing a different type of challenge

### Challenge Doesn't Pass

If the checkbox is clicked but challenge doesn't pass:
- Cloudflare detected the automation
- Try running in **headed mode** to see what's happening
- Consider using Approach 1 (Enhanced Stealth) or Approach 4 (CAPTCHA Service)

### Import Errors

If you get `ModuleNotFoundError: No module named 'cv2'`:
```bash
pip install opencv-python
```

## Alternative Approaches

If this approach doesn't work reliably, consider:

1. **Enhanced Stealth Mode**: Improve browser fingerprinting (free)
2. **Headed Browser**: Manual intervention when needed (free)
3. **CAPTCHA Service**: Use 2Captcha or CapSolver (paid, ~$1-3 per 1000 solves)

See `implementation_plan.md` for details on all approaches.

## Technical Details

### Bezier Curve Mouse Movement

The module uses cubic Bezier curves to create natural mouse movement paths:
- Random control points for variation
- Variable speed (faster at start, slower near target)
- Random delays between movements (5-40ms)

### OpenCV Checkbox Detection

Detection algorithm:
1. Convert screenshot to grayscale
2. Apply binary threshold
3. Find contours
4. Filter by size (15-50px) and aspect ratio (0.8-1.2)
5. Prefer candidates in upper portion of page
6. Return center coordinates

### Human-like Timing

- Mouse movement: 5-40ms between points
- Pre-click delay: 100-300ms
- Click duration: 50-150ms
- Post-click delay: 200-500ms
- Challenge wait: 3-5 seconds (random)
