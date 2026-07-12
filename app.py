
from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import random

app = Flask(__name__)

# ===== Model files =====
FACE_PROTO = "models/opencv_face_detector.pbtxt"
FACE_MODEL = "models/opencv_face_detector_uint8.pb"
AGE_PROTO = "models/age_deploy.prototxt"
AGE_MODEL = "models/age_net.caffemodel"
GENDER_PROTO = "models/gender_deploy.prototxt"
GENDER_MODEL = "models/gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
AGE_LIST = ['(0-2)','(4-6)','(8-12)','(15-20)','(25-32)','(38-43)','(48-53)','(60-100)']
GENDER_LIST = ['Male','Female']

COMPLIMENTS = [
    "You have a wonderful smile! 😊",
    "You look confident today!",
    "You're looking fantastic!",
    "Your positive energy stands out!",
    "Keep being awesome!"
]

faceNet = cv2.dnn.readNet(FACE_MODEL, FACE_PROTO)
ageNet = cv2.dnn.readNet(AGE_MODEL, AGE_PROTO)
genderNet = cv2.dnn.readNet(GENDER_MODEL, GENDER_PROTO)

def highlight_face(frame, conf_threshold=0.7):
    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300,300), (104,117,123), swapRB=True)
    faceNet.setInput(blob)
    detections = faceNet.forward()
    boxes = []
    for i in range(detections.shape[2]):
        conf = detections[0,0,i,2]
        if conf > conf_threshold:
            x1 = int(detections[0,0,i,3]*w)
            y1 = int(detections[0,0,i,4]*h)
            x2 = int(detections[0,0,i,5]*w)
            y2 = int(detections[0,0,i,6]*h)
            boxes.append((x1,y1,x2,y2))
    return boxes

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error":"No image uploaded"}),400

    data = np.frombuffer(request.files["image"].read(), np.uint8)
    frame = cv2.imdecode(data, cv2.IMREAD_COLOR)

    boxes = highlight_face(frame)
    if not boxes:
        return jsonify({"error":"No face detected"})

    x1,y1,x2,y2 = boxes[0]
    pad = 20
    face = frame[max(0,y1-pad):min(frame.shape[0]-1,y2+pad),
                 max(0,x1-pad):min(frame.shape[1]-1,x2+pad)]

    blob = cv2.dnn.blobFromImage(face,1.0,(227,227),MODEL_MEAN_VALUES,swapRB=False)

    genderNet.setInput(blob)
    gender = GENDER_LIST[genderNet.forward()[0].argmax()]

    ageNet.setInput(blob)
    age = AGE_LIST[ageNet.forward()[0].argmax()]

    return jsonify({
        "age": age,
        "gender": gender,
        "compliment": random.choice(COMPLIMENTS)
    })

if __name__ == "__main__":
    app.run(debug=True)
