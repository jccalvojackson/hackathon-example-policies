#!/usr/bin/env python3
"""
Alternative voice recognition setup for Linux containers.
This approach uses different methods that work better in containerized environments.
"""

import os
import subprocess
import sys


def check_container_environment():
    """Detect if we're running in a container."""
    container_indicators = [
        os.path.exists("/.dockerenv"),
        os.path.exists("/run/.containerenv"),
        os.environ.get("container") is not None,
        "docker"
        in subprocess.check_output(
            ["cat", "/proc/1/cgroup"], text=True, errors="ignore"
        ),
    ]

    if any(container_indicators):
        print("🐳 Container environment detected")
        return True
    else:
        print("🖥️  Native Linux environment detected")
        return False


def install_system_dependencies():
    """Install system dependencies for audio."""
    print("📦 Installing system audio dependencies...")

    commands_to_try = [
        # Debian/Ubuntu
        ["sudo", "apt-get", "update"],
        [
            "sudo",
            "apt-get",
            "install",
            "-y",
            "portaudio19-dev",
            "python3-dev",
            "libasound2-dev",
            "libportaudio2",
            "ffmpeg",
        ],
        # Alternative: try with conda if available
        ["conda", "install", "-c", "conda-forge", "pyaudio", "-y"],
        # Alternative: try with system python
        [
            "pip3",
            "install",
            "--global-option=build_ext",
            "--global-option=-I/usr/local/include",
            "--global-option=-L/usr/local/lib",
            "pyaudio",
        ],
    ]

    for cmd in commands_to_try:
        try:
            print(f"🔧 Trying: {' '.join(cmd)}")
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ Success: {' '.join(cmd)}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"❌ Failed: {' '.join(cmd)} - {e}")
            continue

    return False


def create_alternative_voice_implementation():
    """Create alternative voice recognition that works without PyAudio."""
    alt_voice_code = '''
# Alternative voice recognition implementation for containers
import subprocess
import tempfile
import os
import threading
import time
from pathlib import Path

class ContainerVoiceListener:
    """Voice listener that works in container environments."""
    
    def __init__(self):
        self.recording = False
        
    def record_audio_file(self, duration=3):
        """Record audio to a temporary file using system tools."""
        try:
            # Try different recording methods
            temp_file = tempfile.mktemp(suffix='.wav')
            
            recording_commands = [
                # Try arecord (ALSA)
                ['arecord', '-D', 'default', '-f', 'cd', '-t', 'wav', '-d', str(duration), temp_file],
                # Try ffmpeg
                ['ffmpeg', '-f', 'alsa', '-i', 'default', '-t', str(duration), '-y', temp_file],
                # Try sox
                ['sox', '-d', '-t', 'wav', temp_file, 'trim', '0', str(duration)]
            ]
            
            for cmd in recording_commands:
                try:
                    subprocess.run(cmd, check=True, capture_output=True, timeout=duration+2)
                    if os.path.exists(temp_file) and os.path.getsize(temp_file) > 1000:
                        return temp_file
                except:
                    continue
                    
            return None
            
        except Exception as e:
            print(f"Recording error: {e}")
            return None
    
    def transcribe_audio_file(self, audio_file):
        """Transcribe audio file using speech_recognition without PyAudio."""
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            
            # Load audio file
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
            
            # Try recognition
            try:
                text = recognizer.recognize_google(audio).lower()
                return text
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                # Try offline if available
                try:
                    text = recognizer.recognize_sphinx(audio).lower()
                    return text
                except:
                    return None
                    
        except Exception as e:
            print(f"Transcription error: {e}")
            return None
        finally:
            # Clean up temp file
            if os.path.exists(audio_file):
                os.remove(audio_file)
    
    def listen_for_command(self, target_phrase="next step", duration=3):
        """Listen for a specific command."""
        print(f"🎤 Listening for '{target_phrase}'... ({duration}s)")
        
        audio_file = self.record_audio_file(duration)
        if not audio_file:
            return False
            
        text = self.transcribe_audio_file(audio_file)
        if text:
            print(f"🎤 Heard: '{text}'")
            return target_phrase in text
        
        return False

# Function to replace the original voice_listener
def container_voice_listener(switch_flag):
    """Container-compatible voice listener."""
    listener = ContainerVoiceListener()
    
    print("🐳 Container voice listener started")
    print("🎤 Say 'next step' to switch steps")
    
    while not switch_flag["done"]:
        try:
            if listener.listen_for_command("next step", duration=2):
                if not switch_flag["switched"]:
                    switch_flag["switched"] = True
                    print("\\n🔄 Voice command received! Switching to next step!")
            time.sleep(0.5)  # Brief pause between listening cycles
        except Exception as e:
            print(f"❌ Voice recognition error: {e}")
            time.sleep(1)
'''

    # Write the alternative implementation
    alt_file = (
        Path(__file__).parent.parent
        / "src"
        / "example_policies"
        / "robot_deploy"
        / "container_voice.py"
    )
    alt_file.parent.mkdir(parents=True, exist_ok=True)

    with open(alt_file, "w") as f:
        f.write(alt_voice_code)

    print(f"✅ Alternative voice implementation created: {alt_file}")
    return alt_file


def main():
    print("🐳 CONTAINER VOICE RECOGNITION SETUP")
    print("=" * 50)

    # Check environment
    is_container = check_container_environment()

    # Try to install system dependencies
    if install_system_dependencies():
        print("✅ System dependencies installed successfully")
        print("💡 Try running: uv sync")
    else:
        print("⚠️  System dependencies installation failed")
        print("🔄 Creating alternative implementation...")

        # Create alternative implementation
        alt_file = create_alternative_voice_implementation()

        print("\n📝 ALTERNATIVE SETUP INSTRUCTIONS:")
        print("=" * 40)
        print("1. Install speech_recognition only:")
        print("   pip install speechrecognition")
        print("")
        print("2. Install system recording tools:")
        print("   # Ubuntu/Debian:")
        print("   apt-get install alsa-utils ffmpeg")
        print("   # Or try:")
        print("   apt-get install sox")
        print("")
        print("3. Modify deploy.py to use container voice listener:")
        print(
            f"   from example_policies.robot_deploy.container_voice import container_voice_listener"
        )
        print("   # Replace voice_listener with container_voice_listener")
        print("")
        print("4. Test with:")
        print("   python scripts/test_microphone.py")

    print("\n✨ Container setup completed!")


if __name__ == "__main__":
    main()
