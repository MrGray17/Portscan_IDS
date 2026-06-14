# ============================================
# AEGIS — Nmap XML Parser
# Converts Nmap scan outputs → CSV feature vectors
# compatible with the trained ML model.
# ============================================

import os
import sys
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config


# Heuristic defaults per scan type (approximating CICIDS2017 flow characteristics)
SCAN_PROFILES = {
    "syn": {
        "flow_duration": 5000,       # ~5ms (fast SYN scan)
        "total_fwd_packets": 1,
        "syn_flag_count": 1,
        "rst_flag_count": 1,         # RST from closed ports
        "ack_flag_count": 0,
        "iat_mean": 5000,            # microseconds between probes
        "bwd_packet_length_mean": 40, # small RST packets
        "init_win_bytes_forward": 1024,
    },
    "full": {
        "flow_duration": 6000,
        "total_fwd_packets": 1,
        "syn_flag_count": 1,
        "rst_flag_count": 1,
        "ack_flag_count": 0,
        "iat_mean": 6000,
        "bwd_packet_length_mean": 40,
        "init_win_bytes_forward": 1024,
    },
    "service": {
        "flow_duration": 11000,
        "total_fwd_packets": 10,
        "syn_flag_count": 1,
        "rst_flag_count": 0,
        "ack_flag_count": 9,
        "iat_mean": 1100,
        "bwd_packet_length_mean": 200,
        "init_win_bytes_forward": 1024,
    },
    "os": {
        "flow_duration": 16000,
        "total_fwd_packets": 20,
        "syn_flag_count": 5,
        "rst_flag_count": 0,
        "ack_flag_count": 15,
        "iat_mean": 800,
        "bwd_packet_length_mean": 150,
        "init_win_bytes_forward": 1024,
    },
    "aggressive": {
        "flow_duration": 22000,
        "total_fwd_packets": 30,
        "syn_flag_count": 5,
        "rst_flag_count": 0,
        "ack_flag_count": 25,
        "iat_mean": 733,
        "bwd_packet_length_mean": 180,
        "init_win_bytes_forward": 1024,
    },
    "udp": {
        "flow_duration": 20000,
        "total_fwd_packets": 50,
        "syn_flag_count": 0,
        "rst_flag_count": 0,
        "ack_flag_count": 0,
        "iat_mean": 400,
        "bwd_packet_length_mean": 0,  # UDP has no TCP flags
        "init_win_bytes_forward": 0,
    },
    "xmas": {
        "flow_duration": 6000,
        "total_fwd_packets": 1,
        "syn_flag_count": 0,
        "rst_flag_count": 0,
        "ack_flag_count": 0,
        "iat_mean": 6000,
        "bwd_packet_length_mean": 0,
        "init_win_bytes_forward": 1024,
    },
    "slow": {
        "flow_duration": 505000,     # ~505 seconds (slow scan)
        "total_fwd_packets": 1000,
        "syn_flag_count": 1000,
        "rst_flag_count": 998,
        "ack_flag_count": 0,
        "iat_mean": 505000,          # 500ms delay between probes
        "bwd_packet_length_mean": 40,
        "init_win_bytes_forward": 1024,
    },
    "fast": {
        "flow_duration": 4660,
        "total_fwd_packets": 1,
        "syn_flag_count": 1,
        "rst_flag_count": 1,
        "ack_flag_count": 0,
        "iat_mean": 4660,
        "bwd_packet_length_mean": 40,
        "init_win_bytes_forward": 1024,
    },
    "very_fast": {
        "flow_duration": 4660,
        "total_fwd_packets": 1,
        "syn_flag_count": 1,
        "rst_flag_count": 1,
        "ack_flag_count": 0,
        "iat_mean": 4660,
        "bwd_packet_length_mean": 40,
        "init_win_bytes_forward": 1024,
    },
}


def parse_nmap_xml(xml_path):
    """
    Parse an Nmap XML file and extract scan metadata.
    Returns a dict with scan_type, target_ip, open_ports, scan_args.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Extract scan type from args
    args = root.get("args", "")
    scan_type = "unknown"
    for stype in SCAN_PROFILES:
        if f"-s{stype[0].upper()}" in args or f"--{stype}" in args:
            scan_type = stype
            break
    if "aggressive" in args or "-A " in args:
        scan_type = "aggressive"
    if "slow" in xml_path.lower() or "--scan-delay" in args:
        scan_type = "slow"
    if "fast" in xml_path.lower() and "very" in xml_path.lower():
        scan_type = "very_fast"
    elif "fast" in xml_path.lower():
        scan_type = "fast"

    # Extract target IP
    target_ip = "unknown"
    for host in root.findall(".//host"):
        for addr in host.findall("address"):
            if addr.get("addrtype") == "ipv4":
                target_ip = addr.get("addr")
                break

    # Extract open ports
    open_ports = []
    for port_elem in root.findall(".//port"):
        state = port_elem.find("state")
        if state is not None and state.get("state") == "open":
            open_ports.append(int(port_elem.get("portid")))

    return {
        "scan_type": scan_type,
        "target_ip": target_ip,
        "open_ports": open_ports,
        "scan_args": args,
    }


def nmap_xml_to_features(xml_path, src_ip="192.168.100.10"):
    """
    Convert an Nmap XML file into a list of feature vectors
    matching config.FEATURE_NAMES. One row per open port.
    """
    meta = parse_nmap_xml(xml_path)
    profile = SCAN_PROFILES.get(meta["scan_type"], SCAN_PROFILES["syn"])

    rows = []
    for port in meta["open_ports"]:
        row = {
            "Source IP": src_ip,
            "Destination Port": port,
            "Flow Duration": profile["flow_duration"],
            "Total Fwd Packets": profile["total_fwd_packets"],
            "SYN Flag Count": profile["syn_flag_count"],
            "RST Flag Count": profile["rst_flag_count"],
            "ACK Flag Count": profile["ack_flag_count"],
            "Flow IAT Mean": profile["iat_mean"],
            "Bwd Packet Length Mean": profile["bwd_packet_length_mean"],
            "Init_Win_bytes_forward": profile["init_win_bytes_forward"],
        }
        rows.append(row)

    return rows


def nmap_dir_to_csv(scans_dir, output_csv):
    """
    Parse all Nmap XML files in a directory and produce a single CSV
    compatible with the ML bridge.
    """
    all_rows = []
    xml_files = sorted([f for f in os.listdir(scans_dir) if f.endswith(".xml")])

    for xml_file in xml_files:
        xml_path = os.path.join(scans_dir, xml_file)
        try:
            rows = nmap_xml_to_features(xml_path)
            all_rows.extend(rows)
            print(f"  Parsed {xml_file}: {len(rows)} feature vectors")
        except Exception as e:
            print(f"  Skipped {xml_file}: {e}")

    if not all_rows:
        print("[NMAP] No features extracted from any XML file.")
        return None

    df = pd.DataFrame(all_rows)
    df.to_csv(output_csv, index=False)
    print(f"\n[NMAP] Saved {len(df)} feature vectors to {output_csv}")
    return output_csv


# ============================================
# CLI Entry Point
# ============================================
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Parse Nmap XML files → ML-compatible CSV")
    parser.add_argument("--scans-dir", required=True, help="Directory containing Nmap .xml files")
    parser.add_argument("--output", default="nmap_features.csv", help="Output CSV path")
    parser.add_argument("--src-ip", default="192.168.100.10", help="Attacker source IP")
    args = parser.parse_args()

    nmap_dir_to_csv(args.scans_dir, args.output)
