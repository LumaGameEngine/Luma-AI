// Theme switching
document.getElementById('themeSelect').addEventListener('change', function() {
  document.documentElement.setAttribute('data-theme', this.value);
});

// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', function() {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    this.classList.add('active');
    const tab = this.dataset.tab;
    document.querySelectorAll('.tab-pane').forEach(p => p.style.display = 'none');
    document.getElementById('tab-' + tab).style.display = 'block';
  });
});

// --- Global state ---
let devices = {};

// --- Fetch devices ---
async function fetchDevices() {
  try {
    console.log('[DEBUG] Fetching devices...');
    const res = await fetch('/api/devices');
    console.log('[DEBUG] Response status:', res.status);
    const data = await res.json();
    console.log('[DEBUG] Devices data:', data);
    devices = data;
    renderDevices();
    updateStats();
    updateDeviceSelect();
  } catch (e) {
    console.error('[ERROR] Failed to fetch devices:', e);
  }
}

function renderDevices() {
  const container = document.getElementById('deviceList');
  const ids = Object.keys(devices);
  console.log('[DEBUG] Rendering devices, count:', ids.length);
  if (!ids.length) {
    container.innerHTML = '<div class="empty-state">No devices connected yet.<br />Start your worker!</div>';
    return;
  }
  container.innerHTML = ids.map(id => {
    const d = devices[id];
    const m = d.metrics || {};
    const status = d.status === 'online' ? 'status-online' : 'status-offline';
    return `
      <div class="device-card">
        <div class="device-name">
          <span class="status-badge ${status}"></span>
          ${d.name}
          <span style="font-size:0.7rem; color:var(--text-muted); margin-left:auto;">${d.arch}</span>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; font-size:0.75rem; color:var(--text-muted); margin-top:0.25rem;">
          <span>CPU ${m.cpu_usage || '?'}%</span>
          <span>RAM ${m.ram_free || '?'}MB</span>
          <span>Bat ${m.battery || '?'}%</span>
        </div>
      </div>
    `;
  }).join('');
}

function updateStats() {
  const ids = Object.keys(devices);
  const online = ids.filter(id => devices[id].status === 'online');
  document.getElementById('deviceCount').textContent = `${ids.length} Devices`;
  document.getElementById('statDevices').textContent = ids.length;
  document.getElementById('statOnline').textContent = online.length;
  let totalCpu = 0, count = 0;
  for (const id of online) {
    const cpu = devices[id].metrics?.cpu_usage;
    if (cpu !== undefined) { totalCpu += cpu; count++; }
  }
  const avg = count ? (totalCpu / count).toFixed(1) : 0;
  document.getElementById('statAvgCpu').textContent = avg + '%';
  document.getElementById('lastUpdated').textContent = new Date().toLocaleTimeString();
}

function updateDeviceSelect() {
  const select = document.getElementById('deviceSelect');
  const currentVal = select.value;
  select.innerHTML = '<option value="auto">Auto (fastest available)</option>';
  for (const id of Object.keys(devices)) {
    if (devices[id].status === 'online') {
      const opt = document.createElement('option');
      opt.value = id;
      opt.textContent = devices[id].name;
      select.appendChild(opt);
    }
  }
  if (currentVal) select.value = currentVal;
}

// --- Model upload ---
document.getElementById('modelUpload').addEventListener('change', async function(e) {
  const files = this.files;
  if (!files.length) return;
  for (const file of files) {
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await fetch('/api/models/upload', { method: 'POST', body: formData });
      const data = await res.json();
      addLog(`[MODEL] Uploaded ${data.filename} (${data.size_mb} MB)`);
      fetchModels();
    } catch (err) {
      addLog(`[ERROR] Upload failed: ${err.message}`);
    }
  }
  this.value = '';
});

async function fetchModels() {
  try {
    const res = await fetch('/api/models');
    const data = await res.json();
    const container = document.getElementById('modelList');
    if (!data.length) {
      container.innerHTML = '<div class="empty-state">No models uploaded yet.</div>';
      return;
    }
    container.innerHTML = data.map(m => `
      <div style="background:var(--bg-card); padding:0.75rem; border-radius:6px; border:1px solid var(--border);">
        <div style="font-weight:500;">${m.name}</div>
        <div style="font-size:0.8rem; color:var(--text-muted);">${m.size_mb} MB</div>
      </div>
    `).join('');
  } catch (e) { console.error(e); }
}

// --- Inference ---
async function runInference() {
  const prompt = document.getElementById('promptInput').value;
  const device = document.getElementById('deviceSelect').value;
  const resultDiv = document.getElementById('inferenceResult');
  resultDiv.innerHTML = 'Queuing inference...';
  try {
    const res = await fetch('/api/inference', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt, device_id: device === 'auto' ? null : device })
    });
    const data = await res.json();
    resultDiv.innerHTML = `
      ✅ Inference completed on ${data.device_id}
      \n\n${data.response}
    `;
    addLog(`[INFERENCE] Completed on ${data.device_id}`);
  } catch (e) {
    resultDiv.innerHTML = `Error: ${e.message}`;
  }
}

// --- Image processing ---
async function processImage(operation) {
  const fileInput = document.getElementById('imageUpload');
  const file = fileInput.files[0];
  if (!file) { alert('Please select an image first.'); return; }
  const formData = new FormData();
  formData.append('file', file);
  formData.append('operation', operation);
  formData.append('width', 256);
  formData.append('height', 256);
  try {
    const res = await fetch('/api/image/process', { method: 'POST', body: formData });
    const data = await res.json();
    if (data.status === 'ok') {
      const img = document.getElementById('processedImage');
      img.src = 'data:image/png;base64,' + data.image_base64;
      img.style.display = 'block';
      document.getElementById('imageMeta').textContent =
        `${data.operation} | Original: ${data.original_size.join('x')} | New: ${data.new_size.join('x')}`;
      addLog(`[IMAGE] Processed (${data.operation})`);
    }
  } catch (e) {
    alert('Image processing failed: ' + e.message);
  }
}

// --- Logging ---
function addLog(msg) {
  const container = document.getElementById('logContainer');
  const time = new Date().toLocaleTimeString();
  container.innerHTML += `<div>[${time}] ${msg}</div>`;
  container.scrollTop = container.scrollHeight;
}

// --- Drag and drop for models ---
const dropZone = document.getElementById('dropZone');
dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('dragover'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', e => {
  e.preventDefault();
  dropZone.classList.remove('dragover');
  const files = e.dataTransfer.files;
  if (files.length) {
    const input = document.getElementById('modelUpload');
    const dt = new DataTransfer();
    for (const f of files) dt.items.add(f);
    input.files = dt.files;
    input.dispatchEvent(new Event('change'));
  }
});
dropZone.addEventListener('click', () => document.getElementById('modelUpload').click());

// --- Polling ---
setInterval(fetchDevices, 3000);
fetchDevices();
fetchModels();
addLog('[INFO] UI loaded successfully.');
addLog('[INFO] Polling for devices every 3s.');