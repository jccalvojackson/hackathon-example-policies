# 🐳 Container Voice Recognition Setup

This guide helps you set up voice recognition for robot control in Linux containers.

## 🚀 Quick Setup (Recommended)

Run this **on your Linux container**:

```bash
# 1. Quick audio setup with sudo
bash scripts/quick_container_setup.sh

# 2. Install Python dependencies
uv sync

# 3. Test microphone
python scripts/test_microphone.py

# 4. Deploy with voice control
python scripts/03_deploy_policy.py
```

## 🔧 Manual Setup

If the quick setup doesn't work:

### Option 1: Full PyAudio Installation
```bash
# Install system dependencies
bash scripts/install_audio_deps.sh

# Install Python packages including PyAudio
uv sync --group audio
```

### Option 2: Container-Compatible Mode (No PyAudio)
```bash
# Install only basic recording tools
sudo apt-get update
sudo apt-get install -y alsa-utils ffmpeg

# Install Python dependencies (without PyAudio)
uv sync

# The system will automatically use container mode
```

## 🎤 How Voice Control Works

1. **Say "next step"** → Robot progresses through task phases
2. **Automatic fallback** → Uses container mode if PyAudio fails
3. **Multiple recording tools** → Tries `arecord`, `ffmpeg`, `sox`
4. **Online + Offline** → Google Speech Recognition + Sphinx backup

## 🐛 Troubleshooting

### Permission Errors
```bash
# Make sure you have sudo access
sudo apt-get update
```

### Audio Recording Issues
```bash
# Check if recording tools are installed
which arecord ffmpeg sox

# Test manual recording (should create a wav file)
arecord -D default -f cd -t wav -d 2 test.wav
```

### Network Issues
- Online recognition requires internet for Google Speech API
- Offline recognition (Sphinx) works without internet
- System automatically tries both methods

### Container-Specific Issues
- Make sure container has access to host audio devices
- Some containers need `--device /dev/snd` flag
- Check container documentation for audio device mapping

## 📝 Files Created

- `scripts/quick_container_setup.sh` - Fast setup script
- `scripts/install_audio_deps.sh` - Full system dependencies
- `scripts/container_voice_setup.py` - Advanced setup helper  
- `scripts/test_microphone.py` - Test voice recognition

## ✨ Ready to Deploy!

Once setup is complete, just run:
```bash
python scripts/03_deploy_policy.py
```

Then say **"next step"** to control your robot! 🤖🎤
