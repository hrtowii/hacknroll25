import cv2
import time
import asyncio
from deepface import DeepFace
from collections import defaultdict
from emotionsFunction import happy, angry, unangry, sad, sleepy, unsleepy
from dotenv import load_dotenv
import os
import base64
from texttospeech import speak_text
import numpy as np

load_dotenv()

current_emotion = None

# Initialize variables
last_t = time.time()  # Track the start time of the interval
emotion_counter = defaultdict(int)  # Track emotions in the current interval
drowsy_counter = 0  # Track drowsiness in the current interval

# Load face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load eye cascade classifier
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# Start capturing video
cap = cv2.VideoCapture(1)

if os.getenv("OPENROUTER_KEY") is None:
    raise ValueError("Please set the OPENROUTER_KEY environment variable")


def preprocess_frame(frame):
    # Convert to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian Blur to reduce noise
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    
    # Apply edge detection using Canny
    edges = cv2.Canny(blurred_frame, 50, 150)
    
    # Combine the edges with the original frame to enhance features
    enhanced_frame = cv2.addWeighted(gray_frame, 0.7, edges, 0.3, 0)
    
    # Convert back to RGB for DeepFace analysis
    rgb_frame = cv2.cvtColor(enhanced_frame, cv2.COLOR_GRAY2RGB)
    return rgb_frame

async def detect_emotion(frame):
    # Preprocess the frame
    preprocessed_frame = preprocess_frame(frame)

    # Detect faces
    faces = face_cascade.detectMultiScale(preprocessed_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 1:
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        faces = [largest_face]

    for (x, y, w, h) in faces:
        face_roi = preprocessed_frame[y:y + h, x:x + w]

        result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False, detector_backend="retinaface",expand_percentage=10)
        emotion = result[0]['dominant_emotion']
        emotion_counter[emotion] += 1

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    return frame

async def detect_drowsiness(frame):
    global drowsy_counter

    # Drowsiness detection parameters
    CONSECUTIVE_FRAMES = 2
    frame_counter = 0

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 1:
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        faces = [largest_face]

    for (x, y, w, h) in faces:
        face_roi = rgb_frame[y:y + h, x:x + w]
        face_box = (x, y, w, h)
        # Detect eyes
        eyes = eye_cascade.detectMultiScale(face_roi)

        # Function to validate if detected eyes are in the upper part of the face
        def is_eye_in_upper_face(face_box, eye_box):
            face_x, face_y, face_w, face_h = face_box
            eye_x, eye_y, eye_w, eye_h = eye_box

            # Define the upper part of the face as the top half
            upper_face_y_limit = face_y + face_h // 2

            # Check if the eye bounding box is entirely within the upper part of the face
            return eye_y + eye_h <= upper_face_y_limit

        num_eyes = 0

        for (ex, ey, ew, eh) in eyes:
            eye_box = (x + ex, y + ey, ew, eh)
            if is_eye_in_upper_face(face_box, eye_box):
                num_eyes += 1
                cv2.rectangle(frame, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (0, 255, 0), 2)
            else:
                cv2.rectangle(frame, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (0, 0, 255), 2)

        print(f"num eyes: {num_eyes}")
        # Check if both eyes are detected
        if num_eyes >= 2:
            frame_counter = 0
        else:
            frame_counter += 1
            if frame_counter >= CONSECUTIVE_FRAMES:
                cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                # drowsy_counter += 1

    return frame

async def handle_emotion(most_common_emotion, prev_emotion, frame):
    return "fuck"
    # global current_emotion
    # if most_common_emotion == "angry":
    #     print("angry")
    #     cv2.imwrite('tempimg.png', frame)
    #     angry()
    # elif prev_emotion == "angry":
    #     print("unangry")
    #     unangry()
    # elif most_common_emotion == "happy":
    #     print("happy")
    #     happy()
    # elif most_common_emotion == "sad":
    #     print("sad")
    #     sad()

    # current_emotion = most_common_emotion

async def handle_drowsiness():
    global drowsy_counter, prev_drowsy_state

    if drowsy_counter > 0:
        print("drowsy")
        sleepy()
        prev_drowsy_state = "drowsy"
    elif prev_drowsy_state == "drowsy":
        print("undrowsy")
        unsleepy()
        prev_drowsy_state = ""

async def main():
    global last_t, emotion_counter, drowsy_counter
    prev_emotion = ""
    prev_drowsy_state = ""

    while True:
        ret, frame = cap.read()

        # Run emotion and drowsiness detection concurrently
        frame = await asyncio.gather(
            detect_emotion(frame),
            # detect_drowsiness(frame)
        )
        frame = frame[0]  # Use the frame returned by detect_emotion

        now = time.time()
        if now - last_t >= 5:
            if drowsy_counter > 0 or prev_drowsy_state == "drowsy":
                await handle_drowsiness()
            elif emotion_counter:
                most_common_emotion = max(emotion_counter, key=emotion_counter.get)
                print(f"Most common emotion in the last 5 seconds: {most_common_emotion}")
                # await handle_emotion(most_common_emotion, prev_emotion, frame)
                # prev_emotion = most_common_emotion

            emotion_counter = defaultdict(int)
            drowsy_counter = 0
            last_t = now

        cv2.imshow('Real-time Emotion and Drowsiness Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# for flask
def get_current_emotion(frame_data):
    frame = cv2.imdecode(np.frombuffer(base64.b64decode(frame_data), dtype=np.uint8), cv2.IMREAD_COLOR)

    # Run emotion and drowsiness detection
    emotion = asyncio.run(detect_emotion(frame))
    drowsiness = asyncio.run(detect_drowsiness(frame))

    # Handle responses
    response = {
        'emotion': emotion,
        'drowsiness': drowsiness,
        'message': handle_emotion(emotion),
        'alert': handle_drowsiness(drowsiness)
    }
    return response

if __name__ == "__main__":
    asyncio.run(main())