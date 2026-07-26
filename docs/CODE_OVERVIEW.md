# Code Overview

Luma AI is organized into several independent components.

```
Luma-AI/

backend/
frontend/
worker/
storage/
scripts/
docs/
```

---

# backend/

Contains the coordinator.

Main responsibilities:

- REST API
- Device registry
- Model management
- Request routing
- Image processing

Main entry point:

```
backend/main.py
```

---

# frontend/

Contains the web interface.

Files:

```
index.html
```

Application layout.

```
style.css
```

Themes and styling.

```
app.js
```

Dashboard logic, chat, device management and model controls.

---

# worker/

Runs on Android devices.

Important files:

```
client.py
```

Registers with the coordinator and sends heartbeats.

```
inference_server.py
```

Runs a lightweight HTTP server exposing inference endpoints.

```
llama-cli
```

Compiled llama.cpp executable used to run GGUF models.

---

# storage/

Stores AI models.

```
storage/models/
```

GGUF files downloaded by the coordinator.

Workers synchronize models from this directory.

---

# scripts/

Utility scripts for installation, building and automation.

Examples:

- install.sh
- start.sh
- build.sh

---

# docs/

Project documentation.

Contains build guides, architecture, setup instructions and troubleshooting documentation.

---

## Request Flow

```
User

↓

Dashboard

↓

Coordinator

↓

Worker

↓

llama.cpp

↓

Response

↓

Dashboard
```

The coordinator acts as the central controller while workers only execute assigned tasks.