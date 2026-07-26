# Architecture

Luma AI follows a distributed client-server architecture.

```
                 User
                  │
                  ▼
        Web Dashboard (Frontend)
                  │
                  ▼
        FastAPI Coordinator
                  │
      Local Wi-Fi Network
     ───────────────────────
        │            │
        ▼            ▼
 Android Worker  Android Worker
     ARMv7          ARM64
        │            │
        ▼            ▼
      llama.cpp    llama.cpp
```

---

## Coordinator

The coordinator is responsible for:

- Managing connected workers
- Hosting the web interface
- Managing GGUF models
- Routing inference requests
- Monitoring device health

Only one coordinator is required per cluster.

---

## Worker

A worker is an Android device running the Luma AI client.

Each worker:

- Registers with the coordinator
- Sends heartbeats
- Downloads models when needed
- Executes inference
- Returns generated responses

Workers are independent and can disconnect without affecting the rest of the cluster.

---

## Model Storage

Models are stored on the coordinator.

When a worker needs a model:

1. The coordinator checks if it already exists.
2. If missing, the worker downloads it.
3. The worker switches to the requested model.
4. Inference begins.

This avoids storing unnecessary models on every device.

---

## Communication

Communication uses HTTP over the local network.

Coordinator API

```
Port 8000
```

Worker API

```
Port 8080
```

Every request is initiated by the coordinator.

---

## Future Architecture

Planned improvements include:

- Distributed scheduling
- Smart worker selection
- Automatic device discovery
- Cluster benchmarking
- Load balancing