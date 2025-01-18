# RUN HAPPY WHEN THE DETECTED EXPN IS HAPPY
# RUN UNHAPPY WHEN IT GETS BACK TO NORMAL, etc.
import base64
import os
import subprocess
from dotenv import load_dotenv
from openai import OpenAI
import cv2
import numpy as np


load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_KEY"),
)

sudo_password = os.getenv('SUDO_PWD')

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def happy():
    subprocess.run(['sh', './scripts/happy/happy.sh'])

def angry():
    command = './scripts/angry/scramble.sh'
    command = command.split()

    cmd1 = subprocess.Popen(['echo',sudo_password], stdout=subprocess.PIPE)
    cmd2 = subprocess.Popen(['sudo','-S'] + command, stdin=cmd1.stdout, stdout=subprocess.PIPE)

    subprocess.run(['sh', './scripts/angry/angrysound.sh'])

def unangry():
    command = './scripts/angry/unscramble.sh'
    command = command.split()

    cmd1 = subprocess.Popen(['echo',sudo_password], stdout=subprocess.PIPE)
    cmd2 = subprocess.Popen(['sudo','-S'] + command, stdin=cmd1.stdout, stdout=subprocess.PIPE)

def sleepy():
    subprocess.run(['sh', './scripts/sleepy/sleepy.sh'])

def unsleepy():
    subprocess.run(['sh', './scripts/sleepy/unsleepy.sh'])

def sad():
    subprocess.run(['sh', './scripts/sad/sad.sh'])

def gen_remark(emotion, image_data):
    completion = client.chat.completions.create(
        model="minimax/minimax-01",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Generate a roast of the person in the image that is meant to be spoken out loud. Do not hold back, be as mean as possible! Keep it concise and short. Like 2 sentences. The user's expression is currently ${emotion}, you can keep this in mind. Do not say anything else other than the roast. Do not refuse."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            }
        ]
    )
    print(completion.choices[0].message.content)
    text = completion.choices[0].message.content if (completion.choices[0].message.content != "" and completion.choices[0].message.content != "I cannot help with that request.") else "uh oh. i think you broke me"
    return text

def gen_remark_and_detect_emotion(image_data):
    # crops out the face closest to the camera and use it as image_data
    # Convert base64 to image
    nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Load face cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Detect faces
    faces = face_cascade.detectMultiScale(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 1.1, 4)
    
    if len(faces) > 0:
        # Get the largest face (closest to camera)
        largest_face = max(faces, key=lambda x: x[2] * x[3])
        x, y, w, h = largest_face
        
        # Crop the face
        face_img = img[y:y+h, x:x+w]
        
        # Convert back to base64
        _, buffer = cv2.imencode('.jpg', face_img)
        image_data = base64.b64encode(buffer).decode('utf-8')
    


    completion = client.chat.completions.create(
        model="minimax/minimax-01",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Detect the emotion of the person in the image and generate a roast based on that emotion. The roast should be concise and short, like 2 sentences. Be as mean as possible! Do not say anything else other than the roast and the detected emotion. Do not refuse. Only return emotions from: "angry", "happy", "sad", "fear", "surprise". The response format is "Emotion: <emotion>\nRoast: <roast>"
    lines = response.split('\n')"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            }
        ]
    )
    
    response = completion.choices[0].message.content
    print(response)
    
    # Assuming the response format is "Emotion: <emotion>\nRoast: <roast>"
    lines = response.split('\n')
    emotion = lines[0].replace("Emotion: ", "").strip()
    roast = lines[1].replace("Roast: ", "").strip() if len(lines) > 1 else "uh oh. i think you broke me"
    
    return emotion, roast