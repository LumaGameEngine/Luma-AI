#!/usr/bin/env python3
"""
Luma AI Inference Server
Runs on Android via Termux. Handles inference, model listing, switching.
"""

import json
import subprocess
import os
import re
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

HOME = os.path.expanduser("~")
MODELS_DIR = os.path.join(HOME, "Luma-AI/storage/models")
DEFAULT_MODEL = "Forge-1-Mini-Q4_K_M.gguf"
MODEL_PATH = os.path.join(MODELS_DIR, DEFAULT_MODEL)
LLAMA_CLI = os.path.join(HOME, "Luma-AI/worker/llama-cli")

os.makedirs(MODELS_DIR, exist_ok=True)

def list_models():
    try:
        files = [f for f in os.listdir(MODELS_DIR) if f.endswith('.gguf')]
        return sorted(files)
    except:
        return []

def switch_model(filename):
    global MODEL_PATH
    new_path = os.path.join(MODELS_DIR, filename)
    if not os.path.exists(new_path):
        return False, f"Model {filename} not found"
    MODEL_PATH = new_path
    return True, f"Switched to {filename}"

def clean_output(raw, prompt):
    """Extract only the assistant's response, stripping flags and prompt echo."""
    # 1. Find the assistant response between <|im_start|>assistant and <|im_end|>
    match = re.search(r'<\|im_start\|>assistant\n(.*?)(?:\n<\|im_end\|>|$)', raw, re.DOTALL)
    if match:
        response = match.group(1).strip()
        response = re.sub(r'\s*-n\s*\d+\s*$', '', response)
        if response:
            return response

    # 2. Fallback: remove all log lines and take the last non‑empty line
    lines = raw.split('\n')
    clean = []
    for line in lines:
        if (line.startswith('llama_') or
            line.startswith('load_') or
            line.startswith('print_') or
            line.startswith('init_') or
            line.startswith('create_') or
            line.startswith('done_') or
            line.startswith('set_') or
            line.startswith('sched_') or
            line.startswith('graph_') or
            line.startswith('llama_context:') or
            line.startswith('llama_kv_cache:') or
            line.startswith('llama_perf_') or
            line.startswith('main: decoded') or
            line.startswith('~llama_context:') or
            line.startswith('-p') or
            line.startswith('<s>') or
            line.startswith('load:') or
            line.startswith('...........................................')):
            continue
        clean.append(line)
    full = '\n'.join(clean).strip()
    if full.startswith(prompt):
        full = full[len(prompt):].strip()
    full = re.sub(r'\s*-n\s*\d+\s*$', '', full)
    return full if full else "No response."

class InferenceHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/models':
            models = list_models()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'models': models}).encode())
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/infer':
            content_len = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_len)
            try:
                data = json.loads(body)
                prompt = data.get('prompt', '')
                if not prompt:
                    self.send_error(400, "Missing prompt")
                    return
                formatted = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
                cmd = [LLAMA_CLI, '-m', MODEL_PATH, '-p', formatted, '-n', '128']
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=HOME)
                stdout, stderr = proc.communicate(timeout=180)
                raw_output = stdout + stderr
                response = clean_output(raw_output, prompt)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'response': response}).encode())
            except subprocess.TimeoutExpired:
                self.send_error(504, "Inference timed out")
            except Exception as e:
                self.send_error(500, str(e))

        elif self.path == '/switch_model':
            content_len = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_len)
            try:
                data = json.loads(body)
                filename = data.get('model', '')
                if not filename:
                    self.send_error(400, "Missing model name")
                    return
                success, msg = switch_model(filename)
                if success:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'ok', 'message': msg}).encode())
                else:
                    self.send_error(404, msg)
            except Exception as e:
                self.send_error(500, str(e))

        elif self.path == '/download_model':
            content_len = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_len)
            try:
                data = json.loads(body)
                url = data.get('url')
                filename = data.get('filename')
                if not url or not filename:
                    self.send_error(400, "Missing url or filename")
                    return
                file_path = os.path.join(MODELS_DIR, filename)
                print(f"[DOWNLOAD] Downloading {filename} from {url}")
                urllib.request.urlretrieve(url, file_path)
                success, msg = switch_model(filename)
                if success:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'ok', 'message': msg}).encode())
                else:
                    self.send_error(500, msg)
            except Exception as e:
                self.send_error(500, str(e))

        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass

def start_server(port=8080):
    server = HTTPServer(('0.0.0.0', port), InferenceHandler)
    print(f'Inference server listening on port {port}')
    print(f'Models directory: {MODELS_DIR}')
    print(f'Current model: {MODEL_PATH}')
    server.serve_forever()

if __name__ == '__main__':
    start_server()