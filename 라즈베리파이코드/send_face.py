# # import cv2
# # import numpy as np
# # import requests
# # import time
# # import os

# # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# # cap = cv2.VideoCapture(0)
# # time.sleep(2)

# # SERVER_URL = "http://10.150.2.110:5005/upload"

# # while True:
# #     ret, frame = cap.read()
# #     if not ret:
# #         continue

# #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# #     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3)

# #     if len(faces) > 0:
# #         (x, y, w, h) = faces[0]
# #         face_crop = frame[y:y+h, x:x+w]

# #         filename = "face.jpg"
# #         cv2.imwrite(filename, face_crop)

# #         with open(filename, "rb") as f:
# #             try:
# #                 res = requests.post(SERVER_URL, files={"image": f})
# #                 print("send ok:", res.status_code)
# #             except Exception as e:
# #                 print("send fail:", e)

# #         break

# #     cv2.imshow("Face Detection", frame)
# #     if cv2.waitKey(1) == 27:  
# #         break

# # cap.release()
# # cv2.destroyAllWindows()
# # raspberry_send.py

# import cv2
# import requests
# import time
# import socket
# import serial
# import threading

# server_url = "http://10.150.2.110:5005/upload"
    

# #ser = serial.Serial('/dev/tty.usbserial-1440', 115200)
# #time.sleep(2)

# def udp_listener():
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.bind(("0.0.0.0", 5002))

#     while True:
#         data, addr = sock.recvfrom(1024)
#         msg = data.decode().strip()

#         # if msg == "1":
#         #     ser.write(b"1\n")
#         #     ser.flush()

# threading.Thread(target=udp_listener, daemon=True).start()

# cap = cv2.VideoCapture(0)
# time.sleep(2)

# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         continue

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3)

#     if len(faces) > 0:
#         (x, y, w, h) = faces[0]
#         face_crop = frame[y:y+h, x:x+w]

#         filename = "face.jpg"
#         cv2.imwrite(filename, face_crop)

#         with open(filename, "rb") as f:
#             try:
#                 res = requests.post(server_url, files={"image": f})
#                 print("send ok:", res.status_code)
#             except Exception as e:
#                 print("send fail:", e)

#         time.sleep(3)  


import cv2
import requests
import time
import socket
import serial
import threading

server_url = "http://10.150.2.110:5005/upload"

#ser = serial.Serial('/dev/tty.usbserial-1440', 115200)
#time.sleep(2)

def udp_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 5002))

    while True:
        data, addr = sock.recvfrom(1024)
        msg = data.decode().strip()

        # if msg == "1":
        #     ser.write(b"1\n")
        #     ser.flush()

threading.Thread(target=udp_listener, daemon=True).start()

cap = cv2.VideoCapture(0)
time.sleep(2)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3)

    if len(faces) > 0:
        (x, y, w, h) = faces[0]

        time.sleep(2)

        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3)

        if len(faces) == 0:
            print("no face")
            continue

        (x, y, w, h) = faces[0]

        margin_x = int(w * 0.6)   
        margin_y = int(h * 0.3)   

        x1 = max(0, x - margin_x)
        y1 = max(0, y - margin_y)
        x2 = min(frame.shape[1], x + w + margin_x)
        y2 = min(frame.shape[0], y + h + margin_y)

        face_crop = frame[y1:y2, x1:x2]

        filename = "face.jpg"
        cv2.imwrite(filename, face_crop)

        with open(filename, "rb") as f:
            try:
                res = requests.post(server_url, files={"image": f})
                print("send ok:", res.status_code)
            except Exception as e:
                print("send fail:", e)

        time.sleep(3)  # 중복 방지

