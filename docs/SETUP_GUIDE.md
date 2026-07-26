# Setup Guide

This guide walks you through setting up a complete Luma AI environment, including the coordinator and one Android worker.

---

## Requirements

### Coordinator

- Linux (Ubuntu/Debian recommended)
- Python 3.11+
- Git
- Wi-Fi connection

### Worker

- Android 8+
- Termux (F-Droid version)
- Python
- Git
- OpenSSH

---

## 1. Clone the repository

```bash
git clone https://github.com/LumaGameEngine/Luma-AI.git
cd Luma-AI
```

---

## 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r backend/requirements.txt
```

---

## 4. Start the coordinator

```bash
python backend/main.py
```

The dashboard is available at:

```
http://localhost:8000
```

---

# Android Worker

Install the required packages.

```bash
pkg update
pkg upgrade
pkg install python git openssh cmake clang make wget
```

Clone the repository.

```bash
git clone https://github.com/LumaGameEngine/Luma-AI.git
cd Luma-AI
```

Create `worker/config.json`.

```json
{
    "server_ip":"192.168.1.25",
    "server_port":8000
}
```

Replace the IP with the coordinator's local address.

---

## Start the inference server

```bash
cd worker
python inference_server.py
```

In another Termux session:

```bash
python client.py
```

The worker should appear automatically in the dashboard.

---

## Next Steps

- Build `llama-cli` (see `BUILD_LLAMA_CLI.md`)
- Download a GGUF model
- Select the worker from the dashboard
- Start chatting