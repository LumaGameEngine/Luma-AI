# Building llama-cli for 32‑bit ARM (ARMv7)

Luma AI relies on `llama.cpp` for inference. For 32‑bit Android devices (e.g., Tecno Spark Go, ARMv7), you must cross‑compile the binary. This guide walks you through the exact steps we used.

## Prerequisites

- **Ubuntu/Debian** laptop (or any Linux system)
- **Android NDK r26d** (or later)
- **CMake** and **make** installed

## 1. Install the Android NDK

```bash
cd ~
wget https://dl.google.com/android/repository/android-ndk-r26d-linux.zip
unzip android-ndk-r26d-linux.zip
export NDK=~/android-ndk-r26d

Add the NDK toolchain to your PATH:

export PATH=$NDK/toolchains/llvm/prebuilt/linux-x86_64/bin:$PATH

```

## 2. Clone llama.cpp

git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp