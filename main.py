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
from openai import OpenAI

load_dotenv()

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

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_KEY"),
)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

async def detect_emotion(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 1:
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        faces = [largest_face]

    for (x, y, w, h) in faces:
        face_roi = rgb_frame[y:y + h, x:x + w]

        result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False, detector_backend="yolov8")
        emotion = result[0]['dominant_emotion']
        emotion_counter[emotion] += 1
        print(emotion_counter)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    return frame

async def detect_drowsiness(frame):
    global drowsy_counter

    # Drowsiness detection parameters
    CONSECUTIVE_FRAMES = 1
    frame_counter = 0

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face_roi = gray_frame[y:y + h, x:x + w]

        # Detect eyes
        eyes = eye_cascade.detectMultiScale(face_roi)

        # Check if both eyes are detected
        if len(eyes) >= 2:
            frame_counter = 0
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(frame, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (0, 255, 0), 2)
        else:
            frame_counter += 1
            if frame_counter >= CONSECUTIVE_FRAMES:
                cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                drowsy_counter += 1

    return frame

async def handle_emotion(most_common_emotion, prev_emotion, frame):
    if most_common_emotion == "angry":
        print("angry")
        cv2.imwrite('assets/tempimg.png', frame)

        completion = client.chat.completions.create(
            model="meta-llama/llama-3.2-11b-vision-instruct:free",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Generate a roast of the person in the image that is meant to be spoken out loud. Do not hold back, be as mean as possible! Keep it concise and short. Like 2 sentences."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encode_image('assets/tempimg.png')}"
                            }
                        }
                    ]
                }
            ]
        )
        print(completion.choices[0].message.content)
        if completion.choices[0].message.content != "" and completion.choices[0].message.content != "I cannot help with that request.":
            audio = f'''{completion.choices[0].message.content}'''
            # speak_text(audio)
        angry()
    elif prev_emotion == "angry":
        print("unangry")
        unangry()
    elif most_common_emotion == "happy":
        print("happy")
        happy()
    elif most_common_emotion == "sad":
        print("sad")
        sad()

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
            detect_drowsiness(frame)
        )
        frame = frame[0]  # Use the frame returned by detect_emotion

        now = time.time()
        if now - last_t >= 5:
            if drowsy_counter > 0 or prev_drowsy_state == "drowsy":
                await handle_drowsiness()
            elif emotion_counter:
                most_common_emotion = max(emotion_counter, key=emotion_counter.get)
                print(f"Most common emotion in the last 5 seconds: {most_common_emotion}")
                await handle_emotion(most_common_emotion, prev_emotion, frame)
                prev_emotion = most_common_emotion

            emotion_counter = defaultdict(int)
            drowsy_counter = 0
            last_t = now

        cv2.imshow('Real-time Emotion and Drowsiness Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())