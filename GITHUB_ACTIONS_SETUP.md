# GitHub Actions Deployment - Quick Start Guide

## What This Does

The GitHub Actions workflow will:
- ✅ Run automatically every day at 8 AM Bangkok time
- ✅ Check flight prices for your configured routes
- ✅ Save results to `price_history.json`
- ✅ Commit and push the updated history to your repository
- ✅ Run in the cloud (no need to keep your computer on)

## Setup Steps

### 1. Configure Your Routes

Edit `check_prices.py` and update the `ROUTES` list:

```python
ROUTES = [
    {"origin": "KOP", "destination": "DMK", "date": "04/04/2026"},
    {"origin": "DMK", "destination": "KOP", "date": "05/05/2026"},
    # Add more routes as needed
]
```

### 2. Initialize Git Repository (if not already done)

```bash
cd /home/bamboosam/AI\ Coding/flightPriceChecker
git init
git add .
git commit -m "Initial commit with flight price checker"
```

### 3. Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., `flight-price-checker`)
3. Don't initialize with README (you already have files)

### 4. Push to GitHub

```bash
# Replace with your repository URL
git remote add origin https://github.com/YOUR_USERNAME/flight-price-checker.git
git branch -M main
git push -u origin main
```

### 5. Enable GitHub Actions

GitHub Actions should be enabled by default. The workflow will:
- Run automatically at 8 AM Bangkok time daily
- Can also be triggered manually from the "Actions" tab

### 6. Test the Workflow

**Option A: Wait for scheduled run**
- The workflow will run automatically at 8 AM Bangkok time

**Option B: Trigger manually**
1. Go to your repository on GitHub
2. Click "Actions" tab
3. Click "Daily Flight Price Check" workflow
4. Click "Run workflow" button
5. Click "Run workflow" to confirm

## Viewing Results

### Check Workflow Status

1. Go to your repository on GitHub
2. Click "Actions" tab
3. See the latest workflow runs and their status

### View Price History

1. Go to your repository on GitHub
2. Open `price_history.json`
3. See all historical price checks

### Download Results

```bash
# Pull latest results from GitHub
git pull
cat price_history.json
```

## Customization

### Change Schedule

Edit `.github/workflows/price-check.yml`:

```yaml
on:
  schedule:
    # Run at 1:00 AM UTC (8:00 AM Bangkok time)
    - cron: '0 1 * * *'
```

**Common schedules:**
- `0 1 * * *` - Daily at 8 AM Bangkok time (1 AM UTC)
- `0 13 * * *` - Daily at 8 PM Bangkok time (1 PM UTC)
- `0 1,13 * * *` - Twice daily (8 AM and 8 PM Bangkok time)
- `0 1 * * 1` - Every Monday at 8 AM Bangkok time

### Add Email Notifications

GitHub Actions can send you emails when workflows fail. To get notifications:

1. Go to your GitHub profile → Settings → Notifications
2. Enable "Actions" notifications
3. Choose email delivery

### Add Telegram Notifications

Add to `check_prices.py` before the script ends:

```python
import requests

def send_telegram(results):
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        return
    
    message = "🛫 Daily Flight Price Check:\n\n"
    for result in results:
        if result.get('cheapest'):
            message += f"{result['route']}: THB {result['cheapest']['price']}\n"
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": message})

# Call in main():
send_telegram(results)
```

Then add secrets to GitHub:
1. Go to repository → Settings → Secrets and variables → Actions
2. Add `TELEGRAM_BOT_TOKEN` (from @BotFather)
3. Add `TELEGRAM_CHAT_ID` (your chat ID)

## Troubleshooting

### Workflow not running?

- Check the "Actions" tab for errors
- Verify the cron schedule is correct
- GitHub Actions may have a few minutes delay

### Permission errors?

The workflow needs write permissions:
1. Go to repository → Settings → Actions → General
2. Scroll to "Workflow permissions"
3. Select "Read and write permissions"
4. Click "Save"

### Price history not updating?

- Check the workflow logs in the "Actions" tab
- Verify `price_history.json` is not in `.gitignore`
- Check if the script is finding flights

## Cost

GitHub Actions is **FREE** for public repositories with:
- 2,000 minutes/month for private repos
- Unlimited for public repos

Your workflow uses ~5 minutes per run, so:
- Daily runs = ~150 minutes/month
- Well within the free tier!

## Next Steps

1. Push your code to GitHub
2. Verify the workflow appears in the "Actions" tab
3. Trigger a manual run to test
4. Check `price_history.json` for results
5. Wait for the first scheduled run at 8 AM

Enjoy automated flight price monitoring! 🎉
