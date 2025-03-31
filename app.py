import cv2
from ultralytics import YOLO
from flask import Flask, Response
import os

app = Flask(__name__)

model = YOLO("yolov8n-face.pt")

def generate_frames():
    cap = "http://localhost:5000/video"
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()

            for box in boxes:
                x1, y1, x2, y2 = map(int, box[:4])

                face_img = frame[y1:y2, x1:x2]

                if face_img.size == 0:
                    continue

                # Draw a rectangle around the detected face
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        # Convert the frame to JPEG format for streaming
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    cap.release()

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)