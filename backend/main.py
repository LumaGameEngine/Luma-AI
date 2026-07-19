# backend/main.py
import os
import json
import uuid
import shutil
from datetime import datetime
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import io

# --- Configuration ---
STORAGE_PATH = "storage"
MODELS_PATH = os.path.join(STORAGE_PATH, "models")
os.makedirs(MODELS_PATH, exist_ok=True)
os.makedirs(STORAGE_PATH, exist_ok=True)

app = FastAPI(title="Luma AI - Control Plane")

# CORS for development (allow your phone to hit the API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the frontend static folder
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# --- In-memory device registry (will move to SQLite later) ---
devices: Dict[str, dict] = {}

# --- Pydantic Models ---
class DeviceRegister(BaseModel):
    device_id: str
    name: str
    arch: str
    ram_total: int
    cores: int

class Heartbeat(BaseModel):
    device_id: str
    ram_free: int
    cpu_usage: float
    battery: int

class InferenceRequest(BaseModel):
    prompt: str
    device_id: Optional[str] = None  # If None, scheduler picks one

# --- API Endpoints ---

@app.get("/", response_class=FileResponse)
async def root():
    return "frontend/index.html"

@app.post("/api/register")
async def register(device: DeviceRegister):
    if device.device_id in devices:
        return {"status": "already_registered"}
    devices[device.device_id] = {
        "name": device.name,
        "arch": device.arch,
        "ram_total": device.ram_total,
        "cores": device.cores,
        "status": "online",
        "last_seen": datetime.now().isoformat(),
        "metrics": {}
    }
    print(f"[REGISTER] {device.name} ({device.device_id}) joined.")
    return {"status": "success", "message": f"Welcome {device.name}!"}

@app.post("/api/heartbeat")
async def heartbeat(hb: Heartbeat):
    if hb.device_id not in devices:
        raise HTTPException(404, "Unknown device")
    devices[hb.device_id]["last_seen"] = datetime.now().isoformat()
    devices[hb.device_id]["status"] = "online"
    devices[hb.device_id]["metrics"] = {
        "ram_free": hb.ram_free,
        "cpu_usage": hb.cpu_usage,
        "battery": hb.battery
    }
    return {"status": "ok"}

@app.get("/api/devices")
async def list_devices():
    return devices

@app.get("/api/models")
async def list_models():
    """List all .gguf models in storage/models/"""
    try:
        files = [f for f in os.listdir(MODELS_PATH) if f.endswith('.gguf')]
        models = []
        for f in files:
            path = os.path.join(MODELS_PATH, f)
            size_mb = os.path.getsize(path) // (1024 * 1024)
            models.append({
                "name": f,
                "size_mb": size_mb,
                "path": path
            })
        return models
    except Exception as e:
        return []

@app.post("/api/models/upload")
async def upload_model(file: UploadFile = File(...)):
    """Upload a .gguf model file to the storage/models/ folder"""
    if not file.filename.endswith('.gguf'):
        raise HTTPException(400, "Only .gguf files are allowed")
    
    file_path = os.path.join(MODELS_PATH, file.filename)
    
    # Avoid overwriting
    if os.path.exists(file_path):
        base, ext = os.path.splitext(file.filename)
        counter = 1
        while os.path.exists(os.path.join(MODELS_PATH, f"{base}_{counter}{ext}")):
            counter += 1
        file_path = os.path.join(MODELS_PATH, f"{base}_{counter}{ext}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    size_mb = os.path.getsize(file_path) // (1024 * 1024)
    return {"status": "ok", "filename": os.path.basename(file_path), "size_mb": size_mb}

@app.post("/api/image/process")
async def process_image(file: UploadFile = File(...), operation: str = Form("resize"), width: int = Form(256), height: int = Form(256)):
    """Process an image using PIL (resize, grayscale, etc.)"""
    try:
        # Read image
        contents = await file.read()
        img = Image.open(io.BytesIO(contents))
        
        original_size = img.size
        
        # Perform operations
        if operation == "resize":
            img = img.resize((width, height), Image.Resampling.LANCZOS)
        elif operation == "grayscale":
            img = img.convert("L")
        elif operation == "thumbnail":
            img.thumbnail((width, height), Image.Resampling.LANCZOS)
        else:
            raise HTTPException(400, f"Unknown operation: {operation}")
        
        # Convert back to bytes for response
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        # Return processed image as base64 for frontend display
        import base64
        img_base64 = base64.b64encode(buffer.read()).decode()
        
        return {
            "status": "ok",
            "operation": operation,
            "original_size": original_size,
            "new_size": img.size,
            "image_base64": img_base64
        }
    except Exception as e:
        raise HTTPException(500, f"Image processing failed: {str(e)}")

@app.post("/api/inference")
async def run_inference(req: InferenceRequest):
    """
    Send a prompt to a specific device or auto-pick one.
    v0.3: This will actually forward to the phone's llama.cpp.
    v0.2: We just log it and return a placeholder.
    """
    # Pick a device if not specified
    target_device_id = req.device_id
    if not target_device_id:
        online_devices = [k for k, v in devices.items() if v.get("status") == "online"]
        if not online_devices:
            raise HTTPException(503, "No online devices available")
        target_device_id = online_devices[0]  # Round-robin will come later
    
    print(f"[INFERENCE] Device: {target_device_id}, Prompt: {req.prompt[:50]}...")
    
    # For v0.2, we just simulate a response.
    # In v0.3, we'll send an HTTP request to the phone's local server.
    return {
        "status": "queued",
        "device_id": target_device_id,
        "message": "Inference will be processed shortly (v0.3 coming soon!)",
        "prompt": req.prompt
    }

# --- Root endpoint for health check ---
@app.get("/health")
async def health():
    return {"status": "running", "devices": len(devices)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,)