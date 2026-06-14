#!/usr/bin/env python3
"""AEGIS Demo — Custom Slow Scanner (Kali).

Low-rate port scanner that spaces probes over time.
Designed to test the Isolation Forest "slow scan" detection.

Usage:
    python3 kali_custom_scanner.py <target_ip> [duration_seconds]
"""
import sys
import socket
import time
import random

def slow_scan(target_ip, duration=60, min_delay=0.5, max_delay=2.0):
    """Scan common ports at a slow rate over the given duration."""
    ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443,
             445, 993, 995, 1433, 3306, 3389, 5432, 5900, 8080, 8443]
    random.shuffle(ports)

    print(f"[*] Slow scan: {target_ip} over {duration}s")
    print(f"[*] Ports to scan: {len(ports)} common ports")
    print(f"[*] Delay range: {min_delay}s - {max_delay}s between probes")
    print()

    start = time.time()
    open_ports = []
    scanned = 0

    while time.time() - start < duration:
        for port in ports:
            if time.time() - start >= duration:
                break

            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target_ip, port))
                if result == 0:
                    print(f"  [OPEN] {target_ip}:{port}")
                    open_ports.append(port)
                sock.close()
            except socket.error:
                pass

            scanned += 1
            delay = random.uniform(min_delay, max_delay)
            elapsed = time.time() - start
            print(f"  [{elapsed:.1f}s] Scanned {scanned} ports, "
                  f"found {len(open_ports)} open", end="\r")
            time.sleep(delay)

    print()
    print(f"\n[+] Slow scan complete: {scanned} probes in {time.time()-start:.1f}s")
    if open_ports:
        print(f"[+] Open ports: {open_ports}")
    return open_ports


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <target_ip> [duration_seconds]")
        sys.exit(1)

    target = sys.argv[1]
    duration = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    slow_scan(target, duration)
