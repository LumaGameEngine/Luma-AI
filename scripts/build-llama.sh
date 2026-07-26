#!/bin/bash
set -e
echo "Building llama-cli for ARMv7 (32-bit)..."

# Install NDK if missing
if [ ! -d "$HOME/android-ndk-r26d" ]; then
    echo "Downloading Android NDK r26d..."
    wget -q https://dl.google.com/android/repository/android-ndk-r26d-linux.zip -O /tmp/ndk.zip
    unzip -q /tmp/ndk.zip -d $HOME
    rm /tmp/ndk.zip
fi
export NDK=$HOME/android-ndk-r26d

# Clone llama.cpp if missing
if [ ! -d "llama.cpp" ]; then
    git clone https://github.com/ggerganov/llama.cpp
fi
cd llama.cpp
mkdir -p build-cross && cd build-cross

cmake .. \
  -DCMAKE_TOOLCHAIN_FILE=$NDK/build/cmake/android.toolchain.cmake \
  -DANDROID_ABI=armeabi-v7a \
  -DANDROID_PLATFORM=android-21 \
  -DCMAKE_BUILD_TYPE=Release \
  -DLLAMA_BUILD_SERVER=OFF \
  -DLLAMA_BUILD_TESTS=OFF \
  -DLLAMA_BUILD_EXAMPLES=ON \
  -DGGML_LLAMAFILE=OFF \
  -DGGML_ACCELERATE=OFF \
  -DGGML_NEON=ON \
  -DGGML_AVX2=OFF \
  -DGGML_AVX=OFF \
  -DGGML_FMA=OFF \
  -DGGML_OPENMP=OFF

make llama-cli -j2
cp bin/llama-cli ../../worker/llama-cli
echo "Binary copied to worker/llama-cli"

//make executable: chmod +x scripts/build-llama.sh