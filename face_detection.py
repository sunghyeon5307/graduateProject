# import cv2
# import numpy as np
# import sqlite3
# import os
# import time
# from gtts import gTTS
# from insightface.app import FaceAnalysis

# app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
# app.prepare(ctx_id=0)

# instructions = [
#     "정면을 봐주세요",
#     "고개를 왼쪽으로 돌려주세요",
#     "고개를 오른쪽으로 돌려주세요",
#     "고개를 위로 들어주세요",
#     "고개를 아래로 내려주세요"
# ]

# def speak(text):
#     os.makedirs("tts", exist_ok=True)
#     tts = gTTS(text=text, lang='ko')
#     tts.save("tts/temp.mp3")
#     os.system("afplay tts/temp.mp3") 

# def save_vectors(name, vectors):
#     os.makedirs("facevectors", exist_ok=True)
#     conn = sqlite3.connect("facevectors.db")
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS facevectors (
#             name TEXT PRIMARY KEY,
#             vector BLOB
#         )
#     """)
#     stacked = np.stack(vectors).astype(np.float32)
#     cursor.execute("INSERT OR REPLACE INTO facevectors (name, vector) VALUES (?, ?)", (name, stacked.tobytes()))
#     conn.commit()
#     conn.close()
#     np.save(f"facevectors/{name}.npy", stacked)
#     print(f"{name}.npy 저장 완료: shape = {stacked.shape}")

# def vector_video(name):
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         return False

#     vectors = []
#     for i, instruction in enumerate(instructions):
#         print(f"\n-> [{i+1}/5] {instruction}")
#         speak(instruction)
#         time.sleep(3.5)

#         ret, frame = cap.read()
#         if not ret:
#             cap.release()
#             cv2.destroyAllWindows()
#             return False

#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         faces = app.get(rgb)

#         if faces:
#             vec = faces[0].embedding / np.linalg.norm(faces[0].embedding)
#             vectors.append(vec)
#             print(f"벡터 추출 완료 (angle {i+1})")

#         else:
#             print("❌ 얼굴 인식 실패")
#             cap.release()
#             cv2.destroyAllWindows()
#             return False

#     cap.release()
#     cv2.destroyAllWindows()

#     if len(vectors) == 5:
#         save_vectors(name, vectors)
#         return True
#     else:
#         return False

import cv2
import numpy as np
import sqlite3
import os
import time
from gtts import gTTS
from insightface.app import FaceAnalysis

# FaceAnalysis 초기화
app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
app.prepare(ctx_id=0)

# 등록 시 안내 음성 리스트
instructions = [
    "정면을 봐주세요",
    "고개를 왼쪽으로 돌려주세요",
    "고개를 오른쪽으로 돌려주세요",
    "고개를 위로 들어주세요",
    "고개를 아래로 내려주세요"
]

# 음성 출력 함수
def speak(text):
    os.makedirs("tts", exist_ok=True)
    tts = gTTS(text=text, lang='ko')
    tts.save("tts/temp.mp3")
    os.system("afplay tts/temp.mp3")  # macOS용. Windows는 playsound 사용

# 평균 벡터 저장 함수
def save_mean_vector(name, vector):
    os.makedirs("facevectors", exist_ok=True)
    conn = sqlite3.connect("facevectors.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS facevectors (
            name TEXT PRIMARY KEY,
            vector BLOB
        )
    """)
    vector = vector.astype(np.float32)
    cursor.execute("INSERT OR REPLACE INTO facevectors (name, vector) VALUES (?, ?)", (name, vector.tobytes()))
    conn.commit()
    conn.close()
    np.save(f"facevectors/{name}_mean.npy", vector)
    print(f"✅ 평균 벡터 저장 완료: facevectors/{name}_mean.npy, shape = {vector.shape}")

# 벡터 수집 및 평균 저장
def vector_video(name, shots_per_pose=3):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ 카메라 열기 실패")
        return False

    all_vectors = []

    for i, instruction in enumerate(instructions):
        print(f"\n-> [{i+1}/5] {instruction}")
        speak(instruction)
        time.sleep(2)

        count = 0
        tries = 0
        while count < shots_per_pose and tries < shots_per_pose * 5:
            tries += 1
            ret, frame = cap.read()
            if not ret:
                continue

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = app.get(rgb)

            if faces:
                vec = faces[0].embedding / np.linalg.norm(faces[0].embedding)
                all_vectors.append(vec)
                count += 1
                print(f"✅ {i+1}번 포즈 - {count}/{shots_per_pose}장 저장됨")
            else:
                print("😅 얼굴 감지 실패. 다시 시도 중...")

            time.sleep(0.3)

    cap.release()
    cv2.destroyAllWindows()

    expected_count = shots_per_pose * len(instructions)
    if len(all_vectors) == expected_count:
        mean_vector = np.mean(all_vectors, axis=0)
        save_mean_vector(name, mean_vector)
        return True
    else:
        print(f"❌ 벡터 수집 부족: {len(all_vectors)}/{expected_count}")
        return False
