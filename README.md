# Flight Price Checker

Automated AirAsia flight price monitoring using GitHub Actions.

## Features

- ✅ Automated daily price checks at 8 AM Bangkok time
- ✅ Monitors multiple routes simultaneously
- ✅ Saves price history to JSON
- ✅ Runs in the cloud (GitHub Actions)
- ✅ No server or computer needed

## Quick Start

### 1. Configure Schedule and Routes

Edit `config.yml`:

```yaml
schedule:
  cron: '0 1 * * *'  # 8 AM Bangkok time (change as needed)

routes:
  - origin: KOP
    destination: DMK
    date: '04/04/2026'
```

See [CONFIG_GUIDE.md](CONFIG_GUIDE.md) for schedule examples.

### 2. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/flight-price-checker.git
git push -u origin main
```

### 3. Enable Workflow Permissions

1. Go to repository → Settings → Actions → General
2. Under "Workflow permissions", select "Read and write permissions"
3. Click "Save"

### 4. Done!

The workflow will run automatically every day at 8 AM Bangkok time. You can also trigger it manually from the "Actions" tab.

## View Results

Check `price_history.json` in your repository to see all historical price data.

## Manual Testing

Run locally:

```bash
pip install playwright
playwright install chromium
python3 check_prices.py
```

## Documentation

- [GitHub Actions Setup Guide](GITHUB_ACTIONS_SETUP.md) - Detailed setup instructions
- [Deployment Guide](deployment_guide.md) - All deployment options
- [Skill Documentation](.agent/skills/getairasiaprice/SKILL.md) - How the price checker works

## How It Works

1. GitHub Actions triggers the workflow daily at 8 AM Bangkok time
2. The workflow runs `check_prices.py` using Playwright
3. Script navigates to AirAsia search results pages
4. Extracts flight prices and details
5. Saves results to `price_history.json`
6. Commits and pushes the updated history

## Cost

**Free!** GitHub Actions provides:
- Unlimited minutes for public repositories
- 2,000 minutes/month for private repositories
- This workflow uses ~5 minutes per run (~150 minutes/month)

## License

MIT
