import cv2
import time
from deepface import DeepFace
from collections import defaultdict
from emotionsFunction import happy, angry, unangry
from dotenv import load_dotenv
import os
import base64

from texttospeech import speak_text
load_dotenv()
# Initialize variables
last_t = time.time()  # Track the start time of the interval
emotion_counter = defaultdict(int)  # Track emotions in the current interval

# Load face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start capturing video
cap = cv2.VideoCapture(1)
from openai import OpenAI

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

if os.getenv("OPENROUTER_KEY") is None:
    raise ValueError("Please set the OPENROUTER_KEY environment variable")
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_KEY"),
)
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convert grayscale frame to RGB format
    rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Isolate only the largest face
    if len(faces) > 1:
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        faces = [largest_face]

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
                print("angry")
                # take webcam screenshot, send to image vlm model and generate a snarky comment
                # run through kokorotts and speak the audio file
                cv2.imwrite('assets/tempimg.png', frame)


                completion = client.chat.completions.create(
                  model="meta-llama/llama-3.2-11b-vision-instruct:free",
                  messages=[
                    {
                      "role": "user",
                      "content": [
                        {
                          "type": "text",
                          "text": "Generate a roast of the person in the image that is meant to be spoken out loud. Do not hold back, be as mean as possible! Keep it concise and short, spoken within 10 seconds."
                        },
                        {
                          "type": "image_url",
                          "image_url": {
                              "url":  f"data:image/jpeg;base64,{encode_image('assets/tempimg.png')}"
                          }
                        }
                      ]
                    }
                  ]
                )
                print(completion.choices[0].message.content)
                if completion.choices[0].message.content != "":
                    audio = f'''{completion.choices[0].message.content}'''
                    speak_text(audio)
                angry()
            elif prev_emotion == "angry":
                print("unangry")
                unangry()
            if most_common_emotion == "happy":
                print("happy")
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
