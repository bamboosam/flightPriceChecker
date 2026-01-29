# PyAutoGUI Setup Issue - Tkinter Required

## Problem

PyAutoGUI requires `tkinter` (Python's GUI library) to function, but it's not installed in your system.

## Solution

Install tkinter system package:

```bash
sudo apt-get update
sudo apt-get install python3-tk python3-dev
```

## After Installing

Test that PyAutoGUI works:

```bash
./venv/bin/python3 -c "import pyautogui; print('✓ PyAutoGUI works!'); print('Screen:', pyautogui.size())"
```

Then run the real mouse bypass script:

```bash
./venv/bin/python3 check_prices_realmouse.py
```

## Alternative: Manual Intervention Mode

If you don't want to install system packages, I can implement a **manual intervention mode** instead:

- Script detects Cloudflare
- Pauses and waits for you
- You manually click the checkbox
- Script continues automatically

This would be 100% reliable and doesn't require PyAutoGUI.

Let me know which approach you prefer!
