import cv2
import numpy as np
import sqlite3
import os
import time
from gtts import gTTS
from insightface.app import FaceAnalysis

app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
app.prepare(ctx_id=0)

instructions = [
    "정면을 봐주세요",
    "고개를 왼쪽으로 돌려주세요",
    "고개를 오른쪽으로 돌려주세요",
    "고개를 위로 들어주세요",
    "고개를 아래로 내려주세요"
]

def speak(text):
    os.makedirs("tts", exist_ok=True)
    tts = gTTS(text=text, lang='ko')
    tts.save("tts/temp.mp3")
    os.system("afplay tts/temp.mp3") 

def save_vectors(name, vectors):
    os.makedirs("facevectors", exist_ok=True)
    conn = sqlite3.connect("facevectors.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS facevectors (
            name TEXT PRIMARY KEY,
            vector BLOB
        )
    """)
    stacked = np.stack(vectors).astype(np.float32)
    cursor.execute("INSERT OR REPLACE INTO facevectors (name, vector) VALUES (?, ?)", (name, stacked.tobytes()))
    conn.commit()
    conn.close()
    np.save(f"facevectors/{name}.npy", stacked)
    print(f"{name}.npy 저장 완료: shape = {stacked.shape}")

def vector_video(name):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return False

    vectors = []
    for i, instruction in enumerate(instructions):
        print(f"\n👉 [{i+1}/5] {instruction}")
        speak(instruction)
        time.sleep(2)

        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = app.get(rgb)

            if faces:
                vec = faces[0].embedding / np.linalg.norm(faces[0].embedding)
                vectors.append(vec)
                print(f"벡터 추출 완료 (angle {i+1})")
                break

            cv2.putText(frame, instruction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            cv2.imshow("캡처 중", frame)

            if cv2.waitKey(1) == 27:
                cap.release()
                cv2.destroyAllWindows()
                return False

    cap.release()
    cv2.destroyAllWindows()

    if len(vectors) == 5:
        save_vectors(name, vectors)
        return True
    else:
        return False
