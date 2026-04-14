"""
Hand Detection with Mediapipe and OpenCV (Advanced Version)
Uses config.py for easy customization
"""

import cv2
import mediapipe as mp
import os
import sys
from pathlib import Path
from config import *  # Import all settings from config.py

try:
    from playsound import playsound
    AUDIO_LIBRARY = "playsound"
except ImportError:
    try:
        import pygame
        pygame.mixer.init()
        AUDIO_LIBRARY = "pygame"
    except ImportError:
        print("Warning: No audio library found. Install with:")
        print("  pip install playsound  OR  pip install pygame")
        AUDIO_LIBRARY = None


class HandDetector:
    """Hand detection and visualization using Mediapipe"""
    
    def __init__(self, audio_file=AUDIO_FILE, detection_confidence=DETECTION_CONFIDENCE):
        """Initialize the hand detector with configuration settings"""
        
        # Initialize Mediapipe
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=MAX_NUM_HANDS,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=TRACKING_CONFIDENCE
        )
        
        # Audio setup
        script_dir = Path(__file__).parent
        self.audio_file = script_dir / audio_file if not os.path.isabs(audio_file) else audio_file
        self.audio_playing = False
        self.last_hand_detected = False
        self.detection_cooldown = 0
        self.enable_audio = ENABLE_AUDIO
        
        if VERBOSE:
            print(f"Hand Detector initialized")
            print(f"  Detection confidence: {detection_confidence}")
            print(f"  Max hands: {MAX_NUM_HANDS}")
            print(f"  Audio enabled: {ENABLE_AUDIO}")
            if ENABLE_AUDIO:
                print(f"  Audio file: {self.audio_file}")
    
    def play_sound(self):
        """Play the audio alert when hand is detected"""
        if not self.enable_audio or not self.audio_file or not AUDIO_LIBRARY:
            return
        
        if self.detection_cooldown > 0:
            self.detection_cooldown -= 1
            return
        
        if not os.path.exists(self.audio_file):
            if VERBOSE:
                print(f"Warning: Audio file not found: {self.audio_file}")
            return
        
        try:
            if AUDIO_LIBRARY == "playsound":
                playsound(str(self.audio_file))
            elif AUDIO_LIBRARY == "pygame":
                sound = pygame.mixer.Sound(str(self.audio_file))
                sound.play()
            
            self.detection_cooldown = AUDIO_COOLDOWN_FRAMES
            if VERBOSE:
                print("Hand detected - Audio played!")
        except Exception as e:
            print(f"Error playing audio: {e}")
    
    def detect_hands(self, frame):
        """Detect hands in frame and return results"""
        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        hand_detected = False
        
        if results.multi_hand_landmarks and results.multi_handedness:
            hand_detected = True
            
            # Draw landmarks for each detected hand
            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks, results.multi_handedness
            ):
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(
                        color=LANDMARK_COLOR,
                        thickness=LANDMARK_THICKNESS,
                        circle_radius=LANDMARK_RADIUS
                    ),
                    self.mp_drawing.DrawingSpec(
                        color=CONNECTION_COLOR,
                        thickness=CONNECTION_THICKNESS
                    )
                )
                
                # Show which hand (Left/Right)
                if VERBOSE:
                    hand_label = handedness.classification[0].label
                    confidence = handedness.classification[0].score
                    cv2.putText(
                        frame,
                        f"{hand_label} ({confidence:.2f})",
                        (int(hand_landmarks.landmark[0].x * w) + 10,
                         int(hand_landmarks.landmark[0].y * h) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (200, 200, 0),
                        2
                    )
            
            # Play sound when hand is first detected
            if not self.last_hand_detected:
                self.play_sound()
        
        self.last_hand_detected = hand_detected
        
        # Status display
        status = "Hand Detected!" if hand_detected else "No hand detected"
        color = STATUS_TEXT_COLOR if hand_detected else STATUS_TEXT_COLOR_NO_HAND
        cv2.putText(
            frame,
            status,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            STATUS_TEXT_SIZE,
            color,
            2
        )
        
        # Exit instruction
        cv2.putText(
            frame,
            f"Press '{EXIT_KEY}' to exit",
            (10, h - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (200, 200, 200),
            1
        )
        
        return frame, hand_detected
    
    def run(self, camera_id=CAMERA_ID):
        """Run the hand detection with webcam feed"""
        
        cap = cv2.VideoCapture(camera_id)
        
        if not cap.isOpened():
            print(f"Error: Could not open camera {camera_id}")
            return
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        cap.set(cv2.CAP_PROP_FPS, FPS)
        
        if VERBOSE:
            print("\n" + "="*50)
            print("Hand Detector Started")
            print(f"Audio library: {AUDIO_LIBRARY if AUDIO_LIBRARY else 'None'}")
            print(f"Camera ID: {camera_id}")
            print(f"Resolution: {int(FRAME_WIDTH)}x{int(FRAME_HEIGHT)}")
            print(f"Press '{EXIT_KEY.upper()}' to exit")
            print("="*50 + "\n")
        
        try:
            frame_count = 0
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    print("Error: Failed to read frame from camera")
                    break
                
                processed_frame, hand_detected = self.detect_hands(frame)
                cv2.imshow("Hand Detection", processed_frame)
                
                frame_count += 1
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord(EXIT_KEY):
                    if VERBOSE:
                        print(f"\nExiting... (processed {frame_count} frames)")
                    break
        
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        
        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.hands.close()
            if VERBOSE:
                print("Camera released. Goodbye!")


def main():
    """Main entry point"""
    detector = HandDetector()
    detector.run()


if __name__ == "__main__":
    main()
