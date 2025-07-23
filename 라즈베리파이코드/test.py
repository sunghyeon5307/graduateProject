import cv2
import numpy as np
import requests
import time
import os

# Haar Cascade 로드 (정면 얼굴용)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(1)
time.sleep(2)

SERVER_URL = "http://10.150.2.110:5005/upload"

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3)

    for (x, y, w, h) in faces:
        face_crop = frame[y:y+h, x:x+w]

        filename = "face.jpg"
        cv2.imwrite(filename, face_crop)

        with open(filename, "rb") as f:
            try:
                res = requests.post(SERVER_URL, files={"image": f})
                print("send ok:", res.status_code)
            except Exception as e:
                print("send fail:", e)

        # 첫 번째 얼굴만 전송하고 루프 탈출
        break

    # 얼굴에 사각형 그리기 (옵션)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow("Face Detection", frame)
    if cv2.waitKey(1) == 27:  # ESC 누르면 종료
        break

cap.release()
cv2.destroyAllWindows()
