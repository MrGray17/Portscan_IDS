#!/usr/bin/env python3
"""
AEGIS Live Capture -- Real-time packet capture and ML classification.

Sniffs packets on the AEGIS network interface, extracts flow-level
features, runs them through the ML ensemble, and dispatches results
to the dashboard in real-time.

Usage:
    sudo python3 capture/live_capture.py
    sudo python3 capture/live_capture.py --iface enp0s8
    sudo python3 capture/live_capture.py --dry-run
"""
import os
import sys
import time
import json
import argparse
import urllib.request
from datetime import datetime, timezone
from threading import Lock

try:
    from scapy.all import sniff, IP, TCP, conf
except ImportError:
    print("[LIVE] scapy not installed. Run: pip install scapy")
    sys.exit(1)

import numpy as np
import joblib

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
import config

flows = {}
flows_lock = Lock()
rf_model = None
xgb_model = None
scaler = None
DASHBOARD_URL = f"http://{config.DASHBOARD_HOST}:{config.DASHBOARD_PORT}"
PROCESSED_LOG = os.path.join(config.DATA_DIR, "detection_logs.json")
os.makedirs(config.DATA_DIR, exist_ok=True)

def load_models():
    global rf_model, xgb_model, scaler
    print("[LIVE] Loading ML models...")
    rf_model = joblib.load(config.RF_MODEL_PATH)
    xgb_model = joblib.load(config.XGB_MODEL_PATH)
    scaler = joblib.load(config.SCALER_PATH)
    print(f"[LIVE] RF: {rf_model.n_features_in_} features")
    print(f"[LIVE] XGB: {xgb_model.n_features_in_} features")


def extract_flow_features(flow_data):
    dst_port = flow_data.get("dst_port", 0)
    duration = flow_data.get("last_time", 0) - flow_data.get("first_time", 0)
    duration_us = max(int(duration * 1_000_000), 1)
    fwd_packets = flow_data.get("fwd_packets", 0)
    syn_count = flow_data.get("syn_count", 0)
    rst_count = flow_data.get("rst_count", 0)
    ack_count = flow_data.get("ack_count", 0)
    iat_values = flow_data.get("iat_values", [])
    iat_mean = float(np.mean(iat_values)) if iat_values else 0.0
    bwd_lengths = flow_data.get("bwd_lengths", [])
    bwd_pkt_len_mean = float(np.mean(bwd_lengths)) if bwd_lengths else 0.0
    init_win = flow_data.get("init_win_fwd", 0)

    return [
        dst_port, duration_us, fwd_packets,
        syn_count, rst_count, ack_count,
        iat_mean, bwd_pkt_len_mean, init_win,
        0, 0,  # placeholders: shadow_node, mtd_port_delta
    ]


def classify_flow(features):
    X = np.array([features], dtype=np.float64)
    X_scaled = scaler.transform(X)

    rf_pred = int(rf_model.predict(X_scaled)[0])
    xgb_pred = int(xgb_model.predict(X_scaled)[0])
    rf_conf = float(rf_model.predict_proba(X_scaled)[0].max())
    xgb_conf = float(xgb_model.predict_proba(X_scaled)[0].max())

    attack_votes = rf_pred + xgb_pred
    confidence = (rf_conf + xgb_conf) / 2.0
    verdict = "ATTACK" if attack_votes >= 1 else "BENIGN"

    if confidence > 0.95 and attack_votes == 2:
        severity = "HIGH"
    elif confidence > 0.85:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return verdict, confidence, severity

def post_to_dashboard(endpoint, data):
    try:
        req = urllib.request.Request(
            f"{DASHBOARD_URL}{endpoint}",
            data=json.dumps(data).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass


def dispatch_result(src_ip, verdict, confidence, severity, features, dry_run=False):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source_ip": src_ip,
        "destination_port": int(features[0]),
        "verdict": verdict,
        "confidence": round(confidence, 4),
        "severity": severity,
        "model": "ensemble_rf_xgb",
    }

    with open(PROCESSED_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

    if dry_run:
        icon = "!!!" if verdict == "ATTACK" else "   "
        print(f"  {icon} {src_ip}:{features[0]} -> {verdict} "
              f"(conf={confidence:.3f}, sev={severity})")
        return

    post_to_dashboard("/api/alert", entry)

    if verdict == "ATTACK" and confidence > config.CONFIDENCE_THRESHOLD:
        block_entry = {
            "timestamp": entry["timestamp"],
            "source_ip": src_ip,
            "reason": f"ML classification: {verdict} ({confidence:.1%})",
        }
        post_to_dashboard("/api/block", block_entry)
        print(f"  [BLOCK] {src_ip} (confidence {confidence:.1%})")

def process_packet(pkt, dry_run=False):
    if not pkt.haslayer(IP) or not pkt.haslayer(TCP):
        return

    ip_layer = pkt[IP]
    tcp_layer = pkt[TCP]

    flow_key = (ip_layer.src, tcp_layer.sport, ip_layer.dst, tcp_layer.dport, "TCP")
    reverse_key = (ip_layer.dst, tcp_layer.dport, ip_layer.src, tcp_layer.sport, "TCP")

    now = time.time()
    flags = int(tcp_layer.flags)

    with flows_lock:
        if flow_key in flows:
            flow = flows[flow_key]
            flow["last_time"] = now
            flow["fwd_packets"] += 1
            flow["syn_count"] += 1 if flags & 0x02 else 0
            flow["rst_count"] += 1 if flags & 0x04 else 0
            flow["ack_count"] += 1 if flags & 0x10 else 0
            if flow["iat_values"]:
                flow["iat_values"].append(now - flow["last_iat"])
            flow["last_iat"] = now
        elif reverse_key in flows:
            flow = flows[reverse_key]
            flow["last_time"] = now
            flow["bwd_lengths"].append(len(tcp_layer.payload))
            flow["syn_count"] += 1 if flags & 0x02 else 0
            flow["rst_count"] += 1 if flags & 0x04 else 0
            flow["ack_count"] += 1 if flags & 0x10 else 0
            if flow["iat_values"]:
                flow["iat_values"].append(now - flow["last_iat"])
            flow["last_iat"] = now
        else:
            flows[flow_key] = {
                "src_ip": ip_layer.src,
                "dst_port": tcp_layer.dport,
                "first_time": now,
                "last_time": now,
                "fwd_packets": 1,
                "syn_count": 1 if flags & 0x02 else 0,
                "rst_count": 1 if flags & 0x04 else 0,
                "ack_count": 1 if flags & 0x10 else 0,
                "iat_values": [],
                "bwd_lengths": [],
                "init_win_fwd": tcp_layer.window,
                "last_iat": now,
            }

FLOW_TIMEOUT = 5.0  # seconds before a flow is considered complete


def check_flows(dry_run=False):
    global flows
    while True:
        time.sleep(FLOW_TIMEOUT / 2)
        now = time.time()
        completed = []

        with flows_lock:
            for key, flow in list(flows.items()):
                if now - flow["last_time"] >= FLOW_TIMEOUT:
                    completed.append((key, flow))
                    del flows[key]

        for key, flow in completed:
            features = extract_flow_features(flow)
            src_ip = flow["src_ip"]
            verdict, confidence, severity = classify_flow(features)
            dispatch_result(src_ip, verdict, confidence, severity, features, dry_run)


def print_stats():
    while True:
        time.sleep(30)
        with flows_lock:
            count = len(flows)
        print(f"[LIVE] Active flows: {count}")


def main():
    parser = argparse.ArgumentParser(description="AEGIS Live Packet Capture")
    parser.add_argument("--iface", default=config.IDS_INTERFACE,
                        help=f"Network interface (default: {config.IDS_INTERFACE})")
    parser.add_argument("--dry-run", action="store_true",
                        help="Classify but do not POST to dashboard")
    args = parser.parse_args()

    print("=" * 60)
    print("  AEGIS Live Capture")
    print("=" * 60)
    print(f"  Interface: {args.iface}")
    print(f"  Dashboard: {DASHBOARD_URL}")
    print(f"  Dry run:   {args.dry_run}")
    print(f"  Models:    RF + XGBoost ensemble")
    print("=" * 60)

    load_models()

    from threading import Thread
    flow_thread = Thread(target=check_flows, args=(args.dry_run,), daemon=True)
    flow_thread.start()

    stats_thread = Thread(target=print_stats, daemon=True)
    stats_thread.start()

    print(f"[LIVE] Sniffing on {args.iface}... (Ctrl+C to stop)")
    try:
        sniff(
            iface=args.iface,
            filter="tcp",
            prn=lambda pkt: process_packet(pkt, dry_run=args.dry_run),
            store=False,
        )
    except PermissionError:
        print("[LIVE] ERROR: Need root. Run with sudo.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[LIVE] Stopped.")


if __name__ == "__main__":
    main()
