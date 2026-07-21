import os
import io
import shutil
import base64
from datetime import datetime
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import httpx

STORAGE_PATH = "storage"
MODELS_PATH = os.path.join(STORAGE_PATH, "models")
os.makedirs(MODELS_PATH, exist_ok=True)
os.makedirs(STORAGE_PATH, exist_ok=True)

app = FastAPI(title="Luma AI - Control Plane")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- API routes first ----
devices: Dict[str, dict] = {}

class DeviceRegister(BaseModel):
    device_id: str
    name: str
    arch: str
    ram_total: int
    cores: int
    ip: str

class Heartbeat(BaseModel):
    device_id: str
    ram_free: int
    cpu_usage: float
    battery: int

class InferenceRequest(BaseModel):
    prompt: str
    device_id: Optional[str] = None

@app.post("/api/register")
async def register(device: DeviceRegister):
    if device.device_id in devices:
        return {"status": "already_registered"}
    devices[device.device_id] = {
        "name": device.name,
        "arch": device.arch,
        "ram_total": device.ram_total,
        "cores": device.cores,
        "ip": device.ip,
        "status": "online",
        "last_seen": datetime.now().isoformat(),
        "metrics": {}
    }
    print(f"[REGISTER] {device.name} ({device.device_id}) joined from {device.ip}")
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
    try:
        files = [f for f in os.listdir(MODELS_PATH) if f.endswith('.gguf')]
        models = []
        for f in files:
            path = os.path.join(MODELS_PATH, f)
            size_mb = os.path.getsize(path) // (1024 * 1024)
            models.append({"name": f, "size_mb": size_mb, "path": path})
        return models
    except Exception:
        return []

@app.post("/api/models/upload")
async def upload_model(file: UploadFile = File(...)):
    if not file.filename.endswith('.gguf'):
        raise HTTPException(400, "Only .gguf files are allowed")
    file_path = os.path.join(MODELS_PATH, file.filename)
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
async def process_image(
    file: UploadFile = File(...),
    operation: str = Form("resize"),
    width: int = Form(256),
    height: int = Form(256)
):
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents))
        original_size = img.size
        if operation == "resize":
            img = img.resize((width, height), Image.Resampling.LANCZOS)
        elif operation == "grayscale":
            img = img.convert("L")
        elif operation == "thumbnail":
            img.thumbnail((width, height), Image.Resampling.LANCZOS)
        else:
            raise HTTPException(400, f"Unknown operation: {operation}")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
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
    if not req.device_id:
        online = [k for k, v in devices.items() if v.get("status") == "online"]
        if not online:
            raise HTTPException(503, "No online devices available")
        req.device_id = online[0]
    device = devices.get(req.device_id)
    if not device:
        raise HTTPException(404, "Device not found")
    if device.get("status") != "online":
        raise HTTPException(503, "Device is offline")
    phone_ip = device.get("ip")
    if not phone_ip:
        raise HTTPException(500, "Device IP not known")
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            resp = await client.post(
                f"http://{phone_ip}:8080/infer",
                json={"prompt": req.prompt}
            )
            if resp.status_code != 200:
                raise HTTPException(502, f"Inference server error: {resp.text}")
            result = resp.json()
            return {
                "status": "success",
                "device_id": req.device_id,
                "response": result.get("response", ""),
                "prompt": req.prompt
            }
        except httpx.TimeoutException:
            raise HTTPException(504, "Inference timed out on device")
        except Exception as e:
            raise HTTPException(500, f"Failed to forward inference: {str(e)}")

@app.get("/health")
async def health():
    return {"status": "running", "devices": len(devices)}

# ---- Serve frontend files from the root ----
# API routes are defined above, so they take precedence.
# Mount the frontend folder at "/" – this serves index.html, style.css, app.js, etc.
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
