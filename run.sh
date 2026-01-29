#!/bin/bash
# Run flight price checker - supports both visible and invisible modes

MODE=${1:-invisible}

if [ "$MODE" = "visible" ]; then
    echo "=========================================="
    echo "Running in VISIBLE mode (VNC)"
    echo "=========================================="
    echo
    echo "Starting VNC server on :1 (port 5901)..."
    
    # Kill existing VNC server if any
    vncserver -kill :1 2>/dev/null || true
    
    # Start VNC server
    vncserver :1 -geometry 1280x720 -depth 24
    
    echo
    echo "✓ VNC server started!"
    echo "Connect with VNC Viewer to: $(hostname -I | awk '{print $1}'):5901"
    echo
    echo "Starting price checker..."
    
    # Run on VNC display
    DISPLAY=:1 ./venv/bin/python3 check_prices_realmouse.py
    
    echo
    echo "Keep VNC server running? (y/n)"
    read -r response
    if [ "$response" != "y" ]; then
        vncserver -kill :1
        echo "VNC server stopped"
    fi
    
elif [ "$MODE" = "invisible" ]; then
    echo "=========================================="
    echo "Running in INVISIBLE mode (Xvfb)"
    echo "=========================================="
    echo
    
    # Run with virtual display
    xvfb-run -a ./venv/bin/python3 check_prices_realmouse.py
    
elif [ "$MODE" = "test" ]; then
    echo "=========================================="
    echo "Running MOUSE TEST in VISIBLE mode"
    echo "=========================================="
    echo
    
    # Kill existing VNC server if any
    vncserver -kill :1 2>/dev/null || true
    
    # Start VNC server
    vncserver :1 -geometry 1280x720 -depth 24
    
    echo
    echo "✓ VNC server started!"
    echo "Connect with VNC Viewer to: $(hostname -I | awk '{print $1}'):5901"
    echo
    echo "Press ENTER when you're connected and ready to see the mouse test..."
    read
    
    # Run mouse test on VNC display
    DISPLAY=:1 ./venv/bin/python3 test_mouse_movement.py
    
    echo
    vncserver -kill :1
    echo "VNC server stopped"
    
else
    echo "Usage: $0 [visible|invisible|test]"
    echo
    echo "  visible   - Run with VNC server (you can watch)"
    echo "  invisible - Run with Xvfb (headless, for production)"
    echo "  test      - Run mouse test with VNC (for debugging)"
    echo
    exit 1
fi
