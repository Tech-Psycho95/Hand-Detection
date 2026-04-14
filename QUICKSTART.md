# Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies
Run this command in the project directory:
```bash
pip install -r requirements.txt
```

**Or on Windows**, double-click `setup.bat`

### Step 2: Add Audio File
1. Find or create an audio file (MP3, WAV, etc.)
2. Rename it to `custom_voice.mp3`
3. Place it in the same folder as `hand_detector.py`

### Step 3: Verify Setup (Optional)
```bash
python test_setup.py
```

This checks if everything is installed and working correctly.

### Step 4: Run!
```bash
python hand_detector.py
```

## Basic Usage

- **Show your hand** → Audio plays ✓
- **Press 'q'** → Exit program

---

## Which Version to Use?

### `hand_detector.py` (Simple)
- Easiest to understand
- Hardcoded settings
- Good for getting started quickly
- **Recommended for beginners**

### `hand_detector_advanced.py` (Customizable)
- Uses `config.py` for settings
- Easy to customize without editing code
- Better for production use
- **Recommended for customization**

---

## Customization Examples

### Change Detection Sensitivity
**Edit `config.py`:**
```python
DETECTION_CONFIDENCE = 0.7  # Higher = stricter detection
```

### Use Different Audio File
**Edit `config.py`:**
```python
AUDIO_FILE = "my_alarm.mp3"
```

### Disable Audio
**Edit `config.py`:**
```python
ENABLE_AUDIO = False
```

### Use Different Camera
**Edit `config.py`:**
```python
CAMERA_ID = 1  # Try 1, 2, 3... if 0 doesn't work
```

---

## Troubleshooting

### Camera not working?
- Check if Zoom/Skype/etc are using it
- Try changing `CAMERA_ID` in config.py (0 → 1 → 2...)
- Run `python test_setup.py` to diagnose

### No audio?
- Make sure `custom_voice.mp3` exists
- Run `python test_setup.py` to test audio
- Check system volume

### Hand detection not working?
- Ensure good lighting
- Keep hand visible in frame
- Lower `DETECTION_CONFIDENCE` in config.py

---

## Next Steps

- Modify `config.py` for your needs
- Add additional hand gesture recognition
- Integrate with other applications
- Process detected hands (e.g., track movement)

---

## Need Help?

1. Run `python test_setup.py` to check your setup
2. Read `README.md` for detailed information
3. Check the config comments in `config.py`
