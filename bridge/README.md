# AEGIS — Bridge Module

## Purpose

The Bridge module connects the ML detection layer to the dashboard and deception layers. It operates in **offline mode** — reading CSV or Nmap XML input, running predictions through the trained model, and dispatching alerts to the dashboard.

## Files

| File | Purpose |
|---|---|
| `bridge.py` | Core pipeline: CSV → preprocess → predict → dispatch to dashboard |
| `nmap_parser.py` | Parse Nmap XML files into ML-compatible feature vectors |
| `test_pipeline.py` | End-to-end test suite for the bridge |

## Usage

### Run on CICIDS2017 CSV
```bash
python bridge/bridge.py --input detection/data/test.csv
```

### Run on Nmap XML scans
```bash
# Step 1: Parse Nmap XMLs → CSV
python bridge/nmap_parser.py --scans-dir capture/scans --output nmap_features.csv

# Step 2: Run prediction
python bridge/bridge.py --input nmap_features.csv
```

### Run all tests
```bash
python bridge/test_pipeline.py
```

## Dependencies

- `pandas`, `numpy`, `scikit-learn`, `joblib` (already in requirements.txt)
- No new dependencies needed

## Dashboard Integration

The bridge POSTs alerts to the Flask dashboard at `http://localhost:5000/api/alert`. If running the dashboard, start it first:

```bash
python dashboard/app.py
```

## Feature Schema (11 features)

The bridge expects these columns in the input CSV:

| # | Feature | Source |
|---|---|---|
| 0 | Destination Port | CICIDS2017 / Nmap XML |
| 1 | Flow Duration | CICIDS2017 / synthetic |
| 2 | Total Fwd Packets | CICIDS2017 / synthetic |
| 3 | SYN Flag Count | CICIDS2017 / Nmap profile |
| 4 | RST Flag Count | CICIDS2017 / Nmap profile |
| 5 | ACK Flag Count | CICIDS2017 / Nmap profile |
| 6 | Flow IAT Mean | CICIDS2017 / synthetic |
| 7 | Bwd Packet Length Mean | CICIDS2017 / synthetic |
| 8 | Init_Win_bytes_forward | CICIDS2017 / Nmap profile |
| 9 | shadow_node_interaction | 0 (placeholder) |
| 10 | mtd_port_delta | 0 (placeholder) |
