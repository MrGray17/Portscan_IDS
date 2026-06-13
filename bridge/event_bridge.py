"""Event Bridge — Connects detection alerts to the dashboard via Socket.IO.

Reads detection_logs.json and deception_logs.json, then pushes live
updates to all connected dashboard clients via Socket.IO.
"""
import os, sys, json, time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import (
    DATA_DIR, DETECTION_LOG_FILE, DECEPTION_LOG_FILE, REFRESH_MS
)


def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def watch_and_emit(socketio):
    """Background thread: poll log files and emit Socket.IO events."""
    last_det_len = 0
    last_dec_len = 0
    while True:
        det_logs = load_json(DETECTION_LOG_FILE)
        dec_logs = load_json(DECEPTION_LOG_FILE)

        det_len = len(det_logs)
        dec_len = len(dec_logs)

        if det_len != last_det_len or dec_len != last_dec_len:
            socketio.emit("events_update", {
                "detection": det_logs[-50:],
                "deception": dec_logs[-50:]
            })

            det_attacks = sum(1 for e in det_logs if e.get("prediction") == 1)
            det_benign = det_len - det_attacks
            dec_redir = sum(1 for e in dec_logs if e.get("event_type") == "REDIRECT")
            dec_black = sum(1 for e in dec_logs if e.get("event_type") == "BLACKLIST")

            socketio.emit("stats_update", {
                "detection": {
                    "total_events": det_len,
                    "attacks": det_attacks,
                    "benign": det_benign,
                    "attack_rate": round(det_attacks / det_len * 100, 1) if det_len else 0
                },
                "deception": {
                    "total_events": dec_len,
                    "redirects": dec_redir,
                    "blacklists": dec_black
                }
            })

            last_det_len = det_len
            last_dec_len = dec_len

        time.sleep(REFRESH_MS / 1000)
