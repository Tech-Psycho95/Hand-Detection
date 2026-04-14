"""
Hand Detection with Mediapipe and OpenCV
Detects hand presence and plays audio notification
"""

import cv2
import mediapipe as mp
import os
import sys
from pathlib import Path

try:
    import pygame
    pygame.mixer.init()
    AUDIO_LIBRARY = "pygame"
except ImportError:
    try:
        from playsound import playsound
        AUDIO_LIBRARY = "playsound"
    except ImportError:
        print("Warning: No audio library found. Install with:")
        print("  pip install pygame  OR  pip install playsound")
        AUDIO_LIBRARY = None


class HandDetector:
    """Hand detection and visualization using Mediapipe"""
    
    def __init__(self, audio_file="custom_voice.mp3", detection_confidence=0.5):
        """
        Initialize the hand detector
        
        Args:
            audio_file: Path to audio file to play when hand is detected
            detection_confidence: Confidence threshold for hand detection (0-1)
        """
        # Initialize Mediapipe
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=0.5
        )
        
        # Audio setup
        self.audio_file = audio_file
        self.audio_playing = False
        self.last_hand_detected = False
        self.detection_cooldown = 0  # Prevent audio spam
        
        # Validate audio file
        if self.audio_file and not os.path.exists(self.audio_file):
            print(f"Warning: Audio file '{self.audio_file}' not found.")
            print(f"Place your audio file in the script directory and update the path.")
            self.audio_file = None
    
    def play_sound(self):
        """Play the audio alert when hand is detected"""
        if not self.audio_file or not AUDIO_LIBRARY:
            return
        
        # Add cooldown to prevent overlapping audio
        if self.detection_cooldown > 0:
            self.detection_cooldown -= 0.5
            return
        
        try:
            if AUDIO_LIBRARY == "playsound":
                playsound(self.audio_file)
            elif AUDIO_LIBRARY == "pygame":
                sound = pygame.mixer.Sound(self.audio_file)
                sound.play()
            self.detection_cooldown = 30  # Cooldown frames
        except Exception as e:
            print(f"Error playing audio: {e}")
    
    def detect_hands(self, frame):
        """
        Detect hands in the frame and return processing results
        
        Args:
            frame: OpenCV frame from camera
            
        Returns:
            Processed frame with landmarks drawn
            Boolean indicating if hand was detected
        """
        # Flip frame for selfie-view
        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape
        
        # Convert BGR to RGB for Mediapipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        hand_detected = False
        
        # Draw landmarks if hands detected
        if results.multi_hand_landmarks:
            hand_detected = True
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(
                        color=(0, 255, 0),  # Green
                        thickness=2,
                        circle_radius=2
                    ),
                    self.mp_drawing.DrawingSpec(
                        color=(255, 0, 0),  # Blue
                        thickness=2
                    )
                )
            
            # Play sound whenever hand is detected (with cooldown to prevent spam)
            if hand_detected:
                self.play_sound()
        
        self.last_hand_detected = hand_detected
        
        # Add status text
        status = "Hand Detected!" if hand_detected else "No hand detected"
        color = (0, 255, 0) if hand_detected else (0, 0, 255)
        cv2.putText(
            frame,
            status,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            2
        )
        
        # Add exit instruction
        cv2.putText(
            frame,
            "Press 'q' to exit",
            (10, h - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (200, 200, 200),
            1
        )
        
        return frame, hand_detected
    
    def run(self, camera_id=0):
        """
        Run the hand detection with webcam feed
        
        Args:
            camera_id: Index of the camera to use (default 0)
        """
        # Initialize camera
        cap = cv2.VideoCapture(camera_id)
        
        if not cap.isOpened():
            print(f"Error: Could not open camera {camera_id}")
            return
        
        # Set camera properties for better performance
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        print("Hand Detector Started")
        print(f"Audio library: {AUDIO_LIBRARY if AUDIO_LIBRARY else 'None'}")
        if self.audio_file:
            print(f"Audio file: {self.audio_file}")
        print("Press 'q' to exit")
        print("-" * 50)
        
        try:
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    print("Error: Failed to read frame from camera")
                    break
                
                # Detect hands and get processed frame
                processed_frame, hand_detected = self.detect_hands(frame)
                
                # Display frame
                cv2.imshow("Hand Detection", processed_frame)
                
                # Check for exit key
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("Exiting...")
                    break
        
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        
        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.hands.close()
            print("Camera released. Exiting.")


def main():
    """Main entry point"""
    
    # Configure audio file path
    script_dir = Path(__file__).parent
    audio_file = script_dir / "custom_voice.mp3"
    
    # Create detector
    detector = HandDetector(
        audio_file=str(audio_file),
        detection_confidence=0.5
    )
    
    # Run detection
    detector.run(camera_id=0)


if __name__ == "__main__":
    main()
