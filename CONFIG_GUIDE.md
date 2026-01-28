# Configuration Guide

This file allows you to customize the flight price checker without editing code.

## Quick Method: Update Schedule Script

The easiest way to change the schedule:

```bash
# Daily at 8 AM Bangkok time
python3 update_schedule.py 8

# Daily at 8 PM Bangkok time
python3 update_schedule.py 20

# Monday, Wednesday, Friday at 8 AM
python3 update_schedule.py 8 1,3,5

# Every Monday at 12 PM
python3 update_schedule.py 12 1
```

This automatically updates both `config.yml` and the workflow file, and converts Bangkok time to UTC for you!

---

## Changing the Schedule

Edit the `schedule.cron` value in `config.yml`:

```yaml
schedule:
  cron: '0 1 * * *'  # Your desired schedule
```

### Cron Format

```
minute hour day month weekday
```

- **minute**: 0-59
- **hour**: 0-23 (in UTC)
- **day**: 1-31
- **month**: 1-12
- **weekday**: 0-7 (0 and 7 are Sunday)

### Bangkok Time to UTC Conversion

Bangkok is UTC+7, so subtract 7 hours:

- 8 AM Bangkok = 1 AM UTC → `0 1 * * *`
- 12 PM Bangkok = 5 AM UTC → `0 5 * * *`
- 8 PM Bangkok = 1 PM UTC → `0 13 * * *`

### Common Schedules

```yaml
# Daily at 8 AM Bangkok time
schedule:
  cron: '0 1 * * *'

# Daily at 12 PM Bangkok time
schedule:
  cron: '0 5 * * *'

# Daily at 8 PM Bangkok time
schedule:
  cron: '0 13 * * *'

# Twice daily: 8 AM and 8 PM Bangkok time
schedule:
  cron: '0 1,13 * * *'

# Every Monday at 8 AM Bangkok time
schedule:
  cron: '0 1 * * 1'

# Monday, Wednesday, Friday at 8 AM Bangkok time
schedule:
  cron: '0 1 * * 1,3,5'

# Every 6 hours (2 AM, 8 AM, 2 PM, 8 PM Bangkok time)
schedule:
  cron: '0 1,7,13,19 * * *'
```

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

## After Making Changes

1. Save `config.yml`
2. Commit and push to GitHub:
   ```bash
   git add config.yml
   git commit -m "Update schedule/routes"
   git push
   ```

**Note**: Schedule changes in `config.yml` are for documentation. To actually change the GitHub Actions schedule, you need to edit `.github/workflows/price-check.yml` and update the cron value there as well.

**Alternative**: Use the manual "Run workflow" button in GitHub Actions to run at any time without changing the schedule.

## Testing Locally

```bash
# Install dependencies
pip install pyyaml playwright
playwright install chromium

# Run the checker
python3 check_prices.py
```

The script will read routes from `config.yml` automatically.
