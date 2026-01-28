#!/usr/bin/env python3
"""
Helper script to update the GitHub Actions workflow schedule
"""

import yaml
import sys

def bangkok_to_utc(bangkok_hour):
    """Convert Bangkok time (UTC+7) to UTC"""
    utc_hour = (bangkok_hour - 7) % 24
    return utc_hour

def update_schedule(bangkok_hour, days='*'):
    """
    Update the schedule in both config.yml and the workflow file
    
    Args:
        bangkok_hour: Hour in Bangkok time (0-23)
        days: Days of week (e.g., '*' for all, '1,3,5' for Mon/Wed/Fri)
    """
    utc_hour = bangkok_to_utc(bangkok_hour)
    cron_schedule = f'0 {utc_hour} * * {days}'
    
    # Update config.yml
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)
    
    config['schedule']['cron'] = cron_schedule
    
    with open('config.yml', 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    # Update workflow file
    workflow_file = '.github/workflows/price-check.yml'
    with open(workflow_file, 'r') as f:
        lines = f.readlines()
    
    # Find and update the cron line
    for i, line in enumerate(lines):
        if line.strip().startswith('- cron:'):
            lines[i] = f"    - cron: '{cron_schedule}'\n"
            break
    
    with open(workflow_file, 'w') as f:
        f.writelines(lines)
    
    print(f"✓ Schedule updated!")
    print(f"  Bangkok time: {bangkok_hour}:00")
    print(f"  UTC time: {utc_hour}:00")
    print(f"  Cron: {cron_schedule}")
    print(f"\nDon't forget to commit and push:")
    print(f"  git add config.yml .github/workflows/price-check.yml")
    print(f"  git commit -m 'Update schedule to {bangkok_hour}:00 Bangkok time'")
    print(f"  git push")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 update_schedule.py <bangkok_hour> [days]")
        print("\nExamples:")
        print("  python3 update_schedule.py 8        # Daily at 8 AM")
        print("  python3 update_schedule.py 20       # Daily at 8 PM")
        print("  python3 update_schedule.py 8 1,3,5  # Mon/Wed/Fri at 8 AM")
        print("  python3 update_schedule.py 12 1     # Every Monday at 12 PM")
        sys.exit(1)
    
    bangkok_hour = int(sys.argv[1])
    days = sys.argv[2] if len(sys.argv) > 2 else '*'
    
    if bangkok_hour < 0 or bangkok_hour > 23:
        print("Error: Hour must be between 0 and 23")
        sys.exit(1)
    
    update_schedule(bangkok_hour, days)
