
from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)
model = load_model('model/mask_detector_model.h5')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    data = request.get_json()
    img_data = data['image'].split(',')[1]
    img_bytes = base64.b64decode(img_data)
    img = Image.open(BytesIO(img_bytes))
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_img = frame[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (150, 150))
        face_img = np.expand_dims(face_img, axis=0) / 255.0
        prediction = model.predict(face_img)[0][0]
        label = "Memakai Masker" if prediction < 0.5 else "Tidak Memakai Masker"
        color = (255, 0, 0) if prediction < 0.5 else (0, 0, 255)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    _, img_encoded = cv2.imencode('.jpg', frame)
    img_base64 = base64.b64encode(img_encoded).decode('utf-8')

    return jsonify({"image": img_base64})

if __name__ == '__main__':
    app.run(debug=True)
