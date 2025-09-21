#!/usr/bin/env python3
"""
Container-specific microphone test that doesn't require direct audio device access.
This script tests the container-compatible voice recognition approach.
"""

import os
import subprocess
import tempfile
import time
import sys

def test_container_environment():
    """Check if we're in a container and detect the issue."""
    print("🐳 CONTAINER MICROPHONE TEST")
    print("=" * 50)
    
    # Check for container indicators
    container_indicators = [
        os.path.exists('/.dockerenv'),
        os.path.exists('/run/.containerenv'),
        os.environ.get('container') is not None,
    ]
    
    if any(container_indicators):
        print("✅ Container environment detected")
    else:
        print("🖥️  Native Linux environment detected")
    
    # Check for audio device access
    try:
        result = subprocess.run(['ls', '/dev/snd/'], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            print("✅ Audio devices found in /dev/snd/:")
            print(f"   {result.stdout.strip()}")
            return "devices_available"
        else:
            print("❌ No audio devices found in /dev/snd/")
            return "no_devices"
    except:
        print("❌ Cannot access /dev/snd/ directory")
        return "no_access"

def test_recording_tools():
    """Test if recording tools are available."""
    print("\n🔧 Testing audio recording tools...")
    
    tools = {
        'arecord': ['arecord', '--version'],
        'ffmpeg': ['ffmpeg', '-version'],
        'sox': ['sox', '--version']
    }
    
    available_tools = []
    
    for tool_name, cmd in tools.items():
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=5)
            if result.returncode == 0:
                print(f"✅ {tool_name} is available")
                available_tools.append(tool_name)
            else:
                print(f"❌ {tool_name} not working")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print(f"❌ {tool_name} not installed")
    
    return available_tools

def test_mock_recording():
    """Test the container recording approach with a mock audio file."""
    print("\n🎤 Testing container voice recognition approach...")
    
    try:
        import speech_recognition as sr
        print("✅ speech_recognition library available")
        
        # Create a temporary mock audio file (silence)
        print("🔧 Creating test audio file...")
        temp_file = tempfile.mktemp(suffix='.wav')
        
        # Try to create a silent WAV file using ffmpeg
        try:
            cmd = [
                'ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=duration=2',
                '-ar', '44100', '-ac', '1', '-y', temp_file
            ]
            subprocess.run(cmd, check=True, capture_output=True, timeout=10)
            
            if os.path.exists(temp_file) and os.path.getsize(temp_file) > 1000:
                print("✅ Test audio file created successfully")
                
                # Test speech recognition on the file
                recognizer = sr.Recognizer()
                try:
                    with sr.AudioFile(temp_file) as source:
                        audio = recognizer.record(source)
                    print("✅ Audio file loaded into speech recognizer")
                    
                    # Try recognition (will fail on silence, but tests the pipeline)
                    try:
                        text = recognizer.recognize_google(audio)
                        print(f"✅ Recognition successful: {text}")
                    except sr.UnknownValueError:
                        print("✅ Recognition pipeline working (no speech in test file)")
                    except sr.RequestError as e:
                        print(f"⚠️  Network recognition failed: {e}")
                        print("💡 This is normal if no internet access")
                    
                    return True
                    
                except Exception as e:
                    print(f"❌ Audio file processing failed: {e}")
                    return False
            else:
                print("❌ Test audio file creation failed")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ ffmpeg test failed: {e}")
            return False
            
    except ImportError:
        print("❌ speech_recognition not available")
        return False
    
    finally:
        # Clean up
        if 'temp_file' in locals() and os.path.exists(temp_file):
            os.remove(temp_file)

def provide_container_solutions():
    """Provide solutions for container audio issues."""
    print("\n" + "=" * 50)
    print("🔧 CONTAINER AUDIO SOLUTIONS")
    print("=" * 50)
    
    print("\n🐳 For Docker containers:")
    print("   docker run --device /dev/snd:/dev/snd your-container")
    print("   # OR")
    print("   docker run --privileged your-container")
    
    print("\n🏗️  For other container systems:")
    print("   - Ensure audio device mapping")
    print("   - Check container documentation for audio support")
    print("   - Consider host network mode")
    
    print("\n🎤 Alternative: External microphone setup:")
    print("   1. Use a USB microphone on the host")
    print("   2. Stream audio to container via network")
    print("   3. Use host-based voice recognition with API")
    
    print("\n💡 For development/testing:")
    print("   - The robot deployment will still work!")
    print("   - It will automatically use container-compatible mode")
    print("   - Consider testing on the actual deployment environment")

def main():
    """Run container-specific microphone tests."""
    
    # Test 1: Environment detection
    env_status = test_container_environment()
    
    # Test 2: Recording tools
    available_tools = test_recording_tools()
    
    # Test 3: Container recording approach
    recording_works = test_mock_recording()
    
    # Results summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    if env_status == "no_devices" or env_status == "no_access":
        print("🐳 CONTAINER AUDIO ISSUE DETECTED")
        print("   → Your container doesn't have access to audio devices")
        print("   → This is normal for most container setups")
        print("")
        
        if available_tools:
            print(f"✅ Recording tools available: {', '.join(available_tools)}")
        else:
            print("❌ No recording tools available")
            print("   → Run: sudo apt-get install alsa-utils ffmpeg")
        
        if recording_works:
            print("✅ Container voice recognition pipeline working")
            print("   → The robot deployment will work in container mode")
        else:
            print("❌ Container voice recognition needs setup")
        
        provide_container_solutions()
        
    else:
        print("✅ Audio devices seem to be available")
        print("   → You might be able to use regular PyAudio mode")
        print("   → Try running the regular test: python scripts/test_microphone.py")
    
    print("\n🚀 NEXT STEPS FOR ROBOT DEPLOYMENT:")
    print("1. The robot deployment script will automatically detect container mode")
    print("2. It will use file-based audio recording instead of direct microphone access")
    print("3. Just run: python scripts/03_deploy_policy.py")
    print("4. Say 'next step' - the system will handle container compatibility!")
    
    print("\n✨ Container compatibility test completed!")

if __name__ == "__main__":
    main()
