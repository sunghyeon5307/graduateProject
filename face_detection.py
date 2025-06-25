# retinaface + arcface -> 평균 벡터값 vector.db에 저장
import cv2
import numpy as np
from insightface.app import FaceAnalysis
import sqlite3
import serial
import time

# ser = serial.Serial('/dev/cu.usbmodem11201', 9600)  
# time.sleep(2)

app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
app.prepare(ctx_id=0)


def save_vector(name, vector):
    conn = sqlite3.connect("vectors.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vectors (
        name TEXT PRIMARY KEY,
        vector BLOB
    )
    """)
    cursor.execute("INSERT OR REPLACE INTO vectors (name, vector) VALUES (?, ?)", (name, vector.tobytes()))
    conn.commit()
    conn.close()

def vector_video(filepath, name):
    frame_count = 0
    max_frame = 30
    cap = cv2.VideoCapture(filepath)
    embeddings = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame_count >= max_frame:
            break
    
        frame_count += 1
        frame = cv2.resize(frame, (960, 540))
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        faces = app.get(rgb_frame)
        print(f"frame {frame_count} 얼굴 수: {len(faces)}개")

        for face in faces:
            x1, y1, x2, y2 = face.bbox.astype(int)
            vec = face.embedding / np.linalg.norm(face.embedding)
            embeddings.append(vec)

            np.set_printoptions(precision=4, suppress=True, linewidth=120)
            print(f"벡터값: {vec[:100]}")

    cap.release()
    cv2.destroyAllWindows()

    print("임베딩 개수:", len(embeddings))

    if embeddings:
        mean_vec = np.mean(embeddings, axis=0)
        print("평균 벡터:", mean_vec)
        save_vector(name, mean_vec)
        np.save(f"vectors/{name}.npy", mean_vec) 


