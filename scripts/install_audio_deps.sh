#!/bin/bash
# Install system dependencies for PyAudio on Linux containers

echo "🐧 Installing system audio dependencies for Linux container..."

# Detect the package manager and install PortAudio
if command -v apt-get &> /dev/null; then
    echo "📦 Using apt-get (Debian/Ubuntu)..."
    sudo apt-get update
    sudo apt-get install -y \
        portaudio19-dev \
        python3-pyaudio \
        libasound2-dev \
        libportaudio2 \
        libportaudiocpp0 \
        ffmpeg
        
elif command -v yum &> /dev/null; then
    echo "📦 Using yum (RHEL/CentOS)..."
    sudo yum install -y \
        portaudio-devel \
        alsa-lib-devel \
        python3-pyaudio \
        ffmpeg
        
elif command -v dnf &> /dev/null; then
    echo "📦 Using dnf (Fedora)..."
    sudo dnf install -y \
        portaudio-devel \
        alsa-lib-devel \
        python3-pyaudio \
        ffmpeg
        
elif command -v pacman &> /dev/null; then
    echo "📦 Using pacman (Arch)..."
    sudo pacman -Sy --noconfirm \
        portaudio \
        python-pyaudio \
        alsa-lib \
        ffmpeg
        
else
    echo "❌ Could not detect package manager"
    echo "💡 Please install PortAudio manually for your distribution"
    exit 1
fi

echo "✅ System audio dependencies installed!"
echo "💡 Now try: uv sync"
