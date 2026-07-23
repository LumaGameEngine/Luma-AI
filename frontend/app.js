// Theme switching
document.getElementById('themeSelect').addEventListener('change', function() {
  document.documentElement.setAttribute('data-theme', this.value);
  if (this.value === 'custom') loadCustomTheme();
});

// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', function() {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    this.classList.add('active');
    const tab = this.dataset.tab;
    document.querySelectorAll('.tab-pane').forEach(p => p.style.display = 'none');
    document.getElementById('tab-' + tab).style.display = 'block';
    if (tab === 'chat') {
      fetchDevices();
      const ds = document.getElementById('chatDeviceSelect');
      if (ds.value && ds.value !== 'auto') fetchWorkerModels(ds.value);
    }
  });
});

let devices = {};
let activeDownloads = {};
let chatModelLocked = false;

// ----- Devices -----
async function fetchDevices() {
  try {
    const res = await fetch('/api/devices');
    const data = await res.json();
    devices = data;
    renderDevices();
    updateStats();
    updateDeviceSelects();
  } catch (e) { console.error(e); }
}

function renderDevices() {
  const container = document.getElementById('deviceList');
  const ids = Object.keys(devices);
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
          <span>CPU ${m.cpu_usage ?? '?'}%</span>
          <span>RAM ${m.ram_free ?? '?'}MB</span>
          <span>Bat ${m.battery ?? '?'}%</span>
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

function updateDeviceSelects() {
  const selects = ['deviceSelect', 'chatDeviceSelect'];
  for (const selId of selects) {
    const select = document.getElementById(selId);
    if (!select) continue;
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
}

// ----- Worker Models -----
async function fetchWorkerModels(deviceId) {
  if (!deviceId || deviceId === 'auto') {
    document.getElementById('chatModelSelect').innerHTML = '<option value="">Auto</option>';
    return;
  }
  try {
    const res = await fetch(`/api/worker/models?device_id=${deviceId}`);
    if (!res.ok) {
      document.getElementById('chatModelSelect').innerHTML = `<option value="">Error: ${res.status}</option>`;
      return;
    }
    const data = await res.json();
    const select = document.getElementById('chatModelSelect');
    select.innerHTML = '<option value="">Select a model</option>';
    if (data.models && data.models.length) {
      for (const m of data.models) {
        const opt = document.createElement('option');
        opt.value = m;
        opt.textContent = m;
        select.appendChild(opt);
      }
    } else {
      select.innerHTML = '<option value="">No models found on device</option>';
    }
  } catch (e) {
    console.error('Failed to fetch worker models:', e);
    document.getElementById('chatModelSelect').innerHTML = '<option value="">Error loading models</option>';
  }
}

document.getElementById('chatDeviceSelect').addEventListener('change', function() {
  const deviceId = this.value;
  if (deviceId !== 'auto') fetchWorkerModels(deviceId);
  else document.getElementById('chatModelSelect').innerHTML = '<option value="">Auto</option>';
  chatModelLocked = false;
  document.getElementById('chatModelSelect').disabled = false;
});

// ----- Model Upload & Download (coordinator storage) -----
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
        <button class="secondary" style="margin-top:0.5rem; font-size:0.7rem;" onclick="selectModel('${m.name}')">Select</button>
      </div>
    `).join('');
    // Update chat model dropdown (optional)
    const chatSelect = document.getElementById('chatModelSelect');
    if (chatSelect && chatSelect.options.length <= 1) {
      const workerModels = chatSelect.querySelectorAll('option:not([value=""])');
      if (workerModels.length === 0) {
        for (const m of data) {
          const opt = document.createElement('option');
          opt.value = m.name;
          opt.textContent = m.name + ' (' + m.size_mb + ' MB)';
          chatSelect.appendChild(opt);
        }
      }
    }
  } catch (e) { console.error(e); }
}

function selectModel(name) {
  document.getElementById('chatModelSelect').value = name;
  addLog(`[MODEL] Selected: ${name}`);
}

// ----- Download from URL (to coordinator) -----
async function downloadModel() {
  const url = document.getElementById('modelUrlInput').value.trim();
  if (!url) { alert('Please enter a model URL.'); return; }
  const filename = url.split('/').pop() || 'model.gguf';
  if (activeDownloads[filename]) { alert('Already downloading ' + filename); return; }

  const container = document.getElementById('downloadsList');
  const item = document.createElement('div');
  item.className = 'download-item';
  item.id = 'dl-' + filename;
  item.innerHTML = `
    <div class="name">${filename}</div>
    <div class="progress-bar"><div class="fill" id="progress-${filename}" style="width:0%;"></div></div>
    <div class="status" id="status-${filename}">Starting...</div>
    <div class="actions"><button class="danger" onclick="cancelDownload('${filename}')">Cancel</button></div>
  `;
  container.prepend(item);
  activeDownloads[filename] = { cancelled: false };

  try {
    const res = await fetch('/api/models/download', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, filename })
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Download failed');
    }
    const reader = res.body.getReader();
    const contentLength = res.headers.get('content-length');
    const total = contentLength ? parseInt(contentLength) : 0;
    let loaded = 0;
    const chunks = [];
    while (true) {
      if (activeDownloads[filename]?.cancelled) {
        reader.cancel();
        document.getElementById('status-' + filename).textContent = 'Cancelled';
        document.getElementById('progress-' + filename).style.width = '0%';
        delete activeDownloads[filename];
        setTimeout(() => { const el = document.getElementById('dl-' + filename); if (el) el.remove(); }, 2000);
        return;
      }
      const { done, value } = await reader.read();
      if (done) break;
      chunks.push(value);
      loaded += value.length;
      if (total) {
        const pct = Math.min(100, (loaded / total) * 100);
        document.getElementById('progress-' + filename).style.width = pct + '%';
        document.getElementById('status-' + filename).textContent =
          `Downloading... ${Math.round(pct)}% (${(loaded/1024/1024).toFixed(1)} MB / ${(total/1024/1024).toFixed(1)} MB)`;
      } else {
        document.getElementById('status-' + filename).textContent =
          `Downloading... ${(loaded/1024/1024).toFixed(1)} MB`;
      }
    }
    const blob = new Blob(chunks);
    const formData = new FormData();
    formData.append('file', blob, filename);
    const uploadRes = await fetch('/api/models/upload', { method: 'POST', body: formData });
    const uploadData = await uploadRes.json();
    document.getElementById('status-' + filename).textContent = '✅ Done!';
    document.getElementById('progress-' + filename).style.width = '100%';
    addLog(`[MODEL] Downloaded ${filename} (${uploadData.size_mb} MB)`);
    fetchModels();
    const actions = item.querySelector('.actions');
    actions.innerHTML = `<span style="color:var(--accent);">✓ Complete</span>`;
    delete activeDownloads[filename];
  } catch (err) {
    document.getElementById('status-' + filename).textContent = '❌ Failed: ' + err.message;
    document.getElementById('progress-' + filename).style.width = '0%';
    const actions = item.querySelector('.actions');
    actions.innerHTML = `
      <button class="secondary" onclick="retryDownload('${filename}', '${url}')">Retry</button>
      <button class="danger" onclick="cancelDownload('${filename}')">Remove</button>
    `;
    activeDownloads[filename] = { cancelled: false, failed: true };
  }
}

function cancelDownload(filename) {
  if (activeDownloads[filename]) activeDownloads[filename].cancelled = true;
  else { const el = document.getElementById('dl-' + filename); if (el) el.remove(); }
}

async function retryDownload(filename, url) {
  const el = document.getElementById('dl-' + filename); if (el) el.remove();
  delete activeDownloads[filename];
  document.getElementById('modelUrlInput').value = url;
  downloadModel();
}

// ----- Chat -----
function lockModelSelection() {
  chatModelLocked = true;
  document.getElementById('chatModelSelect').disabled = true;
  addLog('[CHAT] Model locked for this conversation. Clear chat to change model.');
}

async function sendChat() {
  const input = document.getElementById('chatInput');
  const prompt = input.value.trim();
  if (!prompt) return;
  input.value = '';

  const messages = document.getElementById('chatMessages');
  const userMsg = document.createElement('div');
  userMsg.className = 'chat-message user';
  userMsg.innerHTML = `<div class="role">you</div><div class="content">${escapeHtml(prompt)}</div>`;
  messages.appendChild(userMsg);
  messages.scrollTop = messages.scrollHeight;

  const assistantMsg = document.createElement('div');
  assistantMsg.className = 'chat-message assistant';
  assistantMsg.id = 'chat-assistant-response';
  assistantMsg.innerHTML = `<div class="role">assistant</div><div class="content">⏳ Thinking...</div>`;
  messages.appendChild(assistantMsg);
  messages.scrollTop = messages.scrollHeight;

  const device = document.getElementById('chatDeviceSelect').value;
  const model = document.getElementById('chatModelSelect').value;

  if (model && !chatModelLocked) lockModelSelection();

  try {
    const res = await fetch('/api/inference', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt: prompt,
        device_id: device === 'auto' ? null : device,
        model: model || undefined
      })
    });
    const data = await res.json();
    if (data.status === 'success') {
      const responseText = data.response || 'No response from model.';
      document.getElementById('chat-assistant-response').innerHTML =
        `<div class="role">assistant</div><div class="content">${escapeHtml(responseText)}</div>`;
      addLog(`[CHAT] Response from ${data.device_id || 'unknown'} (model: ${data.model || 'default'})`);
    } else {
      document.getElementById('chat-assistant-response').innerHTML =
        `<div class="role">assistant</div><div class="content" style="color:#ff6b6b;">❌ Error: ${data.detail || 'Unknown error'}</div>`;
    }
  } catch (e) {
    document.getElementById('chat-assistant-response').innerHTML =
      `<div class="role">assistant</div><div class="content" style="color:#ff6b6b;">❌ Error: ${e.message}</div>`;
  }
  messages.scrollTop = messages.scrollHeight;
}

function clearChat() {
  const messages = document.getElementById('chatMessages');
  messages.innerHTML = `
    <div class="chat-message assistant">
      <div class="role">assistant</div>
      <div class="content">Chat cleared. How can I help you?</div>
    </div>
  `;
  chatModelLocked = false;
  document.getElementById('chatModelSelect').disabled = false;
  addLog('[CHAT] Cleared and unlocked model selection');
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// ----- Image Processing -----
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
    } else {
      alert('Image processing failed.');
    }
  } catch (e) {
    alert('Image processing failed: ' + e.message);
  }
}

// ----- Theme Customizer -----
function loadCustomTheme() {
  const bgPrimary = localStorage.getItem('luma_custom_bgPrimary') || '#0d0a14';
  const bgSecondary = localStorage.getItem('luma_custom_bgSecondary') || '#140f1e';
  const accent = localStorage.getItem('luma_custom_accent') || '#ff6b9d';
  const textPrimary = localStorage.getItem('luma_custom_textPrimary') || '#f0e8f5';
  document.getElementById('customBgPrimary').value = bgPrimary;
  document.getElementById('customBgSecondary').value = bgSecondary;
  document.getElementById('customAccent').value = accent;
  document.getElementById('customTextPrimary').value = textPrimary;
  applyCustomTheme();
}

function applyCustomTheme() {
  const bgPrimary = document.getElementById('customBgPrimary').value;
  const bgSecondary = document.getElementById('customBgSecondary').value;
  const accent = document.getElementById('customAccent').value;
  const textPrimary = document.getElementById('customTextPrimary').value;
  localStorage.setItem('luma_custom_bgPrimary', bgPrimary);
  localStorage.setItem('luma_custom_bgSecondary', bgSecondary);
  localStorage.setItem('luma_custom_accent', accent);
  localStorage.setItem('luma_custom_textPrimary', textPrimary);
  const root = document.documentElement;
  root.style.setProperty('--bg-primary', bgPrimary);
  root.style.setProperty('--bg-secondary', bgSecondary);
  root.style.setProperty('--bg-card', darken(bgSecondary, 10));
  root.style.setProperty('--bg-input', darken(bgSecondary, 20));
  root.style.setProperty('--accent', accent);
  root.style.setProperty('--accent-dim', accent + '26');
  root.style.setProperty('--accent-glow', accent + '4D');
  root.style.setProperty('--text-primary', textPrimary);
  root.style.setProperty('--text-secondary', lighten(textPrimary, 20));
  root.style.setProperty('--text-muted', lighten(textPrimary, 40));
  root.style.setProperty('--border', accent + '1E');
  document.documentElement.setAttribute('data-theme', 'custom');
  document.getElementById('themeSelect').value = 'custom';
  addLog('[THEME] Custom theme applied');
}

function resetCustomTheme() {
  localStorage.removeItem('luma_custom_bgPrimary');
  localStorage.removeItem('luma_custom_bgSecondary');
  localStorage.removeItem('luma_custom_accent');
  localStorage.removeItem('luma_custom_textPrimary');
  document.documentElement.setAttribute('data-theme', 'luma');
  document.getElementById('themeSelect').value = 'luma';
  const root = document.documentElement;
  root.style.removeProperty('--bg-primary');
  root.style.removeProperty('--bg-secondary');
  root.style.removeProperty('--bg-card');
  root.style.removeProperty('--bg-input');
  root.style.removeProperty('--accent');
  root.style.removeProperty('--accent-dim');
  root.style.removeProperty('--accent-glow');
  root.style.removeProperty('--text-primary');
  root.style.removeProperty('--text-secondary');
  root.style.removeProperty('--text-muted');
  root.style.removeProperty('--border');
  addLog('[THEME] Reset to Luma');
}

function darken(hex, amount) {
  let r = parseInt(hex.slice(1,3), 16);
  let g = parseInt(hex.slice(3,5), 16);
  let b = parseInt(hex.slice(5,7), 16);
  r = Math.max(0, r - amount);
  g = Math.max(0, g - amount);
  b = Math.max(0, b - amount);
  return `#${r.toString(16).padStart(2,'0')}${g.toString(16).padStart(2,'0')}${b.toString(16).padStart(2,'0')}`;
}
function lighten(hex, amount) {
  let r = parseInt(hex.slice(1,3), 16);
  let g = parseInt(hex.slice(3,5), 16);
  let b = parseInt(hex.slice(5,7), 16);
  r = Math.min(255, r + amount);
  g = Math.min(255, g + amount);
  b = Math.min(255, b + amount);
  return `#${r.toString(16).padStart(2,'0')}${g.toString(16).padStart(2,'0')}${b.toString(16).padStart(2,'0')}`;
}

// ----- Logging -----
function addLog(msg) {
  const container = document.getElementById('logContainer');
  const time = new Date().toLocaleTimeString();
  container.innerHTML += `<div>[${time}] ${msg}</div>`;
  container.scrollTop = container.scrollHeight;
}

// ----- Drag and Drop for Models -----
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

// ----- Polling -----
setInterval(fetchDevices, 3000);
setInterval(fetchModels, 10000);
fetchDevices();
fetchModels();
addLog('[INFO] UI loaded successfully.');
addLog('[INFO] Polling for devices every 3s.');
