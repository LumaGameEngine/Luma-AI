# 🚀 Luma AI

> Turn old Android devices into a distributed edge-AI cluster.

![Luma AI Banner](docs/banner.png)

Luma AI is an open-source distributed computing framework designed to transform old Android smartphones and tablets into useful edge computing nodes.

Instead of letting old hardware collect dust, Luma AI gives these devices a second life by turning them into lightweight AI workers capable of processing tasks locally.

The goal: **make AI more accessible by using hardware people already own.**

---

## 🧠 Vision

Modern AI often requires expensive GPUs and powerful servers.

Luma AI explores another approach:

         Luma Coordinator
         (Laptop / Server)

                |
             Wi-Fi

    +-----------+-----------+
    |           |           |

 Phone A     Phone B     Tablet
 ARMv7       ARM64       ARM64

    \           |          /

      Distributed Edge AI

A cluster made from old devices.

---

# ✨ Features

## ✅ Current

- Python-based coordinator architecture
- Android worker concept
- ARMv7 / ARM64 compatibility target
- Lightweight device communication
- CPU-first design philosophy
- Designed for low-end hardware

## 🚧 In Development

- Worker registration system
- Device heartbeat monitoring
- Web dashboard
- Remote task execution
- Image processing workloads
- Model management

## 🔮 Future

- Multi-device scheduling
- Distributed inference
- Automatic hardware benchmarking
- Offline AI clusters
- Community-powered edge computing

---

# 🏗️ Architecture

             Luma AI Coordinator

              FastAPI Backend

                    |
                    |
               Local Network

    +---------------+---------------+

    Spark Go     Galaxy A15     Tablet
    ARMv7        ARM64          ARM64

    Worker       Worker         Worker

The coordinator manages connected devices while workers execute assigned tasks.

---

# 📱 Tested Hardware

## Tecno Spark Go 2020

| Component | Specification |
|-|-|
| CPU | MediaTek Helio P22 |
| Architecture | ARMv7 |
| Cores | 8x Cortex-A53 |
| RAM | 2GB |
| Storage | 32GB |
| Android | 10 |

The Spark Go is currently used as a low-end test device to ensure Luma AI remains efficient.

---

# 🛠️ Installation

## Coordinator (Laptop)

Clone the repository:

```bash
git clone https://github.com/LumaGameEngine/Luma-AI.git

cd Luma-AI

Create a Python environment:

python3 -m venv .venv

source .venv/bin/activate

Install dependencies:

pip install -r backend/requirements.txt

Start the coordinator:

python backend/main.py
Android Worker

Install Termux from F-Droid.

Install requirements:

pkg update
pkg install python git

Clone:

git clone https://github.com/LumaGameEngine/Luma-AI.git

cd Luma-AI

Start worker:

python worker.py
📂 Project Structure
Luma-AI/

├── backend/
│   ├── main.py
│   ├── database.py
│   └── requirements.txt
│
├── frontend/
│   └── dashboard
│
├── inference/
│   └── AI execution layer
│
├── storage/
│   └── models/
│
├── scripts/
│
├── docs/
│
└── README.md
🎯 Roadmap
v0.1 — Foundation
 Repository created
 Backend skeleton
 Worker architecture design
v0.2 — Communication
 Worker registration
 Heartbeat system
 Device information reporting
v0.3 — Edge Processing
 Image processing jobs
 Remote task execution
 Resource monitoring
v0.4 — AI Workloads
 llama.cpp integration
 Lightweight model support
 Local inference
v1.0 — Distributed AI
 Multi-device scheduling
 Intelligent workload distribution
 Community edge AI network
🤝 Contributing

Contributions are welcome!

Ideas, optimizations, documentation, and hardware testing are appreciated.

Steps:

git clone your-fork

git checkout -b feature/my-feature

git commit -m "Add feature"

git push origin feature/my-feature

Open a Pull Request.

📜 License

Luma AI is released under the MIT License.

🌙 Part of the Luma Ecosystem

Luma AI is part of the LumaGameEngine ecosystem.

Related projects:

🎮 Luma Engine — CPU-first game engine
🛒 Luma Store — digital marketplace

Built with ❤️ for forgotten hardware.

Luma AI — Give old devices a second life.
