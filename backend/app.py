import base64
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from emotionsFunction import angry, gen_remark, happy, sad, unangry, sleepy, unsleepy, gen_remark_and_detect_emotion
from main2 import get_current_emotion, get_prev_emotion
import numpy
import json
app = Flask(__name__)

CORS(app)

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers['X-Content-Type-Options'] = '*'
        return res

# get image
@app.route('/detect', methods=['POST'])
def detect():
    data = request.json
    frame_data = data.get('frame')

    # TODO: implement isolation of face
    

    # Use the new function to detect emotion and generate a roast in one API call
    current_emotion, remark = gen_remark_and_detect_emotion(frame_data)

    # Get the previous emotion
    previous_emotion = get_prev_emotion()

    # Handle the transition from the previous emotion to the current emotion
    match previous_emotion:
        case "angry":
            unangry()
        case "fear":
            unsleepy()
        case "surprise":
            unsleepy()

    # Handle the current emotion
    match current_emotion:
        case "angry":
            angry()
        case "happy":
            happy()
        case "sad":
            sad()
        case "fear":
            sleepy()
        case "surprise":
            sleepy()

    # Update the previous emotion file with the current emotion
    with open('prev_emotion.txt', 'w') as f:
        f.write(current_emotion)

    # Return the detected emotion and the generated roast
    return {"emotion": current_emotion, "remark": remark}

if __name__ == '__main__':
    app.run(port=4444)