
---

## docs/CONFIGURATION.md

Every configurable option.

```md
# Configuration

## Coordinator

server_ip

Port used by the backend.

Default

8000

---

storage/models

Location where GGUF models are stored.

---

## Worker

worker/config.json

Example

```json
{
    "server_ip":"192.168.1.20",
    "heartbeat_interval":10
}