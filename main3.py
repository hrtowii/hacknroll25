import cv2
from deepface import DeepFace
import numpy as np

def get_current_emotion(frame):
    # Load face cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Frames
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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

        result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
        curr_emotion = result[0]['dominant_emotion']

        # Draw bounding box and emotion text
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, curr_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    return frame

def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = get_current_emotion(frame)

        cv2.imshow('Emotion Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()