# RUN HAPPY WHEN THE DETECTED EXPN IS HAPPY
# RUN UNHAPPY WHEN IT GETS BACK TO NORMAL, etc.
import base64
import os
import subprocess
from dotenv import load_dotenv
from openai import OpenAI

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
    subprocess.Popen('firefox https://www.complex.com/tag/sad ', shell=True)

def angry():
    command = './scripts/angry/scramble.sh'
    command = command.split()

    cmd1 = subprocess.Popen(['echo',sudo_password], stdout=subprocess.PIPE)
    cmd2 = subprocess.Popen(['sudo','-S'] + command, stdin=cmd1.stdout, stdout=subprocess.PIPE)

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

def gen_remark(emotion):
    completion = client.chat.completions.create(
        model="meta-llama/llama-3.2-11b-vision-instruct:free",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Generate a roast of the person in the image that is meant to be spoken out loud. Do not hold back, be as mean as possible! Keep it concise and short. Like 2 sentences. The user's expression is currently ${emotion}, you can keep this in mind."
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
    text = completion.choices[0].message.content if (completion.choices[0].message.content != "" and completion.choices[0].message.content != "I cannot help with that request.") else "uh oh. i think you broke me"
    return text