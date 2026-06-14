"""
AEGIS Bridge — End-to-End Test Script
Tests: bridge.py, nmap_parser.py, full offline pipeline
Run: python bridge/test_pipeline.py
"""

import os
import sys
import json
import tempfile
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
import config
from bridge import AegisBridge
from nmap_parser import nmap_xml_to_features, nmap_dir_to_csv


# --- Test 1: Generate synthetic CSV that mimics CICIDS2017 schema ---
def generate_test_csv(output_path, n_benign=20, n_scan=10):
    """Generate a small CSV with known patterns."""
    np.random.seed(42)
    rows = []

    # Benign flows (SSH, HTTP, etc.)
    for _ in range(n_benign):
        rows.append({
            "Destination Port": np.random.choice([22, 80, 443]),
            "Flow Duration": np.random.randint(100000, 2000000),
            "Total Fwd Packets": np.random.randint(10, 80),
            "SYN Flag Count": np.random.randint(0, 2),
            "RST Flag Count": np.random.randint(0, 1),
            "ACK Flag Count": np.random.randint(5, 50),
            "Flow IAT Mean": np.random.uniform(10000, 50000),
            "Bwd Packet Length Mean": np.random.uniform(50, 500),
            "Init_Win_bytes_forward": np.random.choice([29200, 65535, 1024]),
            "Label": "BENIGN",
        })

    # Port scan flows (SYN scan pattern)
    scan_ports = np.random.choice(range(1, 65535), size=n_scan)
    for port in scan_ports:
        rows.append({
            "Destination Port": int(port),
            "Flow Duration": np.random.randint(0, 200),
            "Total Fwd Packets": 1,
            "SYN Flag Count": 1,
            "RST Flag Count": np.random.randint(0, 2),
            "ACK Flag Count": 0,
            "Flow IAT Mean": np.random.randint(0, 500),
            "Bwd Packet Length Mean": 0.0,
            "Init_Win_bytes_forward": 1024,
            "Label": "PortScan",
        })

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"[TEST] Generated test CSV: {output_path} ({len(df)} rows)")
    return output_path


# --- Test 2: Test bridge preprocessing ---
def test_preprocessing():
    """Test that the bridge correctly preprocesses the 9 features + 2 placeholders."""
    print("\n=== Test: Preprocessing ===")
    with tempfile.TemporaryDirectory() as tmp:
        csv_path = os.path.join(tmp, "test_data.csv")
        generate_test_csv(csv_path, n_benign=5, n_scan=3)

        bridge = AegisBridge()
        df = pd.read_csv(csv_path)
        X_scaled, df_raw = bridge.preprocess(df)

        expected_cols = len(config.FEATURE_NAMES)
        assert X_scaled.shape[1] == expected_cols, f"Expected {expected_cols} features, got {X_scaled.shape[1]}"
        assert X_scaled.shape[0] == 8, f"Expected 8 rows, got {X_scaled.shape[0]}"
        print(f"  [PASS] Output shape: {X_scaled.shape} (rows x {expected_cols} features)")


# --- Test 3: Test full pipeline with mock model ---
def test_full_pipeline():
    """Test the full pipeline with an actual model if available."""
    print("\n=== Test: Full Pipeline ===")

    if not os.path.exists(config.RF_MODEL_PATH):
        print(f"  [SKIP] Model not found: {config.RF_MODEL_PATH}")
        return

    with tempfile.TemporaryDirectory() as tmp:
        csv_path = os.path.join(tmp, "test_data.csv")
        generate_test_csv(csv_path, n_benign=10, n_scan=10)

        bridge = AegisBridge()
        results = bridge.run_csv(csv_path)

        alerts = [r for r in results if r["prediction"] == 1]
        benign = [r for r in results if r["prediction"] == 0]
        print(f"  [PASS] Results: {len(alerts)} alerts, {len(benign)} benign out of {len(results)}")

        # Check confidence scores exist
        for r in results[:3]:
            assert "confidence" in r, "Missing confidence in results"
            assert 0 <= r["confidence"] <= 1, f"Confidence out of range: {r['confidence']}"
        print(f"  [PASS] Confidence scores in [0, 1]")


# --- Test 4: Test Nmap XML parser ---
def test_nmap_parser():
    """Test Nmap XML → feature vector conversion."""
    print("\n=== Test: Nmap XML Parser ===")
    scans_dir = os.path.join(config.PROJECT_ROOT, "capture", "azerty", "scans")

    if not os.path.exists(scans_dir):
        print(f"  [SKIP] Scans directory not found: {scans_dir}")
        return

    xml_files = [f for f in os.listdir(scans_dir) if f.endswith(".xml")]
    if not xml_files:
        print(f"  [SKIP] No XML files found in {scans_dir}")
        return

    # Parse first XML
    xml_path = os.path.join(scans_dir, xml_files[0])
    rows = nmap_xml_to_features(xml_path)

    assert len(rows) > 0, "No features extracted from XML"
    assert "Destination Port" in rows[0], "Missing Destination Port in features"
    assert "Flow Duration" in rows[0], "Missing Flow Duration in features"
    print(f"  [PASS] Parsed {xml_files[0]}: {len(rows)} feature vectors")

    # Test batch conversion
    output_csv = os.path.join(scans_dir, "..", "test_nmap_features.csv")
    result = nmap_dir_to_csv(scans_dir, output_csv)
    if result:
        df = pd.read_csv(result)
        assert len(df) > 0, "Empty output CSV"
        assert len(df.columns) >= 9, f"Expected >= 9 columns, got {len(df.columns)}"
        print(f"  [PASS] Batch conversion: {len(df)} feature vectors, {len(df.columns)} columns")
        os.remove(output_csv)


# --- Test 5: Test JSONL logging format ---
def test_jsonl_format():
    """Test that deception modules write valid JSONL."""
    print("\n=== Test: JSONL Logging Format ===")
    test_log = os.path.join(tempfile.gettempdir(), "test_log.jsonl")

    # Simulate a deception log entry
    import datetime
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "module": "test",
        "event": "honeypot_interaction",
        "src_ip": "10.0.0.5",
        "port": 4444,
        "profile": "SSH",
    }

    with open(test_log, "a") as f:
        f.write(json.dumps(entry) + "\n")
        f.write(json.dumps(entry) + "\n")

    # Read back and verify
    with open(test_log) as f:
        lines = [json.loads(line) for line in f if line.strip()]

    assert len(lines) == 2, f"Expected 2 entries, got {len(lines)}"
    assert lines[0]["event"] == "honeypot_interaction"
    print(f"  [PASS] JSONL write/read: {len(lines)} valid entries")
    os.remove(test_log)


# --- Test 6: Test config consistency ---
def test_config():
    """Verify config.py has all required keys."""
    print("\n=== Test: Config Consistency ===")
    assert hasattr(config, "FEATURE_NAMES"), "Missing FEATURE_NAMES"
    assert len(config.FEATURE_NAMES) == 11, f"Expected 11 features, got {len(config.FEATURE_NAMES)}"
    assert hasattr(config, "RF_MODEL_PATH"), "Missing RF_MODEL_PATH"
    assert hasattr(config, "SCALER_PATH"), "Missing SCALER_PATH"
    assert hasattr(config, "CONFIDENCE_THRESHOLD"), "Missing CONFIDENCE_THRESHOLD"
    assert hasattr(config, "ALERT_THRESHOLD"), "Missing ALERT_THRESHOLD"
    assert hasattr(config, "DASHBOARD_PORT"), "Missing DASHBOARD_PORT"
    print(f"  [PASS] config.py has all required keys (11 features, thresholds set)")


# --- Run all tests ---
if __name__ == "__main__":
    print("=" * 60)
    print("AEGIS Bridge — Test Suite")
    print("=" * 60)

    tests = [
        test_config,
        test_preprocessing,
        test_jsonl_format,
        test_nmap_parser,
        test_full_pipeline,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)}")
    print("=" * 60)
