#!/bin/bash
# Container Audio Configuration Helper

echo "🐳 CONTAINER AUDIO CONFIGURATION HELPER"
echo "========================================="

# Check if we're in a container
if [ -f /.dockerenv ] || [ -f /run/.containerenv ] || [ -n "$container" ]; then
    echo "✅ Container environment detected"
else
    echo "🖥️  Not running in a container"
fi

# Check for audio devices
echo ""
echo "🔍 Checking audio device access..."

if [ -d "/dev/snd" ]; then
    audio_devices=$(ls /dev/snd 2>/dev/null | wc -l)
    if [ "$audio_devices" -gt 0 ]; then
        echo "✅ Found $audio_devices audio device(s):"
        ls -la /dev/snd/
    else
        echo "❌ /dev/snd exists but is empty"
    fi
else
    echo "❌ /dev/snd directory not found"
fi

# Check ALSA configuration
echo ""
echo "🔧 Checking ALSA configuration..."
if command -v aplay &> /dev/null; then
    echo "📋 Available audio devices:"
    aplay -l 2>/dev/null || echo "❌ No audio devices found by ALSA"
else
    echo "❌ aplay not installed"
fi

# Provide specific solutions
echo ""
echo "🛠️  CONTAINER AUDIO SOLUTIONS"
echo "================================"

echo ""
echo "🐳 For Docker containers, restart with:"
echo "   # Option 1: Map audio devices"
echo "   docker run --device /dev/snd:/dev/snd your-container"
echo ""
echo "   # Option 2: Privileged mode (less secure)"
echo "   docker run --privileged your-container"
echo ""
echo "   # Option 3: Specific audio device mapping"
echo "   docker run --device /dev/snd/controlC0 --device /dev/snd/pcmC0D0c your-container"

echo ""
echo "🏗️  For Kubernetes/other orchestrators:"
echo "   # Add to your pod spec:"
echo "   securityContext:"
echo "     privileged: true"
echo "   # OR mount audio devices as volumes"

echo ""
echo "⚡ IMMEDIATE WORKAROUND (without container restart):"
echo "   1. Install recording tools:"
echo "      sudo apt-get update && sudo apt-get install -y alsa-utils ffmpeg"
echo ""
echo "   2. Use container-compatible test:"
echo "      python scripts/test_container_microphone.py"
echo ""
echo "   3. Deploy robot control (will auto-use container mode):"
echo "      python scripts/03_deploy_policy.py"

echo ""
echo "🎤 ALTERNATIVE: Host-based audio setup:"
echo "   1. Run voice recognition on host machine"
echo "   2. Send commands to container via network/IPC"
echo "   3. Use external microphone service"

# Test if basic recording works
echo ""
echo "🧪 Quick recording test..."
if command -v arecord &> /dev/null; then
    echo "⏱️  Testing 1-second recording..."
    if timeout 2s arecord -D default -f cd -t wav -d 1 /tmp/test.wav 2>/dev/null; then
        if [ -f /tmp/test.wav ] && [ -s /tmp/test.wav ]; then
            echo "✅ Basic recording works!"
            rm -f /tmp/test.wav
        else
            echo "❌ Recording produced empty file"
        fi
    else
        echo "❌ Recording failed - no audio device access"
    fi
else
    echo "❌ arecord not available - install with: sudo apt-get install alsa-utils"
fi

echo ""
echo "✨ Configuration check completed!"
echo ""
echo "💡 RECOMMENDED NEXT STEPS:"
echo "   → If recording failed: Use the container restart options above"
echo "   → If you can't restart: The robot deployment will still work!"
echo "   → Test with: python scripts/test_container_microphone.py"
