# Context for El Yazid — Deception-Dashboard Integration

> **Purpose:** This document gives you complete situational awareness of the project
> so you can pick up the deception-dashboard integration without asking questions.
> Written by Adil, June 14, 2026.

---

## 1. Where You Left Off

Your last commit was `ca6ead5` — `docs: add defense subsystem LaTeX documentation`.

Since then, **7 commits** happened that affect your work:
- Conflict resolution from the colleague merge
- Folder reorganization (docs, scans, reports consolidated)
- Dashboard rewrite with 3 POST endpoints
- Deception modules updated to use `config.DECEPTION_LOG_FILE`
- Models retrained on current Python environment

---

## 2. What Changed Since Your Last Commit (A→Z)

### Folder Reorganization
- `capture/azerty/scans/` → `capture/scans/` (30 Nmap scan files)
- `detection/report/` → `docs/reports/02_data/` (ML pipeline report + figures)
- `docs/defense_documentation.tex` → `docs/reports/03_defense/`
- All planning docs, deliverables, interviews consolidated under `docs/`

### Config.py (Single Source of Truth)
```python
FEATURE_NAMES = [
    "Destination Port", "Flow Duration", "Total Fwd Packets",
    "SYN Flag Count", "RST Flag Count", "ACK Flag Count",
    "Flow IAT Mean", "Bwd Packet Length Mean", "Init_Win_bytes_forward",
    "shadow_node_interaction",  # 9 - from honeypot (your module)
    "mtd_port_delta"            # 10 - from MTD (your module)
]

DETECTION_LOG_FILE = "detection/data/detection_logs.json"
DECEPTION_LOG_FILE = "detection/data/deception_logs.json"
```

### Dashboard — 3 New POST Endpoints (dashboard/app.py)
```python
POST /api/alert          # bridge sends detection alerts here
POST /api/block          # bridge sends block requests here
POST /api/honeypot_event # YOUR modules send deception events here
```
Each endpoint:
1. Receives JSON from the caller
2. Appends to the appropriate log file (JSONL format)
3. Emits a Socket.IO event to all connected dashboard clients

### Deception Modules — Updated Log Paths
All 3 files (`core_deception.py`, `network_mutator.py`, `traffic_shaper.py`) now:
- Import `config` from project root
- Write to `config.DECEPTION_LOG_FILE` instead of hardcoded `mutation_logs.json`
- Still POST to `http://localhost:5000/api/honeypot_event` (unchanged)

### Bridge — Local Fallback
If the dashboard is offline when the bridge tries to POST, it writes the event
locally to `detection_logs.json` instead of losing it.

### Models — Retrained
All 3 models (RF, XGBoost, Isolation Forest) retrained on current environment.
Pickle files now load correctly on this Python/sklearn version.

---

## 3. Current Architecture — Data Flow

```
=== OFFLINE MODE (what we have now) ===

Nmap XMLs → nmap_parser.py → CSV → bridge.py → ML prediction → dashboard
                                                           ↓
                                              writes to detection_logs.json
                                              (detection events only)


=== LIVE MODE (what we need for the presentation) ===

Scapy capture → bridge.py → ML prediction → dashboard
                                        ↓
                                  ┌─────┴──────┐
                                  ↓            ↓
                           detection_logs   deception_logs
                                  ↓            ↓
                            ┌─────┴────────────┴─────┐
                            │    Dashboard (Flask)     │
                            │  - Socket.IO push        │
                            │  - Stats cards           │
                            │  - Event tables          │
                            │  - Threat level          │
                            └─────────────────────────┘
                                  ↑            ↑
                                  │            │
                           bridge.py    YOUR deception modules
                           (POST        (POST to /api/honeypot_event)
                            to /api/alert)
```

---

## 4. What You Need to Do

### Good news: The integration is already wired.

Your deception modules already:
1. ✅ Write to `config.DECEPTION_LOG_FILE` (deception_logs.json)
2. ✅ POST to `http://localhost:5000/api/honeypot_event`
3. ✅ Dashboard has the POST endpoint that accepts and stores these events

### What you need to verify on the live VM:

1. **Import chain works** — your modules import `config` from project root:
   ```python
   sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
   import config
   ```
   Then use `config.DECEPTION_LOG_FILE` for log paths.

2. **Dashboard is running** — your modules POST to `http://localhost:5000/api/honeypot_event`.
   The dashboard must be running for the POST to succeed (otherwise it falls back to local file).

3. **Root privileges** — `monitor_interface.py` uses `sudo ip route add blackhole`
   and `sudo ufw deny from`. Run as root or with passwordless sudo.

4. **NetfilterQueue** — `network_mutator.py` and `traffic_shaper.py` need:
   ```bash
   sudo iptables -A OUTPUT -p tcp -j NFQUEUE --queue-num 1
   ```
   And `libnetfilter-queue-dev` installed.

### The 5 deception event types the dashboard recognizes:
- `REDIRECT` — attacker sent to honeypot
- `BLACKLIST` — IP blocked
- `MUTATE` / `ROTATE_DONE` — MTD port rotation
- `PHANTOM` — phantom network response

---

## 5. What's Missing for Live Demo

| Component | Status | Notes |
|-----------|--------|-------|
| ML models | ✅ Done | Retrained, load correctly |
| Dashboard backend | ✅ Done | POST routes, JSONL, Socket.IO |
| Bridge (offline) | ✅ Done | Nmap XML → ML → dashboard |
| Bridge (live) | ⚠️ Partial | Needs Scapy capture pipeline |
| Deception modules | ✅ Done | Updated log paths, POST integration |
| Honeypot | ✅ Done | 5 profiles, async TCP server |
| MTD | ✅ Done | TTL/window mutation |
| Traffic shaper | ✅ Done | SYN-ACK tarpit |
| IP blocking | ✅ Done | kernel blackhole + UFW |
| VM setup | ⬜ Not started | Ubuntu + Kali VirtualBox VMs |
| Scapy capture | ⬜ Not started | BPF filter + rolling window aggregation |

### For the live demo you need:
1. **2 VirtualBox VMs**: Ubuntu (192.168.100.20) + Kali (192.168.100.10)
2. **Ubuntu VM**: run `demo/ubuntu_setup.sh` to install everything
3. **Scapy capture pipeline**: real-time packet capture → feature extraction → bridge
4. **Kali VM**: run `demo/kali_attack.sh` to simulate attacks

---

## 6. File Map

```
Portscan_IDS/
├── config.py                    # SINGLE SOURCE OF TRUTH — all paths, features, thresholds
├── run_demo.py                  # Unified entry point (interactive menu)
│
├── bridge/
│   ├── bridge.py                # CSV/Nmap → ML → dashboard (with local fallback)
│   ├── nmap_parser.py           # Parse Nmap XML to feature vectors
│   └── test_pipeline.py         # End-to-end test suite (5/5 pass)
│
├── dashboard/
│   ├── app.py                   # Flask + Socket.IO backend (POST routes included)
│   ├── templates/index.html     # SOC dashboard frontend
│   └── static/style.css         # Dark theme CSS
│
├── deception/                   # ← YOUR TERRITORY
│   ├── core_deception.py        # Honeypot (5 profiles), get_honeypot_flag()
│   ├── network_mutator.py       # MTD TTL/window spoofing, compute_mtd_port_delta()
│   ├── traffic_shaper.py        # SYN-ACK tarpit, MSS sabotage
│   ├── monitor_interface.py     # IP blocking (blackhole + UFW)
│   └── README.md                # Integration docs
│
├── detection/
│   ├── src/
│   │   ├── retrain_11features.py  # Model retraining script (11 features)
│   │   ├── cicids2017_pipeline.py # Original pipeline (reference)
│   │   └── config.py              # Detection-specific config (DO NOT MODIFY)
│   └── data/                      # Runtime log files go here
│       ├── detection_logs.json    # Written by bridge + dashboard
│       └── deception_logs.json    # Written by your deception modules + dashboard
│
├── models/saved/
│   ├── rf_model.pkl            # Random Forest (99.91% acc)
│   ├── xgb_model.pkl           # XGBoost (99.91% acc)
│   ├── isolation_forest.pkl    # Isolation Forest (24.6% — expected)
│   ├── scaler.pkl              # StandardScaler (11 features)
│   └── feature_columns.json    # Feature name list
│
├── capture/
│   ├── scans/                  # 10 Nmap scan outputs (30 files)
│   └── fetch_and_align_datasets.py  # Dataset downloader
│
├── demo/
│   ├── kali_attack.sh          # 5-phase attack simulation
│   ├── kali_custom_scanner.py  # Low-rate stealth scanner
│   └── ubuntu_setup.sh         # VM setup script
│
└── docs/reports/
    ├── 02_data/                # ML pipeline report (TEX + figures)
    ├── 03_defense/             # Your defense_documentation.tex
    └── 04_capture/             # Moulay Anas's capture report
```

---

## 7. Key Contacts

| Person | Role | Status |
|--------|------|--------|
| Adil (you're reading his doc) | Dashboard, Response, Integration | Active |
| Khadija | ML Pipeline, Training | Report done |
| **El Yazid (you)** | **Deception, MTD, Honeypot** | **Your turn** |
| Anas El Kartouti | Conception | Report pending |
| Moulay Anas | Capture/Network | Report pending |

---

## 8. Summary

The deception-dashboard integration is **already wired** in the code. Your modules
write to the right log files and POST to the right endpoints. The dashboard accepts
and displays deception events.

What's left is **testing on the live VM** — making sure the full stack works with
real network traffic. That requires the 2-VM setup and the Scapy capture pipeline.

If you have questions, check `deception/README.md` or `config.py` first.
