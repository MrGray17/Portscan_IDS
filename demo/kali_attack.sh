#!/bin/bash
# =============================================================
# AEGIS — Kali Attack Script
# Run this from your Kali VM to simulate port scans
# Adjust TARGET_IP to your Ubuntu Server's IP
# =============================================================

TARGET_IP="${1:-192.168.56.10}"
RESULTS_DIR="/tmp/aegis_results"
mkdir -p "$RESULTS_DIR"

echo "============================================="
echo "  AEGIS — Port Scan Simulation"
echo "  Target: $TARGET_IP"
echo "============================================="

# --- Check connectivity ---
echo ""
echo "[*] Checking connectivity to $TARGET_IP..."
if ! ping -c 1 -W 2 "$TARGET_IP" > /dev/null 2>&1; then
    echo "  [!] Cannot reach $TARGET_IP — check network and VM settings"
    exit 1
fi
echo "  [+] Target reachable."

# --- Phase 1: Fast aggressive scan (Nmap) ---
echo ""
echo "[Phase 1] Fast aggressive scan (Nmap -T4 -sS)"
echo "  This generates high-volume SYN scan traffic."
echo "  Expected: AEGIS detects and classifies as ATTACK"
nmap -T4 -sS -p 1-1000 --open "$TARGET_IP" -oN "$RESULTS_DIR/nmap_fast.txt" -oX "$RESULTS_DIR/nmap_fast.xml" 2>&1 | tail -5
echo "  [+] Fast scan complete. Results saved to $RESULTS_DIR/"

# Wait for detection pipeline to process
sleep 3

# --- Phase 2: Service version scan ---
echo ""
echo "[Phase 2] Service version scan (Nmap -sV)"
echo "  Probes detected services for version info."
nmap -sV -p 22,80,443,5000 "$TARGET_IP" -oN "$RESULTS_DIR/nmap_service.txt" 2>&1 | tail -5
echo "  [+] Service scan complete."

sleep 3

# --- Phase 3: Slow stealth scan (custom) ---
echo ""
echo "[Phase 3] Slow stealth scan (custom scanner)"
echo "  Low-rate scan over 60 seconds — tests Isolation Forest."
python3 "$(dirname "$0")/kali_custom_scanner.py" "$TARGET_IP" 2>&1
echo "  [+] Slow scan complete."

sleep 3

# --- Phase 4: OS Detection ---
echo ""
echo "[Phase 4] OS detection scan (Nmap -O)"
nmap -O --osscan-guess "$TARGET_IP" -oN "$RESULTS_DIR/nmap_os.txt" 2>&1 | tail -5
echo "  [+] OS detection complete."

sleep 3

# --- Phase 5: UDP scan (bonus) ---
echo ""
echo "[Phase 5] Top UDP ports scan"
echo "  Scans common UDP ports — different protocol signature."
nmap -sU --top-ports 20 "$TARGET_IP" -oN "$RESULTS_DIR/nmap_udp.txt" 2>&1 | tail -5
echo "  [+] UDP scan complete."

# --- Summary ---
echo ""
echo "============================================="
echo "  Attack simulation complete!"
echo "============================================="
echo ""
echo "  Check your AEGIS dashboard for:"
echo "  - Detection events (attacks blocked)"
echo "  - Deception redirects (honeypot captures)"
echo "  - Threat level changes"
echo ""
echo "  Results saved to: $RESULTS_DIR/"
echo ""
echo "  Attack phases:"
echo "    Phase 1: Fast SYN scan (1000 ports)"
echo "    Phase 2: Service version probe"
echo "    Phase 3: Slow stealth scan (60s)"
echo "    Phase 4: OS detection"
echo "    Phase 5: UDP scan"
