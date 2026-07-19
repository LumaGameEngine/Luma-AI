<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Luma AI – Distributed Edge AI Cluster</title>
    <style>
        /* Minimal, readable styling */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            background: #0b0e14;
            color: #e4e7ee;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            padding: 2rem 1rem;
            max-width: 1000px;
            margin: 0 auto;
        }
        h1, h2, h3, h4 {
            color: #ffffff;
            font-weight: 600;
            margin-top: 2rem;
            margin-bottom: 0.75rem;
        }
        h1 {
            font-size: 2.5rem;
            border-bottom: 2px solid #00ff88;
            padding-bottom: 0.5rem;
            display: inline-block;
        }
        h1 small {
            font-size: 1rem;
            font-weight: 400;
            color: #00ff88;
            margin-left: 0.5rem;
        }
        a {
            color: #66d9ff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        p, li {
            margin-bottom: 0.75rem;
            color: #d0d5e0;
        }
        ul, ol {
            padding-left: 1.5rem;
            margin-bottom: 1rem;
        }
        code {
            background: #1a1f2b;
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            font-family: "Fira Code", "JetBrains Mono", monospace;
            font-size: 0.9rem;
            color: #d4e0ff;
        }
        pre {
            background: #0f1420;
            padding: 1rem;
            border-radius: 8px;
            overflow-x: auto;
            border: 1px solid #2a3140;
            margin: 1rem 0;
            font-size: 0.9rem;
            color: #b8c7e6;
        }
        pre code {
            background: transparent;
            padding: 0;
            color: inherit;
        }
        .badge {
            display: inline-block;
            background: #00ff8822;
            color: #00ff88;
            padding: 0.15rem 0.7rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
            margin-right: 0.3rem;
            border: 1px solid #00ff8844;
        }
        .badge-blue {
            background: #3399ff22;
            color: #66d9ff;
            border-color: #3399ff44;
        }
        .badge-yellow {
            background: #ffaa0033;
            color: #ffcc44;
            border-color: #ffaa0044;
        }
        hr {
            border: 0;
            border-top: 1px solid #2a3140;
            margin: 2rem 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
            font-size: 0.9rem;
        }
        th, td {
            padding: 0.6rem 1rem;
            border: 1px solid #2a3140;
            text-align: left;
        }
        th {
            background: #1a1f2b;
            color: #fff;
        }
        td {
            background: #0f1420;
        }
        .container {
            background: #11161f;
            padding: 2rem;
            border-radius: 16px;
            border: 1px solid #2a3140;
            box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        }
        .emoji-big {
            font-size: 1.8rem;
            vertical-align: middle;
        }
        @media (max-width: 600px) {
            body { padding: 1rem; }
            .container { padding: 1rem; }
            h1 { font-size: 1.8rem; }
        }
        .footer {
            margin-top: 2rem;
            text-align: center;
            color: #6a7a8e;
            font-size: 0.9rem;
            border-top: 1px solid #2a3140;
            padding-top: 1.5rem;
        }
    </style>
</head>
<body>
<div class="container">

    <!-- HEADER -->
    <header>
        <h1>🚀 Luma AI <small>Turn your old Android phones into a distributed AI cluster.</small></h1>
        <p style="margin-top: 0.5rem;">
            <span class="badge">Python 3.10+</span>
            <span class="badge badge-blue">FastAPI 0.115+</span>
            <span class="badge badge-yellow">MIT License</span>
            <span class="badge">PRs Welcome</span>
        </p>
    </header>

    <!-- WHAT IS LUMA AI -->
    <section>
        <h2>🧠 What is Luma AI?</h2>
        <p>
            Luma AI is an open‑source framework that turns outdated Android smartphones and tablets into a
            <strong>distributed edge‑AI compute cluster</strong>.
            Instead of throwing away old devices, you can repurpose them to run lightweight language models locally —
            completely offline, with no cloud dependency.
        </p>
        <p>
            <strong>This project proves that 2GB RAM, 32‑bit ARM phones can still be part of the AI revolution.</strong>
        </p>
    </section>

    <!-- FEATURES -->
    <section>
        <h2>✨ Features</h2>
        <ul>
            <li><strong>🗄️ Coordinator‑Worker Architecture</strong> – A central FastAPI server manages all connected devices.</li>
            <li><strong>📱 Multi‑Architecture Support</strong> – Works on both 32‑bit (ARMv7) and 64‑bit (AArch64) Android devices.</li>
            <li><strong>🌐 Real‑time Dashboard</strong> – A beautiful Tailwind CSS UI showing live device metrics (CPU, RAM, battery).</li>
            <li><strong>📦 Model Manager</strong> – Upload <code>.gguf</code> models directly via the web UI – no command line required.</li>
            <li><strong>🖼️ Image Processing Lab</strong> – Resize, grayscale, or create thumbnails using Pillow, all inside the dashboard.</li>
            <li><strong>🔌 Plug‑and‑Play Workers</strong> – Termux workers register themselves automatically over Wi‑Fi.</li>
            <li><strong>📈 Cluster‑Ready Scheduler</strong> (coming soon) – Distribute prompts across multiple devices.</li>
        </ul>
    </section>

    <!-- ARCHITECTURE -->
    <section>
        <h2>🏗️ Architecture</h2>
        <pre>
                 ┌─────────────────────────┐
                 │    Luma Coordinator     │
                 │  (FastAPI + SQLite)     │
                 │   Runs on your Laptop   │
                 └────────────┬────────────┘
                              │
                 ┌────────────┴────────────┐
                 │      Wi‑Fi Network      │
                 └────────────┬────────────┘
                ┌─────────────┼─────────────┐
                │             │             │
         ┌──────▼──────┐ ┌────▼─────┐ ┌────▼─────┐
         │  Spark Go   │ │ Galaxy   │ │ Tablet   │
         │  (ARMv7)   │ │ (ARM64)  │ │ (ARM64)  │
         │  2GB RAM   │ │  4GB RAM │ │  3GB RAM │
         └────────────┘ └──────────┘ └──────────┘
        </pre>
    </section>

    <!-- HARDWARE REQUIREMENTS -->
    <section>
        <h2>📦 Hardware Requirements</h2>
        <h3>Coordinator (Laptop / Server)</h3>
        <ul>
            <li>Python 3.10+</li>
            <li>4GB+ RAM</li>
            <li>Wi‑Fi or Ethernet</li>
        </ul>
        <h3>Worker (Android Device)</h3>
        <ul>
            <li><strong>Android 8.0 or higher</strong></li>
            <li><strong>2GB RAM minimum</strong> (1.8GB is the lowest tested)</li>
            <li><strong>Storage:</strong> 500MB free (more for models)</li>
            <li><strong>Architecture:</strong> ARMv7 (32‑bit) or AArch64 (64‑bit)</li>
            <li><strong>Termux</strong> (available on F‑Droid)</li>
        </ul>
        <p><strong>✅ Tested Device:</strong> Tecno Spark Go 2020 (MediaTek Helio P22, 2GB RAM, Android 10, ARMv7).</p>
    </section>

    <!-- QUICK START -->
    <section>
        <h2>🛠️ Quick Start</h2>
        <h3>1. Clone the Repository</h3>
        <pre><code>git clone https://github.com/LumaGameEngine/Luma-AI.git
cd Luma-AI</code></pre>

        <h3>2. Set Up the Coordinator (on your laptop)</h3>
        <pre><code>python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python backend/main.py</code></pre>
        <p>Open your browser at <a href="http://localhost:8000">http://localhost:8000</a> — you should see the dashboard.</p>

        <h3>3. Set Up a Worker (on your Android device)</h3>
        <p>Install <strong>Termux</strong> from <a href="https://f-droid.org/packages/com.termux/">F‑Droid</a> (the Play Store version is outdated).</p>
        <p>Open Termux on your Android device and run:</p>
        <pre><code># Update and install dependencies
pkg update && pkg upgrade -y
pkg install python git wget

# Clone the worker scripts
git clone https://github.com/LumaGameEngine/Luma-AI.git
cd Luma-AI/worker/android

# Edit the config with your laptop's IP
nano config.json</code></pre>
        <p>Replace <code>"server_ip"</code> with your laptop’s local IP address (e.g. <code>"192.168.1.9"</code>).<br>
        Then start the worker:</p>
        <pre><code>python worker.py</code></pre>
        <p>You should see:</p>
        <pre><code>🚀 Luma AI Worker: Spark-Go-2020
📡 Connecting to http://192.168.1.9:8000
[REGISTER] Welcome Spark-Go-2020!
✅ Registered. Starting heartbeats...
...........</code></pre>
        <p>Refresh the dashboard on your laptop—the device will appear in the sidebar.</p>
    </section>

    <!-- RUNNING A MODEL -->
    <section>
        <h2>🧠 Running a Model</h2>
        <h3>Upload a Tiny Model</h3>
        <ol>
            <li>Go to the <strong>Models</strong> tab in the dashboard.</li>
            <li>Drag and drop a <code>.gguf</code> file, or click to browse.</li>
            <li>The model will be stored in <code>storage/models/</code> on your laptop.</li>
        </ol>

        <h3>Recommended Models for Low‑RAM Devices</h3>
        <table>
            <thead>
                <tr>
                    <th>Model</th>
                    <th>Size (GGUF)</th>
                    <th>Best For</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><strong>Forge‑1‑Mini (Q4_K_M)</strong></td><td>3.8 MB</td><td>Ultra‑lightweight chat</td></tr>
                <tr><td><strong>MobileLLM‑125M</strong></td><td>~150 MB</td><td>General‑purpose chat</td></tr>
                <tr><td><strong>rb‑nano</strong></td><td>~80 MB</td><td>Short conversations</td></tr>
                <tr><td><strong>TinyStories‑33M</strong></td><td>~65 MB</td><td>Story generation</td></tr>
            </tbody>
        </table>

        <p>Download Forge‑1‑Mini directly on your Android worker:</p>
        <pre><code>cd ~/LumaAI/models
wget https://huggingface.co/North-ML1/Forge-1-Mini-GGUF/resolve/main/Forge-1-Mini-Q4_K_M.gguf</code></pre>

        <h3>Run Inference (Coming in v0.3)</h3>
        <p>Once the model is uploaded, go to the <strong>Inference</strong> tab, select a device, enter a prompt, and hit <strong>Run</strong>.<br>
        The worker will execute the model locally and stream the response back to the dashboard.</p>
    </section>

    <!-- ROADMAP -->
    <section>
        <h2>🎯 Roadmap</h2>
        <table>
            <thead>
                <tr><th>Version</th><th>Milestone</th><th>Status</th></tr>
            </thead>
            <tbody>
                <tr><td><strong>v0.1</strong></td><td>Worker registers + heartbeats</td><td>✅ Done</td></tr>
                <tr><td><strong>v0.2</strong></td><td>Dashboard with live metrics</td><td>✅ Done</td></tr>
                <tr><td><strong>v0.3</strong></td><td>Single‑device inference (llama.cpp)</td><td>🚧 In progress</td></tr>
                <tr><td><strong>v0.4</strong></td><td>Multi‑worker round‑robin scheduler</td><td>📋 Planned</td></tr>
                <tr><td><strong>v0.5</strong></td><td>SQLite persistence for devices &amp; chat</td><td>📋 Planned</td></tr>
                <tr><td><strong>v1.0</strong></td><td>Fully distributed inference pipeline</td><td>🔮 Future</td></tr>
            </tbody>
        </table>
    </section>

    <!-- PROJECT STRUCTURE -->
    <section>
        <h2>📂 Project Structure</h2>
        <pre><code>Luma-AI/
├── backend/                 # FastAPI coordinator
│   ├── api/                 # Routes and endpoints
│   ├── scheduler/           # Future task distribution
│   ├── database/            # SQLite models
│   ├── workers/             # Worker management
│   ├── main.py              # Entry point
│   └── requirements.txt
├── frontend/                # Web dashboard
│   └── index.html           # Tailwind UI
├── worker/                  # Android worker code
│   ├── android/             # Termux scripts
│   └── client.py            # Pure Python worker (no external deps)
├── storage/
│   ├── models/              # Uploaded .gguf files
│   └── cache/
├── docs/                    # Architecture and design docs
├── tests/                   # Unit and integration tests
├── .gitignore
├── LICENSE                  # MIT
└── README.md                # This file</code></pre>
    </section>

    <!-- CONTRIBUTING -->
    <section>
        <h2>🤝 Contributing</h2>
        <p>We welcome contributions from all skill levels!</p>
        <ol>
            <li><strong>Fork</strong> the repository.</li>
            <li><strong>Create a feature branch:</strong> <code>git checkout -b feature/amazing-idea</code></li>
            <li><strong>Commit your changes:</strong> <code>git commit -m "Add amazing idea"</code></li>
            <li><strong>Push:</strong> <code>git push origin feature/amazing-idea</code></li>
            <li>Open a <strong>Pull Request</strong>.</li>
        </ol>
        <p>Check the <a href="#-roadmap">Roadmap</a> for open milestones or suggest your own!</p>
    </section>

    <!-- LICENSE -->
    <section>
        <h2>📄 License</h2>
        <p>Distributed under the <strong>MIT License</strong>. See the <a href="LICENSE">LICENSE</a> file for details.</p>
    </section>

    <!-- ACKNOWLEDGMENTS -->
    <section>
        <h2>⚡ Acknowledgments</h2>
        <ul>
            <li><a href="https://github.com/ggerganov/llama.cpp">ggerganov/llama.cpp</a> for the amazing inference engine.</li>
            <li><a href="https://termux.com">Termux</a> for bringing a Linux environment to Android.</li>
            <li>The open‑source community for making edge AI possible.</li>
        </ul>
    </section>

    <!-- STAY IN TOUCH -->
    <section>
        <h2>💬 Stay in Touch</h2>
        <ul>
            <li><strong>GitHub Issues:</strong> For bug reports and feature requests.</li>
            <li><strong>Discussions:</strong> For questions and community support.</li>
        </ul>
        <p><em>Built with ❤️ for the planet’s forgotten hardware.</em></p>
    </section>

    <!-- FOOTER -->
    <div class="footer">
        <p>&copy; 2026 LumaGameEngine – Open Source MIT License</p>
    </div>

</div>
</body>
</html>