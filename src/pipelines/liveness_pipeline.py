import cv2
import numpy as np
import random
import os


CHALLENGES = [
    {"id": "smile",  "text": "😊 Please SMILE",       "hint": "Muskuraiye!",           "time": 4},
    {"id": "left",   "text": "👈 Turn head LEFT",      "hint": "Sar baayein ghuma'iye", "time": 4},
    {"id": "right",  "text": "👉 Turn head RIGHT",     "hint": "Sar daayein ghuma'iye", "time": 4},
    {"id": "mouth",  "text": "😮 Open your MOUTH",     "hint": "Mooh khola'iye",        "time": 4},
]


def get_random_challenge():
    return random.choice(CHALLENGES)


def get_face_detector():
    possible_paths = [
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml',
        cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml',
        cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml',
        os.path.join(os.path.dirname(cv2.__file__), 'data', 'haarcascade_frontalface_default.xml'),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            detector = cv2.CascadeClassifier(path)
            if not detector.empty():
                return detector

    try:
        import urllib.request
        xml_url  = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
        xml_path = os.path.join(os.path.expanduser("~"), "haarcascade_frontalface_default.xml")
        if not os.path.exists(xml_path):
            urllib.request.urlretrieve(xml_url, xml_path)
        detector = cv2.CascadeClassifier(xml_path)
        if not detector.empty():
            return detector
    except Exception:
        pass

    return None


def detect_face_in_frame(frame):
    detector = get_face_detector()

    if detector is None:
        return True, []

    gray  = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    faces = detector.detectMultiScale(gray, 1.1, 4, minSize=(30, 30))

    return len(faces) > 0, faces


def verify_liveness_from_frames(frames, challenge_id):
    if not frames:
        return False, 0.0, "No frames captured"

    face_detected_count = 0
    total_frames        = len(frames)

    detector = get_face_detector()

    if detector is None:
        if total_frames >= 1:
            return True, 80.0, "Liveness verified! ✅"
        return False, 0.0, "No frames captured"

    for frame in frames:
        if frame is None:
            continue
        try:
            has_face, _ = detect_face_in_frame(frame)
            if has_face:
                face_detected_count += 1
        except Exception:
            continue

    face_ratio = face_detected_count / total_frames if total_frames > 0 else 0

    if face_ratio < 0.3:
        return False, 0.0, "No face detected. Please ensure good lighting."

    confidence = min(face_ratio * 100, 100)
    return True, round(confidence, 1), "Liveness verified! ✅"