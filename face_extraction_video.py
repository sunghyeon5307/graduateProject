from flask import Flask, request, jsonify
import cv2
import os
import numpy as np
from ultralytics import YOLO

app = Flask(__name__)

model = YOLO("/Users/bagseonghyeon/Documents/지켜락/yolov8n-face.pt")

UPLOAD_FOLDER = "/Users/bagseonghyeon/Documents/지켜락/video"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['video']
    file_path = os.path.join(UPLOAD_FOLDER, "uploaded_video.webm")
    file.save(file_path)

    cap = cv2.VideoCapture(file_path)
    frame_count = 0
    saved_faces = 0

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'vp80')
    output_path = os.path.join(UPLOAD_FOLDER, "faces_only.webm")
    out = cv2.VideoWriter(output_path, fourcc, 30, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        faces_frame = np.zeros_like(frame)

        for r in results:
            if hasattr(r, 'boxes'):
                for box in r.boxes:
                    cls = int(box.cls)
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    face = frame[y1:y2, x1:x2]
                    if face.size != 0:
                        faces_frame[y1:y2, x1:x2] = face
                        saved_faces += 1

        out.write(faces_frame)

        frame_count += 1

    cap.release()
    out.release()

    return jsonify({"message": "Face extraction complete", "total_faces": saved_faces, "total_frames": frame_count})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)