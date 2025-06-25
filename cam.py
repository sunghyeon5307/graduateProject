import cv2
import numpy as np
import sqlite3
import time
import serial
from scipy.spatial.distance import cosine
from insightface.app import FaceAnalysis

# ser = serial.Serial('/dev/cu.usbserial-1110', 115200)  
# time.sleep(2)

app = FaceAnalysis(name='buffalo_l', providers=["CPUExecutionProvider"])
app.prepare(ctx_id=0)

def load_all_vectors():
    conn = sqlite3.connect("/Users/bagseonghyeon/Desktop/0421지켜락/web/vectors.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, vector FROM vectors")
    rows = cursor.fetchall()
    conn.close()

    vectors = []
    for name, vector_blob in rows:
        vector = np.frombuffer(vector_blob, dtype=np.float32)
        vectors.append((name, vector))
    return vectors

threshold = 0.6

db_vectors = load_all_vectors()

cap = cv2.VideoCapture(0)
time.sleep(2)

ret, frame = cap.read()
if not ret:
    exit()

frame = cv2.resize(frame, (960, 540))
rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

faces = app.get(rgb_frame)
if faces:
    face = max(faces, key=lambda f: f.bbox[2] * f.bbox[3])  
    new_embedding = face.embedding / np.linalg.norm(face.embedding)
    for name, saved_embedding in db_vectors:
        similarity = 1 - cosine(saved_embedding, new_embedding)

        if similarity > threshold:
            print(f"일치: {name} (유사도: {similarity:.4f})")
            ser.write(b"1\n") 
            ser.flush()
            print("전송완료")
            break 
        else:
            print(f"불일치: {name} (유사도: {similarity:.4f})")

cv2.imshow('picture', frame)
cv2.waitKey(3000)

cap.release()
cv2.destroyAllWindows()
