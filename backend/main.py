import os
import io
import shutil
import base64
import httpx
from datetime import datetime
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image

# Optional background removal
try:
    from rembg import remove
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False

STORAGE_PATH = "storage"
MODELS_PATH = os.path.join(STORAGE_PATH, "models")
os.makedirs(MODELS_PATH, exist_ok=True)
os.makedirs(STORAGE_PATH, exist_ok=True)

app = FastAPI(title="Luma AI - Control Panel")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

devices: Dict[str, dict] = {}
round_robin_counter = 0

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
    model: Optional[str] = None

@app.post("/api/register")
async def register(device: DeviceRegister, request: Request):
    if device.device_id in devices:
        return {"status": "already_registered"}
    coordinator_url = str(request.base_url)
    devices[device.device_id] = {
        "name": device.name,
        "arch": device.arch,
        "ram_total": device.ram_total,
        "cores": device.cores,
        "ip": device.ip,
        "status": "online",
        "last_seen": datetime.now().isoformat(),
        "metrics": {},
        "current_model": None,
        "coordinator_url": coordinator_url
    }
    print(f"[REGISTER] {device.name} ({device.device_id}) from {device.ip}")
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
        return [{"name": f, "size_mb": os.path.getsize(os.path.join(MODELS_PATH, f)) // (1024*1024), "path": os.path.join(MODELS_PATH, f)} for f in files]
    except:
        return []

@app.post("/api/models/upload")
async def upload_model(file: UploadFile = File(...)):
    if not file.filename.endswith('.gguf'):
        raise HTTPException(400, "Only .gguf allowed")
    file_path = os.path.join(MODELS_PATH, file.filename)
    if os.path.exists(file_path):
        base, ext = os.path.splitext(file.filename)
        counter = 1
        while os.path.exists(os.path.join(MODELS_PATH, f"{base}_{counter}{ext}")):
            counter += 1
        file_path = os.path.join(MODELS_PATH, f"{base}_{counter}{ext}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    size_mb = os.path.getsize(file_path) // (1024*1024)
    return {"status": "ok", "filename": os.path.basename(file_path), "size_mb": size_mb}

@app.post("/api/models/download")
async def download_model(request: Request):
    data = await request.json()
    url = data.get("url")
    filename = data.get("filename")
    if not url or not filename:
        raise HTTPException(400, "Missing url/filename")
    if not url.endswith('.gguf') or 'huggingface.co' not in url:
        raise HTTPException(400, "Only .gguf from huggingface.co allowed")
    file_path = os.path.join(MODELS_PATH, filename)
    if os.path.exists(file_path):
        raise HTTPException(400, f"File '{filename}' already exists")
    async with httpx.AsyncClient(timeout=600.0, follow_redirects=True) as client:
        try:
            resp = await client.get(url)
            if resp.status_code != 200:
                raise HTTPException(502, f"Download failed: {resp.status_code}")
            with open(file_path, "wb") as f:
                f.write(resp.content)
            size_mb = os.path.getsize(file_path) // (1024*1024)
            return {"status": "ok", "filename": filename, "size_mb": size_mb}
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(500, f"Download failed: {str(e)}")

@app.get("/api/models/file/{filename}")
async def serve_model_file(filename: str):
    file_path = os.path.join(MODELS_PATH, filename)
    if not os.path.exists(file_path):
        raise HTTPException(404, "Model not found")
    return FileResponse(file_path, media_type='application/octet-stream', filename=filename)

@app.delete("/api/models/delete/{filename}")
async def delete_model(filename: str):
    """Delete a model file from coordinator storage."""
    file_path = os.path.join(MODELS_PATH, filename)
    if not os.path.exists(file_path):
        raise HTTPException(404, f"Model {filename} not found")
    try:
        os.remove(file_path)
        return {"status": "ok", "message": f"Deleted {filename}"}
    except Exception as e:
        raise HTTPException(500, f"Failed to delete: {str(e)}")

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

@app.post("/api/image/remove_bg")
async def remove_background(file: UploadFile = File(...)):
    """Remove background from an image using rembg (if installed)."""
    if not REMBG_AVAILABLE:
        raise HTTPException(503, "Background removal is not available. Install rembg: pip install rembg onnxruntime")
    try:
        contents = await file.read()
        input_image = Image.open(io.BytesIO(contents))
        output_image = remove(input_image)
        buffer = io.BytesIO()
        output_image.save(buffer, format="PNG")
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode()
        return {"status": "ok", "image_base64": img_base64}
    except Exception as e:
        raise HTTPException(500, f"Background removal failed: {str(e)}")

@app.get("/api/worker/models")
async def get_worker_models(device_id: str):
    device = devices.get(device_id)
    if not device:
        raise HTTPException(404, "Device not found")
    phone_ip = device.get("ip")
    if not phone_ip:
        raise HTTPException(500, "Device IP not known")
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            resp = await client.get(f"http://{phone_ip}:8080/models")
            if resp.status_code != 200:
                raise HTTPException(502, f"Worker error: {resp.text}")
            return resp.json()
        except httpx.TimeoutException:
            raise HTTPException(504, "Worker not responding")

@app.post("/api/worker/switch_model")
async def switch_worker_model(request: Request):
    data = await request.json()
    device_id = data.get("device_id")
    model = data.get("model")
    if not device_id or not model:
        raise HTTPException(400, "Missing device_id or model")
    device = devices.get(device_id)
    if not device:
        raise HTTPException(404, "Device not found")
    phone_ip = device.get("ip")
    if not phone_ip:
        raise HTTPException(500, "Device IP not known")
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(f"http://{phone_ip}:8080/switch_model", json={"model": model})
            if resp.status_code != 200:
                raise HTTPException(502, f"Worker error: {resp.text}")
            devices[device_id]["current_model"] = model
            return resp.json()
        except httpx.TimeoutException:
            raise HTTPException(504, "Model switch timed out")

@app.post("/api/inference")
async def run_inference(req: InferenceRequest):
    global round_robin_counter
    if not req.device_id:
        online = [k for k, v in devices.items() if v.get("status") == "online"]
        if not online:
            raise HTTPException(503, "No online devices")
        idx = round_robin_counter % len(online)
        round_robin_counter += 1
        req.device_id = online[idx]

    device = devices.get(req.device_id)
    if not device or device.get("status") != "online":
        raise HTTPException(404, "Device not found or offline")

    phone_ip = device.get("ip")
    if not phone_ip:
        raise HTTPException(500, "Device IP not known")

    # Auto‑download model if needed
    if req.model:
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                resp = await client.get(f"http://{phone_ip}:8080/models")
                if resp.status_code == 200:
                    phone_models = resp.json().get('models', [])
                    if req.model not in phone_models:
                        coordinator_url = device.get("coordinator_url")
                        if not coordinator_url:
                            raise HTTPException(500, "Coordinator URL missing")
                        file_url = f"{coordinator_url}api/models/file/{req.model}"
                        print(f"[MODEL] Downloading {req.model} to {req.device_id}")
                        download_resp = await client.post(
                            f"http://{phone_ip}:8080/download_model",
                            json={"url": file_url, "filename": req.model},
                            timeout=120.0
                        )
                        if download_resp.status_code != 200:
                            raise HTTPException(502, f"Model download failed: {download_resp.text}")
            except httpx.TimeoutException:
                raise HTTPException(504, "Could not reach phone")

        # Switch model if needed
        current = device.get("current_model")
        if current != req.model:
            async with httpx.AsyncClient(timeout=60.0) as client:
                try:
                    resp = await client.post(f"http://{phone_ip}:8080/switch_model", json={"model": req.model})
                    if resp.status_code != 200:
                        raise HTTPException(502, f"Model switch failed: {resp.text}")
                    devices[req.device_id]["current_model"] = req.model
                except httpx.TimeoutException:
                    raise HTTPException(504, "Model switch timed out")

    # Run inference
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            resp = await client.post(f"http://{phone_ip}:8080/infer", json={"prompt": req.prompt})
            if resp.status_code != 200:
                raise HTTPException(502, f"Inference server error: {resp.text}")
            result = resp.json()
            response_text = result.get("response", "No response")
            return {
                "status": "success",
                "device_id": req.device_id,
                "response": response_text,
                "prompt": req.prompt,
                "model": req.model or device.get("current_model")
            }
        except httpx.TimeoutException:
            raise HTTPException(504, "Inference timed out")
        except Exception as e:
            raise HTTPException(500, f"Failed to forward inference: {str(e)}")

@app.get("/health")
async def health():
    return {"status": "running", "devices": len(devices)}

# Mount frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)