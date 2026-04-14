# Hand Detection with OpenCV & Mediapipe

A Python application that detects hand presence using your webcam and plays audio alerts when hands are detected.

## Features

- **Real-time Hand Detection**: Uses Google's Mediapipe for fast, accurate hand detection
- **Visual Feedback**: Displays hand landmarks (joints and connections) on the video feed
- **Audio Alerts**: Plays a custom audio file when a hand is detected
- **Clean Interface**: Shows detection status and instructions on screen
- **Cooldown System**: Prevents audio spam with intelligent cooldown

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install opencv-python mediapipe playsound
```

### 2. Prepare Your Audio File

Place your custom audio file in the same directory as the script:
- **Filename**: `custom_voice.mp3`
- **Location**: Same folder as `hand_detector.py`
- **Supported formats**: MP3, WAV, OGG, etc. (depends on what playsound/pygame supports)

You can use any audio file. Example sources:
- Download from free sound libraries (Freesound.org, Zapsplat)
- Generate using text-to-speech tools
- Record your own voice

### 3. Run the Script

```bash
python hand_detector.py
```

## Usage

Once the script is running:

1. Allow camera access when prompted
2. Position your hand in front of the webcam
3. When a hand is detected:
   - The status text will change to "Hand Detected!" (green)
   - Your custom audio file will play
4. Press **`q`** to exit the program

## Configuration

Edit the `hand_detector.py` script to customize:

### Change Detection Confidence
```python
detector = HandDetector(
    audio_file=str(audio_file),
    detection_confidence=0.7  # 0-1, higher = stricter
)
```

### Use Different Camera
```python
detector.run(camera_id=1)  # Use camera index 1 instead of 0
```

### Change Audio File Path
```python
audio_file = script_dir / "my_custom_sound.wav"
detector = HandDetector(audio_file=str(audio_file))
```

## Audio Library Options

The script automatically tries to use the best available audio library:

1. **playsound** (recommended): Lightweight, simple
2. **pygame.mixer**: More features, slightly heavier

If neither is installed, the script will run without audio (you'll see a warning).

To install pygame instead:
```bash
pip install pygame
```

## Troubleshooting

### Camera Not Working
- Check if another application is using the camera
- Try changing `camera_id` from 0 to 1, 2, etc.
- Verify camera permissions in your OS settings

### Audio Not Playing
- Ensure `custom_voice.mp3` exists in the script directory
- Check that the audio file format is supported
- Verify audio libraries are installed: `pip install playsound`
- Check system volume settings

### Slow Performance
- Reduce `Frame_width` and `frame_height` in the code
- Lower the FPS value
- Decrease detection confidence threshold

### Hand Detection Not Working Well
- Ensure good lighting
- Keep hand fully or mostly visible in frame
- Adjust `detection_confidence` parameter (lower = more sensitive)

## Project Structure

```
hand detector/
├── hand_detector.py      # Main script
├── custom_voice.mp3      # Your audio file (add this)
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Performance Tips

- **GPU Support**: Install `opencv-python-headless` and configure GPU support if available
- **Multi-threading**: For better responsiveness, consider threading audio playback
- **Resolution**: Reduce camera resolution for faster processing on slower machines

## License

Free to use and modify for personal and commercial projects.

## Notes

- The script flips the video feed for a mirror effect (natural selfie view)
- Hand detection runs on both CPU and GPU, automatically selecting the best available
- Cooldown system prevents rapid audio playback (every ~0.5 seconds minimum)
