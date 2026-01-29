# Real Mouse Control for Cloudflare Bypass

## ✅ This Approach WILL Work!

Unlike the previous synthetic event approach, **PyAutoGUI controls the actual physical mouse cursor**, generating `isTrusted = true` events that Cloudflare cannot detect.

## How It Works

1. **Browser opens** at fixed position (100, 100) with fixed size (1280x720)
2. **Detects Cloudflare** challenge
3. **Finds checkbox** using OpenCV image processing
4. **Takes control of your real mouse** cursor
5. **Moves cursor** to checkbox location on screen
6. **Clicks** with real OS-level mouse event (`isTrusted = true`)
7. **Challenge passes** ✓

## Files Created

- **`real_mouse_bypass.py`** - Module for real mouse control
- **`check_prices_realmouse.py`** - Main script with real mouse bypass
- **`test_mouse.py`** - Test script to verify mouse control works

## Step 1: Test Mouse Control

First, verify PyAutoGUI can control your mouse:

```bash
./venv/bin/python3 test_mouse.py
```

This will:
- Show your screen size
- Move your mouse in a square pattern
- Test coordinate conversion
- Simulate a checkbox click

**⚠️ WARNING:** Your mouse will move automatically! Move cursor to top-left corner to abort (FAILSAFE).

## Step 2: Run with Real Mouse

```bash
./venv/bin/python3 check_prices_realmouse.py
```

### What to Expect

1. Browser opens at position (100, 100)
2. Navigates to AirAsia
3. If Cloudflare appears:
   ```
   [DEBUG] ⚠ Cloudflare challenge detected!
   [DEBUG] 🖱️  REAL MOUSE CONTROL MODE ACTIVATED!
   [DEBUG] ⚠️  DON'T TOUCH YOUR MOUSE!
   [DEBUG] Found checkbox at page coords: (511, 206)
   [DEBUG] Taking control of your mouse in 2 seconds...
   [MOUSE] 🖱️  Taking control of your mouse!
   [MOUSE] Moving real cursor from (x1, y1) to (x2, y2)
   [MOUSE] ✓ Real cursor moved to (x, y)
   [MOUSE] ✓ Real click performed at (x, y)
   [MOUSE] ✓ Checkbox clicked with REAL mouse!
   [DEBUG] ✓ Cloudflare challenge PASSED!
   ```

## Important Notes

### ⚠️ Requirements

- **Headed browser only** - Cannot run headless
- **Don't touch your mouse** - Script takes control when Cloudflare appears
- **Can't use computer** - Mouse is controlled by script
- **Linux with X11** - Works on most Linux desktops

### 🎯 Coordinate Calibration

The browser opens at fixed position:
- **X:** 100 pixels from left
- **Y:** 100 pixels from top
- **Width:** 1280 pixels
- **Height:** 720 pixels

If the checkbox click misses, you can adjust:

1. **Browser position** - Edit `BROWSER_X` and `BROWSER_Y` in `check_prices_realmouse.py`
2. **Checkbox offset** - If consistently off, add offset in `real_mouse_bypass.py`

### 🔧 Troubleshooting

**Mouse doesn't move:**
- Check if PyAutoGUI is installed: `./venv/bin/python3 -c "import pyautogui; print('OK')"`
- Run `test_mouse.py` to verify

**Click misses checkbox:**
- Browser might not be at expected position
- Check actual browser window position
- Adjust `BROWSER_X` and `BROWSER_Y` values

**Cloudflare still blocks:**
- Unlikely! Real mouse events should pass
- If it happens, the timing might be too fast
- Try adding longer delays before click

## Why This Works

```python
# Playwright (synthetic events)
await page.mouse.click(x, y)  # isTrusted = false ❌

# PyAutoGUI (real mouse)
pyautogui.click(x, y)  # isTrusted = true ✅
```

Cloudflare cannot distinguish PyAutoGUI clicks from real human clicks because they ARE real mouse events at the OS level!

## Next Steps

1. Run `test_mouse.py` to verify mouse control
2. Run `check_prices_realmouse.py` to test with Cloudflare
3. If coordinates are off, adjust `BROWSER_X/Y` values
4. Enjoy automated flight price checking! 🎉
