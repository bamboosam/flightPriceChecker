# Configuration Guide

This file allows you to customize the flight price checker.

## Changing Routes

Edit the `routes` list in `config.yml`:

```yaml
routes:
  - origin: KOP
    destination: DMK
    date: '04/04/2026'
    
  - origin: BKK
    destination: CNX
    date: '15/02/2026'
```

**Date format**: DD/MM/YYYY

## Airport Codes

Common Thai airport codes:
- **DMK** - Don Mueang (Bangkok)
- **BKK** - Suvarnabhumi (Bangkok)
- **CNX** - Chiang Mai
- **HKT** - Phuket
- **KOP** - Nakhon Phanom

## Setting Up Cron (Optional)

To run automatically on a schedule, set up a cron job:

```bash
# Open crontab editor
crontab -e

# Add a line to run daily at 8 AM
0 8 * * * cd /path/to/flightPriceChecker && ./run.sh >> /var/log/flight_checker.log 2>&1
```

### Cron Format

```
minute hour day month weekday
```

- **minute**: 0-59
- **hour**: 0-23
- **day**: 1-31
- **month**: 1-12
- **weekday**: 0-7 (0 and 7 are Sunday)

### Common Schedules

```bash
# Daily at 8 AM
0 8 * * * cd /path/to/project && ./run.sh

# Daily at 8 PM
0 20 * * * cd /path/to/project && ./run.sh

# Twice daily: 8 AM and 8 PM
0 8,20 * * * cd /path/to/project && ./run.sh

# Every Monday at 8 AM
0 8 * * 1 cd /path/to/project && ./run.sh

# Monday, Wednesday, Friday at 8 AM
0 8 * * 1,3,5 cd /path/to/project && ./run.sh
```

## After Making Changes

1. Save `config.yml`  
2. Run the script manually to test:
   ```bash
   ./run.sh
   ```

## Testing

```bash
# Activate virtual environment
source venv/bin/activate

# Run the checker
python3 check_prices_realmouse.py
```

The script will read routes from `config.yml` automatically.
