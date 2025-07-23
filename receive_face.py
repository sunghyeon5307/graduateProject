from flask import Flask, request
import os
import time

app = Flask(__name__)
UPLOAD_FOLDER = "./received_faces"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "No file uploaded", 400

    image = request.files['image']
    filename = f"face.jpg"
    image.save(os.path.join(UPLOAD_FOLDER, filename))
    return "Received", 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005)
