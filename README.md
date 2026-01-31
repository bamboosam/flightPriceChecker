# Flight Price Checker

Automated AirAsia flight price monitoring for VM with desktop environment.

## Features

- ✅ Automated daily price checks
- ✅ Monitors multiple routes simultaneously
- ✅ Saves price history to JSON
- ✅ Uses real mouse movements to bypass Cloudflare
- ✅ Runs in a VM with desktop environment

## Quick Start

### 1. Setup VM Environment

Run the setup script:

```bash
chmod +x vm_setup.sh
./vm_setup.sh
```

Or follow [DEBIAN_SETUP.md](DEBIAN_SETUP.md) for manual setup.

### 2. Configure Routes

Edit `config.yml`:

```yaml
routes:
  - origin: KOP
    destination: DMK
    date: '04/04/2026'
```

See [CONFIG_GUIDE.md](CONFIG_GUIDE.md) for all options.

### 3. Run

```bash
./run.sh
```

Or manually:

```bash
source venv/bin/activate
python3 check_prices_realmouse.py
```

## View Results

Check `price_history.json` to see all historical price data.

## Documentation

- [VM Startup Guide](VM_STARTUP_GUIDE.md) - How to start the VM and run checks
- [Fresh Install Guide](FRESH_INSTALL_GUIDE.md) - Complete setup from scratch
- [Debian Setup](DEBIAN_SETUP.md) - Debian-specific instructions
- [Config Guide](CONFIG_GUIDE.md) - Configuration options

## How It Works

1. Script opens a headed browser with real mouse control
2. Navigates to AirAsia search results pages
3. Uses PyAutoGUI for human-like mouse movements (Cloudflare bypass)
4. Extracts flight prices and details
5. Saves results to `price_history.json`

## Requirements

- VM with desktop environment (XFCE, GNOME, etc.)
- Python 3.8+
- Chromium browser
- PyAutoGUI for mouse control

## License

MIT
