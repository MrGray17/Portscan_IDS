# ============================================
# AEGIS — Response Engine
# IP Blocking + Kernel Blackholing + Dashboard Integration
# ============================================
# Adapted from Yazid's monitor_interface.py (Aegis Morph Command Center).
# Provides block_ip() and unblock_ip() callable from the Flask dashboard.
# ============================================

import sys
import os
import subprocess
import json
import urllib.request

# Add project root for config import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config

banned_ips = set()


def block_ip(ip_address):
    """
    Deploy kernel blackhole + UFW deny for the given IP.
    Returns True if blocked, False if skipped (localhost or already banned).
    """
    if ip_address in ["127.0.0.1", "0.0.0.0", "localhost"]:
        return False
    if ip_address in banned_ips:
        return False

    print(f"[BLOCK] Deploying countermeasure for IP: {ip_address}")

    # 1. Kernel route blackhole — drops packets at routing layer (zero-CPU cost)
    subprocess.run(
        ["sudo", "ip", "route", "add", "blackhole", ip_address],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # 2. UFW deny — persistent Layer 3 isolation
    subprocess.run(
        ["sudo", "ufw", "insert", "1", "deny", "from", ip_address],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    banned_ips.add(ip_address)
    print(f"[+] IP {ip_address} successfully blackholed.")

    # 3. POST to dashboard (best-effort)
    try:
        payload = json.dumps({"ip": ip_address}).encode("utf-8")
        req = urllib.request.Request(
            "http://localhost:5000/api/block",
            method="POST",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        urllib.request.urlopen(req, timeout=2.0)
    except Exception:
        pass

    return True


def unblock_ip(ip_address):
    """Remove blackhole + UFW deny rule for the given IP."""
    if ip_address not in banned_ips:
        return False

    subprocess.run(
        ["sudo", "ip", "route", "del", "blackhole", ip_address],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    subprocess.run(
        ["sudo", "ufw", "delete", "deny", "from", ip_address],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    banned_ips.discard(ip_address)
    print(f"[+] IP {ip_address} unblocked.")
    return True


def is_blocked(ip_address):
    """Check if an IP is currently blackholed."""
    return ip_address in banned_ips
