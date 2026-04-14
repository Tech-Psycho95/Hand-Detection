"""
Configuration file for hand_detector.py
Modify these settings to customize behavior
"""

# Camera Settings
CAMERA_ID = 0  # Default camera (0 is usually built-in webcam)
FRAME_WIDTH = 1280  # Camera frame width
FRAME_HEIGHT = 720  # Camera frame height
FPS = 30  # Target frames per second

# Hand Detection Settings
DETECTION_CONFIDENCE = 0.5  # 0-1, higher = more strict (fewer false positives)
TRACKING_CONFIDENCE = 0.5  # Confidence for tracking already detected hands
MAX_NUM_HANDS = 2  # Maximum hands to detect simultaneously

# Audio Settings
AUDIO_FILE = "custom_voice.mp3"  # Path to audio file (relative to script location)
AUDIO_COOLDOWN_FRAMES = 15  # Frames to wait before playing sound again (prevents spam)
ENABLE_AUDIO = True  # Set to False to disable audio

# Visual Settings
LANDMARK_COLOR = (0, 255, 0)  # BGR color for hand joints (Green)
CONNECTION_COLOR = (255, 0, 0)  # BGR color for hand connections (Blue)
LANDMARK_THICKNESS = 2
CONNECTION_THICKNESS = 2
LANDMARK_RADIUS = 2

# Text Display Settings
STATUS_TEXT_SIZE = 1.0  # Font size for status text
STATUS_TEXT_COLOR = (0, 255, 0)  # Color when hand detected (Green)
STATUS_TEXT_COLOR_NO_HAND = (0, 0, 255)  # Color when no hand (Red)

# Exit Key
EXIT_KEY = 'q'  # Press this key to exit

# Debug Settings
VERBOSE = True  # Print detection info to console
SHOW_FPS = False  # Display FPS on screen (requires additional code)
