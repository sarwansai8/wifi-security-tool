# Wi-Fi Security Assessment Tool

An educational tool for demonstrating Wi-Fi security concepts and network vulnerability assessment.

## Disclaimer

**IMPORTANT**: This tool is designed for educational purposes only. Only scan networks you own or have explicit permission to test. Unauthorized scanning or testing of networks may violate laws and regulations.

## Features

- **Network Discovery**: Scan and identify nearby Wi-Fi networks
- **Handshake Capture**: Guide for capturing WPA/WPA2 handshakes
- **Password Analysis**: Test password strength and estimate cracking time
- **Educational Resources**: Learn about Wi-Fi security best practices

## Requirements

- Python 3.8+
- Required packages listed in requirements.txt

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

# Update packages
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Install Buildozer
pip3 install --user --upgrade buildozer

# Add Python user base to PATH
echo 'export PATH=$PATH:$HOME/.local/bin' >> ~/.bashrc
source ~/.bashrc# Add the remote
git remote add origin https://github.com/sarwansai8/wifi-security-tool.git

# Set up your Git credentials (one-time setup)
git config --global credential.helper store

# Push your code (you'll be prompted for credentials)
git push -u origin main
## License

For educational purposes only.
