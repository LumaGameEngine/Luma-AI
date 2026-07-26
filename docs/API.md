# API Reference

This document describes every REST endpoint exposed by the coordinator and worker.

## Coordinator

### POST /api/register

Registers a worker.

Request

```json
{
  "device_id": "...",
  "name": "...",
  "arch": "armv7"
}

Response

{
  "success": true
}

POST /api/heartbeat

Updates worker metrics.

GET /api/models

Returns all available models.

POST /api/inference

Runs inference on a worker.