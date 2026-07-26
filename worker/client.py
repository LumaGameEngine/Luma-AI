#!/usr/bin/env python3
"""
Luma AI Worker Client
Auto‑discovers coordinator via config.json, mDNS, or IP scan.
"""

import json
import time
import socket
import sys
import urllib.request
import urllib.error
import os
import subprocess
import re

# ---------- CONFIGURATION ----------
DEVICE_NAME = "Spark-Go-2020"
HEARTBEAT_TIMEOUT = 20
HEARTBEAT_INTERVAL = 10
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

# ---------- AUTO-DISCOVER COORDINATOR ----------
def discover_coordinator():
    """Return the coordinator base URL (http://IP:8000)."""
    # 1. Try config.json
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                if 'server_ip' in config and config['server_ip']:
                    return f"http://{config['server_ip']}:8000"
        except:
            pass

    # 2. Try mDNS via avahi-browse (if installed)
    try:
        result = subprocess.run(
            ['avahi-browse', '-r', '-t', '_luma._tcp', '-p'],
            capture_output=True, text=True, timeout=2
        )
        for line in result.stdout.split('\n'):
            if '=' in line:
                parts = line.split(';')
                if len(parts) > 6 and parts[0] == '=':
                    ip = parts[-3].strip()
                    if ip and ip != '127.0.0.1':
                        return f"http://{ip}:8000"
    except:
        pass

    # 3. Fallback: scan common IPs on local subnet
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        base = '.'.join(local_ip.split('.')[:-1]) + '.'
        for i in [1, 19, 21, 100, 200]:
            test_ip = base + str(i)
            if test_ip == local_ip:
                continue
            try:
                with urllib.request.urlopen(f"http://{test_ip}:8000/health", timeout=1) as resp:
                    if resp.status == 200:
                        return f"http://{test_ip}:8000"
            except:
                continue
    except:
        pass

    # 4. Prompt user
    print("Could not auto-discover coordinator. Please enter its IP manually:")
    ip = input("IP: ").strip()
    if ip:
        return f"http://{ip}:8000"
    return "http://192.168.1.19:8000"

# ---------- OVERRIDE via command line ----------
SERVER_BASE = discover_coordinator()
for i, arg in enumerate(sys.argv):
    if arg == "--server" and i+1 < len(sys.argv):
        SERVER_BASE = sys.argv[i+1]
    elif arg == "--name" and i+1 < len(sys.argv):
        DEVICE_NAME = sys.argv[i+1]

# ---------- STABLE DEVICE ID ----------
def get_device_id():
    try:
        serial = subprocess.check_output(["getprop", "ro.serialno"], text=True).strip()
        if serial and serial != "unknown":
            return serial
    except:
        pass
    try:
        result = subprocess.check_output(["ip", "link", "show", "wlan0"], text=True)
        match = re.search(r'link/ether ([0-9a-fA-F:]+)', result)
        if match:
            return match.group(1).replace(':', '')
    except:
        pass
    return socket.gethostname() + "-" + hex(int(time.time()))[2:][-6:]

DEVICE_ID = get_device_id()

# ---------- SYSTEM INFO ----------
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def get_cpu_usage():
    try:
        result = subprocess.run(["top", "-n", "1"], capture_output=True, text=True, timeout=3)
        for line in result.stdout.split('\n'):
            if 'CPU:' in line:
                idle_match = re.search(r'(\d+)% idle', line)
                if idle_match:
                    return round(100 - int(idle_match.group(1)), 1)
        return 0
    except:
        return 0

def get_mem_free():
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if "MemAvailable" in line:
                    return int(line.split()[1]) // 1024
    except:
        pass
    return 0

def get_battery():
    try:
        result = subprocess.run(["termux-battery-status"], capture_output=True, text=True, timeout=2)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get("percentage", 80)
    except:
        pass
    return 80

def http_post(url, data, timeout=HEARTBEAT_TIMEOUT):
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        print(f"[HTTP ERROR] {e}")
        return None

def http_post_with_retry(url, data, max_retries=3, base_delay=2):
    for attempt in range(max_retries):
        result = http_post(url, data)
        if result is not None:
            return result
        if attempt < max_retries - 1:
            wait = base_delay * (2 ** attempt)
            print(f"[RETRY] Attempt {attempt+1} failed, retrying in {wait}s...")
            time.sleep(wait)
    return None

def main():
    local_ip = get_local_ip()
    payload = {
        "device_id": DEVICE_ID,
        "name": DEVICE_NAME,
        "arch": "armv7l",
        "ram_total": 1800,
        "cores": 8,
        "ip": local_ip
    }
    print(f"Luma AI Worker: {DEVICE_NAME} (ID: {DEVICE_ID})")
    print(f"Coordinator: {SERVER_BASE} (IP: {local_ip})")

    result = http_post_with_retry(f"{SERVER_BASE}/api/register", payload, max_retries=3)
    if result:
        print(f"[REGISTER] {result.get('message', 'OK')}")
    else:
        print("[ERROR] Registration failed after retries.")
        sys.exit(1)

    print("Registered. Starting heartbeats...")
    while True:
        try:
            hb = {
                "device_id": DEVICE_ID,
                "ram_free": get_mem_free(),
                "cpu_usage": get_cpu_usage(),
                "battery": get_battery()
            }
            result = http_post_with_retry(f"{SERVER_BASE}/api/heartbeat", hb, max_retries=2, base_delay=1)
            if result:
                sys.stdout.write(".")
                sys.stdout.flush()
            else:
                print("\n[HEARTBEAT] Failed after retries.")
        except KeyboardInterrupt:
            print("\nShutting down worker.")
            break
        except Exception as e:
            print(f"\n[ERROR] Heartbeat error: {e}")
        time.sleep(HEARTBEAT_INTERVAL)

if __name__ == "__main__":
    main()