import cv2
import time
from deepface import DeepFace
from collections import defaultdict

# Initialize variables
last_t = time.time()  # Track the start time of the interval
emotion_counter = defaultdict(int)  # Track emotions in the current interval

# Load face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start capturing video
cap = cv2.VideoCapture(1)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convert grayscale frame to RGB format
    rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for face in faces:


    for (x, y, w, h) in faces:
        # Extract the face ROI (Region of Interest)
        face_roi = rgb_frame[y:y + h, x:x + w]

        # Perform emotion analysis on the face ROI
        result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)

        # Determine the dominant emotion
        emotion = result[0]['dominant_emotion']
        emotion_counter[emotion] += 1  # Update the emotion counter

        # Draw rectangle around face and label with predicted emotion
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Check if 5 seconds have passed
    now = time.time()
    prev_emotion = ""
    if now - last_t >= 5:
        # Find the most common emotion in the last 5 seconds
        if emotion_counter:
            most_common_emotion = max(emotion_counter, key=emotion_counter.get)
            print(f"Most common emotion in the last 5 seconds: {most_common_emotion}")
            if most_common_emotion == "angry":
                angry()
            elif prev_emotion == "angry":
                unangry()
            if most_common_emotion == "happy":
                happy()
            prev_emotion = most_common_emotion

        # Reset the emotion counter and timer for the next interval
        emotion_counter = defaultdict(int)
        last_t = now

    # Display the resulting frame
    cv2.imshow('Real-time Emotion Detection', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close all windows
cap.release()
cv2.destroyAllWindows()
