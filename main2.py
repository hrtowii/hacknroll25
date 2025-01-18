import cv2
from deepface import DeepFace
from collections import defaultdict
import os
import base64
import numpy as np


def get_current_emotion(frame_data):
    # decode frame data from base64
    frame_data = cv2.imdecode(np.frombuffer(base64.b64decode(frame_data), dtype=np.uint8), cv2.IMREAD_COLOR)

    # Load face cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Frames
    gray_frame = cv2.cvtColor(frame_data, cv2.COLOR_BGR2GRAY)
    rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Isolate only the face closest to the computer screen
    if len(faces) > 1:
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        faces = [largest_face]
    curr_emotion = "neutral"
    # Gets the emotions of the faces
    for (x, y, w, h) in faces:
        face_roi = rgb_frame[y:y + h, x:x + w]

        result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False, detector_backend="yolov8")
        curr_emotion = result[0]['dominant_emotion']

    # just replce prev_emotion.txt w/ contents of current emotion var.
    with open('prev_emotion.txt', 'w') as f:
        f.write(curr_emotion)

    return curr_emotion


def get_prev_emotion():
    # Get the previous emotion
    with open('prev_emotion.txt', 'r') as f:
        prev_emotion = f.read()
    return prev_emotion