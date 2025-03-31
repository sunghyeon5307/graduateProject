import cv2
import torch
from ultralytics import YOLO

model = YOLO("/Users/bagseonghyeon/Documents/지켜락/yolov8n-face.pt")

cap = cv2.VideoCapture("video.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    for r in results:
        for box in r.boxes:
            cls = int(box.cls)
            if cls == 0:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                face = frame[y1:y2, x1:x2]
                cv2.imshow("Face", face)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()