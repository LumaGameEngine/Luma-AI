# Luma AI

> A distributed edge AI framework that transforms old Android devices into intelligent compute nodes.

<p align="center">
  <img src="docs/banner.png" alt="Luma AI Banner" width="100%">
</p>

<p align="center">
  <strong>Build AI clusters from hardware you already own.</strong><br>
  Lightweight • Open Source • Cross-Architecture • Edge Computing
</p>

---

# Table of Contents

* [Overview](#overview)
* [Vision](#vision)
* [Why Luma AI?](#why-luma-ai)
* [Key Features](#key-features)
* [Architecture](#architecture)
* [Communication Pipeline](#communication-pipeline)
* [System Components](#system-components)
* [Project Structure](#project-structure)
* [Getting Started](#getting-started)
* [Coordinator Installation](#coordinator-installation)
* [Android Worker Installation](#android-worker-installation)
* [Configuration](#configuration)
* [How Luma AI Works](#how-luma-ai-works)
* [Inference Lifecycle](#inference-lifecycle)
* [Supported Hardware](#supported-hardware)
* [REST API Overview](#rest-api-overview)
* [Roadmap](#roadmap)
* [Performance Goals](#performance-goals)
* [Contributing](#contributing)
* [Development Guidelines](#development-guidelines)
* [License](#license)
* [Acknowledgments](#acknowledgments)

---

# Overview

Luma AI is an open-source distributed edge computing framework designed to give aging Android devices a new purpose.

Instead of requiring expensive GPUs or cloud servers, Luma AI allows multiple Android phones and tablets to work together as intelligent AI workers connected over a local network.

Each device contributes CPU power, memory, and storage to a shared cluster capable of running language models, image processing tasks, and future AI workloads.

The project is built around one simple philosophy:

> Hardware should become obsolete because it cannot meet your needs—not because software refuses to use it.

Whether you're experimenting with AI, building a local assistant, or learning distributed systems, Luma AI provides an accessible platform that runs on devices people already own.

---

# Vision

Artificial Intelligence has become increasingly centralized around expensive hardware.

Large language models typically require:

* Dedicated GPUs
* Powerful desktop computers
* Cloud subscriptions
* High electricity consumption

Millions of Android phones become electronic waste every year despite still having:

* Multi-core processors
* Several gigabytes of RAM
* Wi-Fi connectivity
* Battery backup
* Linux-based operating systems

Luma AI explores a different direction.

Rather than replacing old hardware, it repurposes it.

```
                     Luma Coordinator
                  (Laptop / Mini Server)

                          │
                     Local Wi-Fi
                          │

      ┌─────────────┬──────────────┬─────────────┐
      │             │              │             │
  Spark Go      Galaxy A15      Tablet      Raspberry Pi
    Worker         Worker         Worker        Worker
      │              │              │             │
      └──────────────┴──────────────┴─────────────┘

             Distributed Edge AI Cluster
```

Every connected device becomes a worker capable of receiving tasks, executing inference, and returning results.

---

# Why Luma AI?

Luma AI focuses on accessibility instead of raw performance.

## Advantages

* Makes use of existing hardware
* Reduces electronic waste
* Low power consumption
* No GPU required
* Local inference
* Private by design
* Modular architecture
* Cross-platform coordinator
* ARM32 and ARM64 support
* Completely open source

Instead of replacing hardware, Luma AI extends its lifespan.

---

# Key Features

| Feature                         | Status         |
| ------------------------------- | -------------- |
| Device Registration             | Complete       |
| Heartbeat Monitoring            | Complete       |
| Live Dashboard                  | Complete       |
| Model Management                | Complete       |
| Automatic Model Synchronization | Complete       |
| Chat Interface                  | Complete       |
| Theme System                    | Complete       |
| Image Processing Utilities      | Complete       |
| ARMv7 Support                   | Complete       |
| ARM64 Support                   | Complete       |
| Multi-device Scheduling         | In Development |
| Distributed Inference           | Planned        |
| Image Generation                | Planned        |
| Smart Load Balancing            | Planned        |
| Automatic Device Discovery      | Planned        |
| Cluster Benchmarking            | Planned        |

---

# Architecture

```
                        User Interface
                             │
                             ▼
                    FastAPI Coordinator
               REST API + Dashboard + Scheduler
                             │
         ─────────────────────────────────────────
                     Local Network (Wi-Fi)
         ─────────────────────────────────────────
             │                │               │
             ▼                ▼               ▼
       Android Worker   Android Worker   Android Worker
        ARMv7 Phone      ARM64 Phone       Tablet

             │                │               │
             ▼                ▼               ▼
          llama.cpp       llama.cpp      llama.cpp
```

---

# Communication Pipeline

Every worker communicates with the coordinator through HTTP.

```
Worker Startup
      │
      ▼
Device Registration
      │
      ▼
Heartbeat Loop
      │
      ▼
Coordinator Dashboard Update
      │
      ▼
User Sends Prompt
      │
      ▼
Scheduler Selects Worker
      │
      ▼
Inference Execution
      │
      ▼
Worker Response
      │
      ▼
Dashboard Displays Result
```

---

# System Components

## Coordinator

The coordinator is the brain of the cluster.

Responsibilities include:

* Managing connected devices
* Monitoring worker health
* Scheduling inference
* Hosting the dashboard
* Managing AI models
* Synchronizing workers
* Serving REST APIs

Technology stack:

* Python
* FastAPI
* Uvicorn
* SQLite (future)
* WebSockets (future)

---

## Worker

Each Android device runs a lightweight worker.

Responsibilities:

* Register with coordinator
* Report hardware information
* Execute inference
* Monitor system resources
* Download requested models
* Process AI tasks

Designed to consume as little memory as possible.

---

## Dashboard

The dashboard provides a centralized interface for:

* Connected devices
* CPU usage
* RAM usage
* Battery level
* Model management
* Live logs
* Chat interface
* Theme customization

---

## Model Storage

Models are stored on the coordinator.

Workers download models only when required.

Benefits:

* No duplicated storage
* Easy updates
* Version consistency
* Faster deployment

---

# Project Structure

```
Luma-AI/

backend/
│
├── api/
├── models/
├── routes/
├── scheduler/
├── storage/
├── utils/
├── main.py
└── requirements.txt

frontend/
│
├── assets/
├── css/
├── js/
├── index.html
└── themes/

worker/
│
├── client.py
├── inference_server.py
├── monitor.py
├── config.json
└── llama-cli

storage/
└── models/

scripts/
├── install.sh
├── build.sh
└── start.sh

docs/
├── banner.png
├── screenshots/
└── architecture/

LICENSE
README.md
```

---

# Getting Started

## Requirements

Coordinator

* Python 3.11+
* Git
* Wi-Fi network

Worker

* Android 8+
* Termux
* Python
* Git
* CMake
* Clang

---

# Coordinator Installation

Clone the repository.

```bash
git clone https://github.com/LumaGameEngine/Luma-AI.git

cd Luma-AI
```

Create a virtual environment.

```bash
python3 -m venv .venv
```

Activate it.

Linux

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r backend/requirements.txt
```

Launch the coordinator.

```bash
python backend/main.py
```

Open your browser.

```
http://localhost:8000
```

---

# Android Worker Installation

Install Termux from F-Droid.

Update packages.

```bash
pkg update

pkg upgrade
```

Install dependencies.

```bash
pkg install python git clang cmake make wget openssh
```

Clone the repository.

```bash
git clone https://github.com/LumaGameEngine/Luma-AI.git

cd Luma-AI
```

Configure the coordinator.

```json
{
    "server_ip":"192.168.1.25",
    "server_port":8000
}
```

Start the inference server.

```bash
python inference_server.py
```

Launch the worker.

```bash
python client.py
```

The worker should appear in the dashboard within a few seconds.

---

# Configuration

Example worker configuration:

```json
{
    "device_name":"Spark-Go",
    "server_ip":"192.168.1.25",
    "server_port":8000,
    "heartbeat_interval":10,
    "architecture":"armv7"
}
```

---

# How Luma AI Works

## Step 1 — Device Registration

When a worker starts, it gathers information including:

* Device name
* Device ID
* Local IP
* CPU architecture
* Available RAM
* CPU cores
* Android version

It sends a registration request.

```
POST /api/register
```

The coordinator validates the request and stores the worker.

---

## Step 2 — Heartbeat

Every ten seconds the worker reports:

* CPU usage
* RAM usage
* Battery level
* Temperature (future)
* Storage usage (future)

The coordinator updates the dashboard in real time.

---

## Step 3 — Model Synchronization

When a model is selected:

Coordinator checks

↓

Worker inventory

↓

Missing?

↓

Download

↓

Verify checksum

↓

Ready

Workers never download models they already possess.

---

## Step 4 — Inference

The coordinator selects a worker.

The worker executes:

```bash
llama-cli \
-m model.gguf \
-p "Hello"
```

The response is returned to the coordinator and immediately displayed inside the web interface.

---

# Inference Lifecycle

```
User Prompt
     │
     ▼
Coordinator
     │
Scheduler
     │
Selected Worker
     │
llama.cpp
     │
Response
     │
Coordinator
     │
Dashboard
```

Future versions will support splitting workloads across multiple workers simultaneously.

---

# Supported Hardware

## Minimum Supported Device

| Component    | Specification      |
| ------------ | ------------------ |
| CPU          | MediaTek Helio P22 |
| Architecture | ARMv7              |
| RAM          | 2 GB               |
| Android      | Android 10         |
| Storage      | 32 GB              |

Reference device:

Tecno Spark Go 2020

---

## Recommended Device

| Component    | Specification      |
| ------------ | ------------------ |
| CPU          | Helio G99 or newer |
| Architecture | ARM64              |
| RAM          | 4 GB or more       |
| Android      | Android 12+        |

Reference device:

Samsung Galaxy A15

---

# REST API Overview

## Register Worker

```
POST /api/register
```

Registers a new worker.

---

## Heartbeat

```
POST /api/heartbeat
```

Updates worker status.

---

## Device List

```
GET /api/devices
```

Returns every connected worker.

---

## Available Models

```
GET /api/models
```

Lists installed models.

---

## Download Model

```
POST /api/download
```

Transfers a model to a worker.

---

## Inference

```
POST /api/inference
```

Runs a prompt on a selected worker.

---

# Roadmap

| Version | Goal                   | Status         |
| ------- | ---------------------- | -------------- |
| v0.1    | Coordinator Foundation | Complete       |
| v0.2    | Worker Registration    | Complete       |
| v0.3    | Dashboard              | Complete       |
| v0.4    | Chat Interface         | Complete       |
| v0.5    | Model Synchronization  | Complete       |
| v0.6    | Smart Scheduling       | In Development |
| v0.7    | Distributed Inference  | In Development |
| v0.8    | Automatic Discovery    | Planned        |
| v0.9    | Cluster Benchmarking   | Planned        |
| v1.0    | Stable Release         | Planned        |

---

# Performance Goals

Luma AI aims to support:

* 50+ connected workers
* Less than 100 MB RAM for coordinator
* Less than 30 MB RAM per worker
* Local inference over Wi-Fi
* Automatic recovery from disconnects
* Cross-generation Android compatibility

The project prioritizes efficiency over maximum throughput.

---

# Contributing

Contributions of every size are welcome.

You can help by:

* Reporting bugs
* Improving documentation
* Testing on additional Android devices
* Implementing new schedulers
* Optimizing performance
* Designing interfaces
* Writing tutorials

Development workflow:

```bash
git checkout -b feature/my-feature

git commit -m "Implement feature"

git push origin feature/my-feature
```

Then open a Pull Request.

---

# Development Guidelines

The project follows several core principles.

* Keep dependencies lightweight.
* Prefer readability over complexity.
* Prioritize compatibility with older hardware.
* Document every public API.
* Write modular code.
* Benchmark performance before optimization.

Every contribution should move the project toward making AI more accessible.

---

# License

This project is licensed under the MIT License.

See the `LICENSE` file for more information.

---

# Acknowledgments

Luma AI would not be possible without the work of the open-source community.

Special thanks to:

* llama.cpp
* FastAPI
* Termux
* Python
* F-Droid
* Every contributor, tester, and early adopter

---

# The Luma Philosophy

Luma AI is more than another AI framework.

It is an experiment in sustainable computing.

Instead of asking users to buy more powerful hardware, it asks a different question:

**"What if the hardware you already own is enough?"**

By transforming forgotten Android devices into distributed AI workers, Luma AI demonstrates that innovation is not always about acquiring more computing power—it is often about using existing resources more intelligently.

The long-term objective is to build a complete distributed AI ecosystem that anyone can run at home, in schools, makerspaces, or small businesses without specialized hardware.

Old devices deserve a second life.

Luma AI gives them one.

Made with ♥️ by Princeflouz :)
