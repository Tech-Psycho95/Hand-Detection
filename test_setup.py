"""
Test script to verify all dependencies are installed correctly
Run this before running the main hand_detector script
"""

import sys
from pathlib import Path

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing Python dependencies...\n")
    
    packages = {
        "cv2": "opencv-python",
        "mediapipe": "mediapipe",
        "playsound": "playsound",
    }
    
    missing = []
    
    for module_name, package_name in packages.items():
        try:
            __import__(module_name)
            print(f"✓ {module_name} ({package_name})")
        except ImportError:
            print(f"✗ {module_name} ({package_name}) - NOT INSTALLED")
            missing.append(package_name)
    
    return missing


def test_camera():
    """Test if camera is accessible"""
    print("\n" + "="*50)
    print("Testing camera access...\n")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✓ Camera is accessible")
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            fps = cap.get(cv2.CAP_PROP_FPS)
            print(f"  Resolution: {int(width)}x{int(height)}")
            print(f"  FPS: {int(fps)}")
            cap.release()
            return True
        else:
            print("✗ Camera is NOT accessible")
            print("  Check if another application is using the camera")
            return False
    except Exception as e:
        print(f"✗ Camera test failed: {e}")
        return False


def test_audio_file():
    """Test if audio file exists"""
    print("\n" + "="*50)
    print("Testing audio file...\n")
    
    script_dir = Path(__file__).parent
    audio_file = script_dir / "custom_voice.mp3"
    
    if audio_file.exists():
        print(f"✓ Audio file found: {audio_file}")
        print(f"  Size: {audio_file.stat().st_size} bytes")
        return True
    else:
        print(f"✗ Audio file NOT found: {audio_file}")
        print("  Please place 'custom_voice.mp3' in the script directory")
        return False


def test_audio_playback():
    """Test if audio playback works"""
    print("\n" + "="*50)
    print("Testing audio playback...\n")
    
    script_dir = Path(__file__).parent
    audio_file = script_dir / "custom_voice.mp3"
    
    if not audio_file.exists():
        print("✗ Cannot test audio playback - file not found")
        return False
    
    # Try playsound
    try:
        from playsound import playsound
        print("Testing with playsound...")
        playsound(str(audio_file))
        print("✓ Audio playback successful (playsound)")
        return True
    except ImportError:
        print("  playsound not available")
    except Exception as e:
        print(f"  playsound error: {e}")
    
    # Try pygame
    try:
        import pygame
        pygame.mixer.init()
        print("Testing with pygame...")
        sound = pygame.mixer.Sound(str(audio_file))
        sound.play()
        print("✓ Audio playback successful (pygame)")
        return True
    except ImportError:
        print("  pygame not available")
    except Exception as e:
        print(f"  pygame error: {e}")
    
    print("✗ No audio library available")
    return False


def main():
    """Run all tests"""
    print("="*50)
    print("Hand Detection Setup Test")
    print("="*50 + "\n")
    
    # Test imports
    missing = test_imports()
    
    # Test camera
    camera_ok = test_camera()
    
    # Test audio file
    audio_file_ok = test_audio_file()
    
    # Test audio playback
    audio_playback_ok = test_audio_playback()
    
    # Summary
    print("\n" + "="*50)
    print("Test Summary")
    print("="*50)
    
    if missing:
        print(f"\n⚠ Missing packages: {', '.join(missing)}")
        print("\nInstall missing packages with:")
        print(f"  pip install {' '.join(missing)}")
    else:
        print("\n✓ All packages installed")
    
    print(f"{'✓' if camera_ok else '✗'} Camera accessible")
    print(f"{'✓' if audio_file_ok else '✗'} Audio file present")
    print(f"{'✓' if audio_playback_ok else '✗'} Audio playback working")
    
    all_ok = not missing and camera_ok and audio_file_ok
    
    print("\n" + "="*50)
    if all_ok:
        print("✓ Everything looks good! Run:")
        print("  python hand_detector.py")
    else:
        print("⚠ Please fix the issues above before running the detector")
    print("="*50)
    
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
