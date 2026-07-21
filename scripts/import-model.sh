#!/bin/bash
if [ -z "$1" ]; then
  echo "Usage: $0 <path-to-model.gguf>"
  exit 1
fi
cd "$(dirname "$0")/.."
source .venv/bin/activate
curl -X POST -F "file=@$1" http://localhost:8000/api/models/upload
