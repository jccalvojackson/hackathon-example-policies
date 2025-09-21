#!/usr/bin/env python3
"""
Test script to verify microphone and speech recognition functionality.
This script tests the voice recognition setup used in the robot deployment system.
"""

import time
import sys
from typing import Optional

def test_imports() -> bool:
    """Test if required libraries are installed."""
    print("🔍 Testing imports...")
    try:
        import speech_recognition as sr
        import pyaudio
        print("✅ speech_recognition and pyaudio imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Run 'uv sync' to install missing dependencies")
        return False

def test_microphone_access() -> Optional[object]:
    """Test microphone access and list available devices."""
    try:
        import speech_recognition as sr
        
        print("\n🎤 Testing microphone access...")
        
        # List available microphones
        print("📋 Available microphones:")
        try:
            mic_list = sr.Microphone.list_microphone_names()
            if not mic_list:
                print("  (No microphones found)")
            else:
                for i, name in enumerate(mic_list):
                    print(f"  {i}: {name}")
        except Exception as e:
            print(f"  ❌ Could not list microphones: {e}")
        
        # Test default microphone
        mic = sr.Microphone()
        print(f"✅ Default microphone initialized: {mic.device_index}")
        return mic
        
    except Exception as e:
        print(f"❌ Microphone access error: {e}")
        
        # Check if this looks like a container issue
        import os
        if not os.path.exists('/dev/snd') or not os.listdir('/dev/snd'):
            print("\n🐳 CONTAINER AUDIO ISSUE DETECTED!")
            print("   → Your container doesn't have access to audio devices")
            print("   → This is very common in containerized environments")
            print("\n💡 SOLUTIONS:")
            print("   1. Run container-specific test: python scripts/test_container_microphone.py")
            print("   2. Check audio config: bash scripts/container_audio_helper.sh") 
            print("   3. Or restart container with audio access:")
            print("      docker run --device /dev/snd:/dev/snd your-container")
            print("\n✅ The robot deployment will still work!")
            print("   → It automatically uses container-compatible mode")
            print("   → Just run: python scripts/03_deploy_policy.py")
        
        return None

def test_ambient_noise_calibration(mic) -> Optional[object]:
    """Test ambient noise calibration."""
    try:
        import speech_recognition as sr
        
        print("\n🔧 Testing ambient noise calibration...")
        recognizer = sr.Recognizer()
        
        print("🔇 Please be quiet for 2 seconds for calibration...")
        time.sleep(1)  # Give user time to read
        
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=2)
        
        print("✅ Ambient noise calibration completed")
        print(f"📊 Energy threshold: {recognizer.energy_threshold}")
        return recognizer
        
    except Exception as e:
        print(f"❌ Calibration error: {e}")
        return None

def test_audio_input(recognizer, mic) -> bool:
    """Test basic audio input without recognition."""
    try:
        import speech_recognition as sr
        
        print("\n🎵 Testing audio input...")
        print("🗣️  Say something (you have 3 seconds)...")
        
        with mic as source:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
        
        print("✅ Audio captured successfully")
        print(f"📏 Audio data length: {len(audio.get_raw_data())} bytes")
        return True
        
    except sr.WaitTimeoutError:
        print("⏰ No speech detected within timeout")
        return False
    except Exception as e:
        print(f"❌ Audio input error: {e}")
        return False

def test_speech_recognition(recognizer, mic) -> bool:
    """Test speech recognition with different engines."""
    try:
        import speech_recognition as sr
        
        print("\n🧠 Testing speech recognition...")
        print("🗣️  Say 'next step' (you have 5 seconds)...")
        
        with mic as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        
        # Test Google Speech Recognition (online)
        try:
            print("🌐 Trying Google Speech Recognition...")
            text = recognizer.recognize_google(audio).lower()
            print(f"✅ Google recognized: '{text}'")
            
            if "next step" in text:
                print("🎉 SUCCESS: 'next step' command recognized!")
                return True
            else:
                print("⚠️  Command recognized but not 'next step'")
                
        except sr.UnknownValueError:
            print("❓ Google couldn't understand the audio")
        except sr.RequestError as e:
            print(f"🌐 Google Speech Recognition service error: {e}")
            print("💡 Check your internet connection")
        
        # Test offline recognition (Sphinx) as fallback
        try:
            print("💻 Trying offline recognition (Sphinx)...")
            text = recognizer.recognize_sphinx(audio).lower()
            print(f"✅ Sphinx recognized: '{text}'")
            
            if "next step" in text:
                print("🎉 SUCCESS: 'next step' command recognized offline!")
                return True
            else:
                print("⚠️  Command recognized but not 'next step'")
                
        except sr.UnknownValueError:
            print("❓ Sphinx couldn't understand the audio")
        except sr.RequestError as e:
            print(f"💻 Sphinx error: {e}")
            print("💡 Sphinx may not be installed - this is optional")
        
        return False
        
    except sr.WaitTimeoutError:
        print("⏰ No speech detected within timeout")
        return False
    except Exception as e:
        print(f"❌ Speech recognition error: {e}")
        return False

def run_interactive_test(recognizer, mic) -> None:
    """Run an interactive test loop."""
    import speech_recognition as sr
    
    print("\n🔄 Interactive test mode")
    print("🗣️  Say 'next step' to test command recognition")
    print("📝 Say 'quit' or 'stop' to exit")
    print("⏰ Press Ctrl+C to force quit")
    
    try:
        while True:
            try:
                print("\n👂 Listening...")
                with mic as source:
                    audio = recognizer.listen(source, timeout=2, phrase_time_limit=4)
                
                try:
                    text = recognizer.recognize_google(audio).lower()
                    print(f"🎤 Heard: '{text}'")
                    
                    if "next step" in text:
                        print("🎉 COMMAND RECOGNIZED: Next step!")
                    elif "quit" in text or "stop" in text:
                        print("👋 Stopping interactive test...")
                        break
                        
                except sr.UnknownValueError:
                    print("❓ Could not understand audio")
                except sr.RequestError:
                    print("🌐 Network error - trying offline...")
                    try:
                        text = recognizer.recognize_sphinx(audio).lower()
                        print(f"🎤 Heard (offline): '{text}'")
                        if "next step" in text:
                            print("🎉 COMMAND RECOGNIZED: Next step!")
                    except:
                        print("❓ Offline recognition also failed")
                        
            except sr.WaitTimeoutError:
                print("⏰ Listening... (no speech detected)")
            except KeyboardInterrupt:
                print("\n👋 Test interrupted by user")
                break
                
    except Exception as e:
        print(f"❌ Interactive test error: {e}")

def main():
    """Main test function."""
    print("🎤 MICROPHONE & SPEECH RECOGNITION TEST")
    print("=" * 50)
    
    # Test 1: Imports
    if not test_imports():
        sys.exit(1)
    
    # Test 2: Microphone access
    mic = test_microphone_access()
    if mic is None:
        print("\n❌ Cannot proceed without microphone access")
        sys.exit(1)
    
    # Test 3: Ambient noise calibration
    recognizer = test_ambient_noise_calibration(mic)
    if recognizer is None:
        print("\n❌ Cannot proceed without speech recognizer")
        sys.exit(1)
    
    # Test 4: Basic audio input
    if not test_audio_input(recognizer, mic):
        print("\n⚠️  Audio input failed - microphone may not be working")
    
    # Test 5: Speech recognition
    print("\n" + "=" * 50)
    print("🧪 MAIN TEST: Voice Command Recognition")
    if test_speech_recognition(recognizer, mic):
        print("\n🎉 SUCCESS: Voice recognition is working!")
        print("✅ Your microphone setup is ready for robot deployment")
    else:
        print("\n⚠️  Voice command recognition needs attention")
        print("💡 Try speaking more clearly or adjusting microphone position")
    
    # Test 6: Interactive mode (optional)
    print("\n" + "=" * 50)
    response = input("🔄 Would you like to run interactive test mode? (y/N): ")
    if response.lower().startswith('y'):
        run_interactive_test(recognizer, mic)
    
    print("\n✨ Test completed!")
    print("💡 If tests passed, you can now use voice control with 03_deploy_policy.py")

if __name__ == "__main__":
    main()
