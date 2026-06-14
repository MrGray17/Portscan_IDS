#!/bin/bash
# AEGIS Ubuntu Server Setup
# Run on Ubuntu Victime (192.168.100.20)

set -e
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== AEGIS Ubuntu Server Setup ===${NC}"

# Install dependencies
echo -e "${YELLOW}[1/6] Installing system packages...${NC}"
sudo apt update -qq
sudo apt install -y python3 python3-pip python3-venv nmap ufw libnetfilter-queue-dev nftables

# Setup Python environment
echo -e "${YELLOW}[2/6] Setting up Python environment...${NC}"
cd /home/$USER/AEGIS 2>/dev/null || cd ~/Portscan_IDS
python3 -m venv venv
source venv/bin/activate
pip install -q flask flask-socketio scapy joblib xgboost scikit-learn pandas numpy

# Configure firewall
echo -e "${YELLOW}[3/6] Configuring firewall...${NC}"
sudo ufw --force reset
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow from 192.168.100.0/24
sudo ufw allow from 192.168.100.0/24 to any port 5000
sudo ufw --force enable

# Verify models
echo -e "${YELLOW}[4/6] Verifying models...${NC}"
python3 -c "
import joblib, os
for f in ['models/saved/rf_model.pkl', 'models/saved/xgb_model.pkl', 'models/saved/scaler.pkl']:
    if os.path.exists(f):
        m = joblib.load(f)
        print(f'  OK: {f} ({type(m).__name__})')
    else:
        print(f'  MISSING: {f}')
"

# Start dashboard
echo -e "${YELLOW}[5/6] Starting AEGIS dashboard...${NC}"
echo -e "${GREEN}Dashboard will be at: http://192.168.100.20:5000${NC}"
echo -e "${GREEN}Run: source venv/bin/activate && python dashboard/app.py${NC}"

echo -e "${YELLOW}[6/6] Offline demo commands...${NC}"
echo -e "${GREEN}  Parse Nmap scans: python3 bridge/nmap_parser.py --scans-dir capture/scans --output nmap_features.csv${NC}"
echo -e "${GREEN}  Run detection:    python3 bridge/bridge.py --input nmap_features.csv${NC}"

echo ""
echo -e "${GREEN}=== Setup complete ===${NC}"
