# DevPod / DevContainer Setup

This project includes a DevContainer configuration for easy development environment setup.

## What is DevPod?

DevPod creates reproducible development environments that work the same way on any machine. It's like GitHub Codespaces but can run locally or on your own infrastructure.

## Quick Start

### Using DevPod CLI

1. **Install DevPod**: https://devpod.sh/docs/getting-started/install

2. **Start the environment**:
   ```bash
   devpod up .
   ```

3. **Open in your IDE**:
   ```bash
   devpod ide .
   ```

### Using VS Code

1. Install the **Dev Containers** extension
2. Open this folder in VS Code
3. Click "Reopen in Container" when prompted (or use Command Palette: "Dev Containers: Reopen in Container")

## What's Included

The devcontainer automatically sets up:

- ✅ **Python 3.11** environment
- ✅ **Playwright** with Chromium browser
- ✅ **All dependencies** from `requirements.txt`
- ✅ **VS Code extensions**: Python, Pylance, Black formatter
- ✅ **Git** for version control

## First Run

After the container starts, everything is ready to go:

```bash
# Run the headed version (with visible browser)
python check_prices_headed.py

# Run the headless version
python check_prices.py
```

## Configuration

Edit `.devcontainer/devcontainer.json` to customize:
- Python version
- VS Code extensions
- Additional tools
- Port forwarding

## Troubleshooting

**Browser not launching?**
The devcontainer installs Chromium and its dependencies automatically. If you still have issues, run:
```bash
playwright install-deps chromium
```

**Permission issues?**
The container runs as the `vscode` user by default. All files should be accessible.
