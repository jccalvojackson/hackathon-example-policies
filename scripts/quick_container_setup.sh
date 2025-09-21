#!/bin/bash
# Quick setup script for Linux containers with sudo access

echo "🐳 Quick Container Audio Setup"
echo "==============================="

# Update package lists
echo "📦 Updating package lists..."
sudo apt-get update

# Install essential audio dependencies
echo "🎤 Installing audio recording tools..."
sudo apt-get install -y alsa-utils ffmpeg

# Install PyAudio dependencies (optional - may fail, that's okay)
echo "🔊 Installing PyAudio dependencies (optional)..."
sudo apt-get install -y \
    portaudio19-dev \
    python3-dev \
    libasound2-dev \
    libportaudio2 \
    libportaudiocpp0 || echo "⚠️  PyAudio deps failed (using fallback mode)"

echo "✅ Container setup completed!"
echo ""
echo "🚀 Next steps:"
echo "1. Install Python dependencies: uv sync"
echo "2. Test microphone: python scripts/test_microphone.py"
echo "3. Run deployment: python scripts/03_deploy_policy.py"
echo ""
echo "💡 The system will automatically use container-compatible voice recognition"
echo "   if PyAudio is not available. Just say 'next step' to control the robot!"
