import base64
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from emotionsFunction import angry, gen_remark, happy, sad, unangry, sleepy, unsleepy
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
    previous_emotion = get_prev_emotion()
    current_emotion = get_current_emotion(frame_data)
    match previous_emotion:
        case "angry":
            unangry()
        case "fear":
            unsleepy()

    match current_emotion:
        case "angry":
            angry()
        case "happy":
            happy()
        case "sad":
            sad()
        case "fear":
            sleepy()

    remark = gen_remark(current_emotion, frame_data)

    return {"emotion": current_emotion, "remark": remark}

if __name__ == '__main__':
    app.run(port=4444)